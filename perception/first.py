from datetime import datetime
from math import sqrt
from typing import Optional

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
print('Loading and indexing time:', datetime.now() - loading_time)

# Saving and reloading shapes in VisualSTM in UNNECESSARY! They can be directly passed to Perception for analysis.
# But they must certainly be indexed before, BUT what if we first put them there and then save them?
# Should we search a shape in the whole STM or just the previous one?
# VisualSTM MIGHT be deprecated in its entirety then!!! (at least the indexes might be removed but not the /shapes/)

# search through Volatile Indices and choose the most proximate candidate based on their position
tracking_time = datetime.now()
diff: dict[int, list] = {}  # 0=>sid_a, 1=>distance, 2=>dif_w, 3=>dif_h, 4=>dif_y, 5=>dif_u, 6=>dif_v, 7=>dif_r
not_tracked: int = 0
a_y, a_u, a_v, a_r = list(), list(), list(), list()
# candidates: dict[int, float] = {}
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
    nearest_dist: Optional[float] = None
    best: int = -1
    for can in a_y:
        if can in a_u and can in a_v and can in a_r:
            dist = sqrt(pow(s.cx - a[can].cx, 2) + pow(s.cy - a[can].cy, 2))
            # candidates[can] = dist
            if nearest_dist is None:
                nearest_dist = dist
                best = can
            elif dist < nearest_dist:
                nearest_dist = dist
                best = can
    a_y.clear()
    a_u.clear()
    a_v.clear()
    a_r.clear()
    if best != -1:
        diff[sid] = [best, int(nearest_dist)]
    else:
        not_tracked += 1
    # candidates.clear()
print(not_tracked, 'shapes could not be tracked!')
print('+ Tracking time:', datetime.now() - tracking_time)

# We could also create a scoring system which includes both proximity and details,
# but we better avoid that for both accuracy and performance.

# Now see which details have changed
other_diff_time = datetime.now()
for sid in diff.keys():
    s_a = a[diff[sid][0]]
    s_b = b[sid]
    diff[sid].append(s_a.w - s_b.w)
    diff[sid].append(s_a.h - s_b.h)
    diff[sid].append(s_a.m[0] - s_b.m[0])
    diff[sid].append(s_a.m[1] - s_b.m[1])
    diff[sid].append(s_a.m[2] - s_b.m[2])
    diff[sid].append(s_a.r - s_b.r)
    print(sid - 50, diff[sid])
print('+ Measuring other differences:', datetime.now() - other_diff_time)
