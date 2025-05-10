from Constants import *
import uvage as u
from Entities.Player import Player, PlayerPath
from uvage import SpriteBox


class Meowolas(Player):
    def __init__(self, x_pos, y_pos, facing: FaceDirection = FaceDirection.RIGHT):
        super().__init__(x_pos, y_pos, PlayerPath.Meowolas.value, facing, run=8)

        self.run_right_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run.png",
                                                       1,
                                                       self.sprite_dict[AnimationAction.RUN])
        self.run_left_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run_left.png",
                                                      1,
                                                      self.sprite_dict[AnimationAction.RUN])
        self.jump_right_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/jump.png",
                                                        1,
                                                        self.sprite_dict[AnimationAction.JUMP])

        self.look_back_start_frame = None
        self.look_back_done = False
        self.jump_done = False

        # place holder positions until we spawn it in
        self.envelope_tilted: SpriteBox = u.from_image(0, 0, "Assets/envelope_tilted.png")
        self.envelope_tilted_x_vel = 0
        self.envelope_tilted_x_speed = 4
        self.envelope_tilted_y_speed = 2
        self.show_tilted_envelope = False
        self.envelope_picked_up = False
        self.envelope_fall_start_frame = None

        self.envelope: SpriteBox = u.from_image(0, 0, "Assets/envelope.png")
        self.envelope_x_done = False
        self.envelope_y_done = False

        self.letter = u.from_image(screen_width / 2, screen_height / 2, "Assets/letter.png")


    def draw(self, camera, control_enabled, frame_count):
        super().draw(camera, control_enabled, frame_count)

        if self.show_tilted_envelope and not self.envelope_picked_up:
            self.envelope_tilted = u.from_image(self.envelope_tilted.x, self.envelope_tilted.y, "Assets/envelope_tilted.png")
            camera.draw(self.envelope_tilted)
        elif self.envelope_picked_up and not (self.envelope_x_done and self.envelope_y_done):
            self.envelope = u.from_image(self.envelope.x, self.envelope.y, "Assets/envelope.png")
            camera.draw(self.envelope)
        elif self.envelope_x_done and self.envelope_y_done:
            camera.draw(self.letter)

    def update_physics(self, control_enabled, frame_count):
        if self.show_tilted_envelope and not self.envelope_picked_up:
            if self.envelope_tilted.y < screen_height / 2 + 280:
                if (frame_count - self.envelope_fall_start_frame) / fps % .5 == 0:
                    if self.envelope_tilted_x_vel < 0:
                        self.envelope_tilted_x_vel = self.envelope_tilted_x_speed
                    else:
                        self.envelope_tilted_x_vel = -self.envelope_tilted_x_speed
                self.envelope_tilted.y += self.envelope_tilted_y_speed
            else:
                self.envelope_tilted_x_vel = 0
                self.envelope.x = self.envelope_tilted.x
                self.envelope.y = self.envelope_tilted.y

        if not self.envelope_picked_up and not self.show_tilted_envelope and (frame_count - self.look_back_start_frame) / fps >= 2.2:
            self.show_tilted_envelope = True
            self.envelope_fall_start_frame = frame_count
            self.envelope_tilted.x = self.x_pos
            self.envelope_tilted.y = self.y_pos + 70
            self.envelope_tilted_x_vel = -self.envelope_tilted_x_speed
        elif self.envelope_picked_up:
            # calculate distance to center
            dist_to_x_center = (screen_width / 2) - self.envelope.x
            if (screen_width / 2) - self.envelope.x > 5:
                self.envelope.x += dist_to_x_center / 10
            else:
                self.envelope.x = screen_width / 2
                self.envelope_x_done = True
                
            dist_to_y_center = (screen_height / 2) - self.envelope.y
            if self.envelope.y - (screen_height / 2) > 5:
                self.envelope.y += dist_to_y_center / 10
            else:
                self.envelope.y = screen_height / 2
                self.envelope_y_done = True

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
        self.envelope_tilted.x += self.envelope_tilted_x_vel


    def update_animation(self):
        if self.x_vel == 0:
            self.animation = (self.idle_right_animation if self.facing == FaceDirection.RIGHT else self.idle_left_animation)
            self.num_sprite_frame = self.sprite_dict[AnimationAction.IDLE]

        super().update_animation()

    def look_back_jump_away(self, frame_count):
        if not self.look_back_done:
            if self.look_back_start_frame is None:
                self.look_back_start_frame = frame_count
                return

            look_back_frame = frame_count - self.look_back_start_frame
            if look_back_frame == 20:
                self.facing = FaceDirection.LEFT
                return

        # look_back_frame = frame_count - self.look_back_start_frame
        if self.look_back_done or look_back_frame >= 50:
                self.facing = FaceDirection.RIGHT
                self.look_back_done = True
                self.jump()

    def jump(self):
        if not self.jump_done:
            if self.animation != self.jump_right_animation:
                self.x_vel = self.run_speed
                self.y_vel = -9 - .25
                self.animation = self.jump_right_animation
                self.num_sprite_frame = self.sprite_dict[AnimationAction.JUMP]
                self.frame_count = 0

            self.y_vel += .375

            # one jump animation completed
            if self.frame_count != 0 and self.frame_count % self.num_sprite_frame == 0:
                self.jump_done = True
                self.y_vel = 0

                self.animation = self.run_right_animation
                self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN]
                self.frame_count = 0
