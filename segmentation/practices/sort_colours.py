from functools import cmp_to_key

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# print(list(Image.fromarray(np.array([[[255, 255, 255], [0, 0, 0]]], dtype=np.uint8), 'RGB')
#           .convert('HSV').getdata()))
# quit()  # [(0, 0, 255), (0, 0, 0)]
# Make sure this happens in C++ too!
MIN_S = 5


def sort_by_brightness(a: list[int], b: list[int]) -> int:
    dif = a[2] - b[2]
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


def sort_by_hue(a: list[int], b: list[int]) -> int:
    dif = a[0] - b[0]
    if a[1] < MIN_S:
        return 0
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


# Those with S:0 will be placed at the end of the array
def sort_by_saturation(a: list[int], b: list[int]) -> int:
    aa = a[1] < MIN_S  # a[1] == 0
    bb = b[1] < MIN_S  # b[1] == 0
    if not aa and bb:
        return -1
    elif aa and not bb:
        return 1
    else:  # aa and bb
        return 0


colours: list[list[int]] = [
    [150, 255, 150],
    [200, 255, 200],
    [50, 255, 50],
    [250, 255, 250],
    [100, 255, 100],

    [255, 255, 25],
    [225, 255, 50],
    [200, 255, 50],
    [175, 255, 100],
    [150, 255, 100],
    [125, 255, 150],
    [100, 255, 150],
    [75, 255, 200],
    [50, 255, 200],
    [25, 255, 250],
    [0, 255, 250],

    [250, 3, 0],
    [200, 3, 50],
    [150, 3, 100],
    [100, 3, 150],
    [50, 3, 200],
    [0, 3, 250],
]
colours.sort(key=cmp_to_key(sort_by_brightness))
colours.sort(key=cmp_to_key(sort_by_hue))
colours.sort(key=cmp_to_key(sort_by_saturation))

bw_colours: list[list[int]] = list()
bw_min = len(colours)
for i in range(0, bw_min, -1):
    print(i)  # TO-DO
    if colours[i][1] < MIN_S:
        bw_min -= 1
bw_colours = colours[bw_min:]
colour = colours[:bw_min]
# now you have to separate the coloured pixels from the black/white one.
# the former represents a circle, the latter is just a gradient line.

# TO-DO it must be a circular clustering not linear, so H:0 and H:255 must be in a single cluster.
# But when S is low, high V means white and low V means black!!
# Think of Hue as a circle of 360 degrees and then multiply it. But deal with the other 2 values as linear.
# If there are only varieties of green colours, the boundaries of the cluster must not get out
# of the boundaries of the green colour.

plot.imshow(Image.fromarray(np.array([colours], dtype=np.uint8), 'HSV').convert('RGB'))
plot.show()
