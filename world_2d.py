import random as rng
import config
from typing import List
import numpy as np

class World2D:
    
    def __init__(self, size):
        """Generates and returns a new 2d world with a given square size"""
        self._world = np.random.randint(2, size=(size,size))
    
    def getWorld(self):
        return self._world
        
    def count_whites(self, ind: int, r: int) -> int:
        """Returns how many white micropixels there are from [x,y] to [x+r,y+r] (ind = (x,y) )"""
        y,x = ind
        return sum(sum(self._world[x:x+r, y:y+r]))
    
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
        """
        y,x = ind
        out = np.zeros((k,k), dtype="int")
        for xi in range(k):
            for yi in range(k):
                r1 = rng.randint(0, r-1)
                r2 = rng.randint(0, r-1)
                #print((x+xi+r1), (y+yi+r2))
                out[xi,yi] = self._world[(x+xi+r1), (y+yi+r2)]
        return out