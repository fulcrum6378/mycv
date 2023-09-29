import json
import os
import struct
from datetime import datetime

from config import bitmap

# make sure it's not trigger unintentionally
if input('Are you sure? (y/any): ') != 'y': quit()

# prepare the output folders
output_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(output_dir, 'y'), os.path.join(output_dir, 'u'), os.path.join(output_dir, 'v')
dir_ratio, dir_shapes = os.path.join(output_dir, 'r'), os.path.join(output_dir, 'shapes')
for folder in [dir_y, dir_u, dir_v, dir_ratio, dir_shapes]:
    if not os.path.isdir(folder): os.mkdir(folder)

# determine the next shape ID
next_id = len(os.listdir(dir_shapes))

# Shape File (structure of bytes):
# 3 | average colour (YUV)
# 2 | width
# 2 | height
# N | path points in double 32-bit (both 64-bit)


# load data from the /tracing/ section
load_and_save_time = datetime.now()
input_dir, ext_json = os.path.join('tracing', 'output', bitmap), '.json'
for o in sorted(os.listdir(input_dir), key=lambda fn: int(fn[:-5])):
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    y, u, v = seg['mean']
    w, h = seg['dimensions']
    ratio = w / h

    # write to shape file
    with open(os.path.join(dir_shapes, str(next_id)), 'wb') as shf:
        shf.write(struct.pack('>B', y) + struct.pack('>B', u) + struct.pack('>B', v))
        shf.write(struct.pack('>H', w))
        shf.write(struct.pack('>H', h))
        for point in seg['path']:
            shf.write(struct.pack('>f', point[0]) + struct.pack('>f', point[1]))

    # write to sequence files
    with open(os.path.join(dir_y, str(y)), 'ab') as y_f:
        y_f.write(struct.pack('>H', next_id))
    with open(os.path.join(dir_u, str(u)), 'ab') as u_f:
        u_f.write(struct.pack('>H', next_id))
    with open(os.path.join(dir_v, str(v)), 'ab') as v_f:
        v_f.write(struct.pack('>H', next_id))
    with open(os.path.join(dir_ratio, str(int(ratio * 10))), 'ab') as rtf:
        rtf.write(struct.pack('>H', next_id))

    next_id += 1
print('Loading + saving time:', datetime.now() - load_and_save_time)
print('Note: the time delta above includes reading from JSON files too!')
