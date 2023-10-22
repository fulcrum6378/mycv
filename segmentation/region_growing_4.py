import os
import pickle
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap, bitmap_folder, dim, min_seg

# read the image
loading_time = datetime.now()
arr: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap + '.bmp')),
                               cv2.COLOR_BGR2YUV)
# YCbCr (correspondant to YUV) != YCrCb (provided by `cv2`)
print('Loading time:', datetime.now() - loading_time)


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


def find_a_segment_to_dissolve_in(seg_: Segment) -> Optional[tuple[int, int]]:
    y_, x_ = seg_.p[0] >> 16, seg_.p[0] & 0xFFFF
    if y_ > 0:
        return y_ - 1, x_
    if x_ > 0:
        return y_, x_ - 1
    last = len(seg_.p) - 1
    y_, x_ = seg_.p[last] >> 16, seg_.p[last] & 0xFFFF
    if y_ < dim - 1:
        return y_ + 1, x_
    if x_ < dim - 1:
        return y_, x_ + 1
    return None


# detect segments by single-pixel colour differences
segmentation_time = datetime.now()
status: np.ndarray = np.zeros((dim, dim), np.int32)
segments: list[Segment] = []
stack: dict[int, int] = {}
stack_order: list[int] = []
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
    cor = (thisY << 16) | thisX
    stack[cor] = 0
    stack_order.append(cor)
    while len(stack_order) != 0:
        l_ = len(stack_order) - 1
        cor = stack_order[l_]
        yy, xx = cor >> 16, cor & 0xFFFF
        dr = stack[cor]
        if dr == 0:
            seg.p.append((yy << 16) | xx)
            status[yy, xx] = seg.id
            # if dr <= 0:  # left
            stack[cor] += 1
            if xx > 0 and status[yy, xx - 1] == 0 and compare_colours(arr[yy, xx], arr[yy, xx - 1]):
                cor_n = (yy << 16) | (xx - 1)
                if cor_n in stack:
                    stack[cor_n] = 0
                    stack_order.append(cor_n)
                    continue
        # TODO recheck for status[yy, xx]
        if dr <= 1:  # top
            stack[cor] += 1
            if yy > 0 and status[yy - 1, xx] == 0 and compare_colours(arr[yy, xx], arr[yy - 1, xx]):
                cor_n = ((yy - 1) << 16) | xx
                if cor_n in stack:
                    stack[cor_n] = 0
                    stack_order.append(cor_n)
                    continue
        if dr <= 2:  # right
            stack[cor] += 1
            if xx < (dim - 1) and status[yy, xx + 1] == 0 and compare_colours(arr[yy, xx], arr[yy, xx + 1]):
                cor_n = (yy << 16) | (xx + 1)
                if cor_n in stack:
                    stack[cor_n] = 0
                    stack_order.append(cor_n)
                    continue
        if dr <= 3:  # bottom
            stack[cor] += 1
            if yy < (dim - 1) and status[yy + 1, xx] == 0 and compare_colours(arr[yy, xx], arr[yy + 1, xx]):
                cor_n = ((yy + 1) << 16) | xx
                if cor_n in stack:
                    stack[cor_n] = 0
                    stack_order.append(cor_n)
                    continue
        stack.pop(cor)
        stack_order.pop()
    segments.append(seg)

# dissolve smaller segments
if min_seg > 1:
    dissolution_time = datetime.now()
    for seg in range(len(segments) - 1, -1, -1):
        if len(segments[seg].p) < min_seg:
            absorber_index = find_a_segment_to_dissolve_in(segments[seg])
            if absorber_index is None: continue  # rarely
            absorber: Segment = segments[status[*absorber_index] - 1]  # `- 1` is because segment IDs start from 0!
            for p in segments[seg].p:
                absorber.p.append(p)
                status[p >> 16, p & 0xFFFF] = absorber.id
            segments.pop(seg)
    print('Dissolution time:', datetime.now() - dissolution_time)
print('+ Segmentation time:', datetime.now() - segmentation_time)

# it is actually a temporary part of tracing, but is done here for efficiency.
average_colours_time = datetime.now()
for seg in segments:
    for p in seg.p:
        y, x = p >> 16, p & 0xFFFF
        seg.ys += arr[y, x][0]
        seg.us += arr[y, x][1]
        seg.vs += arr[y, x][2]
    seg.calculate_mean(len(seg.p))
print('+ Average colours time:', datetime.now() - average_colours_time)

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

# save the output
dumping_time = datetime.now()
pickle.dump(status, open(os.path.join('segmentation', 'output', 'rg4_' + bitmap + '_status.pickle'), 'wb'))
pickle.dump(segments, open(os.path.join('segmentation', 'output', 'rg4_' + bitmap + '_segments.pickle'), 'wb'))
print('Dumping time:', datetime.now() - dumping_time)
