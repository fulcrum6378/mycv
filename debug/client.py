import os
import socket
import struct
from datetime import datetime
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
            path = os.path.join('debug', 'temp', 'arr')
        case Mode.STORAGE.value | Mode.STORAGE_TMP.value:
            path = os.path.join('debug', 'temp', 'memory.zip')
        case _:
            print('Unknown code', mode)
            continue

    file: IO
    if mode < 99:
        connect_time = datetime.now()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((server_address, 3772))
        s.sendall(bytes([1]))
        data: bytes = s.recv(1)
        if data[0] != 0:
            continue
        print('Connection established...', datetime.now() - connect_time)
        file = open(path, 'wb+')
        download_time = datetime.now()
        while True:
            data = s.recv(4096)  # 4734976
            if not data: break
            file.write(data)
        print(file.tell(), 'bytes downloaded...', datetime.now() - download_time)
        file.seek(0, os.SEEK_SET)
    else:
        file = open(path, 'rb')

    match mode:
        case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
            render_time = datetime.now()
            arr: np.ndarray = np.zeros((dim, dim, 3), dtype=np.uint8)
            for yy in range(dim):
                for xx in range(dim):
                    v = struct.unpack('B', file.read(1))[0]
                    u = struct.unpack('B', file.read(1))[0]
                    y = struct.unpack('B', file.read(1))[0]
                    if struct.unpack('b', file.read(1))[0] == 0:
                        arr[yy, xx] = y, u, v  # y, u, v
                    else:
                        arr[yy, xx] = 76, 84, 255
            plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
            print('Rendering time:', datetime.now() - render_time)
            plot.show()
        case Mode.STORAGE.value | Mode.STORAGE_TMP.value:
            pass
    file.close()
