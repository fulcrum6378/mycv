from sf2_global import *

print('Frame:')
for f in sorted(os.listdir(dir_frame), key=sk):
    print(f, ':', read_sequence_file(dir_frame, f))

print('\nY:')
for y in sorted(os.listdir(dir_y), key=sk):
    print(y, ':', read_sequence_file(dir_y, y))

print('\nU:')
for u in sorted(os.listdir(dir_u), key=sk):
    print(u, ':', read_sequence_file(dir_u, u))

print('\nV:')
for v in sorted(os.listdir(dir_v), key=sk):
    print(v, ':', read_sequence_file(dir_v, v))

print('\nRatio:')
for r in sorted(os.listdir(dir_ratio), key=sk):
    print(r, ':', read_sequence_file(dir_ratio, r))
