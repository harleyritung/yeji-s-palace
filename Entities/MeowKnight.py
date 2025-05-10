from Constants import *
from Entities.Player import PlayerPath, Player

class MeowKnight(Player):
    def __init__(self, x_pos, y_pos, facing: FaceDirection = FaceDirection.RIGHT):
        super().__init__(x_pos, y_pos, PlayerPath.MeowKnight.value, facing)

        self.animation = self.idle_left_animation
