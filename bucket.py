import numpy as np
from typing import List
from photo import Photo


def mu(f, r):
    # if f > CAMERA_RESOLUTION: return mu(CAMERA_RESOLUTION)
    return 0.5 + 1/(2 * r) - f/(2 * r**2)

def epsilon(r):
    return 1/(2 * r**2 + 2 * r - 1)

class Bucket:

    def __init__(self, principal_voice: Photo, r: int):
        self.r: int = r
        self.k: int = len(principal_voice.photo)
        self.principal: Photo = principal_voice
        self.photos: List[Photo] = []
        self.photos.append(principal_voice)

    def is_photo_aligned(self, photo: Photo) -> bool:
        currentGuesses = 0
        for macro_guessed, macro_actual in zip(self.principal.photo, photo.photo):
            if macro_guessed == macro_actual:
                currentGuesses += 1

        return currentGuesses >= (1 + epsilon(self.r)) * mu(0, self.r) * self.k

    def add_photo(self, photo: Photo):
        self.photos.append(photo)

    def get_photos(self) -> List[Photo]:
        return self.photos

    def get_bucket_size(self) -> int:
        return len(self.photos)

    def get_whites_count(self) -> List[float]:
        whites = [0 for _ in range(self.k)]
        for photo in self.photos:
            for ind, macro in enumerate(photo.photo):
                whites[ind] += macro
        return [count*self.r/len(self.photos) for count in whites]
    
    def get_whites_count_int(self) -> List[int]:
        whites = [0 for _ in range(self.k)]
        for photo in self.photos:
            for ind, macro in enumerate(photo.photo):
                whites[ind] += macro
        return [int(round(count*self.r/len(self.photos))) for count in whites]

    # def get_bucket_diff(self, bucket: 'Bucket') -> List[List[int]]:
    #     diff = [[0 for _ in range(self.k)] for _ in range(self.k)]
    #     my_count = self.get_whites_count()
    #     his_count = bucket.get_whites_count()
    #     for ind in range(self.k):
    #         diff[ind] = [my_c - his_c for my_c,
    #                      his_c in zip(my_count[ind], his_count[ind])]
    #     return diff

    # def get_photo_diff(self, photo: Photo) -> List[List[int]]:
    #     return [[main_k - k for main_k, k in zip(main_line, line)] for main_line, line in zip(self.principal, photo)]

    # def is_equal(self, bucket: 'Bucket') -> bool:
    #     # if the difference of each macro is 0, the zones are the same
    #     for line in self.get_bucket_diff(bucket):
    #         for count in line:
    #             if count != 0:
    #                 return False
    #     return True

    # def is_bucket_aligned(self, bucket: 'Bucket') -> bool:
    #     diff = self.get_bucket_diff(bucket)
    #     diff_sum = np.array(diff).sum()
    #     return abs(diff_sum) <= self.r / 8

    #     # if the difference is not in the range [-1,1] the buckets are NOT aligned
    #     diff = self.get_diff(bucket)
    #     for line in diff:
    #         for count in line:
    #             if count > 1 or count < -1:
    #                 return False

    #     # they're also not aligned if, watching pixel by pixel, as one increases, the other increases too
    #     # or if one decreases the other decreases too
    #     # basically to be valid, +1 and -1 must alternate (ignoring 0s)

    #     for line in diff:
    #         parity = None
    #         for count in line:
    #             if count == 0:
    #                 continue  # ignore 0s
    #             if parity == None:
    #                 parity = count  # set starting parity as equal
    #                 continue
    #             if parity == count:
    #                 # if parity of the last change is the same as this, then it doesn't alternate, so this is not valid
    #                 return False
    #             else:
    #                 parity = count

    #     return True
