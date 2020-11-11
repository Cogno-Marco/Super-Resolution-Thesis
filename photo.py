from math import sqrt
from typing import List
from world import World
import math

class Photo:
    currentID = 0
    
    def __init__(self, world: World, k: int, r: int, offset: int):
        self.photo = world.photo(offset, k, r)
        self.r = r
        self.k = k
        self.offset = offset
        self.ID = Photo.currentID
        Photo.currentID += 1
    
    def get_photo(self) -> List[int]:
        return self.photo
    
    def get_distance(self, photo: "Photo"):
        return sum([k1 ^ k2 for k1, k2 in zip(photo.get_photo(), self.photo)])
    
    def is_photo_aligned(self, photo: "Photo"):
        return False
        #return self.get_distance(photo) < (self.k / 2 - math.sqrt(self.k) / 2)
        #return self.get_distance(photo) < self.k *3 / 4