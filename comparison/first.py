import os
import struct
from datetime import datetime

from config import subject

# prepare the input folders
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_shapes = os.path.join(input_dir, 'ratio'), os.path.join(input_dir, 'shapes')

# load the shape
loading_time = datetime.now()
shf_path = os.path.join(dir_shapes, str(subject))
with open(shf_path, 'rb') as shf:
    y: int = struct.unpack('>B', shf.read(1))[0]
    u: int = struct.unpack('>B', shf.read(1))[0]
    v: int = struct.unpack('>B', shf.read(1))[0]
    w: int = struct.unpack('>H', shf.read(2))[0]
    h: int = struct.unpack('>H', shf.read(2))[0]
    path: list[tuple[float, float]] = []
    for b in range(7, os.path.getsize(shf_path), 8):
        path.append((
            struct.unpack('>f', shf.read(4))[0], struct.unpack('>f', shf.read(4))[0]
        ))
print('Loading time:', datetime.now() - loading_time)

# TODO find candidates

print('Colour:', y, u, v)
print('Dimensions:', w, h, w / h)
# print('Path:', path)

# 2  : (74 119 171), 1.959016393442623
# 12 : (75 119 172), 1.9833333333333334
# 21 : (71 119 169), 2.0166666666666666
# 32 : (72 119 170), 2.045325779036827

