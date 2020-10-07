from typing import List
import math
import matplotlib#type: ignore
import matplotlib.pyplot as plt#type: ignore
import config
import world as w


# Data for plotting
k_values: List[int] = [i for i in range(1,20)]
grays_prob: List[float] = [0 for k in k_values]
upper_bound = [math.pow(math.e, -i*1369/12400) for i in k_values]

# for each k, test a lot of times
# count how many grays you got out of k pixels
# count how many times you got too many grays (or too little coloured)
# probability of event "too many grays" is 
# how many times you got too many / how many times you tested

for current_k in k_values:
    too_many_grays_count = 0
    test_times = 1_000
    for i in range(test_times):
        # generate new world
        currentWorld = w.World(current_k*config.CAMERA_RESOLUTION)
        # count how many grays there are in this round
        current_grays: int = currentWorld.count_grays(current_k)
        current_coloured = current_k - current_grays
        
        # count the event "too little coloured"if I got it this time
        if current_coloured <= current_k / 4:
            too_many_grays_count += 1
        
    print(f"total grays for {current_k} k, got too many grays for {too_many_grays_count} times")
    #prob is how many you got / how max you could get
    prob: float = too_many_grays_count / (test_times)
    grays_prob[current_k - k_values[0]] = prob

# calculate better bound
c = - math.log(grays_prob[0], math.e) / k_values[0] # starting c
for i,x in enumerate(k_values):
    c2 = - math.log(grays_prob[i] or 1, math.e) / x # current c
    # if I've found a new c2 smaller than the others..
    if c2 < c and c2 > 1369/12400:
        # it becomes the new upper bound
        c = c2

better_bound = [math.pow(math.e, -i*c) for i in k_values]

fig, ax = plt.subplots()
ax.plot(k_values, grays_prob, label='Tested Probability')
ax.plot(k_values, upper_bound, label=f'Upper Bound (c = {1369/12400})')
ax.plot(k_values, better_bound, label=f'Better Bound (c = {c})')
matplotlib.pyplot.xticks(k_values)

ax.set(xlabel='k', ylabel='P(X<=k/4)',
       title='Probability of too many grays')
ax.grid()
ax.legend()

plt.show()