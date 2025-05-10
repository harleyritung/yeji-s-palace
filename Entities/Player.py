import uvage as u
from Constants import *
from Entities.Entity import Entity


class Player(Entity):
    run_start_right_animation = []
    run_start_loop_animation = []
    run_right_animation = []
    run_left_animation = []
    run_stop_right_animation = []
    run_stop_left_animation = []

    # player stats
    run_speed = 14

    # num of animation frames in each animation
    num_sprite_frame = 6

    default_facing = FaceDirection.RIGHT
    width: int

    assetPathPrefix = "Assets/Sprites/Players/"

    def __init__(self, x_pos, y_pos, player_path: str, facing: FaceDirection = FaceDirection.RIGHT, idle=6, run=4, run_start=None, run_stop=None, jump=12):
        super().__init__(x_pos, y_pos, facing)
        self.player_path = player_path
        self.sprite_dict = {
            AnimationAction.IDLE: idle,
            AnimationAction.RUN: run,
            AnimationAction.RUN_START: run_start,
            AnimationAction.RUN_STOP: run_stop,
            AnimationAction.JUMP: jump,
            AnimationAction.DEATH: 8,
            AnimationAction.DODGE: 5
        }

        self.idle_right_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/idle.png",
                                                        1,
                                                        self.sprite_dict[AnimationAction.IDLE])
        self.idle_left_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/idle_left.png",
                                                       1,
                                                       self.sprite_dict[AnimationAction.IDLE])

        if self.sprite_dict[AnimationAction.RUN_START] is not None:
            self.run_start_right_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/run_start.png",
                                                                 1,
                                                                 self.sprite_dict[AnimationAction.RUN_START])
            self.run_start_left_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/run_start_left.png",
                                                                1,
                                                                self.sprite_dict[AnimationAction.RUN_START])
        if self.sprite_dict[AnimationAction.RUN_STOP] is not None:
            self.run_stop_right_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/run_stop.png",
                                                                1,
                                                                self.sprite_dict[AnimationAction.RUN_STOP])
            self.run_stop_left_animation = u.load_sprite_sheet(self.assetPathPrefix + player_path + "/run_stop_left.png",
                                                               1,
                                                               self.sprite_dict[AnimationAction.RUN_STOP])

        self.num_sprite_frame = self.sprite_dict[AnimationAction.IDLE]

    def draw(self, camera, control_enabled, frame_count):
        self.update(control_enabled, frame_count)

        # need to reverse the order of frames for the flipped animations
        if self.get_if_flipped():
            self.animation_frame.image = self.animation[
                self.num_sprite_frame - int(self.frame_count % self.num_sprite_frame) - 1]
        else:
            self.animation_frame.image = self.animation[int(self.frame_count % self.num_sprite_frame)]
        camera.draw(self.animation_frame)

        # increment sprite animations
        self.frame_count += frame_increment

    def update(self, control_enabled, frame_count):
        self.update_physics(control_enabled, frame_count)
        self.update_animation()

    def update_physics(self, control_enabled, frame_count):
        return

    def update_animation(self):
        self.animation_frame = u.from_image(self.x_pos, self.y_pos, self.animation[0])

    def update_animation_helper(self):
        if self.x_vel == 0:
            self.animation = (self.idle_right_animation if self.facing == FaceDirection.RIGHT else self.idle_left_animation)
            self.num_sprite_frame = self.sprite_dict[AnimationAction.IDLE]
        elif self.x_vel > 0:
            if self.animation != self.run_right_animation:
                self.facing = FaceDirection.RIGHT
                self.animation = self.run_right_animation
                self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN]
                self.frame_count = 0
        elif self.x_vel < 0:
            if self.animation != self.run_left_animation:
                self.facing = FaceDirection.LEFT
                self.animation = self.run_left_animation
                self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN]
                self.frame_count = 0

class PlayerPath(enum.Enum):
    Meowtar = "Meowtar The Blue"
    KingMeowthur = "King Meowthur"
    Meowolas = "Meowolas"
    MeowKnight = "Meow Knight"