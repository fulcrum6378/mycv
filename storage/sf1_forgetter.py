import os
import struct

# prepare the folders
output_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(output_dir, 'y'), os.path.join(output_dir, 'u'), os.path.join(output_dir, 'v')
dir_ratio, dir_shapes = os.path.join(output_dir, 'ratio'), os.path.join(output_dir, 'shapes')
dir_trash = os.path.join(output_dir, 'trash')
if not os.path.isdir(dir_trash): os.mkdir(dir_trash)

# what to forget?
forget_about: list[int] = []
for ssid in input('What to forget? (0,1,2,3): ').split(','):
    try:
        forget_about.append(int(ssid))
    except ValueError:
        print('Invalid ID:', ssid)
        quit()

# FIXME not efficient in forgetting a large number of shapes

for sid in forget_about:
    # open the shape file and read its details, then move it to the trash directory
    f_path = os.path.join(dir_shapes, str(sid))
    with open(f_path, 'rb') as shf:
        y: int = struct.unpack('B', shf.read(1))[0]
        u: int = struct.unpack('B', shf.read(1))[0]
        v: int = struct.unpack('B', shf.read(1))[0]
        rt = int((struct.unpack('<H', shf.read(2))[0] / struct.unpack('<H', shf.read(2))[0]) * 10)
    os.rename(f_path, os.path.join(dir_trash, str(sid)))

    # now delete its attributes from Sequence Files
    f_path = os.path.join(dir_y, str(y))
    f_size = os.path.getsize(f_path)
    with open(f_path, 'r+b') as y_f:
        a_y: list[int] = []
        for _ in range(0, f_size, 8):
            y_sid = struct.unpack('<Q', y_f.read(8))[0]
            if y_sid != sid: a_y.append(y_sid)
        if len(a_y) > 0:
            y_f.seek(0)
            y_f.truncate(f_size - 8)
            for y_sid in a_y:
                y_f.write(struct.pack('<Q', y_sid))
    if len(a_y) == 0: os.remove(f_path)
    del a_y

    f_path = os.path.join(dir_u, str(u))
    f_size = os.path.getsize(f_path)
    with open(f_path, 'r+b') as u_f:
        a_u: list[int] = []
        for _ in range(0, f_size, 8):
            u_sid = struct.unpack('<Q', u_f.read(8))[0]
            if u_sid != sid: a_u.append(u_sid)
        if len(a_u) > 0:
            u_f.seek(0)
            u_f.truncate(f_size - 8)
            for u_sid in a_u:
                u_f.write(struct.pack('<Q', u_sid))
    if len(a_u) == 0: os.remove(f_path)
    del a_u

    f_path = os.path.join(dir_v, str(v))
    f_size = os.path.getsize(f_path)
    with open(f_path, 'r+b') as v_f:
        a_v: list[int] = []
        for _ in range(0, f_size, 8):
            v_sid = struct.unpack('<Q', v_f.read(8))[0]
            if v_sid != sid: a_v.append(v_sid)
        if len(a_v) > 0:
            v_f.seek(0)
            v_f.truncate(f_size - 8)
            for v_sid in a_v:
                v_f.write(struct.pack('<Q', v_sid))
    if len(a_v) == 0: os.remove(f_path)
    del a_v

    f_path = os.path.join(dir_ratio, str(rt))
    f_size = os.path.getsize(f_path)
    with open(f_path, 'r+b') as rt_f:
        a_rt: list[tuple[int, float]] = []
        for _ in range(0, f_size, 12):
            rt_sh = (struct.unpack('<Q', rt_f.read(8))[0], struct.unpack('<f', rt_f.read(4))[0])
            if rt_sh[0] != sid: a_rt.append(rt_sh)
        a_rt.sort(key=lambda rt_: rt_[1])
        if len(a_rt) > 0:
            rt_f.seek(0)
            rt_f.truncate(f_size - 12)
            for rt_sh in a_rt:
                rt_f.write(struct.pack('<Q', rt_sh[0]) + struct.pack('<f', rt_sh[1]))
    if len(a_rt) == 0: os.remove(f_path)
    del a_rt
