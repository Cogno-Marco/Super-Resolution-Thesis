from skimage import measure
from skimage import filters
from skimage import data
from skimage.color import rgb2gray
import matplotlib.pyplot as plt
import numpy as np
import math
import os
from skimage import io

#setup graphs
fig, axs = plt.subplots(4, 4)

#load images into graph
folder = "ConnectedComponentsAnalysis/"
images = ["Lenna", "airplane", "cat", "tulips"]
for i, image in enumerate(images):
    #load image and put in first square
    loaded = io.imread(f"{folder}{image}.png")
    axs[0,i].imshow(loaded)

    #grayscale image
    step_count = 8
    grayscale = rgb2gray(loaded) * step_count
    grayscale = np.array([[int(p) for p in line] for line in grayscale])
    axs[1, i].imshow(grayscale, cmap='gray')
    
    #find connected components
    all_labels = measure.label(grayscale, connectivity=1, background=0)
    axs[2,i].imshow(all_labels, cmap='viridis')
    
    #convert matrix into array of connected components (cc) of type [(id, size)]
    regions_sizes = {}
    for line in all_labels:
        for cell in line:
            if cell not in regions_sizes:
                regions_sizes[cell] = 1
            else:
                regions_sizes[cell] += 1
    connected_comps = list(regions_sizes.items())
    
    print(connected_comps)
    
    #count for each cc size how many pixels
    sizes_count = {}
    for comp_id, size in connected_comps:
        actual_size = int(math.pow(2,int(math.log2(size))))
        exponent = int(math.log2(actual_size))
        if exponent not in sizes_count:
            sizes_count[exponent] = size
        else:
            sizes_count[exponent] += size
    
    #separate into arrays
    sizes = [k for k,_ in sizes_count.items()]
    count = [v for _,v in sizes_count.items()]
    
    #show scatter plot
    axs[3,i].scatter(sizes, count)
    axs[3,i].set_ylim([-5000, max(count)+5000])
    axs[3,i].set_xticks(range(max(sizes)+1))
    axs[3,i].set_yticks(range(0,max(count), 40000))
    
    


plt.suptitle(f"Relation between component size and component count")

for i in range(4):
    for j in range(3):
        axs[j,i].get_xaxis().set_visible(False)
        axs[j,i].get_yaxis().set_visible(False)
    
    axs[3,i].get_xaxis().grid()
    axs[3,i].get_yaxis().grid()
    for ax in axs.flat:
        ax.set(xlabel="i")
    axs[3,0].set(ylabel="pixel count")
        

#plt.xlabel("i")
#plt.ylabel("Numero pixel di componenti connesse di taglia[2^i,2^(i+1) )")
plt.show()

