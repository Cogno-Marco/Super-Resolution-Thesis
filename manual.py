import random as rng
import numpy as np
from world_2d import World2D

w = World2D(5)
print(w.getWorld())

print(w.count_whites((0,0), 5))
print(w.count_whites((2,2), 2))
print(w.count_whites((0,2), 2))

print(w.photo((0,0), 5, 1))
print(w.photo((0,0), 2, 2))
print(w.photo((1,1), 2, 2))