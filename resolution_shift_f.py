import config
import math
import world as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List


repetitions: int = 1_000
CAMERA_RESOLUTION = 5
CAMERA_SIZE = 1600
WORLD_SIZE = 9_000

def mu(f):
    return 0.5 + 1/(2 * CAMERA_RESOLUTION) - f/(2 * CAMERA_RESOLUTION**2)

# test each shift from 0 to r
offsets = [f for f in range(CAMERA_RESOLUTION+1)]

rightGuesses = [0 for i in offsets]

#calculate epsilon and mu(0)
epsilon = 1/(2 * CAMERA_RESOLUTION**2 + 2 * CAMERA_RESOLUTION - 1)

for test in range(repetitions):
    world = w.World(WORLD_SIZE)
    for f in offsets:
        # try to guess at offset f, 
        # if you guess right count it, else continue
        
        currentGuesses = 0
        #calculate mu(f)
        mu_f = mu(f)
        
        #check a photo
        photoValue_1 = world.photo(0, CAMERA_SIZE, CAMERA_RESOLUTION)
        #check another photo
        photoValue_2 = world.photo(f, CAMERA_SIZE, CAMERA_RESOLUTION)
        
        #check how many are guessed correctly
        for macro_guessed, macro_actual in zip(photoValue_1, photoValue_2):
            if macro_guessed == macro_actual:
                currentGuesses += 1
        
        if currentGuesses >= (1 + epsilon) * mu_f * CAMERA_SIZE:
            rightGuesses[f] += 1
        # if f != 0:
        # else:
        #     if currentGuesses <= (1- epsilon) * mu_f * CAMERA_SIZE:
        #         rightGuesses[f] += 1
        
        if test % int(repetitions/10) == 0 and f == 0:
            print(f"reached repetition n. {test}")

# Data for plotting
print(rightGuesses)
guessesProb: List[float] = [guess/repetitions for guess in rightGuesses]
print(guessesProb)

# upper bound formula in the thesis
upper_bound = [math.pow(math.e, -CAMERA_SIZE * f/(150*CAMERA_RESOLUTION**3)) for f in offsets]

# calculate better bound
# starting c
c = math.log(guessesProb[0], math.e) + (CAMERA_SIZE) / (768 * CAMERA_RESOLUTION**3)
for i,x in enumerate(offsets):
    c2 = math.log(guessesProb[i], math.e) + (CAMERA_SIZE * (x**2 or 1)) / (768 * CAMERA_RESOLUTION**3)
    # if I've found a new c2 smaller than the others..
    if c2 > c:
        # it becomes the new upper bound
        c = c2

#calculate improved bound
better_bound = [math.pow(math.e, c-CAMERA_SIZE*(f**2 or 1)/(768*CAMERA_RESOLUTION**3)) for f in offsets]

#plot results
fig, ax = plt.subplots()
ax.plot(offsets, guessesProb, label='Tested Probability')
ax.plot(offsets, upper_bound, label=f'Upper Bound (c = 1/768)')
#ax.plot(offsets, better_bound, label=f'Improved Upper Bound (c = {c})')
matplotlib.pyplot.xticks(offsets)
ax.set_ylim([-.1,1.1])

ax.set(xlabel='f', ylabel='P right guess',
       title='Probability of guessing at different offsets')
ax.grid()
ax.legend()

plt.show()