import uvage as u
import pygame
from Constants import *

class Dialogue:
    transition_speed = 10

    letter_spacing = 20
    line_spacing = 45

    def __init__(self, camera: u.Camera, text, position: Position, headshot_file_name, sound: pygame.mixer.Sound, mute, headshot_position: Position = Position.TOP):
        self.camera = camera

        self.text = text
        self.lines_printing_now: list[SlowPrintLine] = []
        self.unprinted_lines: list[SlowPrintLine] = []
        self.finished_printing = False

        self.position = position
        if self.position == Position.TOP:
            self.box_y = -100
            self.target_box_y = 150
        else:
            self.box_y = screen_height + 100
            self.target_box_y = screen_height - 150

        self.box = u.from_image(screen_width / 2, self.box_y, "Assets/UI/ChatBubble.png")
        self.box_width = self.box.width - 300

        self.done_transitioning = False
        self.show = False
        self.dismissed = False

        self.enter_key = u.from_image(self.box.x + self.box_width / 2 + 90, self.target_box_y + self.box.height / 2 - 36, "Assets/UI/enter_key.png")
        # self.enter_key: pygame.Surface = pygame.image.load("Assets/UI/enter_key.png").convert()
        # self.frame_start = None

        self.sound = sound
        self.sound_started = False
        self.mute = mute

        # print_speed = 1 / (letters / frame)
        # frames per second = fps
        # frames = sound.get_length * fps
        # print_speed = 1 / (len(self.text) / (sound.get_length * fps))
        self.print_speed = 1 / (len(self.text) / (self.sound.get_length() * fps))

        # create line separations
        self.lines: list[SlowPrintLine] = []
        overall_remaining_text = self.text
        while (len(overall_remaining_text) * self.letter_spacing) > self.box_width:
            line_text = ""
            remaining_words = overall_remaining_text.split(" ")
            while (len(line_text) * self.letter_spacing) < self.box_width:
                line_text += remaining_words[0] + " "
                remaining_words.pop(0)
            self.lines.append(SlowPrintLine(self.camera,
                                            line_text.strip(),
                                            self.letter_spacing,
                                            self.line_spacing,
                                            self.target_box_y,
                                            self.box.height,
                                            self.print_speed))
            overall_remaining_text = overall_remaining_text[len(line_text) - 1:]
        if len(overall_remaining_text) != 0:
            self.lines.append(SlowPrintLine(self.camera,
                                            overall_remaining_text.strip(),
                                            self.letter_spacing,
                                            self.line_spacing,
                                            self.target_box_y,
                                            self.box.height,
                                            self.print_speed))
        self.unprinted_lines = self.lines.copy()

        self.headshot = Headshot(self.camera, self.position, headshot_file_name, headshot_position)

    def set_text(self, text):
        self.text = text

    def draw(self, frame_count):
        if self.show and not self.dismissed:
            self.draw_box(frame_count)
            if self.done_transitioning:
                self.slow_print(frame_count)

                if not self.mute and not self.sound_started:
                    self.sound_started = True
                    self.sound.play()

            self.headshot.draw()

    def draw_box(self, frame_count):
        self.camera.draw(self.box)

        if not self.done_transitioning:
            if self.box_y != self.target_box_y:
                if self.position == Position.TOP:
                    self.box_y += self.transition_speed
                else:
                    self.box_y -= self.transition_speed
            else:
                self.finish_transition()
        self.box = u.from_image(screen_width / 2, self.box_y, "Assets/UI/ChatBubble.png")

        if self.finished_printing:
            # if self.frame_start is None:
            #     self.frame_start = frame_count
            # image: pygame.Surface = self.enter_key.copy()
            # image.fill((255, 255, 255, (frame_count - self.frame_start) % 100), None, pygame.BLEND_RGB_MULT)
            # image.blit(self.camera.__dict__['_surface'],
            #            (self.box.x + self.box_width / 2 + 90, self.target_box_y + self.box.height / 2 - 36))
            self.camera.draw(self.enter_key)

    def slow_print(self, frame_count):
        if len(self.unprinted_lines) != 0 and (len(self.lines_printing_now) == 0 or self.lines_printing_now[-1].done_printing):
            self.lines_printing_now.append(self.unprinted_lines.pop(0))
        elif len(self.unprinted_lines) == 0 and self.lines_printing_now[-1].done_printing:
            self.finished_printing = True

        for row, slow_print_line in enumerate(self.lines_printing_now):
            slow_print_line.print(frame_count, row, len(self.lines))

    def advance(self):
        if self.show:
            if not self.done_transitioning:
                self.finish_transition()
            elif not self.finished_printing:
                self.finish_printing()
            else:
                self.show = False
                self.dismissed = True

    def finish_transition(self):
        self.box_y = self.target_box_y
        self.done_transitioning = True
        self.headshot.finish_transition()

    def finish_printing(self):
        for slow_print_line in self.lines:
            slow_print_line.finish_printing()
        self.unprinted_lines = []
        self.lines_printing_now = self.lines.copy()
        self.finished_printing = True

        pygame.mixer.stop()


