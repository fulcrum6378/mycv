import os
import struct
from datetime import datetime

from config import rt_radius, subject, u_radius, v_radius, y_radius

# prepare the input folders
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_shapes = os.path.join(input_dir, 'ratio'), os.path.join(input_dir, 'shapes')

# load the subject shape
loading_time = datetime.now()
shf_path = os.path.join(dir_shapes, str(subject))
with open(shf_path, 'rb') as shf:
    y: int = struct.unpack('>B', shf.read(1))[0]
    u: int = struct.unpack('>B', shf.read(1))[0]
    v: int = struct.unpack('>B', shf.read(1))[0]
    w: int = struct.unpack('>H', shf.read(2))[0]
    h: int = struct.unpack('>H', shf.read(2))[0]
    rt = int((w / h) * 10)
    path: list[tuple[float, float]] = []
    for b in range(7, os.path.getsize(shf_path), 8):
        path.append((
            struct.unpack('>f', shf.read(4))[0], struct.unpack('>f', shf.read(4))[0]
        ))
print('Loading time:', datetime.now() - loading_time)

print('Colour:', y, u, v, '; Dimensions:', w, h, '(', rt / 10, ')')
# 2  : (74 119 171), 1.959016393442623
# 12 : (75 119 172), 1.9833333333333334
# 21 : (71 119 169), 2.0166666666666666
# 32 : (72 119 170), 2.045325779036827
# print('Path:', path)

# collect shapes with close features
searching_time = datetime.now()
a_y, a_u, a_v, a_rt = list(), list(), list(), list()
for y_ in range(y - y_radius, y + y_radius):
    f_path = os.path.join(dir_y, str(y_))
    if not os.path.isfile(f_path): continue
    with open(f_path, 'rb') as y_f:
        for _ in range(0, os.path.getsize(f_path), 8):
            a_y.append(struct.unpack('>Q', y_f.read(8))[0])
for u_ in range(u - u_radius, u + u_radius):
    f_path = os.path.join(dir_u, str(u_))
    if not os.path.isfile(f_path): continue
    with open(f_path, 'rb') as u_f:
        for _ in range(0, os.path.getsize(f_path), 8):
            a_u.append(struct.unpack('>Q', u_f.read(8))[0])
for v_ in range(v - v_radius, v + v_radius):
    f_path = os.path.join(dir_v, str(v_))
    if not os.path.isfile(f_path): continue
    with open(f_path, 'rb') as v_f:
        for _ in range(0, os.path.getsize(f_path), 8):
            a_v.append(struct.unpack('>Q', v_f.read(8))[0])
for rt_ in range(rt - rt_radius, rt + rt_radius):
    f_path = os.path.join(dir_ratio, str(rt_))
    if not os.path.isfile(f_path): continue
    with open(f_path, 'rb') as rtf:
        for _ in range(0, os.path.getsize(f_path), 12):
            # a_rt.append((
            #    struct.unpack('>Q', rtf.read(8))[0], struct.unpack('>f', rtf.read(4))[0]
            # ))
            a_rt.append(struct.unpack('>Q', rtf.read(8))[0])
            rtf.seek(4, os.SEEK_CUR)

# exclude candidates
candidates: list[int] = []
for sid in a_u:
    if sid in a_y and sid in a_v and sid in a_rt:
        candidates.append(sid)
del a_y, a_u, a_v, a_rt
print('Searching time:', datetime.now() - searching_time)
print('Candidates:', candidates)  # [2, 12, 21, 32]

# TODO advanced comparison of the candidates
