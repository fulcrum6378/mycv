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
    s = Shape(str(sid))
    a[sid] = s
    if s.m[0] not in ax.yi: ax.yi[s.m[0]] = set()
    ax.yi[s.m[0]].add(sid)
    if s.m[1] not in ax.ui: ax.ui[s.m[1]] = set()
    ax.ui[s.m[1]].add(sid)
    if s.m[2] not in ax.vi: ax.vi[s.m[2]] = set()
    ax.vi[s.m[2]].add(sid)
    if s.r not in ax.ri: ax.ri[s.r] = set()
    ax.ri[s.r].add(sid)
    i += 1
for sid in frames[frame_names[1]]:
    b[sid] = Shape(str(sid))
    i += 1
print('Loading time:', datetime.now() - loading_time)

# Saving and reloading shapes in VisualSTM in UNNECESSARY! They can be directly passed to Perception for analysis.
# But they must certainly be indexed before, BUT what if we first put them there and then save them?
# Should we search a shape in the whole STM or just the previous one?
# VisualSTM MIGHT be deprecated in its entirety then!!! (at least the indexes might be removed but not the /shapes/)

# search through Volatile Indices
searching_time = datetime.now()
a_y, a_u, a_v, a_r = list(), list(), list(), list()
candidates: list[int] = []
for sid, s in b.items():
    for y_ in range(s.m[0] - y_radius, s.m[0] + y_radius):
        if y_ not in ax.yi: continue
        a_y.extend(ax.yi[y_])
    for u_ in range(s.m[1] - u_radius, s.m[1] + u_radius):
        if u_ not in ax.ui: continue
        a_u.extend(ax.ui[u_])
    for v_ in range(s.m[2] - v_radius, s.m[2] + v_radius):
        if v_ not in ax.vi: continue
        a_v.extend(ax.vi[v_])
    for r_ in range(s.r - r_radius, s.r + r_radius):
        if r_ not in ax.ri: continue
        a_r.extend(ax.ri[r_])
    for can in a_y:
        if can in a_y and can in a_v and can in a_r:
            candidates.append(can)
    a_y.clear()
    a_u.clear()
    a_v.clear()
    a_r.clear()
    print('Candidates of', sid, ':', candidates)
    candidates.clear()
print('+ Searching time:', datetime.now() - searching_time)

# for fid, rng in read_frames_file_with_ranges().items():
#    print('Frame', fid, ':')
#    pif: list[tuple[int, int]] = read_pif_index(fid)
#    i = 0
#    for sid in rng:
#        print(sid, ':', pif[i])
#        i += 1
