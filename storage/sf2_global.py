import os
import struct

# Input directories and files
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v, dir_r = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), \
    os.path.join(input_dir, 'v'), os.path.join(input_dir, 'r')  # dir_pif = os.path.join(input_dir, 'pif')
frames_file, numbers_file = os.path.join(input_dir, 'frames'), os.path.join(input_dir, 'numbers')


# Reads all data from a Sequence File into a list.
def read_sequence_file(directory: str, value: str) -> list[int]:
    path = os.path.join(directory, value)
    with open(path, 'rb') as sf:
        seq: list[int] = []
        for bid in range(0, os.path.getsize(path), 2):
            seq.append(struct.unpack('<H', sf.read(2))[0])
    return seq


# Reads the frame index into a dictionary.
def read_frames_file() -> dict[int, tuple[int, int]]:
    data: dict[int, tuple[int, int]] = {}
    with open(frames_file, 'rb') as fif:
        for bid in range(0, os.path.getsize(frames_file), 12):
            fid = struct.unpack('<Q', fif.read(8))[0]
            beg = struct.unpack('<H', fif.read(2))[0]
            end = struct.unpack('<H', fif.read(2))[0]
            data[fid] = (beg, end)
    return data


# Reads the frame index into a dictionary with ranges instead of tuples.
def read_frames_file_with_ranges() -> dict[int, range]:
    data: dict[int, range] = {}
    with open(frames_file, 'rb') as fif:
        for bid in range(0, os.path.getsize(frames_file), 12):
            fid = struct.unpack('<Q', fif.read(8))[0]
            beg = struct.unpack('<H', fif.read(2))[0]
            end = struct.unpack('<H', fif.read(2))[0]
            data[fid] = range(beg, end)
    return data


# Reads a tiny file exported in the C++ side, indicating first/last IDs of shapes and frames
def read_numbers_file() -> tuple[int, int, int]:
    with open(numbers_file, 'rb') as n_f:
        return (struct.unpack('<Q', n_f.read(8))[0],
                struct.unpack('<Q', n_f.read(8))[0],
                struct.unpack('<H', n_f.read(2))[0])


# Reads "Position In Frame" indexes
# def read_pif_index(frame_id: int) -> list[tuple[int, int]]:
#    path = os.path.join(dir_pif, str(frame_id))
#    with open(path, 'rb') as sf:
#        pif: list[tuple[int, int]] = []
#        for bid in range(0, os.path.getsize(path), 4):
#            pif.append((struct.unpack('<H', sf.read(2))[0], struct.unpack('<H', sf.read(2))[0]))
#    return pif


# Sorting key for Sequence Files
sk = lambda fn: int(fn)  # sorting key
