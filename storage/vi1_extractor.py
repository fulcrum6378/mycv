import os
import shutil
import struct

from storage.vi1_global import vi_read, VolatileIndex

# load the pickle file
output_dir = os.path.join('storage', 'output')
index_path = os.path.join(output_dir, 'volatile_index_1.pickle')
if not os.path.isfile(index_path):
    print('No pickle file was found in', index_path)
    quit()
x: VolatileIndex = vi_read(index_path)

# remove previous STM files after making sure about the whole process (NOT THIS PART)
if input('Are you sure you want to erase all the previous STM data? (any/n): ') == 'n': quit()
dir_shapes = os.path.join(output_dir, 'shapes')
for f in os.listdir(output_dir):
    path = os.path.join(output_dir, f)
    if os.path.isdir(path) and path != dir_shapes:
        shutil.rmtree(path)

# prepare the output folders
dir_y, dir_u, dir_v, dir_r, dir_pif = os.path.join(output_dir, 'y'), os.path.join(output_dir, 'u'), \
    os.path.join(output_dir, 'v'), os.path.join(output_dir, 'r'), os.path.join(output_dir, 'pif')
for folder in [dir_y, dir_u, dir_v, dir_r, dir_pif]:
    if not os.path.isdir(folder): os.mkdir(folder)

# write frame index
with open(os.path.join(output_dir, 'frames'), 'ab') as fif:
    for fid, rng in x.fi.items():
        fif.write(struct.pack('<Q', fid))
        fif.write(struct.pack('<H', rng[0]))
        fif.write(struct.pack('<H', rng[1]))

# write indices Y, U, V and R
for k, v in x.yi.items():
    with open(os.path.join(dir_y, str(k)), 'wb') as sqf:
        for sid in v:
            sqf.write(struct.pack('<H', sid))
for k, v in x.ui.items():
    with open(os.path.join(dir_u, str(k)), 'wb') as sqf:
        for sid in v:
            sqf.write(struct.pack('<H', sid))
for k, v in x.vi.items():
    with open(os.path.join(dir_v, str(k)), 'wb') as sqf:
        for sid in v:
            sqf.write(struct.pack('<H', sid))
for k, v in x.ri.items():
    with open(os.path.join(dir_r, str(k)), 'wb') as sqf:
        for sid in v:
            sqf.write(struct.pack('<H', sid))

# write PIF index
for fid, points in x.pifi.items():
    with open(os.path.join(dir_pif, str(fid)), 'wb') as pif:
        for point in points:
            pif.write(struct.pack('<H', point[0]))
            pif.write(struct.pack('<H', point[1]))
