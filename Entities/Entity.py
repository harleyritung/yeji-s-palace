from Constants import *
from uvage import SpriteBox


class Entity:
    idle_right_animation = None
    idle_left_animation = None

    # entity animation state
    moving = False
    jumping = False
    dodging = False

    # collider box for entity
    collider = None

    # records total animation frames for each animation
    sprite_dict = {}

    """animation info"""
    # tells what frame of animation to draw
    animation_frame: SpriteBox = None
    # tells how many frames total are in the animation
    num_sprite_frame: int
    # used for calculating how far into an animation the sprite is
    frame_count = 0

    # relative positions and velocity
    x_vel = 0
    y_vel = 0

    # stats
    max_health = 3
    curr_health = 3

    def __init__(self, x, y, facing: FaceDirection = FaceDirection.RIGHT):
        self.x_pos = x
        self.y_pos = y
        self.facing = facing
        self.default_facing = FaceDirection.RIGHT
        # selects which animation to draw
        self.animation = (self.idle_right_animation if self.facing == FaceDirection.RIGHT else self.idle_left_animation)

    def get_if_flipped(self):
        return False if self.facing == self.default_facing else True

    # return collider if entity will touch it in next frame else return false
    def get_will_touch_ground(self, ground_colliders):
        for collider in ground_colliders:
            # don't check self for collision
            if collider != self.collider:
                if collider.contains(self.x_pos + self.x_vel, self.bottom_y + self.y_vel):
                    return collider
        return False
