import os
import socket
import struct
from enum import Enum
from typing import IO

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import dim, server_address


class Mode(Enum):
    SEGMENTATION = 1
    STORAGE = 2
    SEGMENTATION_TMP = 101
    STORAGE_TMP = 102


while True:
    try:
        mode: int = int(input('Debug mode: '))
    except ValueError:
        break

    match mode:
        case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
            path = os.path.join('debug', 'temp', 'arr.bin')
        case Mode.STORAGE.value | Mode.STORAGE_TMP.value:
            path = os.path.join('debug', 'temp', 'memory.zip')
        case _:
            print('Unknown code', mode)
            continue

    file: IO
    if mode < 99:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server_address, 3772))
        s.sendall(bytes([1]))
        data: bytes = s.recv(1)
        if data[0] != 0:
            continue
        file = open(path, 'wb+')
        while True:
            data = s.recv(4096)  # 4734976
            if not data: break
            file.write(data)
        file.seek(0, os.SEEK_SET)
    else:
        file = open(path, 'rb')

    match mode:
        case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
            arr: np.ndarray = np.zeros((dim, dim, 3), dtype=np.uint8)
            for y in range(dim):
                for x in range(dim):
                    v = struct.unpack('B', file.read(1))[0]
                    u = struct.unpack('B', file.read(1))[0]
                    y = struct.unpack('B', file.read(1))[0]
                    if struct.unpack('b', file.read(1))[0] == 0:
                        arr[y, x] = y, u, v
                    else:
                        arr[y, x] = 255, 0, 0
            plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
            plot.show()
    file.close()
