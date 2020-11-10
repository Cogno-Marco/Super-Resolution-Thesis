import random as rng
import config
from typing import List, Tuple, Any
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from nptyping import NDArray

Photo = List[List[int]]


class World2D:

    def __init__(self, size, use_image=False):
        """Generates and returns a new 2d world with a given square size"""
        if use_image:
            # load image
            loaded = io.imread(f"ConnectedComponentsAnalysis/Lenna.png")

            # grayscale image
            step_count = 2
            grayscale = rgb2gray(loaded) * step_count
            self._world: NDArray[(Any, 2, Any)] = np.array(
                [[int(p) for p in line] for line in grayscale])
        else:
            self._world: NDArray[(Any, 2, Any)] = np.array(
                [[rng.randint(0, 1) for _ in range(size)] for _ in range(size)])

    def getWorld(self):
        return self._world

    def count_whites(self, ind: Tuple[int, int], r: int) -> int:
        """Returns how many white micropixels there are from [x,y] to [x+r,y+r] (ind = (x,y) )"""
        y, x = ind
        return sum(sum(self._world[x:x+r, y:y+r]))

    def getPixelColorValue(self, ind: Tuple[int, int], r: int = config.CAMERA_RESOLUTION) -> float:
        """Returns the value of a pixel [0..1] in the world in range [ind, ind+r], 0 means all black, 1 means all white"""
        return self.count_whites(ind, r) / (r**2)

    def getPixelColorType(self, ind: Tuple[int, int], r: int = config.CAMERA_RESOLUTION) -> config.MacroTypes:
        """Returns the enum value of a macropixel in the world in range [ind, ind+r]"""
        whites = self.count_whites(ind, r)
        s = config.getSoglia(r)
        if whites > (r**2)/2 + s:
            return config.MacroTypes.GRAY_WHITE
        if whites < (r**2)/2 - s:
            return config.MacroTypes.GRAY_BLACK
        return config.MacroTypes.GRAY

    def photo(self, ind: Tuple[int, int], k: int = config.CAMERA_SIZE, r: int = config.CAMERA_RESOLUTION) -> Photo:
        """
        returns a photo of the world starting at a given index
        """
        y, x = ind
        out = np.zeros((k, k), dtype="int")
        for xi in range(k):
            for yi in range(k):
                r1 = rng.randint(0, r-1)
                r2 = rng.randint(0, r-1)
                #print((x+xi*r+r1), (y+yi*r+r2))
                out[yi, xi] = self._world[(y+yi*r+r2), (x+xi*r+r1)]
        return out
