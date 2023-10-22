import os
import pickle
from datetime import datetime

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, bitmap2, bitmap_folder, dim


class Segment:
    def __init__(self):
        self.id: int = len(segments) + 1
        self.p: list[tuple[int, int]] = []  # pixels
        self.ys: int = 0  # sum of Y channel
        self.us: int = 0  # sum of U channel
        self.vs: int = 0  # sum of V channel
        self.m: list[int] = []  # average colour

    def calculate_mean(self, al: int):
        self.m = [round(self.ys / al), round(self.us / al), round(self.vs / al)]


def compare_colours(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 4 \
        and abs(int(a[1]) - int(b[1])) <= 4 \
        and abs(int(a[2]) - int(b[2])) <= 4


# load the segmentation output data
loading_time = datetime.now()
status: np.ndarray = pickle.load(open(os.path.join(
    'segmentation', 'output', 'rg4_' + bitmap + '_status.pickle'), 'rb'))
segments: list[Segment] = pickle.load(open(os.path.join(
    'segmentation', 'output', 'rg4_' + bitmap + '_segments.pickle'), 'rb'))

# index previous segments (not required for C++ as it has implemented `s_index`)
s_index: dict[int, int] = {}  # id, offset in `segments`
for seg in range(len(segments)):
    s_index[segments[seg].id] = seg

# read the both image frames
arr: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap + '.bmp')),
                               cv2.COLOR_BGR2YUV)
buf: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap2 + '.bmp')),
                               cv2.COLOR_BGR2YUV)
print('+ Loading time:', datetime.now() - loading_time)

# trace changes in `buf` and write them into `arr`
for y in range(dim):
    for x in range(dim):
        if compare_colours(arr[y, x], buf[y, x]):
            arr[y, x] = buf[y, x]
        else:
            # noinspection PyTypeChecker
            seg = segments[s_index[status[y, x]]]
            # seg.p.remove((y, x))  # FIXME so heavy operation!
            seg.ys -= arr[y, x, 0]
            seg.us -= arr[y, x, 1]
            seg.vs -= arr[y, x, 2]  # TODO calculate_mean() later
            status[y, x] = 0
            arr[y, x] = 76, 84, 255  # FIXME
        # arr[y, x] = buf[y, x]
del buf  # not necessary in C++

# TODO Find new Segments for changed pixels

# Render differences
render_time = datetime.now()
plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
print('Rendering time:', datetime.now() - render_time)
plot.show()
