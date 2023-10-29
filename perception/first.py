from datetime import datetime

from storage.sf2_global import read_frames_file_with_ranges
from storage.shape_2 import Shape

# We may achieve Object Tracking via one (or both) of these methods:
# 1. first via Proximity: (more effort)
#     which looks for nearest shapes in a succeeding frame and requires the "Position In Frame" index.
#     this shall check details too.
#     Problem: objects may move fast.
# 2. first via Details: (CHOSEN)
#     which looks for nearest shapes in the whole short-term memory (Volatile Indices).
#     Problem: similar/equal objects may be numerous.
#         Solution: look for the nearest similar object via their proximity.

# load columns A and B for tracking their shapes
loading_time = datetime.now()
frames: dict[int, range] = read_frames_file_with_ranges()
frame_names = list(frames.keys())
a: dict[int, Shape] = {}
b: dict[int, Shape] = {}
i = 0
for sid in frames[frame_names[0]]:
    a[sid] = Shape(str(sid))
    print(a[sid].m)
    i += 1
for sid in frames[frame_names[1]]:
    b[sid] = Shape(str(sid))
    print(b[sid].m)
    i += 1
print('Loading time:', datetime.now() - loading_time)

# TODO IDENTIFY/TRACK SHAPES

# for fid, rng in read_frames_file_with_ranges().items():
#    print('Frame', fid, ':')
#    pif: list[tuple[int, int]] = read_pif_index(fid)
#    i = 0
#    for sid in rng:
#        print(sid, ':', pif[i])
#        i += 1
