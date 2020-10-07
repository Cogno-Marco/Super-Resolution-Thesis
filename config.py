import math
from enum import Enum

"""
Config file with general constants defined project wide
"""
SOGLIA_CONSTANT: float = 1/4
WORLD_SIZE: int = 10_000
CAMERA_SIZE: int = 2
CAMERA_RESOLUTION: int = 100
CAMERA_MICRO_SIZE: int = CAMERA_SIZE * CAMERA_RESOLUTION

class MacroTypes(Enum):
    GRAY_WHITE = 1
    GRAY = 2
    GRAY_BLACK = 3

def getSoglia(r: int =CAMERA_RESOLUTION):
    """Returns the soglia based on constants in range [0,r]"""
    return math.sqrt(r)*SOGLIA_CONSTANT

def getSoglia_scaled(r: int =CAMERA_RESOLUTION):
    """Returns the soglia based on constants in range [0,1]"""
    return SOGLIA_CONSTANT/math.sqrt(r)

SOGLIA: float = getSoglia(CAMERA_RESOLUTION)
