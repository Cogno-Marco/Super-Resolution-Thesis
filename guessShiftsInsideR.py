import config
import math
import world as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List
import random

repetitions: int = 1_000
config.CAMERA_RESOLUTION = 10
config.CAMERA_SIZE = 3
config.WORLD_SIZE = config.CAMERA_SIZE * config.CAMERA_RESOLUTION+config.CAMERA_RESOLUTION

# test each shift from 0 to r
offsets = [f for f in range(config.CAMERA_RESOLUTION+1)]
k_values = [k for k in range(config.CAMERA_SIZE)]

rightGuesses = [0 for i in range(len(offsets))]
for test in range(repetitions):
    world = w.World(config.WORLD_SIZE)
    for f in offsets:
        # try to guess at offset f, 
        # if you guess right count it, else continue
        guess: List[int] = []
        for k in range(config.CAMERA_SIZE):
            pixelType = world.getPixelColorType(f + k*config.CAMERA_SIZE, config.CAMERA_RESOLUTION)
            #guess based on the color
            if pixelType == config.MacroTypes.GRAY_WHITE:
                guess.append(1)
            elif pixelType == config.MacroTypes.GRAY_BLACK:
                guess.append(0)
            elif pixelType == config.MacroTypes.GRAY:
                guess.append(random.choice([0,1]))
            
        # snap at photo at index 0, let's see how many we guess at the wrong index
        photoValue = world.photo(0, config.CAMERA_SIZE, config.CAMERA_RESOLUTION)

        if photoValue == guess:
            rightGuesses[f] += 1
        
        if test % int(repetitions/10) == 0 and f == 0: print(f"reached repetition n. {test}")

# Data for plotting
guessesProb: List[float] = [guess/repetitions for guess in rightGuesses]
print(guessesProb)
upper_bound = [math.pow(math.e, -config.CAMERA_SIZE*(i**2 or 1)/(768*config.CAMERA_RESOLUTION**3)) for i in offsets]

fig, ax = plt.subplots()
ax.plot(offsets, guessesProb, label='Tested Probability')
ax.plot(offsets, upper_bound, label=f'Upper Bound')
matplotlib.pyplot.xticks(offsets)

ax.set(xlabel='f', ylabel='P right guess',
       title='Probability of guessing at different offsets')
ax.grid()
ax.legend()

plt.show()