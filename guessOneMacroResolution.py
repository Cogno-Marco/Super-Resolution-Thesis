import config
import world as w
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
from typing import List
import random

config.CAMERA_SIZE = 1 # set k = 1
config.CAMERA_RESOLUTION = 100
config.WORLD_SIZE = config.CAMERA_SIZE * config.CAMERA_RESOLUTION+1

offset = 50
repetitions: int = 200_000

xPossibles = [i/config.WORLD_SIZE for i in range(config.WORLD_SIZE)]

print("calculated possibles")

yCalculated: List[float] = []

# strategy to guess one macro: if world has more whites guess it as white,
# if world has more blacks guess it as black
# P to guess one macro right = how many times I got it right / how many I tried
print(config.WORLD_SIZE)
tries = [0 for i in range(config.WORLD_SIZE)]
correctGuesses = [0 for i in range(config.WORLD_SIZE)]
for i in range(repetitions):
    world = w.World(config.WORLD_SIZE)
    
    #check a photo
    photoValue_1 = world.photo(0, config.CAMERA_SIZE, config.CAMERA_RESOLUTION)[0]
    
    #check another photo
    photoValue_2 = world.photo(offset, config.CAMERA_SIZE, config.CAMERA_RESOLUTION)[0]

    tries[world.count_whites(0, config.CAMERA_RESOLUTION)] += 1
    
    if photoValue_1 == photoValue_2:
        correctGuesses[world.count_whites(0, config.CAMERA_RESOLUTION)] += 1
    
    if i % int(repetitions/10) == 0: print(f"reached i = {i}")


print("finished worlds")
expected_f0 = [2*(i/config.WORLD_SIZE)**2 -2*(i/config.WORLD_SIZE)+1 for i in range(config.WORLD_SIZE)]
expected_f1 = [2*(i/config.WORLD_SIZE)**2 * (1-offset/config.CAMERA_RESOLUTION) 
              -2*(i/config.WORLD_SIZE) * (1-offset/config.CAMERA_RESOLUTION) 
              + 1 - offset/(2*config.CAMERA_RESOLUTION)
              for i in range(config.WORLD_SIZE)]
              
print("finished expecteds")
actual = [correctGuesses[i]/tries[i] if tries[i] else 0 for i in range(config.WORLD_SIZE)]

fig, ax1 = plt.subplots()
matplotlib.pyplot.xticks([0,0.2,0.4,0.6,0.8,1])

color = 'tab:red'
ax1.set_xlabel(f'pixel value (offset = {offset})')
ax1.set_ylabel('probability', color=color)
ax1.plot(xPossibles, expected_f0, label='Expected Probability (f=0)', color=color)
ax1.plot(xPossibles, expected_f1, label='Expected Probability (f=1)', color="tab:gray")
ax1.plot(xPossibles, actual, label='Actual Probability', color="tab:green")
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('tries count', color=color)  # we already handled the x-label with ax1
ax2.plot(xPossibles, tries, label=f'Tries (total = {repetitions})', color=color)
ax2.tick_params(axis='y', labelcolor=color)

#ax1.set(xlabel='k', ylabel='P(X<=k/4)',
#       title='Probability of guessing right one macro (f=0)')

ax1.grid()
ax1.legend()
ax2.legend()

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()