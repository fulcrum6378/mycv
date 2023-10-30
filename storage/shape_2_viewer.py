import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import shape_path_max
from storage.shape_2 import *

while True:
    # load the subject shape
    inp = input('Enter the ID of the shape: ')
    try:
        sh = Shape(inp)
    except:
        if inp == '':
            break
        else:
            print('Invalid shape ID!')
            continue
    print('Frame', sh.frame, ':', sh.m, sh.w, 'x', sh.h, '(', sh.r, ')')
    print(len(sh.path), 'points; centre:', sh.cx, 'x', sh.cy)

    # draw the segment into the cadre and display it
    sh.w *= 1.0 - (0.25 * (3 - shape_path_bytes))
    sh.h *= 1.0 - (0.25 * (3 - shape_path_bytes))
    arr = np.repeat(np.repeat(np.array([[sh.m]]), sh.w + 1, 1), sh.h + 1, 0)
    for p in sh.path:
        arr[int(p[1] / (shape_path_max / sh.h)), int(p[0] / (shape_path_max / sh.w))] = \
            0, 128, 128  # m[0], m[1], m[2]
    plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
    plot.show()
