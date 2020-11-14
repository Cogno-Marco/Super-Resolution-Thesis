from typing import List, Tuple
import world as w
import numpy as np
from bucket import Bucket
from photo import Photo
import random
import matplotlib.pyplot as plt

#CAMERA_SIZE: int = 50000
#CAMERA_RESOLUTION: int = 8

CAMERA_SIZE: int = 100000
CAMERA_RESOLUTION: int = 8

# load world with image
world: w.World = w.World(CAMERA_SIZE * CAMERA_RESOLUTION)
PHOTOS_PER_OFFSET: int = 16


# Algorithm:

photo_list: List[Photo] = []

print("taking photos")

# for each try for each offset
for x in range(CAMERA_RESOLUTION):
    for _ in range(PHOTOS_PER_OFFSET):
        # Take a picture
        photo: Photo = Photo(world, CAMERA_SIZE, CAMERA_RESOLUTION, x)
        photo_list.append(photo)
    print(f"taken photos for group {x+1}/{CAMERA_RESOLUTION}")

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
while len(photo_list) > 0:
    if len(photo_list) % 10 == 0:
        print(f"remaining {len(photo_list)} images")
    hasJoinedImage: bool = False

    # find closest image and try to add others
    closest: Photo = photo_list[0]
    indexOfClosest: int = 0
    closestDiffR: int = chain[-1].get_distance(closest)
    closestDiffL: int = chain[0].get_distance(closest)
    for i in range(1, len(photo_list)):
        photo = photo_list[i]
        if chain[-1].is_photo_aligned(photo) or chain[0].is_photo_aligned(photo):
            print("found an aligned photo")
            if chain[0].get_distance(photo) <= chain[-1].get_distance(photo):
                chain.insert(0, photo)
            else:
                chain.insert(-1, photo)
            photo_list.pop(i)
            hasJoinedImage = True
            break

        bucketDiffR: int = chain[-1].get_distance(photo)
        bucketDiffL: int = chain[0].get_distance(photo)

        if min(bucketDiffR, bucketDiffL) < min(closestDiffR, closestDiffL):
            #print(f"new distances: left {bucketDiffL}, right {bucketDiffR}")
            closest = photo
            indexOfClosest = i
            #update closest count
            closestDiffR = chain[-1].get_distance(closest)
            closestDiffL = chain[0].get_distance(closest)

    # skip photo if it was added to a bucket
    if hasJoinedImage:
        continue

    # here I have the closest photo, a simple diff tells me if it's closest left or right
    # add it as a new chain to that side
    if chain[0].get_distance(closest) < chain[-1].get_distance(closest):
        chain.insert(0, closest)
    else:
        chain.insert(-1, closest)
    # remove from list of images and continue
    photo_list.pop(indexOfClosest)

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
#abuse the fact that each group has 16 photos
peaks_indeces: List[int] = [i*16 for i in range(1,CAMERA_RESOLUTION)]

print(f"peaks: {peaks}")
print(f"peaks: {peaks_indeces}")

print(f"distance from first to last: {chain[0].get_distance(chain[-1])}")
print(f"distance from first to second: {chain[0].get_distance(chain[1])}")
print("first photo:")
print(chain[0].photo[0:20])
print("second photo:")
print(chain[1].photo[0:20])
print("last photo:")
print(chain[-1].photo[0:20])
plt.bar(list(range(1, len(chain))), distances)
plt.show()
plt.bar(list(range(len(chain))), offsets)
plt.show()


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
def contruct_frequency_world(whites: List[List[float]]) -> List[int]:
    # calculate frequencies
    out: List[float] = []
    for macro_count in range(len(whites[0])):
        for photo_index in range(len(whites)):
            out.append(whites[photo_index][macro_count])
            #out.append(whites[(photo_index+1) % len(whites)][macro_count] - whites[photo_index][macro_count])
            #out.append(whites[photo_index][(macro_count+1) % len(whites[0])] - whites[photo_index][macro_count])

    print(f"out: {out[0:20]}")
    # remap from [min,max] to [0,1]
    min_in: float = min(out)
    max_in: float = max(out)
    freq: List[float] = [(f-min_in)/(max_in-min_in) for f in out]
    print(f"freq: {freq[0:20]}")

    # convert to world
    # N.B. don't use round(), round(0.5) -> 0 but we want 1
    return [1 if m >=0.5 else 0 for m in freq]


# assume photos are aligned
whites: List[List[float]] = [b.get_whites_count() for b in buckets]
final_photo: List[int] = contruct_frequency_world(whites)

print("photo constructed 0  to 20")
print(final_photo[0:20])
print("original world")
print(world.getWorld()[0:20])

errors_straight = 0
for i in range(min(len(final_photo), len(world.getWorld()))):
    c1, c2 = final_photo[i], world.getWorld()[i]
    if c1 != c2:
        errors_straight += 1

print(f"error rate straight: {100*errors_straight/(CAMERA_RESOLUTION*CAMERA_SIZE):.2f}%")


# assume photos are reversed
whites_rev: List[List[float]] = [b.get_whites_count() for b in reversed(buckets)]
final_photo_rev: List[int] = contruct_frequency_world(whites_rev)

print("photo REVERSED constructed 0  to 20")
print(final_photo_rev[0:20])
print("original world")
print(world.getWorld()[0:20])

errors_reversed = 0
for i in range(min(len(final_photo_rev), len(world.getWorld()))):
    c1, c2 = final_photo_rev[i], world.getWorld()[i]
    if c1 != c2:
        errors_reversed += 1

print(f"error rate REVERSED: {100*errors_reversed/(CAMERA_RESOLUTION*CAMERA_SIZE):.2f}%")