class SlowPrintLine:
    initial_frame: int = None
    done_printing = False
    font = pygame.font.SysFont('Monaco', 30)
    delegate: Dialogue = None

    def __init__(self, camera: u.Camera, text, letter_spacing, line_spacing, box_y, box_height, print_speed):
        self.camera = camera

        self.text = text
        self.letter_spacing = letter_spacing
        self.text_width = len(text) * letter_spacing
        self.line_spacing = line_spacing
        self.box_y = box_y
        self.box_height = box_height
        self.print_speed = print_speed

    def print(self, frame_count, row, row_count):
        if self.initial_frame is None and not self.done_printing:
            self.initial_frame = frame_count

        start_x, y = self.get_position(row, row_count)
        if self.done_printing:
            text_to_print = self.text

        else:
            # add 1 / print_speed amount of characters every frame
            text_to_add = 1 + int((frame_count - self.initial_frame) // self.print_speed)
            text_to_print = self.text[:text_to_add]
            # stop recalculating text_to_print when we've added the full array
            if text_to_add >= len(self.text):
                self.finish_printing()


        for index, char in enumerate(text_to_print):
            char_surface = self.font.render(char, False, pygame.Color("white"))
            self.camera.draw(char_surface, [start_x + (index * self.letter_spacing), y])

    def get_position(self, row, row_count):
        x = (screen_width / 2) - (self.text_width / 2)

        if row_count % 2 == 0:
            y = self.box_y + ((row - (row_count // 2)) * self.line_spacing) + self.line_spacing * 0.5
        else:
            y = self.box_y + ((row - (row_count // 2)) * self.line_spacing)
        return [x, y]

    def finish_printing(self):
        self.done_printing = True
        self.initial_frame = None

class Headshot:
    headshot_path_prefix = "Assets/Headshots/"
    transition_speed = 10

    def __init__(self, camera: u.Camera, position: Position, headshot_file_name, headshot_position: Position):
        self.camera = camera

        self.position = position

        if headshot_position == Position.TOP:
            self.x = screen_width / 2 - 550
        else:
            self.x = screen_width / 2 + 550

        if self.position == Position.TOP:
            self.y = -100
            self.target_y = 150
        else:
            self.y = screen_height + 100
            self.target_y = screen_height - 150

        self.headshot_path = self.headshot_path_prefix + headshot_file_name
        self.done_transitioning = False

    def draw(self):
        self.camera.draw(u.from_image(self.x, self.y, "Assets/UI/HeadshotFrame.png"))
        self.camera.draw(u.from_image(self.x, self.y, self.headshot_path))

        if not self.done_transitioning:
            if self.y != self.target_y:
                if self.position == Position.TOP:
                    self.y += self.transition_speed
                else:
                    self.y -= self.transition_speed
            else:
                self.y = self.target_y
                self.done_transitioning = True

    def finish_transition(self):
        self.y = self.target_y
        self.done_transitioning = True