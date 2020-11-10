from typing import List
import world as w
import numpy as np
#from bucket import Bucket
from photo import Photo

CAMERA_SIZE: int = 7
CAMERA_RESOLUTION: int = 64

# load world with image
world: w.World = w.World(512)
PHOTOS_PER_OFFSET: int = 8


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
# when I have enough photos

# get bucket with more images
mainBucket: Bucket = buckets_list[0]
remainingBuckets: List[Bucket] = []
for i in range(1, len(buckets_list)):
    bucket = buckets_list[i]
    if bucket.get_bucket_size() > mainBucket.get_bucket_size():
        # bucket is big enough, add old one into remaining
        remainingBuckets.append(mainBucket)
        mainBucket = bucket
    else:
        # bucket was not big enough, move images into remaining
        remainingBuckets.append(bucket)

# now compare each photo with bucket
# photos can be part of the bucket (so add them to the bucket)
# else they have some offset >= 1
# the photos with the least offset can be added to the left or to the right
chain: Chain = Chain(mainBucket, CAMERA_RESOLUTION)

while len(remainingBuckets) > 0:
    hasJoinedImage: bool = False

    # find closest image and try to add others
    closest : Bucket = remainingBuckets[0]
    indexOfClosest: int = 0
    for i, bucket in enumerate(remainingBuckets):
        # if chain.try_add_photo(bucket.principal):
        #     remainingBuckets.pop(i)
        #     hasJoinedImage = True
        #     print(f"photo was part of bucket, {len(remainingImages)} remaining")
        #     break
        
        closestDiffR: int = chain.get_right_difference(closest.principal)
        closestDiffL: int = chain.get_left_difference(closest.principal)
        bucketDiffR: int = chain.get_right_difference(bucket.principal)
        bucketDiffL: int = chain.get_left_difference(bucket.principal)
        
        if bucketDiffR < closestDiffR or bucketDiffL < closestDiffL:
            closest = bucket
            indexOfClosest = i

    # skip photo if it was added to a bucket
    if hasJoinedImage:
        continue
    
    #here I have the closest photo, a simple diff tells me if it's closest left or right
    #add it as a new chain to that side
    if chain.get_left_difference(closest.principal) < chain.get_right_difference(closest.principal):
        chain.extend_left(closest)
    else:
        chain.extend_right(closest)
    #remove from list of images and continue
    remainingBuckets.pop(indexOfClosest)
    print(f"removed a bucket, {len(remainingBuckets)} remaining")

# now that I have an order, find out how micropixels change to know how to place them
# if number of white micros increases by 1, a black micro exited and a white entered
# if number of micros decreases by 1, a white micro exited and a black entered
# if number of micros is equal, the micro entered is equal to the micro who exited
# also
# if number of white micros is 0, the whole piece is black
# if number of white micros is r, the whole piece is white
