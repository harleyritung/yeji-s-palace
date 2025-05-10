from Entities import Player, Meowtar, Meowolas, KingMeowthur, MeowKnight
from GUI import Dialogue
import uvage as u
import pygame
from Constants import *

# DEBUG
debug = False
mute = False
full_screen = False

class GameAudio:
    def __init__(self):
        self.metal_crash = pygame.mixer.Sound("Assets/Audio/Sounds/metal_crashing.mp3")
        if mute:
            self.metal_crash.set_volume(0)
        else:
            self.metal_crash.set_volume(.3)
        self.metal_crash_played = False

        self.whoosh = pygame.mixer.Sound("Assets/Audio/Sounds/Whoosh.mp3")
        if mute:
            self.whoosh.set_volume(0)
        self.whoosh_frame_start = 0

        self.victory_song = pygame.mixer.Sound("Assets/Audio/Sounds/victory_song.mp3")
        self.victory_song.set_volume(.3)

        pygame.mixer.music.load("Assets/Audio/Music/I played FOUR 16th Century KAZOOs Renaissance Italian theme.mp3")
        pygame.mixer.music.set_volume(.1)
        if not mute:
            pygame.mixer.music.play(-1)

class GameDialogue:
    def __init__(self, camera):
        voice_normal = pygame.mixer.Sound("Assets/Audio/Sounds/Normal.mp3")
        voice_normal.set_volume(dialogue_volume)
        voice_distressed = pygame.mixer.Sound("Assets/Audio/Sounds/Distressed.mp3")
        voice_distressed.set_volume(dialogue_volume)
        voice_meow_knight = pygame.mixer.Sound('Assets/Audio/Sounds/MeowKnight.mp3')
        voice_meow_knight.set_volume(dialogue_volume + .3)
        voice_victory = pygame.mixer.Sound('Assets/Audio/Sounds/Victory.mp3')
        voice_victory.set_volume(dialogue_volume)

        dialogue_treasure = Dialogue.Dialogue(
            camera,
            "And here is Ironclaw Treasury. Your main responsibility will be guarding this room. ESPECIALLY this chest here.",
            Position.TOP,
            "king_mewrthur.png",
            voice_normal,
            mute)

        dialogue_stolen = Dialogue.Dialogue(
            camera,
            "mrrOWW! A thief has stolen from the chest! You must find them RIGHT MEOW!",
            Position.TOP,
            "king_mewrthur.png",
            voice_distressed,
            mute)

        self.dialogue_meow_knight = Dialogue.Dialogue(
            camera,
            "The thief ran outside! Hurry after him, I'll purrtect the castle.",
            Position.TOP,
            "meow_knight.png",
            voice_meow_knight,
            mute,
            Position.BOTTOM)
        self.dialogue_boxes = [dialogue_treasure, dialogue_stolen]

    def get_next(self):
        return self.dialogue_boxes.pop(0)

class GameAssets:
    def __init__(self):
        self.treasure_backdrop = u.from_image(screen_width / 2, screen_height / 2, treasure_file_path)
        self.blackout_backdrop = u.from_image(screen_width / 2, screen_height / 2, blackout_file_path)
        self.treasure_sacked_backdrop = u.from_image(screen_width / 2, screen_height / 2, treasure_sacked_file_path)
        self.hallway_backdrop = u.from_image(screen_width / 2, screen_height / 2, hallway_3_file_path)
        self.forest_backdrop = u.from_image(screen_width / 2, screen_height / 2 + 10, forest_filepath)

        self.envelope = u.from_image(screen_width / 2, screen_height / 2, "Assets/envelope.png")
        self.letter = u.from_image(screen_width / 2, screen_height / 2, "Assets/letter.png")

