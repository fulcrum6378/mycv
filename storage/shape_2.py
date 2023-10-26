import os
import struct

from config import shape_path_bytes, shape_path_type

dir_shapes = os.path.join('storage', 'output', 'shapes')


class Shape:
    """
    Structure of Bytes:
      - 3 | average colour (YUV)
      - 2 | ratio
      - 8 | frame ID
      - 2 | width
      - 2 | height
      - 2 | central point X
      - 2 | central point Y
      - N | path points in 8/16-bit maxima (together 16/32-bits)
    """

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
            if len(self.path) > (self.w * self.h):
                print('Shape', sid, 'contains points whose number exceed its dimensions!')
