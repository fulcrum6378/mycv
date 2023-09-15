import pickle
from datetime import datetime

import cv2
import matplotlib.pyplot as plot
import numpy as np


class Pixel:
    # When a class instance is unpickled, its __init__() method is usually not invoked.
    def __init__(self):
        self.c = None  # list[int]
        self.y = None  # int
        self.x = None  # int
        self.s = None  # int

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x


class Segment:
    def __init__(self):
        self.a = None  # list[int]


# `arr` will be disposed of at the end of `segmentation`.

# load the segmentation outputs
loading_time = datetime.now()
pixels: list[Pixel] = pickle.load(open('segmentation/output/rg2_pixels.pickle', 'rb'))
segments: dict[int, Segment] = pickle.load(open('segmentation/output/rg2_segments.pickle', 'rb'))
dim = 1088
print('Loading time:', datetime.now() - loading_time)

# get a mean value of all colours + detect border pixels
interpretation_time = datetime.now()
colours_a: list[float] = []
colours_b: list[float] = []
colours_c: list[float] = []
border: list[tuple[int, int]] = []
for p in pixels:
    colours_a.append(float(p.c[0]))
    colours_b.append(float(p.c[1]))
    colours_c.append(float(p.c[2]))
    if p.x < (dim - 1):  # right
        n = pixels[Pixel.get_pos(p.y, p.x + 1)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.border = True
            continue
    if p.y < (dim - 1):  # bottom
        n = pixels[Pixel.get_pos(p.y + 1, p.x)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.border = True
            continue
    if p.x > 0:  # left
        n = pixels[Pixel.get_pos(p.y, p.x - 1)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.border = True
            continue
    if p.x > 0:  # top
        n = pixels[Pixel.get_pos(p.y - 1, p.x)]
        if p.s != n.s:
            border.append((p.y, p.x))
            p.border = True
            continue
mean = [int(sum(colours_a) / len(colours_a)),
        int(sum(colours_b) / len(colours_b)),
        int(sum(colours_c) / len(colours_c))]
print('Interpretation time:', datetime.now() - interpretation_time)

# detect the boundaries of the cadre
display_preparation_time = datetime.now()
min_y, min_x, max_y, max_x = -1, -1, -1, -1
seg = list(segments.items())[2]
for p in seg[1].a:
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
            if not hasattr(p, 'border'):
                xes.append(mean)  # p.c
            else:
                xes.append([17, 107, 255])  # blue (RGB#0000FF)
        else:
            xes.append([255, 127, 127])  # HSV: [0, 0, 255], RGB: [255, 255, 255]
    arr.append(xes)

# show the testing sample
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
print('Display preparation time:', datetime.now() - display_preparation_time)
plot.show()
