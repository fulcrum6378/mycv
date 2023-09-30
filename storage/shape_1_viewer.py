import os
import struct

import cv2
import matplotlib.pyplot as plot
import numpy as np

# NOTE: ARM64 IS LITTLE-ENDIAN!!!

# prepare the input folders
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_shapes = os.path.join(input_dir, 'r'), os.path.join(input_dir, 'shapes')

# load the subject shape
shf_path = os.path.join(dir_shapes, input('Enter the ID of the shape:\n'))
with open(shf_path, 'rb') as shf:
    y: int = struct.unpack('B', shf.read(1))[0]
    u: int = struct.unpack('B', shf.read(1))[0]
    v: int = struct.unpack('B', shf.read(1))[0]
    w: int = struct.unpack('<H', shf.read(2))[0]
    h: int = struct.unpack('<H', shf.read(2))[0]
    # rt = int((w / h) * 10)
    print(y, u, v, w, h)
    # quit()
    path: list[tuple[float, float]] = []
    for b in range(7, os.path.getsize(shf_path), 8):
        path.append((
            struct.unpack('<f', shf.read(4))[0], struct.unpack('<f', shf.read(4))[0]
        ))

# draw the segment into the cadre and display it
arr: list[list[list[int]]] = []
for y in range(100):
    xes: list[list[int]] = []
    for x in range(100):
        xes.append([y, u, v])
    arr.append(xes)
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
plot.show()
