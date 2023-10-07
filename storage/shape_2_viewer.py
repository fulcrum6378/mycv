import os
import struct

import cv2
import matplotlib.pyplot as plot
import numpy as np

# prepare the input folders
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_frame = os.path.join(input_dir, 'r'), os.path.join(input_dir, 'f')
dir_shapes = os.path.join(input_dir, 'shapes')

# load the subject shape
shf_path = os.path.join(dir_shapes, input('Enter the ID of the shape: '))
with open(shf_path, 'rb') as shf:  # NOTE: ARM64 IS LITTLE-ENDIAN!!!
    y: int = struct.unpack('B', shf.read(1))[0]
    u: int = struct.unpack('B', shf.read(1))[0]
    v: int = struct.unpack('B', shf.read(1))[0]
    r: int = struct.unpack('<H', shf.read(2))[0]
    f: int = struct.unpack('<Q', shf.read(8))[0]
    w: int = struct.unpack('<H', shf.read(2))[0]
    h: int = struct.unpack('<H', shf.read(2))[0]
    path: list[tuple[float, float]] = []
    for b in range(shf.tell(), os.path.getsize(shf_path), 8):
        path.append((
            struct.unpack('<f', shf.read(4))[0], struct.unpack('<f', shf.read(4))[0]
        ))
print('Frame', f, ':', '(', y, u, v, ')', w, 'x', h, '(', r, ')', '-', len(path), 'points')

# draw the segment into the cadre and display it
arr = np.repeat(np.repeat(np.array([[[y, u, v]]]), w, 1), h, 0)
for p in path:
    arr[int(p[1] / (100 / h)), int(p[0] / (100 / w))] = 0, 128, 128  # m[0], m[1], m[2]
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
plot.show()
