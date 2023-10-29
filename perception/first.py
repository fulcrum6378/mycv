from datetime import datetime

from config import r_radius, u_radius, v_radius, y_radius
from storage.sf2_global import read_frames_file_with_ranges
from storage.shape_2 import Shape
from storage.vi1_global import VolatileIndex

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
ax: VolatileIndex = VolatileIndex()
i = 0
for sid in frames[frame_names[0]]:
    sh = Shape(str(sid))
    a[sid] = sh
    if sh.m[0] not in ax.yi: ax.yi[sh.m[0]] = set()
    ax.yi[sh.m[0]].add(sid)
    if sh.m[1] not in ax.ui: ax.ui[sh.m[1]] = set()
    ax.ui[sh.m[1]].add(sid)
    if sh.m[2] not in ax.vi: ax.vi[sh.m[2]] = set()
    ax.vi[sh.m[2]].add(sid)
    if sh.r not in ax.ri: ax.ri[sh.r] = set()
    ax.ri[sh.r].add(sid)
    i += 1
for sid in frames[frame_names[1]]:
    b[sid] = Shape(str(sid))
    i += 1
print('Loading time:', datetime.now() - loading_time)

# Saving and reloading shapes in VisualSTM in UNNECESSARY! They can be directly passed to Perception for analysis.
# But they must certainly be indexed before, BUT what if we first put them there and then save them?
# Should we search a shape in the whole STM or just the previous one?
# VisualSTM MIGHT be deprecated in its entirety then!!! (at least the indexes might be removed but not the /shapes/)

# iterate (ALWAYS FIRST) on column B and for each of them, iterate on column A for their similar shapes
for sid, sh_b in b.items():
    for sid_a, sh_a in b.items():
        pass

# for fid, rng in read_frames_file_with_ranges().items():
#    print('Frame', fid, ':')
#    pif: list[tuple[int, int]] = read_pif_index(fid)
#    i = 0
#    for sid in rng:
#        print(sid, ':', pif[i])
#        i += 1