class Game:
    def __init__(self):
        self.camera = u.Camera(screen_width, screen_height, full_screen=full_screen)
        self.control_enabled = False
        self.frame_count = 0
        self.blackout_start = None

        self.audio = GameAudio()
        self.game_dialogue = GameDialogue(self.camera)
        self.curr_dialogue = self.game_dialogue.get_next()
        self.sound_count = 0

        self.curr_scene: Scene = Scene.INTRO
        self.curr_room = Room.TREASURE

        self.assets = GameAssets()
        self.background: u.SpriteBox = self.assets.treasure_backdrop
        # self.background: u.SpriteBox = self.assets.forest_backdrop
        self.background_needs_update = False

        # instantiate entities
        floor_offset_y = screen_height / 2 + 215
        meowtar_offset_y = floor_offset_y
        meowolas_offset_y = 7 + floor_offset_y
        king_meowthur_offset_y = -5 + floor_offset_y

        self.player: Meowtar = Meowtar.Meowtar(screen_width - 300, meowtar_offset_y, facing=FaceDirection.LEFT)
        self.player.width = 40

        self.king_meowthur = KingMeowthur.KingMeowthur(screen_width - 400, king_meowthur_offset_y)
        self.meow_knight = MeowKnight.MeowKnight(screen_width / 2, floor_offset_y)

        self.enemy = Meowolas.Meowolas(430, meowolas_offset_y)
        self.entities: list[Player.Player] = [self.king_meowthur, self.player]

    def loop(self):
        if u.did_keydown(Key.ESCAPE):
            pygame.quit()

        if u.did_keydown(Key.ENTER):
            self.curr_dialogue.advance()

        self.draw_screen()

    def draw_screen(self):
        self.get_room_for_position()

        self.update_scene()

        self.draw_background_for_room()

        self.camera.draw(self.background)

        self.draw_entities()

        self.curr_dialogue.draw(self.frame_count)

        self.camera.display()

    def get_room_for_position(self):
        self.camera.left = self.camera.x - self.camera.width / 2
        self.camera.right = self.camera.x + self.camera.width / 2

        if self.curr_room == Room.TREASURE:
            if self.player.x_pos < self.camera.left:
                self.player.x_pos = self.camera.left
                return
        if self.curr_room == Room.FOREST:
            if self.player.x_pos > 625:
                self.player.x_pos = 625
                return

        if self.curr_scene == Scene.INTRO:
            if self.player.x_pos > self.camera.right:
                self.player.x_pos = self.camera.right
            elif self.player.x_pos < self.camera.left:
                self.player.x_pos = self.camera.left
        else:
            if self.player.x_pos > self.camera.right + self.player.width:
                self.player.x_pos = self.camera.left
                self.background_needs_update = True
                if self.curr_room == Room.TREASURE:
                    self.curr_room = Room.HALLWAY
                    self.entities = [self.meow_knight, self.player]
                elif self.curr_room == Room.HALLWAY:
                    self.curr_room = Room.FOREST
                    self.entities = [self.player, self.enemy]
                    self.player.y_pos = self.player.y_pos - 50
            elif self.player.x_pos < self.camera.left - self.player.width:
                self.player.x_pos = self.camera.right
                self.background_needs_update = True
                if self.curr_room == Room.HALLWAY:
                    self.curr_room = Room.TREASURE
                    self.entities = [self.king_meowthur, self.player]
                elif self.curr_room == Room.FOREST:
                    self.curr_room = Room.HALLWAY
                    self.entities = [self.meow_knight, self.player]
                    self.player.y_pos = self.player.y_pos + 50

    def update_scene(self):
        if self.curr_scene == Scene.INTRO:
            if not self.curr_dialogue.dismissed and self.camera.finished_transition and not self.curr_dialogue.show:
                self.curr_dialogue.show = True

            if self.king_meowthur.x_pos > 275:
                if self.king_meowthur.x_vel == 0 and self.curr_dialogue.done_transitioning:
                    self.king_meowthur.x_vel = -self.king_meowthur.run_speed
            else:
                self.king_meowthur.x_vel = 0
                self.king_meowthur.facing = FaceDirection.RIGHT
                if not self.control_enabled and self.curr_dialogue.dismissed:
                    self.control_enabled = True

            if self.player.x_pos <= 600:
                self.control_enabled = False
                self.player.x_vel = 0

                if self.audio.whoosh_frame_start == 0:
                    self.audio.whoosh_frame_start = self.frame_count
                    self.audio.whoosh.play()
                # if .6 seconds have passed since whoosh started
                elif (self.frame_count - self.audio.whoosh_frame_start) / fps >= .6:
                    self.entities = []
                    self.curr_scene = Scene.BLACKOUT
                    self.background_needs_update = True
        elif self.curr_scene == Scene.BLACKOUT:
            if (self.frame_count - self.audio.whoosh_frame_start) / fps >= 1.6:
                if not self.audio.metal_crash_played:
                    self.audio.metal_crash.play()
                    self.audio.metal_crash_played = True

                if not pygame.mixer.get_busy():
                    self.control_enabled = True
                    self.curr_scene = Scene.SACKED
                    self.background_needs_update = True
                    self.entities = [self.player, self.king_meowthur]
                    self.curr_dialogue = self.game_dialogue.get_next()

        elif self.curr_scene == Scene.SACKED:
            if self.curr_room == Room.TREASURE:
                if not self.king_meowthur.search_done:
                    self.king_meowthur.search(self.frame_count)
                elif not self.curr_dialogue.dismissed and not self.curr_dialogue.show:
                    self.curr_dialogue.show = True
                elif self.curr_dialogue.dismissed:
                    self.king_meowthur.pace(self.frame_count)
            elif self.curr_room == Room.FOREST:
                if not self.enemy.jump_done:
                    self.player.x_vel = 0
                    self.control_enabled = False
                    self.enemy.look_back_jump_away(self.frame_count)
                    if self.enemy.look_back_done:
                        self.control_enabled = True
                if self.player.x_pos >= 624:
                    # play pick up sound/show something
                    self.enemy.envelope_picked_up = True

                if self.enemy.envelope_x_done and self.enemy.envelope_y_done:
                    if not pygame.mixer.get_busy():
                        pygame.mixer.music.stop()
                        self.audio.victory_song.play()

    def draw_background_for_room(self):
        if self.background_needs_update:
            self.background_needs_update = False

            if self.curr_room == Room.TREASURE:
                if self.curr_scene == Scene.INTRO:
                    self.background = self.assets.treasure_backdrop
                elif self.curr_scene == Scene.BLACKOUT:
                    self.background = self.assets.blackout_backdrop
                else:
                    self.background = self.assets.treasure_sacked_backdrop
            elif self.curr_room == Room.HALLWAY:
                self.curr_dialogue.finish_printing()
                self.curr_dialogue.dismissed = True
                self.background = self.assets.hallway_backdrop

                if not self.game_dialogue.dialogue_meow_knight.dismissed and not self.game_dialogue.dialogue_meow_knight.show:
                    self.curr_dialogue = self.game_dialogue.dialogue_meow_knight
                    self.curr_dialogue.show = True
                    self.curr_dialogue.finish_transition()
            elif self.curr_room == Room.FOREST:
                self.curr_dialogue.finish_printing()
                self.curr_dialogue.dismissed = True
                self.background = self.assets.forest_backdrop

        self.camera.draw(self.background)

    def draw_entities(self):
        if self.curr_room == Room.HALLWAY:
            if self.player.x_pos < self.meow_knight.x_pos:
                self.meow_knight.animation = self.meow_knight.idle_left_animation
            else:
                self.meow_knight.animation = self.meow_knight.idle_right_animation

        for entity in self.entities:
            entity.draw(self.camera, self.control_enabled, self.frame_count)

game = Game()

# main loop
def tick():
    game.camera.clear("black")

    game.loop()

    game.frame_count += 1

u.timer_loop(fps, tick)
