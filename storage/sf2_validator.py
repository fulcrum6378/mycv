from storage.sf2_global import *
from storage.shape_2 import *

# 0. Check if things exist

if not os.path.isdir(dir_shapes):
    print('Shapes directory is missing!')
    quit()
if not os.path.isdir(dir_y):
    print('Y indices are missing!')
    quit()
if not os.path.isdir(dir_u):
    print('U indices are missing!')
    quit()
if not os.path.isdir(dir_v):
    print('V indices are missing!')
    quit()
if not os.path.isdir(dir_r):
    print('Ratio indices are missing!')
    quit()
if not os.path.isfile(frames_file):
    print('Frames index is missing!')
    quit()

# 1. Read all indexes and see if no duplicate items are found

f: dict[int, set[int]] = {}
s_: set[int] = set()
prev_len = 0
for fid, rng in read_frames_file_with_ranges().items():
    l_ = list(rng)
    s_.update(l_)
    dif = abs((len(s_) - prev_len) - len(l_))
    if dif != 0: print("Found {0} duplicate items in Frames:{1}!".format(dif, fid))
    prev_len += len(l_)
    f[int(fid)] = s_

y: dict[int, set[int]] = {}
s_ = set()
prev_len = 0
for y_ in sorted(os.listdir(dir_y), key=sk):
    l_ = read_sequence_file(dir_y, y_)
    s_.update(l_)
    dif = abs((len(s_) - prev_len) - len(l_))
    if dif != 0: print("Found {0} duplicate items in Y:{1}!".format(dif, y_))
    prev_len += len(l_)
    y[int(y_)] = s_

u: dict[int, set[int]] = {}
s_ = set()
prev_len = 0
for u_ in sorted(os.listdir(dir_u), key=sk):
    l_ = read_sequence_file(dir_u, u_)
    s_.update(l_)
    dif = abs((len(s_) - prev_len) - len(l_))
    if dif != 0: print("Found {0} duplicate items in U:{1}!".format(dif, u_))
    prev_len += len(l_)
    u[int(u_)] = s_

v: dict[int, set[int]] = {}
s_ = set()
prev_len = 0
for v_ in sorted(os.listdir(dir_v), key=sk):
    l_ = read_sequence_file(dir_v, v_)
    s_.update(l_)
    dif = abs((len(s_) - prev_len) - len(l_))
    if dif != 0: print("Found {0} duplicate items in V:{1}!".format(dif, v_))
    prev_len += len(l_)
    v[int(v_)] = s_

r: dict[int, set[int]] = {}
s_ = set()
prev_len = 0
for r_ in sorted(os.listdir(dir_r), key=sk):
    l_ = read_sequence_file(dir_r, r_)
    s_.update(l_)
    dif = abs((len(s_) - prev_len) - len(l_))
    if dif != 0: print("Found {0} duplicate items in Ratio:{1}!".format(dif, r_))
    prev_len += len(l_)
    r[int(r_)] = s_

del fid, rng, y_, u_, v_, r_, l_, s_, dif

# 2. Check if indexes include all available shapes

f_keys = f.keys()
y_keys = y.keys()
u_keys = u.keys()
v_keys = v.keys()
r_keys = r.keys()
for sid in sorted(os.listdir(dir_shapes), key=sk):
    sh = Shape(sid)
    sh_id = int(sid)
    if sh.frame in f_keys and sh_id in f[sh.frame]:
        f[sh.frame].remove(sh_id)
    else:
        print("Shape {0} is not indexed in Frames!".format(sid))
    if sh.m[0] in y_keys and sh_id in y[sh.m[0]]:
        y[sh.m[0]].remove(sh_id)
    else:
        print("Shape {0} is not indexed in Y!".format(sid))
    if sh.m[1] in u_keys and sh_id in u[sh.m[1]]:
        u[sh.m[1]].remove(sh_id)
    else:
        print("Shape {0} is not indexed in U!".format(sid))
    if sh.m[2] in v_keys and sh_id in v[sh.m[2]]:
        v[sh.m[2]].remove(sh_id)
    else:
        print("Shape {0} is not indexed in V!".format(sid))
    if sh.r in r_keys and sh_id in r[sh.r]:
        r[sh.r].remove(sh_id)
    else:
        print("Shape {0} is not indexed in Ratio!".format(sid))
else:
    del sh, sh_id

# 3. Check if the indexes contain no unavailable shape

ukf: list[tuple[int, int]] = []
for f_ in f_keys:
    if len(f[f_]) != 0:
        for sid in sorted(f[f_]):
            ukf.append((sid, f_))
for sid, f_ in ukf:
    print("Index Frames contains an unavailable shape {0}!".format(f_))

uky: list[tuple[int, int]] = []
for y_ in y_keys:
    if len(y[y_]) != 0:
        for sid in sorted(y[y_]):
            uky.append((sid, y_))
for sid, y_ in sorted(uky):
    print("Index Y contains an unavailable shape {0} of value {1}!".format(sid, y_))

uku: list[tuple[int, int]] = []
for u_ in u_keys:
    if len(u[u_]) != 0:
        for sid in sorted(u[u_]):
            uku.append((sid, u_))
for sid, u_ in sorted(uku):
    print("Index U contains an unavailable shape {0} of value {1}!".format(sid, u_))

ukv: list[tuple[int, int]] = []
for v_ in v_keys:
    if len(v[v_]) != 0:
        for sid in sorted(v[v_]):
            ukv.append((sid, v_))
for sid, v_ in sorted(ukv):
    print("Index V contains an unavailable shape {0} of value {1}!".format(sid, v_))

ukr: list[tuple[int, int]] = []
for r_ in r_keys:
    if len(r[r_]) != 0:
        for sid in sorted(r[r_]):
            ukr.append((sid, r_))
for sid, r_ in sorted(ukr):
    print("Index Ratio contains an unavailable shape {0} of value {1}!".format(sid, r_))
