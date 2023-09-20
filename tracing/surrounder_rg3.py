import json
import pickle
import sys
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np


class Segment:
    def __init__(self):
        self.id: int = 0
        self.p: list[tuple[int, int]] = []  # pixels
        self.m: list[int] = []  # average colour


def check_neighbours(s_: Segment, yy: int, xx: int, avoid_dir: int = -1):
    """ Recursively checks if neighbours are border pixels. directions range are 0..7. """

    if avoid_dir != 0 and yy > 0:  # northern
        n = (yy - 1, xx)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 0)
    if avoid_dir != 1 and yy > 0 and xx < (dim - 1):  # north-eastern
        n = (yy - 1, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 1)
    if avoid_dir != 2 and xx < (dim - 1):  # eastern
        n = (yy, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 2)
    if avoid_dir != 3 and yy < (dim - 1) and xx < (dim - 1):  # south-eastern
        n = (yy + 1, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 3)
    if avoid_dir != 4 and yy < (dim - 1):  # southern
        n = (yy + 1, xx)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 4)
    if avoid_dir != 5 and yy < (dim - 1) and xx > 0:  # south-western
        n = (yy + 1, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 5)
    if avoid_dir != 6 and xx > 0:  # western
        n = (yy, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 6)
    if avoid_dir != 7 and yy > 0 and xx > 0:  # north-western
        n = (yy - 1, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 7)


# noinspection PyTypeChecker
def is_next_b(org_s: Segment, yy: int, xx: int) -> bool:
    """ Checks if this is a border pixel and not detected before FIXME but it's not urgent """

    # WORKS FINE ONLY WITHOUT DISSOLUTION!
    # if b_status[yy, xx] is None:
    #    s_ = status[yy, xx]
    #    check_if_border(s_, yy, xx)
    #    if b_status[yy, xx] and s_ == org_s.id:
    #        return True
    # return False
    # DOESN'T WORK FINE IN THE TEST!!!
    s_ = status[yy, xx]
    if s_ == org_s.id: return False  # AS MUCH AS I THINK, IT SHOULD BE `s_ != org_s.id`, BUT THE OPPOSITE WORKS!
    if b_status[yy, xx] is None:
        check_if_border(s_, yy, xx)
        return b_status[yy, xx]
    return False


def check_if_border(s_id: int, yy: int, xx: int) -> None:
    """ Checks if this pixel is in border. """
    if (xx == (dim - 1) or s_id != status[yy, xx + 1] or  # right
            yy == (dim - 1) or s_id != status[yy + 1, xx] or  # bottom
            xx == 0 or s_id != status[yy, xx - 1] or  # left
            yy == 0 or s_id != status[yy - 1, xx]):  # top
        set_is_border(s_id, yy, xx)
        return
    b_status[yy, xx] = False


def set_is_border(s_id: int, yy: int, xx: int):
    b_status[yy, xx] = True
    if s_id not in s_border: s_border[s_id] = []
    s_border[s_id].append((
        (100.0 / s_dimensions[seg.id][0]) * (s_boundaries[s_id][1] - xx),  # fractional X
        (100.0 / s_dimensions[seg.id][1]) * (s_boundaries[s_id][0] - yy),  # fractional Y
    ))


# load the segmentation output data
loading_time = datetime.now()
status: np.ndarray = pickle.load(open('segmentation/output/rg3_status.pickle', 'rb'))
segments: list[Segment] = pickle.load(open('segmentation/output/rg3_segments.pickle', 'rb'))
dim: int = 1088
sys.setrecursionlimit(dim * dim)
print('Loading time:', datetime.now() - loading_time)

# get a mean value of all colours in all segments, detect their border pixels and also their boundaries
border_time = datetime.now()
# noinspection PyTypeChecker
b_status: np.ndarray[Optional[bool]] = np.repeat([np.repeat(None, dim)], dim, 0)
s_border: dict[int, list[tuple[float, float]]] = {}
s_boundaries: dict[int, list[int, int, int, int]] = {}  # min_y, min_x, max_y, max_x
s_dimensions: dict[int, tuple[int, int]] = {}  # width, height
for seg in segments:
    # detect boundaries (min_y, min_x, max_y, max_x)
    for _p in seg.p:
        if seg.id not in s_boundaries:  # messed because Python has no do... while!
            s_boundaries[seg.id] = [_p[0], _p[1], _p[0], _p[1]]
            continue
        if _p[0] < s_boundaries[seg.id][0]: s_boundaries[seg.id][0] = _p[0]
        if _p[1] < s_boundaries[seg.id][1]: s_boundaries[seg.id][1] = _p[1]
        if _p[0] > s_boundaries[seg.id][2]: s_boundaries[seg.id][2] = _p[0]
        if _p[1] > s_boundaries[seg.id][3]: s_boundaries[seg.id][3] = _p[1]
    s_dimensions[seg.id] = (
        (s_boundaries[seg.id][3] + 1) - s_boundaries[seg.id][1],  # width
        (s_boundaries[seg.id][2] + 1) - s_boundaries[seg.id][0],  # height
    )
# it wouldn't be like this, if `is_next_b()` didn't permit foreign segments!
for seg in segments:
    # find the first encountering border pixel as a checkpoint
    border_checkpoint: Optional[tuple[int, int]] = None
    for p in seg.p:
        if b_status[*p] is None: check_if_border(seg.id, *p)
        if b_status[*p]:
            border_checkpoint = p
            break

    # now start collecting all border pixels using that checkpoint
    check_neighbours(seg, *border_checkpoint)
print('+ Border time:', datetime.now() - border_time)

# store 5 of largest segments
for s in range(15):
    open('tracing/output/' + str(s) + '.json', 'w').write(json.dumps({
        'mean': segments[s].m,
        'path': s_border[segments[s].id],
        'dimensions': [s_dimensions[segments[s].id][0], s_dimensions[segments[s].id][1]],
    }))

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
seg = segments[2]
print('Total border pixels:', len(s_border[seg.id]))
arr: list[list[list[int]]] = []
for y in range(s_boundaries[seg.id][0], s_boundaries[seg.id][2] + 1):
    xes: list[list[int]] = []
    for x in range(s_boundaries[seg.id][1], s_boundaries[seg.id][3] + 1):
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
