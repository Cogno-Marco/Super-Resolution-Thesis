from typing import List, Tuple
import world as w
import numpy as np
from bucket import Bucket
from photo import Photo
import random
import matplotlib.pyplot as plt

#CAMERA_SIZE: int = 50000
#CAMERA_RESOLUTION: int = 8

CAMERA_SIZE: int = 10000
CAMERA_RESOLUTION:int = 4

# load world with image
world: w.World = w.World(500000)
PHOTOS_PER_OFFSET: int = 16



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




# separate images into buckets by finding the r peaks (avoiding first and last photo though)
clean_photos: List[Photo] = chain[0:-1]
clean_distances = [clean_photos[i].get_distance(clean_photos[i-1]) for i in range(1, len(clean_photos))]
peaks: List[Tuple[int,int]] = []
peaks = sorted([(i,dist) for i,dist in enumerate(clean_distances)], key=lambda tup: tup[1], reverse = True)[0:CAMERA_RESOLUTION]
peaks_indeces = sorted([i for i,_ in peaks])

print(f"peaks: {peaks}")
print(f"peaks: {peaks_indeces}")

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


ranges = [(peaks_indeces[i]+2, peaks_indeces[i+1]+1) for i in range(len(peaks_indeces)-1)]
ranges.insert(0, (0,peaks_indeces[0]+1))
ranges.append((peaks_indeces[-1]+1, len(clean_photos)-1))
print(ranges)
buckets: List[Bucket] = []
for start,end in ranges:
    bucket = Bucket(clean_photos[start], CAMERA_RESOLUTION)
    for i in range(start+1, end):
        bucket.add_photo(clean_photos[i])
    buckets.append(bucket)

# now that I have an order, find out how micropixels change to know how to place them
# if number of white micros increases by 1, a black micro exited and a white entered
# if number of micros decreases by 1, a white micro exited and a black entered
# if number of micros is equal, the micro entered is equal to the micro who exited
# also
# if number of white micros is 0, the whole piece is black
# if number of white micros is r, the whole piece is white
def construct_world(whites):
    r = CAMERA_RESOLUTION
    final_photo = [-5 for _ in range((CAMERA_SIZE+2)*r)]
    for i in range(len(whites)-1):
        current_count = whites[i]
        next_count = whites[i+1]
        for ind in range(len(current_count)-1):
            c1,c2 = current_count[ind], next_count[ind]
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
                    choice = random.randint(0,1)
                    final_photo[i+(ind)*r] = choice
                    final_photo[i+(ind+1)*r] = choice
    return final_photo

#assume photos are aligned
whites = [b.get_whites_count() for b in buckets]

for white in whites:
    print(white[0:20])
final_photo = construct_world(whites)

print("photo constructed 0  to 20")
print(final_photo[0:20])
print("original world")
print(world.getWorld()[0:20])
    
errors_straight = 0
for i in range(min(len(final_photo), len(world.getWorld()))):
    c1,c2 = final_photo[i], world.getWorld()[i]
    if c1 != c2:
        errors_straight+=1

print(f"error rate straight: {100*errors_straight/(CAMERA_RESOLUTION*CAMERA_SIZE):.2f}%")
 
 
# assume photos are reversed   
whites = [b.get_whites_count() for b in reversed(buckets)]

for white in whites:
    print(white[0:20])
final_photo = construct_world(whites)

print("photo REVERSED constructed 0  to 20")
print(final_photo[0:20])
print("original world")
print(world.getWorld()[0:20])
    
errors_reversed = 0
for i in range(min(len(final_photo), len(world.getWorld()))):
    c1,c2 = final_photo[i], world.getWorld()[i]
    if c1 != c2:
        errors_reversed+=1

print(f"error rate REVERSED: {100*errors_reversed/(CAMERA_RESOLUTION*CAMERA_SIZE):.2f}%")


