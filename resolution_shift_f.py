import numpy
import math
import world as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List


repetitions: int = 100
CAMERA_RESOLUTION = 8
CAMERA_SIZE = 40_000
WORLD_SIZE = 350_000
f=0
step = 320

def mu(f):
    #if f > CAMERA_RESOLUTION: return mu(CAMERA_RESOLUTION)
    return 0.5 + 1/(2 * CAMERA_RESOLUTION) - f/(2 * CAMERA_RESOLUTION**2)

# test each shift from 0 to r
#offsets = [0,1,CAMERA_RESOLUTION]
k_values = [k for k in range(CAMERA_RESOLUTION, CAMERA_SIZE, step)]

rightGuesses = [0 for _ in k_values]

#calculate epsilon and mu(0)
epsilon = 1/(2 * CAMERA_RESOLUTION**2 + 2 * CAMERA_RESOLUTION - 1)

for test in range(repetitions):
    world = w.World(WORLD_SIZE)
    for k in k_values:
        # try to guess at size k, 
        # if you guess right count it, else continue
        currentGuesses = 0
        
        #check a photo
        photoValue_1 = world.photo(0, k, CAMERA_RESOLUTION)
        #check another photo
        photoValue_2 = world.photo(f, k, CAMERA_RESOLUTION)
        
        #check how many are guessed correctly
        for macro_guessed, macro_actual in zip(photoValue_1, photoValue_2):
            if macro_guessed == macro_actual:
                currentGuesses += 1
        
        #count a successful one if it's over the bound
        if f != 0:
            if currentGuesses >= (1 + epsilon) * mu(f) * k:
                rightGuesses[int((k- k_values[0])/step)] += 1
        else:
            #1-bound for actual result
            if currentGuesses > (1 - epsilon) * mu(f) * k:
                rightGuesses[int((k- k_values[0])/step)] += 1
        
        if test % int(repetitions/10) == 0 and k == k_values[0]:
            print(f"reached repetition n. {test}")

# Data for plotting
print(rightGuesses)
guessesProb: List[float] = [guess/repetitions for guess in rightGuesses]
print(guessesProb)

# upper bound formula in the thesis
upper_bound = [math.pow(math.e, -k * (f or 1)/(150*CAMERA_RESOLUTION**3)) if f != 0
else 1 - math.pow(math.e, -k * (f or 1)/(150*CAMERA_RESOLUTION**3))
for k in k_values]

x = numpy.array(k_values)
y = numpy.array(guessesProb)
a, b = numpy.polyfit(x, numpy.log(y), 1)

# calculate better bound
#c = min([- math.log(p, math.e) * CAMERA_RESOLUTION**3 / (CAMERA_SIZE * (f or 1)) for p,f in zip(guessesProb, offsets)])

#calculate improved bound
#better_bound = [math.pow(math.e, b + a * (f or 1)) for k in k_values]


#plot results
fig, ax = plt.subplots()
ax.plot(k_values, guessesProb, label='Tested Probability')
ax.plot(k_values, upper_bound, label=(f'Upper Bound (c = 1/150)' if f!= 0 else f'Lower Bound (c=1/150)'))
#ax.plot(offsets, better_bound, label=f'Improved Upper Bound (a,b = {a:.2f},{b:.2f})')
#matplotlib.pyplot.xticks([k for k in k_values if (k - k_values[0]) % 100 == 0])
ax.set_ylim([-.1,1.1])

ax.set(xlabel='k', ylabel='P right guess',
       title=f'Resolution Chernoff bound (f={f})')
ax.grid()
ax.legend()

plt.show()