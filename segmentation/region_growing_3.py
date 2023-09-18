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
arr.setflags(write=True)
dim: int = 1088
min_seg = 70
sys.setrecursionlimit(dim * dim)
print('Loading time:', datetime.now() - loading_time)

status: np.ndarray = np.repeat([np.repeat(-1, dim)], dim, 0)  # verified to have no -1 at the end.
segments: list[list[tuple[int, int]]] = list()


def compare_colours(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= 4 \
        and abs(int(a[1]) - int(b[1])) <= 4 \
        and abs(int(a[2]) - int(b[2])) <= 4


def neighbours_of(yy: int, xx: int, pixels: list[tuple[int, int]], sgm_idx: int):
    pixels.append((yy, xx))
    status[yy, xx] = sgm_idx
    if xx > 0 and status[yy, xx - 1] == -1 and compare_colours(arr[yy, xx], arr[yy, xx - 1]):  # left
        neighbours_of(yy, xx - 1, pixels, sgm_idx)
    if yy > 0 and status[yy - 1, xx] == -1 and compare_colours(arr[yy, xx], arr[yy - 1, xx]):  # top
        neighbours_of(yy - 1, xx, pixels, sgm_idx)
    if xx < (dim - 1) and status[yy, xx + 1] == -1 and compare_colours(arr[yy, xx], arr[yy, xx + 1]):  # right
        neighbours_of(yy, xx + 1, pixels, sgm_idx)
    if yy < (dim - 1) and status[yy + 1, xx] == -1 and compare_colours(arr[yy, xx], arr[yy + 1, xx]):  # bottom
        neighbours_of(yy + 1, xx, pixels, sgm_idx)


# It must become more developed. You can also calculate segments' mean values!
def find_a_segment_to_dissolve_in(sgm_pixels: list[tuple[int, int]]) -> Optional[tuple[int, int]]:
    if sgm_pixels[0][0] > 0:
        return sgm_pixels[0][0] - 1, sgm_pixels[0][1]
    if sgm_pixels[0][1] > 0:
        return sgm_pixels[0][0], sgm_pixels[0][1] - 1
    if sgm_pixels[len(sgm_pixels) - 1][0] < dim - 1:
        return sgm_pixels[len(sgm_pixels) - 1][0] + 1, sgm_pixels[len(sgm_pixels) - 1][1]
    if sgm_pixels[len(sgm_pixels) - 1][1] < dim - 1:
        return sgm_pixels[len(sgm_pixels) - 1][0], sgm_pixels[len(sgm_pixels) - 1][1] + 1
    return None


# detect segments by single-pixel colour differences
segmentation_time = datetime.now()
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
    segment = list()
    neighbours_of(thisY, thisX, segment, len(segments))
    segments.append(segment)

# dissolve smaller segments
dissolution_time = datetime.now()
for seg in range(len(segments) - 1, -1, -1):
    if len(segments[seg]) == 0: continue
    if len(segments[seg]) < min_seg:
        segments[seg].sort(key=lambda s: s[1])
        segments[seg].sort(key=lambda s: s[0])
        parent_index = find_a_segment_to_dissolve_in(segments[seg])
        if parent_index is None:
            print('parent_index is None:', segments[seg])
            continue
        parent: list[tuple[int, int]] = segments[status[parent_index[0], parent_index[1]]]
        parent.extend(segments[seg])
        segments.pop(seg)
print('Dissolution time:', datetime.now() - dissolution_time)
print('Segmentation time:', datetime.now() - segmentation_time)

# evaluate the segments
segments.sort(key=lambda s: len(s), reverse=True)
arr = cv2.cvtColor(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB), cv2.COLOR_RGB2HSV)
for big_sgm in range(25):  # colour the biggest ones
    for px in segments[big_sgm]:
        arr[px[0], px[1]] = 5 + (10 * (big_sgm + 1)), 255, 255
for seg in range(len(segments)):  # show the persisting small segments
    if len(segments[seg]) < min_seg:
        for px in segments[seg]:
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
