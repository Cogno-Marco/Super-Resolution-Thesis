from typing import List, Tuple
import world as w
import numpy as np
from bucket import Bucket
from photo import Photo
import random
import matplotlib.pyplot as plt
import resolution_utils as utils

CAMERA_SIZE, CAMERA_RESOLUTION, PHOTOS_PER_OFFSET = utils.input_vars()

# load world with image
world: w.World = w.World(CAMERA_SIZE * CAMERA_RESOLUTION)


# Algorithm:

print("taking photos")
photo_list: List[Photo] = []


# for each try for each offset
for x in range(CAMERA_RESOLUTION):
    for _ in range(PHOTOS_PER_OFFSET):
        # Take a picture
        photo_list.append(Photo(world, CAMERA_SIZE, CAMERA_RESOLUTION, x))
    print(f"Groups of photos taken: {x+1}/{CAMERA_RESOLUTION} ", end="\r")

print("\n")
# print(f"taken photos for group {x+1}/{CAMERA_RESOLUTION}")
print(f"photos taken: {len(photo_list)}")
# randomyze photo list
random.shuffle(photo_list)
# when I have enough photos


# now compare each photo between them
# photos can be part of the bucket (so add them to the bucket)
# else they have some offset >= 1
# the photos with the least offset can be added to the left or to the right
#chain: Chain = Chain(mainBucket, CAMERA_RESOLUTION)
chain: List[Photo] = [photo_list.pop(random.randint(0, len(photo_list)-1))]
print(f"starting offset: {chain[0].offset}")
maximum = CAMERA_RESOLUTION * PHOTOS_PER_OFFSET

while len(photo_list) > 0:
    percentage = round(((maximum - len(photo_list))/maximum) * 100,2)
    print(f"Remaining {len(photo_list)} images --- {percentage}%             ", end="\r")

    # find closest image and try to add others
    closest: Photo = photo_list[0] # assume the first one is closest
    indexOfClosest: int = 0
    closestDiffR: int = chain[-1].get_distance(closest) # get distance to last
    closestDiffL: int = chain[0].get_distance(closest) # get distance to first
    for i, photo in enumerate(photo_list):

        bucketDiffR: int = chain[-1].get_distance(photo)
        bucketDiffL: int = chain[0].get_distance(photo)

        # if this photo has a distance to any side closer than the old ones
        if min(bucketDiffR, bucketDiffL) < min(closestDiffR, closestDiffL):
            closest = photo
            indexOfClosest = i
            
            # update closest count
            closestDiffR = bucketDiffR
            closestDiffL = bucketDiffL

    # add the closest photo in the chain
    utils.insert_in_chain(chain, closest)

    # remove from list of images and continue
    photo_list.pop(indexOfClosest)

print("\n")

distances = [chain[i].get_distance(chain[i-1]) for i in range(1, len(chain))]
offsets = [p.offset for p in chain]


# separate images into buckets by finding the r peaks (avoiding last photo though, very likely it's wrong)
clean_photos: List[Photo] = chain[0:-1]
clean_distances = [clean_photos[i].get_distance(
    clean_photos[i-1]) for i in range(1, len(clean_photos))]
peaks: List[Tuple[int, int]] = []
peaks = sorted([(i, dist) for i, dist in enumerate(clean_distances)],
               key=lambda tup: tup[1], reverse=True)[0:CAMERA_RESOLUTION-1]
#peaks_indeces: List[int] = sorted([i for i, _ in peaks])
#TODO: remove this dependency
#abuse the fact that each group has n photos
peaks_indeces: List[int] = [i*PHOTOS_PER_OFFSET for i in range(1,CAMERA_RESOLUTION)]

ranges = [(peaks_indeces[i]+2, peaks_indeces[i+1]+1)
          for i in range(len(peaks_indeces)-1)]
ranges.insert(0, (0, peaks_indeces[0]+1))
ranges.append((peaks_indeces[-1]+1, len(clean_photos)-1))
print(ranges)
buckets: List[Bucket] = []
for start, end in ranges:
    bucket = Bucket(clean_photos[start], CAMERA_RESOLUTION)
    for i in range(start+1, end):
        bucket.add_photo(clean_photos[i])
    buckets.append(bucket)

# now that I have an order, find out how micropixels change to know how to place them
# if number of white micros increases by 1, a black micro exited and a white entered
# if number of micros decreases by 1, a white micro exited and a black entered
# if number of micros is equal, the micro entered is equal to the micro who exited

