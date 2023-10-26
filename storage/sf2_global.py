import os
import struct

# Input directories
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_frame = os.path.join(input_dir, 'r'), os.path.join(input_dir, 'f')


# Reads all data from a Sequence File into a list.
def read_sequence_file(directory: str, value: str) -> list[int]:
    path = os.path.join(directory, value)
    with open(path, 'rb') as sf:
        seq: list[int] = []
        for bid in range(0, os.path.getsize(path), 2):
            seq.append(struct.unpack('<H', sf.read(2))[0])
    return seq


# Sorting key for Sequence Files
sk = lambda fn: int(fn)  # sorting key
