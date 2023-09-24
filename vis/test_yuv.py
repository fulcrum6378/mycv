import struct

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import dim

arr: list[list[list[int]]] = []

with open('vis/test.yuv', 'rb') as f:
    for y in range(dim):
        x_: list[list[int]] = []
        for x in range(dim):
            x_.append([struct.unpack('>B', f.read(1))[0],
                       struct.unpack('>B', f.read(1))[0],
                       struct.unpack('>B', f.read(1))[0]])
        arr.append(x_)

plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YCrCb2RGB))
plot.show()
