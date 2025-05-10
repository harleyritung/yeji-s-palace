from Constants import *
import uvage as u
from Entities.Player import PlayerPath, Player

class KingMeowthur(Player):
    run_speed = 6

    def __init__(self, x_pos, y_pos, facing: FaceDirection = FaceDirection.RIGHT):
        super().__init__(x_pos, y_pos, PlayerPath.KingMeowthur.value, facing, run=8)

        self.run_right_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run.png",
                                                       1,
                                                       self.sprite_dict[AnimationAction.RUN])
        self.run_left_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run_left.png",
                                                      1,
                                                      self.sprite_dict[AnimationAction.RUN])

        self.search_frame_start = None
        self.search_count = 0
        self.search_done = False

        self.pace_frame_start = None

    def update_physics(self, control_enabled, frame_count):
        self.x_pos += self.x_vel

    def update_animation(self):
        super().update_animation_helper()
        super().update_animation()

    def search(self, frame_count):
        if self.search_frame_start is None:
            self.search_frame_start = frame_count

        search_frame = frame_count - self.search_frame_start
        if search_frame % 20 == 0:
            self.search_count += 1
            if self.facing == FaceDirection.RIGHT:
                self.facing = FaceDirection.LEFT
            else:
                self.facing = FaceDirection.RIGHT

            if self.search_count == 4:
                self.search_done = True

    def pace(self, frame_count):
        if self.pace_frame_start is None:
            self.pace_frame_start = frame_count

        pace_frame = frame_count - self.pace_frame_start
        if pace_frame % 20 == 0:
            if self.facing == FaceDirection.RIGHT:
                self.x_vel = -self.run_speed
            else:
                self.x_vel = self.run_speed