#in a frequency based approach, look how the float count changes pixel by pixel
#if it's above 0.5 it's a white micro, else it's a black micro
def construct_frequency_world(whites: List[List[float]]) -> List[int]:
    print("whites:")
    for f in whites:
        print(f[0:20])
    
    # calculate differences
    diffs: List[List[float]] = []
    for i in range(len(whites)-1):
        diffs.append([b-a for a,b in zip(whites[i], whites[i+1])])
    
    #calculate partial reconstruction
    reconstruction: List[List[float]] = []
    for diff in diffs:
        partial: List[float] = [0]
        for d in diff:
            partial.append(partial[-1] + d)
        partial.pop(-1)
        reconstruction.append(partial)
    
    # remap from [min,max] to [0,1]
    pieces: List[List[int]] = []
    for photo in reconstruction:
        min_in: float = min(photo)
        max_in: float = max(photo)
        
        #print(f"min: {min_in}, max: {max_in}")
        freq: List[float] = [(pixel-min_in)/(max_in-min_in) for pixel in photo]
        #print(f"freq: {freq[0:20]}")
        
        # N.B. don't use round(), round(0.5) -> 0 but we want 1
        pieces.append([1 if m >=0.5 else 0 for m in freq])
    
    #join reconstructions
    out: List[int] = []
    for macro_count in range(len(pieces[0])):
        for photo_index in range(len(pieces)):
            out.append(pieces[photo_index][macro_count])

    print(f"out: {out[0:20]}")
    
    # convert to world
    return out

def construct_world(whites):
    r = CAMERA_RESOLUTION
    final_photo = [-5 for _ in range((CAMERA_SIZE+2)*r)]
    for i in range(len(whites)-1):
        current_count = whites[i]
        next_count = whites[i+1]
        for ind in range(len(current_count)-1):
            c1, c2 = current_count[ind], next_count[ind]
            if c1 == r:
                for m in range(i+(ind)*r, i+(ind+1)*r):
                    final_photo[m] = 1
                    continue
            elif c1 == 0:
                for m in range(i+(ind)*r, i+(ind+1)*r):
                    final_photo[m] = 0
                    continue

            if c1 < c2:
                final_photo[i+(ind)*r] = 0
                final_photo[i+(ind+1)*r] = 1
            elif c1 > c2:
                final_photo[i+(ind)*r] = 1
                final_photo[i+(ind+1)*r] = 0
            elif c1 == c2:
                if final_photo[i+(ind)*r] > -1:
                    final_photo[i+(ind+1)*r] = final_photo[i+(ind)*r]
                elif final_photo[i+(ind+1)*r] > -1:
                    final_photo[i+(ind)*r] = final_photo[i+(ind+1)*r]
                else:
                    choice = random.randint(0, 1)
                    final_photo[i+(ind)*r] = choice
                    final_photo[i+(ind+1)*r] = choice
    return final_photo

# assume photos are aligned
whites: List[List[float]] = [b.get_whites_count_int() for b in buckets]
# add final count using circular world
fin = whites[0]
inverted = fin[1:]
inverted.append(fin[0])
whites.append(inverted)

final_photo: List[int] = construct_frequency_world(whites)

ground_truth = world.getWorld()

print("photo constructed 0  to 20")
print(final_photo[0:20])
print("original world")
print(ground_truth[0:20])

errors_straight: int = sum([k1 ^ k2 for k1, k2 in zip(final_photo, ground_truth)])
error_straigth = 100 * errors_straight / (CAMERA_RESOLUTION * CAMERA_SIZE)

print(f"error rate straight: {error_straigth:.2f}%")


# assume photos are reversed
whites_rev: List[List[float]] = [b.get_whites_count_int() for b in reversed(buckets)]
# add final count using circular world
fin = whites_rev[0]
inverted = fin[:-1]
inverted.append(fin[-1])
whites_rev.append(inverted)
    
final_photo_rev: List[int] = construct_frequency_world(whites_rev)

ground_truth = world.getWorld()
print("photo REVERSED constructed 0  to 20")
print(final_photo_rev[0:20])
print("original world")
print(ground_truth[0:20])

errors_reversed: int = sum([k1 ^ k2 for k1, k2 in zip(final_photo_rev, ground_truth)])
error_reversed = 100 * errors_reversed / (CAMERA_RESOLUTION * CAMERA_SIZE)

print(f"error rate REVERSED: {error_reversed:.2f}%")


print(f"Accuracy straigth: {100 - error_straigth:.2f}%")
print(f"Accuracy reversed: {100 - error_reversed:.2f}%")

input('Press ENTER to exit')
