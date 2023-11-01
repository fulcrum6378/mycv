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
    # shell execution actions
    OPEN = 0

    # primary actions
    START = 1
    STOP = 2
    EXIT = 3
    WIPE_VISUAL_STM = 10

    # actions done requiring at least 1 frame to be captured
    SEGMENTATION = 11

    # actions with file transfer
    VISUAL_STM = 21
    VISUAL_MEM = 22

    # actions which do not require a connection
    SEGMENTATION_TMP = 111  # from cache
    VISUAL_STM_TMP = 121  # from cache
    VISUAL_MEM_TMP = 122  # from cache


print("""> Command codes:

-- primary actions
Open the app                  0 (requires ADB)
Start recording               1
Stop recording                2
Close the app                 3
Wipe visual STM               10

-- capture a frame and...
Segmentate & send results     11 (to use cache: 111)

-- actions with file transfer
Extract visual STM & validate 21 (to use cache: 121)
Extract visual MEM & validate 22 (to use cache: 122)

@ Note: if you use `open` or `close` actions, the power
optimisation mode is automatically turned on and closes
the app when not required for analysis to save power.
""")


# Turns the app on or off.
def turn_app(on: bool):
    ret: int = os.system(
        'adb shell am start -n ir.mahdiparastesh.mergen/ir.mahdiparastesh.mergen.Main' if on else
        'adb shell input keyevent 4'
    )
    if ret != 0:
        global power_optimisation_mode
        power_optimisation_mode = False


# miscellaneous tweaks
power_optimisation_mode: bool = False  # when on, open the app only when needed to save battery of the phone

while True:
    try:
        mode: int = int(input('Debug mode: '))
    except ValueError:
        break

    path = ''
    if mode <= 0:
        match mode:
            case Mode.OPEN.value:
                turn_app(True)
                power_optimisation_mode = True
        continue
    elif mode == Mode.EXIT.value:
        power_optimisation_mode = True
    elif mode > 10:
        match mode:
            case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
                path = os.path.join('debug', 'temp', 'arr')
            case Mode.VISUAL_STM.value | Mode.VISUAL_STM_TMP.value:
                path = os.path.join('debug', 'temp', 'stm.zip')
            case Mode.VISUAL_MEM.value | Mode.VISUAL_MEM_TMP.value:
                path = os.path.join('debug', 'temp', 'mem.zip')
            case _:
                print('Unknown (to client) debug mode', mode)
                continue
        file: IO

        if mode <= 20 and power_optimisation_mode:
            turn_app(True)

    # connect to Debug.java
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
            elif mode == Mode.VISUAL_STM.value and data[0] == 1:
                print('Cannot export visual STM while Mergen is on.')
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
            data = s.recv(4096)
            if not data: break
            file.write(data)
        print(file.tell(), 'bytes downloaded...', datetime.now() - download_time)
        file.seek(0, os.SEEK_SET)
    else:
        file = open(path, 'rb')

    if 10 < mode <= 20 and power_optimisation_mode:
        turn_app(False)

    # process the downloaded file
    match mode:
        case Mode.SEGMENTATION.value | Mode.SEGMENTATION_TMP.value:
            render_time = datetime.now()
            arr: np.ndarray = np.zeros((dim, dim, 3), dtype=np.uint8)
            b_status = open(path, 'rb')
            b_status.seek(3551232)  # out of 4734976
            for yy in range(dim):
                for xx in range(dim):
                    y = struct.unpack('B', file.read(1))[0]
                    u = struct.unpack('B', file.read(1))[0]
                    v = struct.unpack('B', file.read(1))[0]
                    if struct.unpack('B', b_status.read(1))[0] == 0:
                        arr[yy, xx] = y, u, v
                    else:
                        arr[yy, xx] = 76, 84, 255
            b_status.close()
            plot.imshow(cv2.cvtColor(arr, cv2.COLOR_YUV2RGB))
            print('Rendering time:', datetime.now() - render_time)
            plot.show()
        case Mode.VISUAL_STM.value | Mode.VISUAL_STM_TMP.value:
            dest = os.path.join('storage', 'output')
            for f in os.listdir(dest):
                path = os.path.join(dest, f)
                if os.path.isdir(path):
                    shutil.rmtree(path)
            with zipfile.ZipFile(os.path.join('debug', 'temp', 'stm.zip'), 'r') as zip_ref:
                zip_ref.extractall(dest)
            print('Visual short-term memory in /storage/ was replaced.')
            try:
                # noinspection PyUnresolvedReferences
                import storage.sf2_validator
            except FileNotFoundError:
                print('Visual short-term memory is incomplete!')
        case Mode.VISUAL_MEM.value | Mode.VISUAL_MEM_TMP.value:
            dest = os.path.join('storage', 'output')
            for f in os.listdir(dest):
                path = os.path.join(dest, f)
                if os.path.isdir(path):
                    shutil.rmtree(path)
            with zipfile.ZipFile(os.path.join('debug', 'temp', 'mem.zip'), 'r') as zip_ref:
                zip_ref.extractall(dest)
            print('Visual memory in /storage/ was replaced.')
            try:
                # noinspection PyUnresolvedReferences
                import storage.sf2_validator
            except FileNotFoundError:
                print('Visual memory is incomplete!')
    file.close()
