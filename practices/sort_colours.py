from functools import cmp_to_key

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image


def sort_by_colour(a: list[int], b: list[int]) -> int:
    dif = a[0] - b[0]
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0
    # TODO take low saturation into account


def sort_by_brightness(a: list[int], b: list[int]) -> int:
    dif = a[3] - b[3]
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


colours: list[list[int]] = [
    [150, 255, 150],
    [0, 255, 0],
    [200, 255, 200],
    [50, 255, 50],
    [250, 255, 250],
    [100, 255, 100],

    [250, 255, 0],
    [200, 255, 50],
    [150, 255, 100],
    [100, 255, 150],
    [50, 255, 200],
    [0, 255, 250],

    [250, 3, 0],
    [200, 3, 50],
    [150, 3, 100],
    [100, 3, 150],
    [50, 3, 200],
    [0, 3, 250],
]
colours.sort(key=cmp_to_key(sort_by_brightness))
colours.sort(key=cmp_to_key(sort_by_colour))
# TODO it must be a circular clustering not linear, so H:0 and H:255 must be in a single cluster.
# But when S is low, high V means white and low V means black!!
# Think of Hue as a circle of 360 degrees and then multiply it. But deal with the other 2 values as linear.
# If there are only varieties of green colours, the boundaries of the cluster must not get out
# of the boundaries of the green colour.

plot.imshow(Image.fromarray(np.array([colours], dtype=np.uint8), 'HSV').convert('RGB'))
plot.show()
