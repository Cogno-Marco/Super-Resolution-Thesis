from typing import List
import world_2d as w
import numpy as np
from bucket import Bucket

Photo = List[List[int]]  # define photo type

CAMERA_SIZE = 7
CAMERA_RESOLUTION = 64

# load world with image
world_2d = w.World2D(512)
PHOTOS_PER_OFFSET = 32


def mu(f, r):
    # if f > CAMERA_RESOLUTION: return mu(CAMERA_RESOLUTION)
    return 0.5 + 1/(2 * r) - f/(2 * r**2)


def epsilon(r):
    return 1/(2 * r**2 + 2 * r - 1)


class Chain:

    def __init__(self, startingBucket: Bucket, r):
        self.chain: List[Bucket] = [startingBucket]
        self.r = r

    def try_add_photo(self, photo: Photo):
        # try to add a photo to the first element, return true if possible
        if(self.chain[0].is_photo_aligned(photo)):
            self.chain[0].add_photo(photo)
            return True

        # try to add a photo to the last element, return true if possible
        if(self.chain[-1].is_photo_aligned(photo)):
            self.chain[-1].add_photo(photo)
            return True

        # couldn't add any photo, return False
        return False

    def extend_left(self, photo: Photo):
        self.chain.insert(0, Bucket(photo, self.r))

    def extend_right(self, photo: Photo):
        self.chain.insert(-1, Bucket(photo, self.r))

    def get_right_difference(self, photo: Photo) -> int:
        return abs(np.array(self.chain[-1].get_photo_diff(photo)).sum())

    def get_left_difference(self, photo: Photo) -> int:
        return abs(np.array(self.chain[0].get_photo_diff(photo)).sum())

# Algorithm:


buckets_list: List[Bucket] = []

print("adding photos to buckets")

# for each try for each offset
for x in range(CAMERA_RESOLUTION+1):
    for _ in range(PHOTOS_PER_OFFSET):
        # Take a picture
        photo = world_2d.photo((x, 0), CAMERA_SIZE, CAMERA_RESOLUTION)

        # for each bucket look if image can be generated by the bucket
        was_added = False
        for i, bucket in enumerate(buckets_list):
            if bucket.is_photo_aligned(photo):
                # if it can add photo to bucket
                bucket.add_photo(photo)
                was_added = True
                break

        # else create new bucket with the photo
        if not was_added:
            buckets_list.append(Bucket(photo, CAMERA_RESOLUTION))

print(f"photos added to buckets, total buckets={len(buckets_list)}")
# when I have enough photos

# get bucket with more images
mainBucket = buckets_list[0]
remainingImages = []
for i in range(1, len(buckets_list)):
    bucket = buckets_list[i]
    if bucket.get_bucket_size() > mainBucket.get_bucket_size():
        # bucket is big enough, add old ones photos into remaining images
        remainingImages.extend(mainBucket.get_photos())
        mainBucket = bucket
    else:
        # bucket was not big enough, move images into remaining
        remainingImages.extend(bucket.get_photos())


# now compare each photo with bucket
# photos can be part of the bucket (so add them to the bucket)
# else they have some offset >= 1
# the photos with the least offset can be added to the left or to the right
#


# now that I have an order, find out how micropixels change to know how to place them
# if number of white micros increases by 1, a black micro exited and a white entered
# if number of micros decreases by 1, a white micro exited and a black entered
# if number of micros is equal, the micro entered is equal to the micro who exited
# also
# if number of white micros is 0, the whole piece is black
# if number of white micros is r, the whole piece is white
