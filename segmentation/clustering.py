from datetime import datetime

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

whole_time = datetime.now()
# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088


# Perhaps colour is much more important than shape!
# And size matters too.
# Simply find small clusters in exclude them by giving their pixels to their nearest neighbours.
# Keep a cluster's highest and lowest colour values.
# Shape also can be defined using lines and their strokes, so a box would be a dot with a huge stroke.
# There's no need for a 3D simulation, you can store multiple shapes and colours for a single object as its aspects.
# We should detect shapes sooner than we had planned.
# What humans SEE is different from what they STORE in their brains.


class Pixel:
    def __init__(self, _c: np.ndarray, _y: int, _x: int):
        self.c = _c
        self.y = _y
        self.x = _x


pixels: list[Pixel] = list()
for y in range(len(arr)):
    for x in range(len(arr[y])):
        pixels.append(Pixel(arr[y, x], y, x))


def cluster(a: Pixel, b: Pixel) -> int:
    pass


pixels.sort(key=cluster)
# pixels.sort(key=)  # we can also execute multiple sorting methods

# print(pixels)
# TODO show pixels in one dimension of mere colours

# plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
# print('Whole time:', datetime.now() - whole_time)
# plot.show()
