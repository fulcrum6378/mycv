import json
import os
import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, dim, display_segment, max_export_segments


class Segment:
    def __init__(self):
        self.id: int = 0
        self.p: list[tuple[int, int]] = []  # pixels
        self.m: list[int] = []  # average colour


# noinspection PyTypeChecker
def is_next_b(org_s: Segment, yy: int, xx: int) -> bool:
    """ Checks if this is a border pixel and not detected before. """

    # WORKS FINE ONLY WITHOUT DISSOLUTION!
    # if b_status[yy, xx] is None:
    #    s_ = status[yy, xx]
    #    check_if_border(s_, yy, xx)
    #    if b_status[yy, xx] and s_ == org_s.id:
    #        return True
    # return False
    # DOESN'T WORK FINE IN THE TEST!!! FIXME but it's not urgent
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
        b_status[yy, xx] = True
        if s_id not in s_border: s_border[s_id] = []
        s_border[s_id].append((
            (100.0 / s_dimensions[seg.id][0]) * (s_boundaries[s_id][1] - xx),  # fractional X
            (100.0 / s_dimensions[seg.id][1]) * (s_boundaries[s_id][0] - yy),  # fractional Y
        ))
    else:
        b_status[yy, xx] = False


# load the segmentation output data
loading_time = datetime.now()
status: np.ndarray = pickle.load(open(os.path.join(
    'segmentation', 'output', 'rg4_' + bitmap + '_status.pickle'), 'rb'))
segments: list[Segment] = pickle.load(open(os.path.join(
    'segmentation', 'output', 'rg4_' + bitmap + '_segments.pickle'), 'rb'))
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
stack: list[list[int, int, int]] = []
for seg in segments:
    # find the first encountering border pixel as a checkpoint
    y, x = 0, 0
    for p in seg.p:
        if b_status[*p] is None: check_if_border(seg.id, *p)
        if b_status[*p]:
            y, x = p
            break

    # then start collecting all border pixels using that checkpoint
    stack.append([y, x, 0])
    while len(stack) != 0:
        y, x, avoid_dir = stack[0]
        ny, nx = y, x
        if avoid_dir != 1 and y > 0:  # northern
            ny = y - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 1])
        if avoid_dir != 2 and y > 0 and x < (dim - 1):  # north-eastern
            ny = y - 1
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 2])
        if avoid_dir != 3 and x < (dim - 1):  # eastern
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 3])
        if avoid_dir != 4 and y < (dim - 1) and x < (dim - 1):  # south-eastern
            ny = y + 1
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 4])
        if avoid_dir != 5 and y < (dim - 1):  # southern
            ny = y + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 5])
        if avoid_dir != 6 and y < (dim - 1) and x > 0:  # south-western
            ny = y + 1
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 6])
        if avoid_dir != 7 and x > 0:  # western
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 7])
        if avoid_dir != 8 and y > 0 and x > 0:  # north-western
            ny = y - 1
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 8])
        stack.pop(0)
print('+ Border time:', datetime.now() - border_time)

# store 5 of largest segments
branch = os.path.join('tracing', 'output', bitmap)
if not os.path.isdir(branch): os.mkdir(branch)
for s in range(max_export_segments):
    open(os.path.join(branch, str(s) + '.json'), 'w').write(json.dumps({
        'mean': segments[s].m,
        'path': s_border[segments[s].id],
        'dimensions': [s_dimensions[segments[s].id][0], s_dimensions[segments[s].id][1]],
    }))

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
seg = segments[display_segment]
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
