import pickle
from datetime import datetime
from math import sqrt
from typing import Optional

import cv2
import matplotlib.pyplot as plot
import numpy as np


class Pixel:
    # When a class instance is unpickled, its __init__() method is usually not invoked.
    def __init__(self):
        self.c: list[int] = []
        self.y: int = 0
        self.x: int = 0
        self.s: int = 0
        self.b: bool = False

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x

    def check_if_in_border(self) -> None:
        if self.x < (dim - 1):  # right
            n = pixels[Pixel.get_pos(self.y, self.x + 1)]
            if self.s != n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.y < (dim - 1):  # bottom
            n = pixels[Pixel.get_pos(self.y + 1, self.x)]
            if self.s != n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.x > 0:  # left
            n = pixels[Pixel.get_pos(self.y, self.x - 1)]
            if self.s != n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.x > 0:  # top
            n = pixels[Pixel.get_pos(self.y - 1, self.x)]
            if self.s != n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return

    def set_is_border(self):
        border.append((self.y, self.x))
        self.b = True


class Segment:
    def __init__(self):
        self.p: list[int] = []  # pixels
        self.a: list[int] = []  # colour A values
        self.b: list[int] = []  # colour B values
        self.c: list[int] = []  # colour C values
        self.m: list[int] = []  # mean colour

    # THIS PROCESS COULD BE DONE DURING THE SEGMENTATION...
    def add_colour(self, c: list[int]):
        # self.a.append(c[0])
        # self.b.append(c[1])
        # self.c.append(c[2])
        self.a.append(pow(c[0], 2))  # c[0] * c[0] instead
        self.b.append(pow(c[1], 2))
        self.c.append(pow(c[2], 2))

    # without squaring, my pillow gets a little darker!
    def mean(self) -> None:
        # self.m = [sum(self.a) / len(self.a),
        #          sum(self.b) / len(self.b),
        #          sum(self.c) / len(self.c)]
        self.m = [sqrt(sum(self.a) / len(self.a)),
                  sqrt(sum(self.b) / len(self.b)),
                  sqrt(sum(self.c) / len(self.c))]
        del self.a, self.b, self.c


# `arr` will be disposed of at the end of `segmentation`.

# load the segmentation outputs
loading_time = datetime.now()
pixels: list[Pixel] = pickle.load(open('segmentation/output/rg2_pixels.pickle', 'rb'))
segments: dict[int, Segment] = pickle.load(open('segmentation/output/rg2_segments.pickle', 'rb'))
dim = 1088
print('Loading time:', datetime.now() - loading_time)

# get a mean value of all colours + detect the first encountering border pixel
mean_time = datetime.now()
border: list[tuple[int, int]] = []
border_checkpoint: Optional[Pixel] = None
for p in pixels:
    segments[p.s].add_colour(p.c)
    if border_checkpoint is None:
        p.check_if_in_border()
        if p.b: border_checkpoint = p
for seg in segments.values():
    seg.mean()
print('Mean time:', datetime.now() - mean_time)

# resume from the first encountering border pixel
border_time = datetime.now()
this_b: Optional[Pixel] = None
direction: int = 0  # 0..7
while this_b is None or this_b.y != border_checkpoint.y or this_b.x != border_checkpoint.x:  # we could use do...while
    this_dir = direction
    if this_b is None: this_b = border_checkpoint
    next_b = None
    while next_b is None:  # analyse the 1 direction
        match this_dir:
            case 0:  # northern
                n = pixels[Pixel.get_pos(self.y + 1, self.x)]

            case 1:  # north-eastern
                pass
            case 2:  # eastern
                pass
            case 3:  # south-eastern
                pass
            case 4:  # southern
                pass
            case 5:  # south-western
                pass
            case 6:  # western
                pass
            case 7:  # north-western
                pass
        this_dir += 1
        if this_dir == 8: this_dir = 0
    this_b = next_b
print('Border time:', datetime.now() - border_time)

# detect the boundaries of the cadre
display_preparation_time = datetime.now()
min_y, min_x, max_y, max_x = -1, -1, -1, -1
seg = list(segments.items())[2]
for p in seg[1].p:
    if min_y == -1:  # messed because Python has no do... while!
        min_y = pixels[p].y
        max_y = pixels[p].y
        min_x = pixels[p].x
        max_x = pixels[p].x
        continue
    if pixels[p].y < min_y: min_y = pixels[p].y
    if pixels[p].x < min_x: min_x = pixels[p].x
    if pixels[p].y > max_y: max_y = pixels[p].y
    if pixels[p].x > max_x: max_x = pixels[p].x

# draw the segment into the cadre
arr: list[list[list[int]]] = []
for y in range(min_y, max_y + 1):
    xes: list[list[int]] = []
    for x in range(min_x, max_x + 1):
        p = pixels[Pixel.get_pos(y, x)]
        if p.s == seg[0]:
            if not p.b:
                xes.append(seg[1].m)  # p.c
            else:
                xes.append([0, 255, 200])
        else:
            xes.append([255, 127, 127])  # HSV: [0, 0, 255], RGB: [255, 255, 255]
    arr.append(xes)

# show the testing sample
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
