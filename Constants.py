import enum

screen_width = 1512
screen_height = 850

frame_increment = 0.25

fps = 30

# controls
controls = {'right': 'd', 'left': 'a', 'down': 's', 'up': 'w', 'jump': 'space', 'attack': 'return',
            'dodge': 'left shift'}

# GUI
# backgrounds
background_file_path = "Assets/Backgrounds/"

# treasure room
treasure_file_path = background_file_path + "treasure_room.png"
blackout_file_path = background_file_path + "blackout.png"
treasure_sacked_file_path = background_file_path + "treasure_room_sacked.png"

# hallway
hallway_file_path = background_file_path + "castle_hallway_2.png"
hallway_3_file_path = background_file_path + "castle_hallway_3.png"

forest_filepath = background_file_path + "forest.png"

# Audio
dialogue_volume = .3

class AnimationAction(enum.Enum):
    RUN_START = "run_start"
    RUN_STOP = "run_stop"
    IDLE="idle"
    RUN= "run_loop"
    JUMP="jump"
    DEATH="death"
    DODGE="dodge"

class FaceDirection(enum.Enum):
    LEFT="left"
    RIGHT="right"

class Position(enum.Enum):
    TOP = "top"
    BOTTOM = "bottom"

class Key(enum.Enum):
    LEFT = "a"
    RIGHT = "d"
    UP = "w"
    ESCAPE = "escape"
    ENTER = "return"

class Room(enum.Enum):
    HALLWAY = "hallway"
    TREASURE = "treasure"
    FOREST = "forest"

class Scene(enum.Enum):
    INTRO = "intro"
    BLACKOUT = "blackout"
    SACKED = "sacked"


