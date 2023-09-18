import json
import pickle
import sys
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
        self.b: Optional[bool] = None

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x

    # recursively checks if neighbours are border pixels
    # directions range are 0..7!
    def check_neighbours(self, avoid_dir: Optional[int] = None):
        next_ones: list[tuple[Pixel, int]] = []
        if avoid_dir != 0 and self.y > 0:  # northern
            n = pixels[Pixel.get_pos(self.y - 1, self.x)]
            if n.is_next_b(): next_ones.append((n, 0))
        if avoid_dir != 1 and self.y > 0 and self.x < (dim - 1):  # north-eastern
            n = pixels[Pixel.get_pos(self.y - 1, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 1))
        if avoid_dir != 2 and self.x < (dim - 1):  # eastern
            n = pixels[Pixel.get_pos(self.y, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 2))
        if avoid_dir != 3 and self.y < (dim - 1) and self.x < (dim - 1):  # south-eastern
            n = pixels[Pixel.get_pos(self.y + 1, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 3))
        if avoid_dir != 4 and self.y < (dim - 1):  # southern
            n = pixels[Pixel.get_pos(self.y + 1, self.x)]
            if n.is_next_b(): next_ones.append((n, 4))
        if avoid_dir != 5 and self.y < (dim - 1) and self.x > 0:  # south-western
            n = pixels[Pixel.get_pos(self.y + 1, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 5))
        if avoid_dir != 6 and self.x > 0:  # western
            n = pixels[Pixel.get_pos(self.y, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 6))
        if avoid_dir != 7 and self.y > 0 and self.x > 0:  # north-western
            n = pixels[Pixel.get_pos(self.y - 1, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 7))

        for n, d in next_ones: n.check_neighbours(d)

    # checks if this is a border pixel and not detected before
    def is_next_b(self) -> bool:
        if self.b is None:
            self.check_if_border()
            if self.b and self.s == s_id:
                return True
        return False

    def check_if_border(self) -> None:
        if self.x < (dim - 1):  # right
            _n = pixels[Pixel.get_pos(self.y, self.x + 1)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.y < (dim - 1):  # bottom
            _n = pixels[Pixel.get_pos(self.y + 1, self.x)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.x > 0:  # left
            _n = pixels[Pixel.get_pos(self.y, self.x - 1)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.y > 0:  # top
            _n = pixels[Pixel.get_pos(self.y - 1, self.x)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return

    def set_is_border(self):
        self.b = True
        _s = segments[self.s]
        _s.border.append([(100 / _s.w) * _s.min_x - self.x, (100 / _s.h) * _s.min_y - self.y])


class Segment:
    def __init__(self):
        self.p: list[int] = []  # pixels
        self.a: list[int] = []  # colour A values
        self.b: list[int] = []  # colour B values
        self.c: list[int] = []  # colour C values
        self.m: list[int] = []  # mean colour
        self.border: list[list[float]] = []
        self.min_y, self.min_x, self.max_y, self.max_x = -1, -1, -1, -1  # boundaries
        self.w, self.h = -1, -1  # dimensions

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
        self.m = [round(sqrt(sum(self.a) / len(self.a))),
                  round(sqrt(sum(self.b) / len(self.b))),
                  round(sqrt(sum(self.c) / len(self.c)))]
        del self.a, self.b, self.c

    # determine min_y, min_x, max_y, max_x
    def detect_boundaries(self):
        for _p in self.p:
            if self.min_y == -1:  # messed because Python has no do... while!
                self.min_y = pixels[_p].y
                self.max_y = pixels[_p].y
                self.min_x = pixels[_p].x
                self.max_x = pixels[_p].x
                continue
            if pixels[_p].y < self.min_y: self.min_y = pixels[_p].y
            if pixels[_p].x < self.min_x: self.min_x = pixels[_p].x
            if pixels[_p].y > self.max_y: self.max_y = pixels[_p].y
            if pixels[_p].x > self.max_x: self.max_x = pixels[_p].x
        self.w = (seg.max_x + 1) - seg.min_x
        self.h = (seg.max_y + 1) - seg.min_y


# `arr` will be disposed of at the end of `segmentation`.

# load the segmentation outputs
loading_time = datetime.now()
pixels: list[Pixel] = pickle.load(open('segmentation/output/rg2_pixels.pickle', 'rb'))
segments: dict[int, Segment] = pickle.load(open('segmentation/output/rg2_segments.pickle', 'rb'))
dim = 1088
sys.setrecursionlimit(dim * dim)
print('Loading time:', datetime.now() - loading_time)

# get a mean value of all colours in all segments, detect their border pixels and also their boundaries
mean_and_border_time = datetime.now()
for p in pixels: segments[p.s].add_colour(p.c)
for s_id, seg in segments.items():  # couldn't cut the dict properly
    seg.mean()
    seg.detect_boundaries()

    # find the first encountering border pixel as a checkpoint
    border_checkpoint: Optional[Pixel] = None
    for p in seg.p:
        p_ = pixels[p]
        if p_.b is None: p_.check_if_border()
        if p_.b:
            border_checkpoint = p_
            break

    # now start collecting all border pixels using that checkpoint
    border_checkpoint.check_neighbours()
print('Mean and border time:', datetime.now() - mean_and_border_time)

# store 5 of largest segments
exports = sorted(segments.values(), key=lambda item: len(item.p), reverse=True)[:5]
for s in range(len(exports)):
    open('tracing/output/' + str(s + 1) + '.json', 'w').write(json.dumps({
        'mean': exports[s].m,
        'path': exports[s].border,
        'dimensions': [exports[s].w, exports[s].h],
    }))

# draw the segment into the cadre and display it
display_preparation_time = datetime.now()
s_id, seg = list(segments.items())[2]
arr: list[list[list[int]]] = []
for y in range(seg.min_y, seg.max_y + 1):
    xes: list[list[int]] = []
    for x in range(seg.min_x, seg.max_x + 1):
        p = pixels[Pixel.get_pos(y, x)]
        if p.s == s_id:
            if not p.b:
                xes.append(seg.m)  # p.c
            else:
                xes.append([0, 255, 200])
        else:
            xes.append([255, 127, 127])  # HSV: [0, 0, 255], RGB: [255, 255, 255]
    arr.append(xes)
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
