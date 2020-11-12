from skimage import io
from skimage.color import rgb2gray

loaded = io.imread(f"USAF_4000px.png")
grayscale = rgb2gray(loaded)
print(grayscale)

total = sum(sum(grayscale))
print(1 - total / (4000 * 4000))