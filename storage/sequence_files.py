import json
import os
import struct

# prepare output folders
output_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(output_dir, 'y'), os.path.join(output_dir, 'u'), os.path.join(output_dir, 'v')
dir_ratio, dir_shapes = os.path.join(output_dir, 'ratio'), os.path.join(output_dir, 'shapes')
for folder in [dir_y, dir_u, dir_v, dir_ratio, dir_shapes]:
    if not os.path.isdir(folder): os.mkdir(folder)
next_id = len(os.listdir(dir_shapes))
# The last ID should be read from a config file later. After reaching the maximum 64-bit length,
# it can restart from 0, while having the previous shapes forgotten.

# Shape File (structure of bytes):
# 3 | average colour (YUV)
# 2 | width
# 2 | height
# N | path points in double 32-bit (both 64-bit)

# load data from the /tracing/ section
input_dir, ext_json = os.path.join('tracing', 'output'), '.json'
for o in sorted(os.listdir(input_dir)[1:], key=lambda fn: int(fn[:-5])):
    seg = json.loads(open(os.path.join(input_dir, o), 'r').read())
    w, h = seg['dimensions']

    # write the shape file
    with open(os.path.join(dir_shapes, str(next_id)), 'wb') as shf:
        shf.write(
            struct.pack('>B', seg['mean'][0]) +
            struct.pack('>B', seg['mean'][1]) +
            struct.pack('>B', seg['mean'][2])
        )
        shf.write(struct.pack('>H', w))
        shf.write(struct.pack('>H', h))
        for point in seg['path']:
            shf.write(struct.pack('>f', point[0]) + struct.pack('>f', point[1]))

    # write to the
    w / h
    next_id += 1
