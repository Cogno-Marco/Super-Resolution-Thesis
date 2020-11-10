from typing import List
from bucket import Bucket
from world_2d import Photo
import numpy as np

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

    def extend_left(self, bucket: Bucket):
        self.chain.insert(0, bucket)

    def extend_right(self, bucket: Bucket):
        self.chain.insert(-1, bucket)

    def get_right_difference(self, photo: Photo) -> int:
        return abs(np.array(self.chain[-1].get_photo_diff(photo)).sum())

    def get_left_difference(self, photo: Photo) -> int:
        return abs(np.array(self.chain[0].get_photo_diff(photo)).sum())