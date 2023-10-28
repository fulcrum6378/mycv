import json
import os
import struct
from datetime import datetime

from config import bitmap, shape_path_type

# make sure it's not triggered unintentionally
if input('Are you sure? (any/n): ') == 'n': quit()

# prepare the output folders
output_dir = os.path.join('storage', 'output')
dir_shapes = os.path.join(output_dir, 'shapes')
dir_y, dir_u, dir_v, dir_r, dir_pif = os.path.join(output_dir, 'y'), os.path.join(output_dir, 'u'), \
    os.path.join(output_dir, 'v'), os.path.join(output_dir, 'r'), os.path.join(output_dir, 'pif')
for folder in [dir_shapes, dir_y, dir_u, dir_v, dir_r, dir_pif]:
    if not os.path.isdir(folder): os.mkdir(folder)

# determine the next shape ID
next_id = len(os.listdir(dir_shapes))
first_id = next_id
f = int(bitmap)

# load data from the /tracing/ section
load_and_save_time = datetime.now()
pif = open(os.path.join(dir_pif, str(f)), 'wb')
input_dir, ext_json = os.path.join('tracing', 'output', bitmap), '.json'
for o in sorted(os.listdir(input_dir), key=lambda fn: int(fn[:-5])):
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    y, u, v = seg['mean']
    w, h = seg['dimensions']
    cx, cy = seg['centre']
    ratio = int((float(w) / float(h)) * 10.0)

    # write to shape file
    with open(os.path.join(dir_shapes, str(next_id)), 'wb') as shf:
        shf.write(struct.pack('B', y) + struct.pack('B', u) + struct.pack('B', v))
        shf.write(struct.pack('<H', ratio))
        shf.write(struct.pack('<Q', f))
        shf.write(struct.pack('<H', w))
        shf.write(struct.pack('<H', h))
        shf.write(struct.pack('<H', cx))
        shf.write(struct.pack('<H', cy))
        for point in seg['path']:
            shf.write(struct.pack(shape_path_type, point[0]) + struct.pack(shape_path_type, point[1]))

    # write to Sequence Files
    with open(os.path.join(dir_y, str(y)), 'ab') as y_f:
        y_f.write(struct.pack('<H', next_id))
    with open(os.path.join(dir_u, str(u)), 'ab') as u_f:
        u_f.write(struct.pack('<H', next_id))
    with open(os.path.join(dir_v, str(v)), 'ab') as v_f:
        v_f.write(struct.pack('<H', next_id))
    with open(os.path.join(dir_r, str(ratio)), 'ab') as rtf:
        rtf.write(struct.pack('<H', next_id))

    # write to index "Position In Frame"
    pif.write(struct.pack('<H', cx))
    pif.write(struct.pack('<H', cy))

    next_id += 1
pif.close()

# index this frame (not suited for LTM)
with open(os.path.join(output_dir, 'frames'), 'ab') as fif:
    fif.write(struct.pack('<Q', f))
    fif.write(struct.pack('<H', first_id))
    fif.write(struct.pack('<H', next_id))

print('Loading + saving time:', datetime.now() - load_and_save_time)
# Note: the time delta above includes reading from JSON files too!
