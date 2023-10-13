import os
import shutil
import socket
import struct
import zipfile
from datetime import datetime
from enum import Enum
from typing import IO

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import dim, server_address


class Mode(Enum):
    # primary actions
    START = 1
    STOP = 2
    EXIT = 3

    # actions done requiring at least 1 frame to be captured
    SEGMENTATION = 11  # capture 1 frame, process it and send segmentation results

    # actions involving storage
    VISUAL_STM = 21  # export and validate the visual short-term memory

    # actions which do not require a connection
    SEGMENTATION_TMP = 111  # display segmentation results from cache
    VISUAL_STM_TMP = 121  # validate the visual short-term memory from cache


while True:
    try:
        mode: int = int(input('Debug mode: '))
    except ValueError:
        break

    if mode > 10:
        match mode:
            case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
                path = os.path.join('debug', 'temp', 'arr')
            case Mode.VISUAL_STM.value | Mode.VISUAL_STM_TMP.value:
                path = os.path.join('debug', 'temp', 'memory.zip')
            case _:
                print('Unknown (to client) debug mode', mode)
                continue
        file: IO
    else:
        path = ''

    if mode < 100:
        connect_time = datetime.now()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        try:
            s.connect((server_address, 3772))
        except ConnectionRefusedError as cre:
            print(cre)
            continue
        except TimeoutError as toe:
            print(toe)
            continue
        s.sendall(bytes([mode]))
        data: bytes = s.recv(1)
        print('Connection established...', datetime.now() - connect_time)
        if data[0] != 0:
            if data[0] == 255:
                print('Unknown (to server) debug mode', mode)
            elif mode == Mode.START.value and data[0] == 1:
                print('Already started!')
            elif mode == Mode.STOP.value and data[0] == 1:
                print('Already stopped!')
            elif mode == Mode.EXIT.value and data[0] == 1:
                print('Still got work to do!')
            else:
                print('Error code', int(data[0]))
            continue
        if mode <= 10:
            print('Done')
            continue

        # receive the specified file
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

    # process the downloaded file
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
                        arr[yy, xx] = y, u, v
                    else:
                        arr[yy, xx] = 76, 84, 255
            plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
            print('Rendering time:', datetime.now() - render_time)
            plot.show()
        case Mode.VISUAL_STM.value | Mode.VISUAL_STM_TMP.value:
            dest = os.path.join('storage', 'output')
            for f in os.listdir(dest):
                path = os.path.join(dest, f)
                if os.path.isdir(path):
                    shutil.rmtree(path)
            with zipfile.ZipFile(os.path.join('debug', 'temp', 'memory.zip'), 'r') as zip_ref:
                zip_ref.extractall(dest)
            print('Visual short-term memory in /storage/ was replaced.')
            try:
                # noinspection PyUnresolvedReferences
                import storage.sf2_validator
            except FileNotFoundError:
                print('Visual short-term memory is incomplete!')
    file.close()
