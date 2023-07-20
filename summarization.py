from datetime import datetime
import matplotlib.pyplot as plot
import numpy as np
from PIL import Image
import sqlite3 as sql

whole_time = datetime.now()
# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088


# Learning methods:
# 1. Reinforcement Learning (organisms, slow, dangerous!)
# 2. Autonomous Learning (as a machine, fast)
#   2.1. Learning everything just-in-time (consumes much energy)
#   2.2. Learning things randomly
#   2.3. Learning specific kinds of things (stupid!)
# In either way except 2.1, there can be a stress factor which boosts learning as well as draining energy.

# Database:
# Shape: 1. (colour/gradient/pattern), 2. [shape](BREAK THIS)
# Vector: 1. array of shapes and probabilistic positions
# Object (from all senses, PROBABILISTICALLY)

# Colour is more important than shape.
# We can also instead, collect raster images in the storage and create Shapes summaries of them, which is a bad idea!
# we could also store a simplified version of those images!
# Forgetting can be accomplished by setting a last modified timestamp on each shape/vector/object.

def is_hue_close(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 20


status = np.repeat([np.repeat(False, dim)], dim, 0)
sureY, sureX = 0, 0
while sureY < dim:
    print(sureY, sureX)
    thisY, thisX = 0, 0
    for y in range(sureY, dim):
        break_it = False
        for x in range(sureX, dim):
            if not status[y, x]:
                thisY = y
                thisX = x
                break_it = True
                break
            else:
                sureY = y
                sureX = x
        if break_it: break

    is_close: bool
    for yy in range(thisY, dim):
        for xx in range(thisX, dim):
            status[yy, xx] = True
            if yy == thisY and xx == thisX:
                continue

            if xx == thisX:
                is_close = is_hue_close(arr[yy - 1, xx], arr[yy, xx])
            else:
                is_close = is_hue_close(arr[yy, xx - 1], arr[yy, xx])

            if not is_close:
                arr[yy, xx] = np.array([0, 255, 255])
                break

    sureX += 1
    if sureX == dim:
        sureX = 0
        sureY += 1

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print(datetime.now() - whole_time)  # mere File->Image->RGB->HSV->RGB->Image->ImShow: 0:00:00.430~~480
plot.show()
