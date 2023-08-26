from datetime import datetime
from functools import cmp_to_key

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

whole_time = datetime.now()
# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088
MIN_S = 5
SELECTED_ROW = 500


# Perhaps colour is much more important than shape!
# And size matters too.
# Simply find small clusters in exclude them by giving their pixels to their nearest neighbours.
# Keep a cluster's highest and lowest colour values.
# Shape also can be defined using lines and their strokes, so a box would be a dot with a huge stroke.
# There's no need for a 3D simulation, you can store multiple shapes and colours for a single object as its aspects.
# We should detect shapes sooner than we had planned.
# What humans SEE is different from what they STORE in their brains.

# Let's start from a very simple kind of clustering.


class Pixel:
    def __init__(self, _c: np.ndarray, _y: int, _x: int):
        self.c: list[int] = _c.tolist()  # if it is ndarray, sorting won't work!
        self.y: int = _y
        self.x: int = _x


pixels: list[Pixel] = list()
for y in range(len(arr)):  # SELECTED_ROW, SELECTED_ROW + 1
    for x in range(len(arr[y])):
        pixels.append(Pixel(arr[y, x], y, x))


def sort_by_brightness(a: Pixel, b: Pixel) -> int:
    dif = a.c[2] - b.c[2]
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


def sort_by_hue(a: Pixel, b: Pixel) -> int:
    dif = a.c[0] - b.c[0]
    if a.c[1] < MIN_S:
        return 0
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


def sort_by_saturation(a: Pixel, b: Pixel) -> int:
    aa = a.c[1] < MIN_S
    bb = b.c[1] < MIN_S
    if not aa and bb:
        return -1
    elif aa and not bb:
        return 1
    else:
        return 0


pixels.sort(key=cmp_to_key(sort_by_brightness))
pixels.sort(key=cmp_to_key(sort_by_hue))
pixels.sort(key=cmp_to_key(sort_by_saturation))

# Divide into 16 clusters
pixels

# for y in range(len(arr)):
#    for x in range(len(arr[y])):
#        arr[y, x] = pixels[x].c  # arr[SELECTED_ROW, x]

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)
plot.show()
