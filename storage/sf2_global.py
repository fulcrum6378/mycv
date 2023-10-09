import os
import struct

from config import shape_path_bytes, shape_path_type

# input directories
input_dir = os.path.join('storage', 'output')
dir_y, dir_u, dir_v = os.path.join(input_dir, 'y'), os.path.join(input_dir, 'u'), os.path.join(input_dir, 'v')
dir_ratio, dir_frame = os.path.join(input_dir, 'r'), os.path.join(input_dir, 'f')
dir_shapes = os.path.join(input_dir, 'shapes')


class Shape:
    def __init__(self, sid: str):
        shf_path = os.path.join(dir_shapes, sid)
        with open(shf_path, 'rb') as shf:  # NOTE: ARM64 IS LITTLE-ENDIAN!!!
            self.m: list[int] = [
                struct.unpack('B', shf.read(1))[0],
                struct.unpack('B', shf.read(1))[0],
                struct.unpack('B', shf.read(1))[0]
            ]
            self.r: int = struct.unpack('<H', shf.read(2))[0]
            self.frame: int = struct.unpack('<Q', shf.read(8))[0]
            self.w: int = struct.unpack('<H', shf.read(2))[0]
            self.h: int = struct.unpack('<H', shf.read(2))[0]
            self.cx: int = struct.unpack('<H', shf.read(2))[0]
            self.cy: int = struct.unpack('<H', shf.read(2))[0]
            self.path: list[tuple[int, int]] = []
            for b in range(shf.tell(), os.path.getsize(shf_path), 8):
                self.path.append((
                    struct.unpack(shape_path_type, shf.read(shape_path_bytes))[0],
                    struct.unpack(shape_path_type, shf.read(shape_path_bytes))[0]
                ))


def read_sequence_file(directory: str, value: str) -> list[int]:
    path = os.path.join(directory, value)
    with open(path, 'rb') as sf:
        seq: list[int] = []
        for bid in range(0, os.path.getsize(path), 2):
            seq.append(struct.unpack('<H', sf.read(2))[0])
    return seq


# miscellaneous
sk = lambda fn: int(fn)  # sorting key
