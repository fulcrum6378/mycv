import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np


class Segment:
    def __init__(self):
        self.id: int = 0
        self.p: list[tuple[int, int]] = []  # pixels
        self.a: int = 0  # total A colour values
        self.b: int = 0  # total B colour values
        self.c: int = 0  # total C colour values
        self.m: list[int] = []  # mean colour
        self.border: list[list[float]] = []
        self.min_y, self.min_x, self.max_y, self.max_x = -1, -1, -1, -1  # boundaries
        self.w, self.h = -1, -1  # dimensions


# recursively checks if neighbours are border pixels. directions range are 0..7.
def check_neighbours(s_: Segment, yy: int, xx: int, avoid_dir: Optional[int] = None):
    next_ones: list[tuple[int, int, int]] = []
    if avoid_dir != 0 and yy > 0:  # northern
        n = (yy - 1, xx)
        if is_next_b(s_, *n): next_ones.append(n + (0,))
    if avoid_dir != 1 and yy > 0 and xx < (dim - 1):  # north-eastern
        n = (yy - 1, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (1,))
    if avoid_dir != 2 and xx < (dim - 1):  # eastern
        n = (yy, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (2,))
    if avoid_dir != 3 and yy < (dim - 1) and xx < (dim - 1):  # south-eastern
        n = (yy + 1, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (3,))
    if avoid_dir != 4 and yy < (dim - 1):  # southern
        n = (yy + 1, xx)
        if is_next_b(s_, *n): next_ones.append(n + (4,))
    if avoid_dir != 5 and yy < (dim - 1) and xx > 0:  # south-western
        n = (yy + 1, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (5,))
    if avoid_dir != 6 and xx > 0:  # western
        n = (yy, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (6,))
    if avoid_dir != 7 and yy > 0 and xx > 0:  # north-western
        n = (yy - 1, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (7,))

    for y_, x_, d in next_ones: check_neighbours(s_, y_, x_, d)


# checks if this is a border pixel and not detected before
def is_next_b(s_: Segment, yy: int, xx: int) -> bool:
    if b_status[yy, xx] is None:
        self_s = status[yy, xx]
        # noinspection PyTypeChecker
        check_if_border(self_s, yy, xx)
        if b_status[yy, xx] and self_s == s_.id:
            return True
    return False


# checks if this pixel is in border
def check_if_border(s_, yy: int, xx: int) -> None:
    s_id = s_.id if isinstance(s_, Segment) else s_

    if xx < (dim - 1):  # right
        if s_id != status[yy, xx + 1]:
            set_is_border(s_, yy, xx)
            return
    else:
        set_is_border(s_, yy, xx)
        return
    if yy < (dim - 1):  # bottom
        if s_id != status[yy + 1, xx]:
            set_is_border(s_, yy, xx)
            return
    else:
        set_is_border(s_, yy, xx)
        return
    if xx > 0:  # left
        if s_id != status[yy, xx - 1]:
            set_is_border(s_, yy, xx)
            return
    else:
        set_is_border(s_, yy, xx)
        return
    if yy > 0:  # top
        if s_id != status[yy - 1, xx]:
            set_is_border(s_, yy, xx)
            return
    else:
        set_is_border(s_, yy, xx)
        return


def set_is_border(s_, yy: int, xx: int):
    if not isinstance(s_, Segment):
        s_ = next(s for s in segments if s.id == s_)
    b_status[yy, xx] = True
    s_.border.append([(100 / s_.w) * s_.min_x - xx, (100 / s_.h) * s_.min_y - yy])


# load the segmentation output data
loading_time = datetime.now()
status: np.ndarray = pickle.load(open('segmentation/output/rg3_status.pickle', 'rb'))
segments: list[Segment] = pickle.load(open('segmentation/output/rg3_segments.pickle', 'rb'))
dim: int = 1088
print('Loading time:', datetime.now() - loading_time)

# get a mean value of all colours in all segments, detect their border pixels and also their boundaries
mean_and_border_time = datetime.now()
# noinspection PyTypeChecker
b_status: np.ndarray[Optional[bool]] = np.repeat([np.repeat(None, dim)], dim, 0)
for seg in segments:  # don't cut it!
    if len(seg.p) == 0: continue

    # calculate mean colour (NOT USING POW/SQRT)
    l_ = len(seg.p)
    seg.m = [round(seg.a / l_), round(seg.b / l_), round(seg.c / l_)]
    del seg.a, seg.b, seg.c

    # detect boundaries (min_y, min_x, max_y, max_x)
    for _p in seg.p:
        if seg.min_y == -1:  # messed because Python has no do... while!
            seg.min_y = seg.max_y = _p[0]
            seg.min_x = seg.max_x = _p[1]
            continue
        if _p[0] < seg.min_y: seg.min_y = _p[0]
        if _p[1] < seg.min_x: seg.min_x = _p[1]
        if _p[0] > seg.max_y: seg.max_y = _p[0]
        if _p[1] > seg.max_x: seg.max_x = _p[1]
    seg.w = (seg.max_x + 1) - seg.min_x
    seg.h = (seg.max_y + 1) - seg.min_y

    # find the first encountering border pixel as a checkpoint
    border_checkpoint: Optional[tuple[int, int]] = None
    for p in seg.p:
        if b_status[*p] is None: check_if_border(seg, *p)
        if b_status[*p]:
            border_checkpoint = p
            break

    # now start collecting all border pixels using that checkpoint
    check_neighbours(seg, *border_checkpoint)
print('Mean and border time:', datetime.now() - mean_and_border_time)

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
seg = segments[2]
print(len(seg.border))
arr: list[list[list[int]]] = []
for y in range(seg.min_y, seg.max_y + 1):
    xes: list[list[int]] = []
    for x in range(seg.min_x, seg.max_x + 1):
        if status[y, x] == seg.id:
            if not b_status[y, x]:
                xes.append(seg.m)
            else:
                xes.append([0, 255, 200])
        else:
            xes.append([255, 127, 127])
    arr.append(xes)
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
