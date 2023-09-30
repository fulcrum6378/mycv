import os
import struct

import cv2
import matplotlib.pyplot as plot
import numpy as np

# prepare the input folders
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_shapes = os.path.join(input_dir, 'r'), os.path.join(input_dir, 'shapes')

# load the subject shape
shf_path = os.path.join(dir_shapes, input('Enter the ID of the shape: '))
with open(shf_path, 'rb') as shf:
    y: int = struct.unpack('B', shf.read(1))[0]
    u: int = struct.unpack('B', shf.read(1))[0]
    v: int = struct.unpack('B', shf.read(1))[0]
    w: int = struct.unpack('<H', shf.read(2))[0]
    h: int = struct.unpack('<H', shf.read(2))[0]
    # NOTE: ARM64 IS LITTLE-ENDIAN!!!
    path: list[tuple[float, float]] = []
    for b in range(7, os.path.getsize(shf_path), 8):
        path.append((
            struct.unpack('<f', shf.read(4))[0], struct.unpack('<f', shf.read(4))[0]
        ))
print(y, u, v, w, h)
print("Points:", len(path))

# draw the segment into the cadre and display it
# arr = np.repeat([np.repeat(np.repeat([255], 3, 0), w, 0)], h, 0)
arr = np.repeat(255, h * w * 3).reshape(h, w, 3)
print(arr.shape)
m = cv2.cvtColor(np.array([[[y, u, v]]], dtype=np.uint8), cv2.COLOR_YUV2RGB)[0, 0]
for p in path:
    arr[int(p[1] / (100 / h)), int(p[0] / (100 / w))] = 0, 0, 0  # m[0], m[1], m[2]
    # TODO INCOMPLETE
plot.imshow(arr)
plot.show()
