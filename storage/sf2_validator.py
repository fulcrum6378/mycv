from sf2_global import *

# 1. Read all indexes and see if no duplicate items are found

f: dict[int, set[int]] = {}
for f_ in sorted(os.listdir(dir_frame), key=sk):
    l_ = read_sequence_file(dir_frame, f_)
    s_ = set(l_)
    dif = abs(len(l_) - len(s_))
    if dif != 0: print("Found {0} duplicate items in Frames!".format(dif))
    f[int(f_)] = s_

y: dict[int, set[int]] = {}
for y_ in sorted(os.listdir(dir_y), key=sk):
    l_ = read_sequence_file(dir_y, y_)
    s_ = set(l_)
    dif = abs(len(l_) - len(s_))
    if dif != 0: print("Found {0} duplicate items in Y!".format(dif))
    y[int(y_)] = s_

u: dict[int, set[int]] = {}
for u_ in sorted(os.listdir(dir_u), key=sk):
    l_ = read_sequence_file(dir_u, u_)
    s_ = set(l_)
    dif = abs(len(l_) - len(s_))
    if dif != 0: print("Found {0} duplicate items in U!".format(dif))
    u[int(u_)] = s_

v: dict[int, set[int]] = {}
for v_ in sorted(os.listdir(dir_v), key=sk):
    l_ = read_sequence_file(dir_v, v_)
    s_ = set(l_)
    dif = abs(len(l_) - len(s_))
    if dif != 0: print("Found {0} duplicate items in V!".format(dif))
    v[int(v_)] = s_

r: dict[int, set[int]] = {}
for r_ in sorted(os.listdir(dir_ratio), key=sk):
    l_ = read_sequence_file(dir_ratio, r_)
    s_ = set(l_)
    dif = abs(len(l_) - len(s_))
    if dif != 0: print("Found {0} duplicate items in Ratio!".format(dif))
    r[int(r_)] = s_

del f_, y_, u_, v_, r_, l_, s_, dif

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
del sh, sh_id

# 3. Check if the indexes contain no unavailable shape

for f_ in f_keys:
    if len(f[f_]) != 0:
        for sid in f[f_]:
            print("Index Frames contains an unavailable shape {0}!".format(sid))
for y_ in y_keys:
    if len(y[y_]) != 0:
        for sid in y[y_]:
            print("Index Y contains an unavailable shape {0}!".format(sid))
for u_ in u_keys:
    if len(u[u_]) != 0:
        for sid in u[u_]:
            print("Index U contains an unavailable shape {0}!".format(sid))
for v_ in v_keys:
    if len(v[v_]) != 0:
        for sid in v[v_]:
            print("Index V contains an unavailable shape {0}!".format(sid))
for r_ in r_keys:
    if len(r[r_]) != 0:
        for sid in r[r_]:
            print("Index Ratio contains an unavailable shape {0}!".format(sid))
