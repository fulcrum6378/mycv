import json
import os
import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, bitmap_folder, dim, display_segment, max_export_segments


class Segment:
    def __init__(self):
        self.id: int = 0
        self.p: list[int] = []  # pixels
        self.m: list[int] = []  # average colour


# noinspection PyTypeChecker
def is_next_b(org_s: Segment, yy: int, xx: int) -> bool:
    """ Checks if this is a border pixel and not detected before. """
    s_ = status[yy, xx]
    if s_ != org_s.id: return False
    if b_status[yy, xx] is None:
        check_if_border(s_, yy, xx)
        return b_status[yy, xx]
    return False


def check_if_border(s_id: int, yy: int, xx: int) -> None:
    """ Checks if this pixel is in border. """
    if (  # do NOT use "&&" for straight neighbours!
            (yy == 0 or s_id != status[yy - 1, xx]) or  # northern
            ((yy > 0 and xx < (dim - 1)) and s_id != status[yy - 1, xx + 1]) or  # north-eastern
            (xx == (dim - 1) or s_id != status[yy, xx + 1]) or  # eastern
            ((yy < (dim - 1) and xx < (dim - 1)) and s_id != status[yy + 1, xx + 1]) or  # south-eastern
            (yy == (dim - 1) or s_id != status[yy + 1, xx]) or  # southern
            ((yy < (dim - 1) and xx > 0) and s_id != status[yy + 1, xx - 1]) or  # south-western
            (xx == 0 or s_id != status[yy, xx - 1]) or  # western
            ((yy > 0 and xx > 0) and s_id != status[yy - 1, xx - 1])  # north-western
    ):
        b_status[yy, xx] = True
        if s_id not in s_border: s_border[s_id] = []
        s_border[s_id].append((
            (100.0 / s_dimensions[s_id][0]) * (xx - s_boundaries[s_id][1]),  # fractional X
            (100.0 / s_dimensions[s_id][1]) * (yy - s_boundaries[s_id][0]),  # fractional Y
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
        y, x = _p >> 16, _p & 0xFFFF
        if seg.id not in s_boundaries:  # messed because Python has no do... while!
            s_boundaries[seg.id] = [y, x, y, x]
            continue
        if y < s_boundaries[seg.id][0]: s_boundaries[seg.id][0] = y
        if x < s_boundaries[seg.id][1]: s_boundaries[seg.id][1] = x
        if y > s_boundaries[seg.id][2]: s_boundaries[seg.id][2] = y
        if x > s_boundaries[seg.id][3]: s_boundaries[seg.id][3] = x
    s_dimensions[seg.id] = (
        (s_boundaries[seg.id][3] + 1) - s_boundaries[seg.id][1],  # width
        (s_boundaries[seg.id][2] + 1) - s_boundaries[seg.id][0],  # height
    )
stack: list[list[int, int, int]] = []
for seg in segments:
    # find the first encountering border pixel as a checkpoint
    y, x = 0, 0
    for p in seg.p:
        y, x = p >> 16, p & 0xFFFF
        if b_status[y, x] is None: check_if_border(seg.id, y, x)
        if b_status[y, x]:
            break

    # then start collecting all border pixels using that checkpoint
    stack.append([y, x, 0])
    while len(stack) != 0:
        y, x, avoid_dir = stack[len(stack) - 1]
        stack.pop()
        ny, nx = y, x
        if avoid_dir != 5 and y > 0:  # northern
            ny = y - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 1])
        if avoid_dir != 6 and y > 0 and x < (dim - 1):  # north-eastern
            ny = y - 1
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 2])
        if avoid_dir != 7 and x < (dim - 1):  # eastern
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 3])
        if avoid_dir != 8 and y < (dim - 1) and x < (dim - 1):  # south-eastern
            ny = y + 1
            nx = x + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 4])
        if avoid_dir != 1 and y < (dim - 1):  # southern
            ny = y + 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 5])
        if avoid_dir != 2 and y < (dim - 1) and x > 0:  # south-western
            ny = y + 1
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 6])
        if avoid_dir != 3 and x > 0:  # western
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 7])
        if avoid_dir != 4 and y > 0 and x > 0:  # north-western
            ny = y - 1
            nx = x - 1
            if is_next_b(seg, ny, nx): stack.append([ny, nx, 8])
# FIX-ME borders with shapes within another shape are not detected!
#  and since the contrary is also true, that's why we face problems.
#  Because sometimes the checkpoint is INSIDE a shape
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
if display_segment != -1:
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
else:
    arr: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap + '.bmp')),
                                   cv2.COLOR_BGR2RGB)
    for y in range(dim):
        for x in range(dim):
            if b_status[y, x]:
                arr[y, x] = 255, 0, 0
    plot.imshow(arr)
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
