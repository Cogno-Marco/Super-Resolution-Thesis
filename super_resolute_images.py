from typing import List
import world as w
import numpy as np
#from bucket import Bucket
from photo import Photo
import random
import matplotlib.pyplot as plt

CAMERA_SIZE: int = 50000
CAMERA_RESOLUTION: int = 8

# load world with image
world: w.World = w.World(500000)
PHOTOS_PER_OFFSET: int = 16


def mu(f, r):
    # if f > CAMERA_RESOLUTION: return mu(CAMERA_RESOLUTION)
    return 0.5 + 1/(2 * r) - f/(2 * r**2)


def epsilon(r):
    return 1/(2 * r**2 + 2 * r - 1)


# Algorithm:

photo_list: List[Photo] = []

print("adding photos to buckets")

# for each try for each offset
for x in range(CAMERA_RESOLUTION+1):
    for _ in range(PHOTOS_PER_OFFSET):
        # Take a picture
        photo: Photo = Photo(world, CAMERA_SIZE, CAMERA_RESOLUTION, x)
        photo_list.append(photo)

print(f"photos added to buckets, total buckets={len(photo_list)}")
#randomyze photo list
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
    closest : Photo = photo_list[0]
    indexOfClosest: int = 0
    for i in range(1,len(photo_list)):
        photo = photo_list[i]
        # if chain.try_add_photo(bucket.principal):
        #     remainingBuckets.pop(i)
        #     hasJoinedImage = True
        #     print(f"photo was part of bucket, {len(remainingImages)} remaining")
        #     break
        if chain[-1].is_photo_aligned(photo) or chain[0].is_photo_aligned(photo):
            print("found an aligned photo")
            if chain[0].get_distance(photo) <= chain[-1].get_distance(photo):
                chain.insert(0, photo)
            else:
                chain.insert(-1, photo)
            photo_list.pop(i)
            hasJoinedImage = True
            break
        # if chain[0].is_photo_aligned(photo):
            # chain.insert(0, photo)
            # photo_list.pop(i)
            # hasJoinedImage = True
            # break
        
        
        closestDiffR: int = chain[-1].get_distance(closest)
        closestDiffL: int = chain[0].get_distance(closest)
        bucketDiffR: int = chain[-1].get_distance(photo)
        bucketDiffL: int = chain[0].get_distance(photo)
        
        if min(bucketDiffR, bucketDiffL) < min(closestDiffR, closestDiffL):
            #print(f"new distances: left {bucketDiffL}, right {bucketDiffR}")
            closest = photo
            indexOfClosest = i

    # skip photo if it was added to a bucket
    if hasJoinedImage:
        continue
    
    #here I have the closest photo, a simple diff tells me if it's closest left or right
    #add it as a new chain to that side
    if chain[0].get_distance(closest) < chain[-1].get_distance(closest):
        #print("added left")
        chain.insert(0, closest)
    else:
        #print("added right")
        chain.insert(-1, closest)
    #remove from list of images and continue
    photo_list.pop(indexOfClosest)
    #print(f"removed a bucket, {len(photo_list)} remaining")

distances = [chain[i].get_distance(chain[i-1]) for i in range(1, len(chain))]
offsets = [p.offset for p in chain]

for i in range(1,len(chain)):
    p: Photo = chain[i]
    #print(f"offset 1: {chain[i-1].offset}, offset 2: {p.offset}")
    #print(f"photo {i} distance to {i-1}: {p.get_distance(chain[i-1])}")

print(f"distance from first to last: {chain[0].get_distance(chain[-1])}")
print(f"distance from first to second: {chain[0].get_distance(chain[1])}")
print("first photo:")
print(chain[0].photo)
print("second photo:")
print(chain[1].photo)
print("last photo:")
print(chain[-1].photo)
plt.bar(list(range(1, len(chain))), distances)
plt.show()
plt.bar(list(range(len(chain))), offsets)
plt.show()
# now that I have an order, find out how micropixels change to know how to place them
# if number of white micros increases by 1, a black micro exited and a white entered
# if number of micros decreases by 1, a white micro exited and a black entered
# if number of micros is equal, the micro entered is equal to the micro who exited
# also
# if number of white micros is 0, the whole piece is black
# if number of white micros is r, the whole piece is white
