from Constants import *
import uvage as u
from Entities.Player import Player, PlayerPath

class Meowtar(Player):
    def __init__(self, x_pos, y_pos, facing: FaceDirection = FaceDirection.RIGHT):
        super().__init__(x_pos, y_pos, PlayerPath.Meowtar.value, facing, idle=6, run_start=3, run_stop=4, jump=13)

        self.run_right_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run.png",
                                                       1,
                                                       self.sprite_dict[AnimationAction.RUN])
        self.run_left_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/run_left.png",
                                                      1,
                                                      self.sprite_dict[AnimationAction.RUN])
        self.jump_right_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/jump.png",
                                                        1,
                                                        self.sprite_dict[AnimationAction.JUMP])
        self.jump_left_animation = u.load_sprite_sheet(self.assetPathPrefix + self.player_path + "/jump_left.png",
                                                        1,
                                                        self.sprite_dict[AnimationAction.JUMP])

        self.jumping = False

    def update_physics(self, control_enabled, frame_count):
        # modify velocities based on arrow input
        if self.sprite_dict[AnimationAction.RUN_START] is not None:
            run_start_frames = self.sprite_dict[AnimationAction.RUN_START]
        else:
            run_start_frames = 3

        if control_enabled:
            # if u.did_keydown(Key.UP) or self.jumping:
            #     self.jump()
            if u.is_pressing(Key.RIGHT):
                if self.jumping:
                    self.x_vel += 1
                else:
                    # quick turnaround
                    if self.x_vel < 0:
                        self.x_vel = 0
                    if self.x_vel < self.run_speed:
                        self.x_vel += (self.run_speed / (run_start_frames / frame_increment))
            elif u.is_pressing(Key.LEFT):
                if self.jumping:
                    self.x_vel -= 1
                else:
                    # quick turnaround
                    if self.x_vel > 0:
                        self.x_vel = 0
                    if self.x_vel > -self.run_speed:
                        self.x_vel -= (self.run_speed / (run_start_frames / frame_increment))
            else:
                if self.sprite_dict[AnimationAction.RUN_STOP] is not None:
                    run_stop_frames = self.sprite_dict[AnimationAction.RUN_STOP]
                else:
                    run_stop_frames = 4
                deceleration = self.run_speed / (run_stop_frames / frame_increment)

                if self.x_vel != 0:
                    if self.x_vel >= deceleration:
                        self.x_vel -= deceleration
                    elif self.x_vel <= -deceleration:
                        self.x_vel += deceleration
                if (-deceleration < self.x_vel < 0) or (0 < self.x_vel < deceleration):
                    self.x_vel = 0

        # speed limit
        if self.x_vel > self.run_speed:
            self.x_vel = self.run_speed
        elif self.x_vel < -self.run_speed:
            self.x_vel = -self.run_speed

        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    def update_animation(self):
        if self.jumping:
            if u.is_pressing(Key.RIGHT):
                self.facing = FaceDirection.RIGHT
                self.animation = self.jump_right_animation
            if u.is_pressing(Key.LEFT):
                self.facing = FaceDirection.LEFT
                self.animation = self.jump_left_animation
        else:
            if self.x_vel == 0:
                self.animation = (self.idle_right_animation if self.facing == FaceDirection.RIGHT else self.idle_left_animation)
                self.num_sprite_frame = self.sprite_dict[AnimationAction.IDLE]
            elif self.x_vel == self.run_speed:
                if self.animation != self.run_right_animation:
                    self.animation = self.run_right_animation
                    self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN]
                    self.frame_count = 0
            elif self.x_vel == -self.run_speed:
                if self.animation != self.run_left_animation:
                    self.animation = self.run_left_animation
                    self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN]
                    self.frame_count = 0
            elif self.x_vel > 0:
                # increasing speed to the right
                if u.is_pressing(Key.RIGHT):
                    if self.animation != self.run_start_right_animation:
                        self.facing = FaceDirection.RIGHT
                        self.animation = self.run_start_right_animation
                        self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN_START]
                        self.frame_count = 0
                # decreasing speed to the right
                else:
                    if self.animation != self.run_stop_right_animation:
                        self.animation = self.run_stop_right_animation
                        self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN_STOP]
                        self.frame_count = 0
            elif self.x_vel < 0:
                # increasing speed to the left
                if u.is_pressing(Key.LEFT):
                    if self.animation != self.run_start_left_animation:
                        self.facing = FaceDirection.LEFT
                        self.animation = self.run_start_left_animation
                        self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN_START]
                        self.frame_count = 0
                # decreasing speed to the right
                else:
                    if self.animation != self.run_stop_left_animation:
                        self.animation = self.run_stop_left_animation
                        self.num_sprite_frame = self.sprite_dict[AnimationAction.RUN_STOP]
                        self.frame_count = 0

        super().update_animation()

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.y_vel = -6 - .625
            self.num_sprite_frame = self.sprite_dict[AnimationAction.JUMP]
            self.frame_count = 0
            if self.facing == FaceDirection.RIGHT:
                self.animation = self.jump_right_animation
            else:
                self.animation = self.jump_left_animation

        self.y_vel += .25
        print(self.y_vel)

        # one jump animation completed
        if self.frame_count != 0 and self.frame_count % self.num_sprite_frame == 0:
            self.jumping = False
            self.y_vel = 0
