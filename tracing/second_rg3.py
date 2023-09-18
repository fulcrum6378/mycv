import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

# load the segmentation outputs
loading_time = datetime.now()
status: np.ndarray = pickle.load(open('segmentation/output/rg3_status.pickle', 'rb'))
segments: list[list[tuple[int, int]]] = pickle.load(open('segmentation/output/rg3_segments.pickle', 'rb'))
dim = 1088
print('Loading time:', datetime.now() - loading_time)


class SegmentInfo:
    def __int__(self):
        self.a: int = 0  # total colour A values
        self.b: int = 0  # total colour B values
        self.c: int = 0  # total colour C values
        self.m: list[int] = []  # mean colour
        self.border: list[list[float]] = []
        self.min_y, self.min_x, self.max_y, self.max_x = -1, -1, -1, -1  # boundaries
        self.w, self.h = -1, -1  # dimensions

    # THIS PROCESS COULD BE DONE DURING THE SEGMENTATION...
    def add_colour(self, c: list[int]):
        self.a += c[0] * c[0]
        self.b += c[1] * c[1]
        self.c += c[2] * c[2]


# recursively checks if neighbours are border pixels. directions range are 0..7.
def check_neighbours(y: int, x: int, avoid_dir: Optional[int] = None):
    s_ = status[*border_checkpoint]
    next_ones: list[tuple[int, int, int]] = []
    if avoid_dir != 0 and y > 0:  # northern
        n = (y - 1, x)
        if is_next_b(s_, *n): next_ones.append(n + (0,))
    if avoid_dir != 1 and y > 0 and x < (dim - 1):  # north-eastern
        n = (y - 1, x + 1)
        if is_next_b(s_, *n): next_ones.append(n + (1,))
    if avoid_dir != 2 and x < (dim - 1):  # eastern
        n = (y, x + 1)
        if is_next_b(s_, *n): next_ones.append(n + (2,))
    if avoid_dir != 3 and y < (dim - 1) and x < (dim - 1):  # south-eastern
        n = (y + 1, x + 1)
        if is_next_b(s_, *n): next_ones.append(n + (3,))
    if avoid_dir != 4 and y < (dim - 1):  # southern
        n = (y + 1, x)
        if is_next_b(s_, *n): next_ones.append(n + (4,))
    if avoid_dir != 5 and y < (dim - 1) and x > 0:  # south-western
        n = (y + 1, x - 1)
        if is_next_b(s_, *n): next_ones.append(n + (5,))
    if avoid_dir != 6 and x > 0:  # western
        n = (y, x - 1)
        if is_next_b(s_, *n): next_ones.append(n + (6,))
    if avoid_dir != 7 and y > 0 and x > 0:  # north-western
        n = (y - 1, x - 1)
        if is_next_b(s_, *n): next_ones.append(n + (7,))

    for y, x, d in next_ones: check_neighbours(y, x, d)


# checks if this is a border pixel and not detected before
def is_next_b(s: int, y: int, x: int) -> bool:
    if b_status[y, x] is None:
        check_if_border(s, y, x)
        if b_status[y, x] and status[y, x] == s:
            return True
    return False


def check_if_border(s: int, y: int, x: int) -> None:
    if x < (dim - 1):  # right
        if s != status[y, x + 1]:
            set_is_border(y, x)
            return
    else:
        set_is_border(y, x)
        return
    if y < (dim - 1):  # bottom
        if s != status[y + 1, x]:
            set_is_border(y, x)
            return
    else:
        set_is_border(y, x)
        return
    if x > 0:  # left
        if s != status[y, x - 1]:
            set_is_border(y, x)
            return
    else:
        set_is_border(y, x)
        return
    if y > 0:  # top
        if s != status[y - 1, x]:
            set_is_border(y, x)
            return
    else:
        set_is_border(y, x)
        return


def set_is_border(y: int, x: int):
    b_status[y, x] = True
    _s = status[y, x]
    # TODO _s.border.append([(100 / _s.w) * _s.min_x - x, (100 / _s.h) * _s.min_y - y])


# get a mean value of all colours in all segments, detect their border pixels and also their boundaries
mean_and_border_time = datetime.now()
# noinspection PyTypeChecker
b_status: np.ndarray[Optional[bool]] = np.repeat([np.repeat(None, dim)], dim, 0)
s_status: list[SegmentInfo] = []
# TODO for p in pixels: segments[p.s].add_colour(p.c)
for seg in range(len(segments)):
    if len(segments[seg]) == 0: break
    s_status.append(SegmentInfo())
    for
    # TODO seg.mean()
    # TODO seg.detect_boundaries()

    # find the first encountering border pixel as a checkpoint
    border_checkpoint: Optional[tuple[int, int]] = None
    for p in segments[seg]:
        if b_status[*p] is None: check_if_border(status[*p], *p)
        if b_status[*p]:
            border_checkpoint = p
            break

    # now start collecting all border pixels using that checkpoint
    check_neighbours(*border_checkpoint)
print('Mean and border time:', datetime.now() - mean_and_border_time)

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
s_id = 2
seg = segments[s_id]
arr: list[list[list[int]]] = []
for y in range(seg.min_y, seg.max_y + 1):
    xes: list[list[int]] = []
    for x in range(seg.min_x, seg.max_x + 1):
        p = pixels[Pixel.get_pos(y, x)]
        if p.s == s_id:
            if not p.b:
                xes.append(seg.m)  # p.c
            else:
                xes.append([0, 255, 200])
        else:
            xes.append([255, 127, 127])
    arr.append(xes)
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
