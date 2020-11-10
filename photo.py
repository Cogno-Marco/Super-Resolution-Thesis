from typing import List
from world import World

class Photo:
    def __init__(self, world: World, k: int, r: int, offset: int):
        self.photo = world.photo(offset, k, r)
        self.r = r
        self.k = k
        self.offset = offset