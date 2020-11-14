import random as rng
import config
from typing import List
import numpy as np

class World:
    
    def __init__(self, size=config.WORLD_SIZE):
        """Generates and returns a new world with a given size (default taken from config)"""
        self._world = [rng.randint(0,1) for i in range(size)]
    
    def getWorld(self):
        return self._world
        
    def count_whites(self, ind: int, r: int =config.CAMERA_RESOLUTION) -> int:
        """Returns how many white micropixels there are in range [ind, ind+r]"""
        return sum(self._world[ind:ind+r])
    
    def count_grays(self, macro_count: int, r: int =config.CAMERA_RESOLUTION) -> int:
        """Returns how many gray macropixels there are in range [0, macro_count]"""
        s: float = config.getSoglia(r)
        #count whites from index 0 to index r
        out: int = 0
        for k in range(macro_count):
            whites: int = self.count_whites(k*r, r)
            if whites < r/2 + s and whites > r/2 - s:
                out += 1
        return out
    
    def getPixelColorValue(self, ind: int, r: int = config.CAMERA_RESOLUTION) -> float:
        """Returns the value of a pixel [0..1] in the world in range [ind, ind+r], 0 means all black, 1 means all white"""
        return self.count_whites(ind, r) / r
    
    def getPixelColorType(self, ind: int, r: int = config.CAMERA_RESOLUTION) -> config.MacroTypes:
        """Returns the enum value of a macropixel in the world in range [ind, ind+r]"""
        whites = self.count_whites(ind, r)
        s = config.getSoglia(r)
        if whites > r/2 + s: return config.MacroTypes.GRAY_WHITE
        if whites < r/2 + s and whites > r/2 - s: return config.MacroTypes.GRAY
        return config.MacroTypes.GRAY_BLACK
    
    
    def photo(self, ind: int, k:int = config.CAMERA_SIZE, r:int = config.CAMERA_RESOLUTION) -> List[int]:
        """
        returns a photo of the world starting at a given index
        uses a circular photo
        """
        if ind + k * r <= len(self._world):
            return [rng.choice(self._world[ind+r*i:ind+r*(i+1)]) for i in range(k)]
        else:
            # outside photo range, use a circular tactic
            whites: List[int] = [0] * k
            for i in range(k*r):
                whites[int(i/r)] += self._world[(ind+i)%len(self._world)]
            return [1 if rng.random() < whites[i]/r else 0 for i in range(k)]