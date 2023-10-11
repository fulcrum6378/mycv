import json
import os
import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, bitmap_folder, dim, display_segment, max_export_segments, shape_path_max


class Segment:
    def __init__(self):
        self.id: int = 0
        self.p: list[tuple[int, int]] = []  # pixels
        self.m: list[int] = []  # average colour


def check_if_border(y1: int, x1: int, y2: int, x2: int):
    if status[y1, x1] != status[y2, x2]:
        set_as_border(y1, x1)
        set_as_border(y2, x2)


# noinspection PyTypeChecker,PyShadowingNames
def set_as_border(y: int, x: int):
    b_status[y, x] = True
    s_id = status[y, x]
    if s_id not in s_border: s_border[s_id] = set()
    s_border[s_id].add((
        int((shape_path_max / float(s_dimensions[s_id][0])) * float(x - s_boundaries[s_id][1])),  # fractional X
        int((shape_path_max / float(s_dimensions[s_id][1])) * float(y - s_boundaries[s_id][0])),  # fractional Y
    ))


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
s_border: dict[int, set[tuple[int, int]]] = {}
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
for y in range(dim):
    if y == 0 or y == dim - 1:
        for x in range(dim):
            set_as_border(y, x)
    else:
        for x in range(dim):
            if x == 0 or x == dim - 1:
                set_as_border(y, x)
                continue
            if b_status[y, x] is not None: continue
            check_if_border(y, x, y, x + 1)  # eastern
            check_if_border(y, x, y + 1, x + 1)  # south-eastern
            check_if_border(y, x, y + 1, x)  # southern
            check_if_border(y, x, y + 1, x - 1)  # south-western
print('+ Border time:', datetime.now() - border_time)

# store 5 of largest segments
branch = os.path.join('tracing', 'output', bitmap)
if not os.path.isdir(branch): os.mkdir(branch)
for s in range(max_export_segments):
    open(os.path.join(branch, str(s) + '.json'), 'w').write(json.dumps({
        'mean': segments[s].m,
        'path': list(s_border[segments[s].id]),
        'dimensions': [s_dimensions[segments[s].id][0], s_dimensions[segments[s].id][1]],
        'centre': [
            round((s_boundaries[segments[s].id][1] + s_boundaries[segments[s].id][3] + 1) / 2),  # X
            round((s_boundaries[segments[s].id][0] + s_boundaries[segments[s].id][2] + 1) / 2),  # Y
        ],
    }))

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
if display_segment is not None:
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
    arr: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', bitmap_folder, bitmap + '.bmp')), cv2.COLOR_BGR2RGB)
    for y in range(dim):
        for x in range(dim):
            if b_status[y, x]:
                arr[y, x] = 255, 0, 0
    plot.imshow(arr)
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
