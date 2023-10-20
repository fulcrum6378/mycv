import os
from datetime import datetime

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap2, bitmap_folder, dim
from segmentation.region_growing_4 import arr, compare_colours, segments, status

print('--------RESEGMENTATION--------')

# index previous segments (not required for C++ as it has implemented `s_index`)
s_index: dict[int, int] = {}  # id, offset in `segments`
for seg in range(len(segments)):
    s_index[segments[seg].id] = seg
print('All Segments were indexed.')

# read the SECOND image
loading_time = datetime.now()
buf: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap2 + '.bmp')),
                               cv2.COLOR_BGR2YUV)
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
print('+ Loading time:', datetime.now() - loading_time)

# TODO Find Segments for changed pixels

# Render differences
render_time = datetime.now()
plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
print('Rendering time:', datetime.now() - render_time)
plot.show()
