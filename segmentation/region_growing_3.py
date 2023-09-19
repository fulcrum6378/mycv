import pickle
import sys
from datetime import datetime
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np

# read the image
loading_time = datetime.now()
# red pillow: 1689005849386887, shoes: 1689005891979733
arr: np.ndarray = cv2.cvtColor(cv2.imread('vis/2/1689005849386887.bmp'), cv2.COLOR_BGR2YUV)
dim: int = 1088
min_seg = 30
sys.setrecursionlimit(dim * dim)
print('Loading time:', datetime.now() - loading_time)


class Segment:
    def __init__(self):
        self.id: int = len(segments)
        self.p: list[tuple[int, int]] = []  # pixels
        self.a, self.b, self.c = 0, 0, 0  # sum of colour values
        self.m: list[int] = []  # mean colour


def compare_colours(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 4 \
        and abs(int(a[1]) - int(b[1])) <= 4 \
        and abs(int(a[2]) - int(b[2])) <= 4


def neighbours_of(yy: int, xx: int, seg_: Segment):
    seg_.p.append((yy, xx))
    status[yy, xx] = seg_.id
    if xx > 0 and status[yy, xx - 1] == -1 and compare_colours(arr[yy, xx], arr[yy, xx - 1]):  # left
        neighbours_of(yy, xx - 1, seg_)
    if yy > 0 and status[yy - 1, xx] == -1 and compare_colours(arr[yy, xx], arr[yy - 1, xx]):  # top
        neighbours_of(yy - 1, xx, seg_)
    if xx < (dim - 1) and status[yy, xx + 1] == -1 and compare_colours(arr[yy, xx], arr[yy, xx + 1]):  # right
        neighbours_of(yy, xx + 1, seg_)
    if yy < (dim - 1) and status[yy + 1, xx] == -1 and compare_colours(arr[yy, xx], arr[yy + 1, xx]):  # bottom
        neighbours_of(yy + 1, xx, seg_)


# It must become more developed. You can also calculate segments' mean values!
def find_a_segment_to_dissolve_in(seg_: Segment) -> Optional[tuple[int, int]]:
    # seg_.p.sort(key=lambda s: s[1])  # no visible difference
    # seg_.p.sort(key=lambda s: s[0])
    if seg_.p[0][0] > 0:
        return seg_.p[0][0] - 1, seg_.p[0][1]
    if seg_.p[0][1] > 0:
        return seg_.p[0][0], seg_.p[0][1] - 1
    if seg_.p[len(seg_.p) - 1][0] < dim - 1:
        return seg_.p[len(seg_.p) - 1][0] + 1, seg_.p[len(seg_.p) - 1][1]
    if seg_.p[len(seg_.p) - 1][1] < dim - 1:
        return seg_.p[len(seg_.p) - 1][0], seg_.p[len(seg_.p) - 1][1] + 1
    return None


# detect segments by single-pixel colour differences
segmentation_time = datetime.now()
status: np.ndarray = np.repeat([np.repeat(-1, dim)], dim, 0)
segments: list[Segment] = []
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
    segment = Segment()
    neighbours_of(thisY, thisX, segment)
    segments.append(segment)

# dissolve smaller segments
if min_seg > 1:
    dissolution_time = datetime.now()
    for seg in range(len(segments) - 1, -1, -1):
        if len(segments[seg].p) < min_seg:
            absorber_index = find_a_segment_to_dissolve_in(segments[seg])
            if absorber_index is None: continue  # rarely
            absorber: Segment = segments[status[*absorber_index]]
            for p in segments[seg].p:
                absorber.p.append(p)
                status[*p] = absorber.id
            segments.pop(seg)
    print('Dissolution time:', datetime.now() - dissolution_time)
print('+ Segmentation time:', datetime.now() - segmentation_time)

# it is actually a temporary part of tracing, but is done here for efficiency.
counting_colours_time = datetime.now()
for seg in segments:
    for p in seg.p:
        seg.a += arr[*p][0]
        seg.b += arr[*p][1]
        seg.c += arr[*p][2]
print('+ Time for counting colour values:', datetime.now() - counting_colours_time)

# evaluate the segments
segments.sort(key=lambda s: len(s.p), reverse=True)
arr = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB), cv2.COLOR_RGB2HSV)
for big_sgm in range(25):  # colour the biggest ones
    for px in segments[big_sgm].p:
        arr[px[0], px[1]] = 5 + (10 * (big_sgm + 1)), 255, 255
for seg in range(len(segments)):  # show the persisting small segments
    if len(segments[seg].p) < min_seg:
        for px in segments[seg].p:
            arr[px[0], px[1]] = 0, 255, 255
        continue
arr = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_HSV2RGB), cv2.COLOR_RGB2YUV)
print('Total segments:', len(segments))

# show the image
plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
plot.show()

# save the output
dumping_time = datetime.now()
pickle.dump(status, open('segmentation/output/rg3_status.pickle', 'wb'))
pickle.dump(segments, open('segmentation/output/rg3_segments.pickle', 'wb'))
print('Dumping time:', datetime.now() - dumping_time)
