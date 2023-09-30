import os
import struct

input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio = os.path.join(input_dir, 'ratio')
sk = lambda fn: int(fn)

print('Y:')
for y_ in sorted(os.listdir(dir_y), key=sk):
    f_path = os.path.join(dir_y, str(y_))
    with open(f_path, 'rb') as y_f:
        a_y: list[int] = []
        for bid in range(0, os.path.getsize(f_path), 8):
            a_y.append(struct.unpack('<Q', y_f.read(8))[0])
        print(y_, ':', a_y)
print()
print('U:')
for u_ in sorted(os.listdir(dir_u), key=sk):
    f_path = os.path.join(dir_u, str(u_))
    with open(f_path, 'rb') as u_f:
        a_u: list[int] = []
        for bid in range(0, os.path.getsize(f_path), 8):
            a_u.append(struct.unpack('<Q', u_f.read(8))[0])
        print(u_, ':', a_u)
print()
print('V:')
for v_ in sorted(os.listdir(dir_v), key=sk):
    f_path = os.path.join(dir_v, str(v_))
    with open(f_path, 'rb') as v_f:
        a_v: list[int] = []
        for bid in range(0, os.path.getsize(f_path), 8):
            a_v.append(struct.unpack('<Q', v_f.read(8))[0])
        print(v_, ':', a_v)
print()
print('RATIO:')
for rt_ in sorted(os.listdir(dir_ratio), key=sk):
    f_path = os.path.join(dir_ratio, str(rt_))
    with open(f_path, 'rb') as rtf:
        a_rt: list[tuple[int, float]] = []
        for bid in range(0, os.path.getsize(f_path), 12):
            a_rt.append((
                struct.unpack('<Q', rtf.read(8))[0], struct.unpack('<f', rtf.read(4))[0]
            ))
        print(rt_, ':', a_rt)
