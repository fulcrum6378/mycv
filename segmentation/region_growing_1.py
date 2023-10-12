import os
import sys
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

from config import bitmap, bitmap_folder, dim

# import sqlite3 as sql  # for now practice here, don't add SQLite in C++, we may dislike SQLite later.
whole_time = datetime.now()
# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open(os.path.join('vis', 'output', bitmap_folder, bitmap + '.bmp'))
                             .convert('HSV')).copy()
arr.setflags(write=True)
min_seg = 1000  # this must change by the degree of stress!
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

status: np.ndarray = np.repeat([np.repeat(-1, dim)], dim, 0)  # verified to have no -1 at the end.
segments: list[list[tuple[int, int]]] = list()


def is_hue_close(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 5 \
        and abs(int(a[2]) - int(b[2])) <= 5
    # and abs(int(a[1]) - int(b[1])) <= 100 \


def neighbours_of(yy: int, xx: int, pixels: list[tuple[int, int]], sgm_idx: int):
    pixels.append((yy, xx))
    status[yy, xx] = sgm_idx
    if xx > 0 and status[yy, xx - 1] == -1 and is_hue_close(arr[yy, xx], arr[yy, xx - 1]):  # left
        neighbours_of(yy, xx - 1, pixels, sgm_idx)
    if yy > 0 and status[yy - 1, xx] == -1 and is_hue_close(arr[yy, xx], arr[yy - 1, xx]):  # top
        neighbours_of(yy - 1, xx, pixels, sgm_idx)
    if xx < (dim - 1) and status[yy, xx + 1] == -1 and is_hue_close(arr[yy, xx], arr[yy, xx + 1]):  # right
        neighbours_of(yy, xx + 1, pixels, sgm_idx)
    if yy < (dim - 1) and status[yy + 1, xx] == -1 and is_hue_close(arr[yy, xx], arr[yy + 1, xx]):  # bottom
        neighbours_of(yy + 1, xx, pixels, sgm_idx)


# It must become more developed. You can also calculate segments' mean values!
def find_a_segment_to_dissolve_in(sgm_pixels: list[tuple[int, int]]) -> Optional[tuple[int, int]]:
    if sgm_pixels[0][0] > 0:
        return sgm_pixels[0][0] - 1, sgm_pixels[0][1]
    if sgm_pixels[0][1] > 0:
        return sgm_pixels[0][0], sgm_pixels[0][1] - 1
    if sgm_pixels[len(sgm_pixels) - 1][0] < dim - 1:
        return sgm_pixels[len(sgm_pixels) - 1][0] + 1, sgm_pixels[len(sgm_pixels) - 1][1]
    if sgm_pixels[len(sgm_pixels) - 1][1] < dim - 1:
        return sgm_pixels[len(sgm_pixels) - 1][0], sgm_pixels[len(sgm_pixels) - 1][1] + 1
    return None


# detect segments by single-pixel colour differences
segmentation_time = datetime.now()
thisY, thisX, found_sth_to_analyse = 0, 0, True
while found_sth_to_analyse:
    found_sth_to_analyse = False
    for y in range(thisY, dim):
        for x in range(thisX if y == thisY else 0, dim):
            if status[y, x] == -1:
                found_sth_to_analyse = True
                thisY = y
                thisX = x
                break
        if found_sth_to_analyse: break
    if not found_sth_to_analyse: break
    # print(thisY, thisX)

    segment = list()
    neighbours_of(thisY, thisX, segment, len(segments))
    segments.append(segment)

# dissolve smaller segments
# open('vis/before_dissolution.json', 'w').write(json.dumps(segments, indent=2))  # import json
for seg in range(len(segments)):
    if len(segments[seg]) == 0: continue
    if len(segments[seg]) < min_seg:
        segments[seg].sort(key=lambda s: s[1])
        segments[seg].sort(key=lambda s: s[0])
        parent_index = find_a_segment_to_dissolve_in(segments[seg])
        if parent_index is None:
            print('parent_index is None:', segments[seg])
            continue
        parent: list[tuple[int, int]] = segments[status[parent_index[0], parent_index[1]]]
        parent.extend(segments[seg])
        segments[seg].clear()
# open('vis/after_dissolution.json', 'w').write(json.dumps(segments, indent=2))

# temporary double dissolution FIX-ME
for seg in range(len(segments)):
    if len(segments[seg]) == 0: continue
    if len(segments[seg]) < min_seg:
        segments[seg].sort(key=lambda s: s[1])
        segments[seg].sort(key=lambda s: s[0])
        parent_index = find_a_segment_to_dissolve_in(segments[seg])
        if parent_index is None:
            print('parent_index is None:', segments[seg])
            continue
        parent: list[tuple[int, int]] = segments[status[parent_index[0], parent_index[1]]]
        parent.extend(segments[seg])
        segments[seg].clear()

print('Segmentation time:', datetime.now() - segmentation_time)

# FIX-ME neighbours_of does a lot of repeated work!! Although it might be useful!
# TO-DO where are the other segments?!?

segments.sort(key=lambda s: len(s), reverse=True)

# show the persisting small segments
for seg in range(len(segments)):
    if len(segments[seg]) < min_seg:
        for px in segments[seg]:
            arr[px[0], px[1]] = 0, 255, 255
        continue
    print(seg, ':', len(segments[seg]))

# colour the biggest segments
for big_sgm in range(25):
    for px in segments[big_sgm]:
        arr[px[0], px[1]] = 5 + (10 * (big_sgm + 1)), 255, 255

# print a summary
total_segments = 0
for seg in segments:
    if len(seg) > 0:
        total_segments += 1
print('Total segments:', total_segments)

# show the image
plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)  # mere File->Image->RGB->HSV->RGB->Image->ImShow: 0:00:00.430~~480
plot.show()

# I wrote this algorithm days ago, and now I found it in Wikipedia that it is called a "Region-growing" method!!
