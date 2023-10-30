import os
import pickle
from datetime import datetime

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, bitmap_folder, dim, min_seg

# config:
bitmap2: str = '1689005849796309'
just_render_differences = False


class Segment:
    def __init__(self):
        self.id: int = len(segments) + 1
        self.p: list[int] = []  # pixels
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
updating_time = datetime.now()
for y in range(dim):
    for x in range(dim):
        if compare_colours(arr[y, x], buf[y, x]):
            arr[y, x] = buf[y, x]
        else:
            # noinspection PyTypeChecker
            seg = segments[s_index[status[y, x]]]
            seg.p.pop(seg.p.index((y << 16) | x))  # FIX-ME so heavy operation!
            seg.ys -= arr[y, x, 0]
            seg.us -= arr[y, x, 1]
            seg.vs -= arr[y, x, 2]  # TO-DO calculate_mean() later
            status[y, x] = 0
            arr[y, x] = 76, 84, 255  # FIX-ME
        # arr[y, x] = buf[y, x]
del buf  # not necessary in C++
print('+ Updating time:', datetime.now() - updating_time)

if just_render_differences:
    render_time = datetime.now()
    plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
    print('Rendering time:', datetime.now() - render_time)
    plot.show()
    quit()

# repeat the same code
segmentation_time = datetime.now()
stack: list[list[int, int, int]] = []
thisY, thisX, found_sth_to_analyse = 0, 0, True
while found_sth_to_analyse:
    found_sth_to_analyse = False
    for y in range(thisY, dim):
        for x in range(thisX if y == thisY else 0, dim):
            if status[y, x] == 0:
                found_sth_to_analyse = True
                thisY = y
                thisX = x
                break
        if found_sth_to_analyse: break
    if not found_sth_to_analyse: break

    seg = Segment()
    stack.append([thisY, thisX, 0])
    while len(stack) != 0:
        l_ = len(stack) - 1
        yy, xx, dr = stack[l_]
        if dr == 0:
            seg.p.append((yy << 16) | xx)
            status[yy, xx] = seg.id
            # if dr <= 0:  # left
            stack[l_][2] += 1
            if xx > 0 and status[yy, xx - 1] == 0 and compare_colours(arr[yy, xx], arr[yy, xx - 1]):
                stack.append([yy, xx - 1, 0])
                continue
        if dr <= 1:  # top
            stack[l_][2] += 1
            if yy > 0 and status[yy - 1, xx] == 0 and compare_colours(arr[yy, xx], arr[yy - 1, xx]):
                stack.append([yy - 1, xx, 0])
                continue
        if dr <= 2:  # right
            stack[l_][2] += 1
            if xx < (dim - 1) and status[yy, xx + 1] == 0 and compare_colours(arr[yy, xx], arr[yy, xx + 1]):
                stack.append([yy, xx + 1, 0])
                continue
        if dr <= 3:  # bottom
            stack[l_][2] += 1
            if yy < (dim - 1) and status[yy + 1, xx] == 0 and compare_colours(arr[yy, xx], arr[yy + 1, xx]):
                stack.append([yy + 1, xx, 0])
                continue
        stack.pop()
    segments.append(seg)
print('+ Segmentation time:', datetime.now() - segmentation_time)

# evaluate the segments
segments.sort(key=lambda s: len(s.p), reverse=True)
arr = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB), cv2.COLOR_RGB2HSV)
for big_sgm in range(25):  # colour the biggest ones
    for px in segments[big_sgm].p:
        arr[px >> 16, px & 0xFFFF] = 5 + (10 * (big_sgm + 1)), 255, 255
for seg in range(len(segments)):  # show the persisting small segments
    if len(segments[seg].p) < min_seg:
        for px in segments[seg].p:
            arr[px >> 16, px & 0xFFFF] = 0, 255, 255
        continue
arr = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_HSV2RGB), cv2.COLOR_RGB2YUV)
print('Total segments:', len(segments))

# show the image
plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
plot.show()
