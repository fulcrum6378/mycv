import json
import os
import struct
from datetime import datetime

from config import bitmap, shape_path_type
from storage.vi1_global import vi_read, VolatileIndex

# make sure it's not triggered unintentionally
if input('Are you sure? (any/n): ') == 'n': quit()

# prepare the output folder
output_dir = os.path.join('storage', 'output')
dir_shapes = os.path.join(output_dir, 'shapes')
if not os.path.isdir(dir_shapes): os.mkdir(dir_shapes)

# determine the next shape ID and frame ID
next_id = len(os.listdir(dir_shapes))
first_id = next_id
f = int(bitmap)

# load the Volatile Index if exists
index_path = os.path.join(output_dir, 'volatile_index_1.pickle')
if os.path.isfile(index_path):
    x: VolatileIndex = vi_read(index_path)
else:
    x: VolatileIndex = VolatileIndex()

# load data from the /tracing/ section
load_and_save_time = datetime.now()
input_dir, ext_json = os.path.join('tracing', 'output', bitmap), '.json'
for o in sorted(os.listdir(input_dir), key=lambda fn: int(fn[:-5])):
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    y, u, v = seg['mean']
    w, h = seg['dimensions']
    cx, cy = seg['centre']
    r = int((float(w) / float(h)) * 10.0)

    # write to shape file
    with open(os.path.join(dir_shapes, str(next_id)), 'wb') as shf:
        shf.write(struct.pack('B', y) + struct.pack('B', u) + struct.pack('B', v))
        shf.write(struct.pack('<H', r))
        shf.write(struct.pack('<Q', f))
        shf.write(struct.pack('<H', w))
        shf.write(struct.pack('<H', h))
        shf.write(struct.pack('<H', cx))
        shf.write(struct.pack('<H', cy))
        for point in seg['path']:
            shf.write(struct.pack(shape_path_type, point[0]) + struct.pack(shape_path_type, point[1]))

    # write to Volatile Indices
    if y not in x.yi: x.yi[y] = set()
    x.yi[y].add(next_id)
    if u not in x.ui: x.ui[u] = set()
    x.ui[u].add(next_id)
    if v not in x.vi: x.vi[v] = set()
    x.vi[v].add(next_id)
    if r not in x.ri: x.ri[r] = set()
    x.ri[r].add(next_id)
    if f not in x.pifi: x.pifi[f] = list()
    x.pifi[f].append((cx, cy))

    next_id += 1
x.fi[f] = first_id, next_id
print('Loading + saving time:', datetime.now() - load_and_save_time)
# Note: the time delta above includes reading from JSON files too!

x.vi_write(index_path)
