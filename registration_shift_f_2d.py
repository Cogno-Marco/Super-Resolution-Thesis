import config
import math
from config import CAMERA_SIZE
import world_2d as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List
import random

repetitions: int = 100
config.CAMERA_RESOLUTION = 5
config.CAMERA_SIZE = 10
config.WORLD_SIZE = 100

# test each shift from 0 to r
offsets = [f for f in range(config.CAMERA_RESOLUTION+1)]
k_values = [k for k in range(config.CAMERA_SIZE)]

rightGuesses = [0 for i in range(len(offsets))]
for test in range(repetitions):
    world = w.World2D(config.WORLD_SIZE)
    for f in offsets:
        # try to guess at offset f, 
        # if you guess right count it, else continue
        guess: List[int] = []
        for i in range(config.CAMERA_SIZE):
            temp = []
            for k in range(config.CAMERA_SIZE):
                pixelType = world.getPixelColorType((f + k*config.CAMERA_RESOLUTION,i), config.CAMERA_RESOLUTION)
                #guess based on the color
                if pixelType == config.MacroTypes.GRAY_WHITE:
                    temp.append(1)
                elif pixelType == config.MacroTypes.GRAY_BLACK:
                    temp.append(0)
                elif pixelType == config.MacroTypes.GRAY:
                    temp.append(random.choice([0,1]))
            guess.append(temp)
            
        # snap at photo at index 0, let's see how many we guess at the wrong index
        photoValue = world.photo((0,0), config.CAMERA_SIZE, config.CAMERA_RESOLUTION)

        for i in range(len(photoValue)):
            for macro_guessed, macro_actual in zip(guess[i], photoValue[i]):
                if macro_guessed == macro_actual:
                    rightGuesses[f] += 1
        
        if test % int(repetitions/10) == 0 and f == 0:
            print(f"reached repetition n. {test}")

# Data for plotting
guessesProb: List[float] = [guess/repetitions for guess in rightGuesses]
print(guessesProb)
guessesProb: List[float] = [guess/(config.CAMERA_SIZE**2) for guess in guessesProb]
print(guessesProb)

# upper bound formula in the thesis
upper_bound = [math.pow(math.e, -(config.CAMERA_SIZE**2)*(f**2 or 1)/(768*config.CAMERA_RESOLUTION**3)) for f in offsets]

# calculate better bound
# starting c
c = math.log(guessesProb[0], math.e) + (config.CAMERA_SIZE**2) / (768 * config.CAMERA_RESOLUTION**3)
for i,x in enumerate(offsets):
    c2 = math.log(guessesProb[i], math.e) + ((config.CAMERA_SIZE**2) * (x**2 or 1)) / (768 * config.CAMERA_RESOLUTION**3)
    # if I've found a new c2 smaller than the others..
    if c2 > c:
        # it becomes the new upper bound
        c = c2

#calculate improved bound
better_bound = [math.pow(math.e, c-(config.CAMERA_SIZE**2)*(f**2 or 1)/(768*config.CAMERA_RESOLUTION**3)) for f in offsets]

#plot results
fig, ax = plt.subplots()
ax.plot(offsets, guessesProb, label='Tested Probability')
ax.plot(offsets, upper_bound, label=f'Upper Bound (c = 1/768)')
ax.plot(offsets, better_bound, label=f'Improved Upper Bound (c = {c})')
matplotlib.pyplot.xticks(offsets)
ax.set_ylim([-.1,1.1])

ax.set(xlabel='f', ylabel='P right guess',
       title='Probability of guessing at different offsets')
ax.grid()
ax.legend()

plt.show()