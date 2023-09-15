import pickle
from datetime import datetime
from math import sqrt

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
        self.a.append(pow(c[0], 2))
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

# get a mean value of all colours + detect border pixels
interpretation_time = datetime.now()
border: list[tuple[int, int]] = []
for p in pixels:
    segments[p.s].add_colour(p.c)
    if p.x < (dim - 1):  # right
        n = pixels[Pixel.get_pos(p.y, p.x + 1)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.b = True
            continue
    if p.y < (dim - 1):  # bottom
        n = pixels[Pixel.get_pos(p.y + 1, p.x)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.b = True
            continue
    if p.x > 0:  # left
        n = pixels[Pixel.get_pos(p.y, p.x - 1)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.b = True
            continue
    if p.x > 0:  # top
        n = pixels[Pixel.get_pos(p.y - 1, p.x)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.b = True
            continue

for seg in segments.values():
    seg.mean()
print('Interpretation time:', datetime.now() - interpretation_time)

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
