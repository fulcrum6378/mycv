import os
import struct
from datetime import datetime

from config import subject

# we must find shapes similar to `subject`, which is a shape that we're trying to identify.

# load the shape
loading_time = datetime.now()
shf_path = os.path.join('storage', 'output', 'shapes', str(subject))
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

print('Colour:', y, u, v)
print('Dimensions:', w, h)
print('Path:', path)
