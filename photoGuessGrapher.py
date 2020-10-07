import config
import math
import world as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List
import random

repetitions: int = 10_000
config.CAMERA_RESOLUTION = 10
config.CAMERA_SIZE = 10
config.WORLD_SIZE = config.CAMERA_SIZE * config.CAMERA_RESOLUTION+config.CAMERA_RESOLUTION

k_values = [k+1 for k in range(config.CAMERA_SIZE)]

rightGuesses = [0 for i in range(len(k_values))]
for test in range(repetitions):
    world = w.World(config.WORLD_SIZE)
    # try to guess k pixels 
    # if you guess right count it, else continue
    for k in k_values:
        guess: List[int] = []
        for i in range(k):
            pixelType = world.getPixelColorType(k*config.CAMERA_RESOLUTION, config.CAMERA_RESOLUTION)
            #guess based on the color
            if pixelType == config.MacroTypes.GRAY_WHITE:
                guess.append(1)
            elif pixelType == config.MacroTypes.GRAY_BLACK:
                guess.append(0)
            elif pixelType == config.MacroTypes.GRAY:
                guess.append(random.choice([0,1]))
        
        # snap at photo at index 0, let's see how many we guess with changing camera size
        photoValue = world.photo(0, k, config.CAMERA_RESOLUTION)

        if photoValue == guess:
            rightGuesses[k-1] += 1
        
    if test % int(repetitions/10) == 0: print(f"reached repetition n. {test}")

# Data for plotting
guessesProb: List[float] = [guess/repetitions for guess in rightGuesses]
print(guessesProb)

fig, ax = plt.subplots()
ax.plot(k_values, guessesProb, label='Tested Probability')
matplotlib.pyplot.xticks(k_values)

ax.set(xlabel='k', ylabel='P right guess',
       title='Probability of guessing right k pixels')
ax.grid()
ax.legend()

plt.show()