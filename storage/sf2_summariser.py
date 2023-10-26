from storage.sf2_global import *

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
for r in sorted(os.listdir(dir_r), key=sk):
    print(r, ':', read_sequence_file(dir_r, r))

print('\nFrame:')
for fid, rng in read_frames_file().items():
    print(fid, ':', rng.start, 'until', rng.stop - 1)

print('\nNumbers:')
print(read_numbers_file())
