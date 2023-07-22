import sys
from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# import sqlite3 as sql  # for now practice here, don't add SQLite in C++, we may dislike SQLite later.
whole_time = datetime.now()
# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088
sys.setrecursionlimit(dim * dim)

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

status = np.repeat([np.repeat(-1, dim)], dim, 0)
# TODO instead of True and False, indicate where did you put these pixels


def is_hue_close(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 5 \
        and abs(int(a[2]) - int(b[2])) <= 5
    # and abs(int(a[1]) - int(b[1])) <= 100 \


def neighbours_of(yy: int, xx: int, pixels: List[Tuple[int, int]]):
    pixels.append((yy, xx))
    status[yy, xx] = len(pixels) - 1
    if xx > 0 and status[yy, xx - 1] != -1 and is_hue_close(arr[yy, xx], arr[yy, xx - 1]):  # left
        neighbours_of(yy, xx - 1, pixels)
    if yy > 0 and status[yy - 1, xx] != -1 and is_hue_close(arr[yy, xx], arr[yy - 1, xx]):  # top
        neighbours_of(yy - 1, xx, pixels)
    if xx < (dim - 1) and status[yy, xx + 1] != -1 and is_hue_close(arr[yy, xx], arr[yy, xx + 1]):  # right
        neighbours_of(yy, xx + 1, pixels)
    if yy < (dim - 1) and status[yy + 1, xx] != -1 and is_hue_close(arr[yy, xx], arr[yy + 1, xx]):  # bottom
        neighbours_of(yy + 1, xx, pixels)


segmentation_time = datetime.now()
segments: List[List[Tuple[int, int]]] = list()
thisY, thisX, found_sth_to_analyse = 0, 0, True
while found_sth_to_analyse:
    found_sth_to_analyse = False
    for y in range(thisY, dim):
        for x in range(thisX if y == thisY else 0, dim):
            if status[y, x] != -1:
                found_sth_to_analyse = True
                thisY = y
                thisX = x
                break
        if found_sth_to_analyse: break
    if not found_sth_to_analyse: break
    # print(thisY, thisX)

    segment = list()
    neighbours_of(thisY, thisX, segment)
    segments.append(segment)

print('Segmentation time:', datetime.now() - segmentation_time)

# FIXME neighbours_of does a lot of repeated work!! Although it might be useful!
# TODO RESOLVE SMALL SEGMENTS (now 88575)

for seg in range(len(segments)):
    if len(segments[seg]) < 100:
        for px in segments[seg]:
            arr[px[0], px[1]] = 0, 255, 255
        continue
    print(seg, ':', len(segments[seg]))

for px in segments[0]:
    arr[px[0], px[1]] = 40, 255, 255
for px in segments[1380]:
    arr[px[0], px[1]] = 80, 255, 255
for px in segments[15902]:
    arr[px[0], px[1]] = 120, 255, 255
for px in segments[37872]:
    arr[px[0], px[1]] = 160, 255, 255
for px in segments[40822]:
    arr[px[0], px[1]] = 200, 255, 255
for px in segments[54364]:
    arr[px[0], px[1]] = 240, 255, 255

print('Total segments:', len(segments))

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)  # mere File->Image->RGB->HSV->RGB->Image->ImShow: 0:00:00.430~~480
plot.show()
