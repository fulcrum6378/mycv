import pickle
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# In the previous method, we focused on a pixel and analysed its neighbours.
# Here we shall focus on a neighbour, and see if it fits anywhere with its own neighbours.
# This can be easily translated to work using Vulkan.

# read the image
loading_time = datetime.now()
colour_model: str = 'YCbCr'  # RGB, HSV, YCbCr; (tweak Neighbour.__init__ too) TODO YUV
# https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes
# red pillow: 1689005849386887;   28,230(HSV), 18,692(YCC), 24,204(RGB) segments
# shoes:      1689005891979733;  100,302(HSV), 78,930(YCC), 96,025(RGB) segments
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert(colour_model)).copy()
dim: int = 1088


class Neighbour:
    def __init__(self, index: int, dh: int, ds: int, dv: int):
        self.index = index
        # self.qualified = dh <= 4 and ds <= 4 and dv <= 4  # RGB
        # self.qualified = dh <= 10 and ds <= 20 and dv <= 5  # HSV
        self.qualified = dh <= 4 and ds <= 4 and dv <= 4  # YCbCr


class Pixel:
    def __init__(self, _c: np.ndarray, _y: int, _x: int):
        self.c: list[int] = _c.tolist()  # if it is ndarray, sorting won't work!
        self.y: int = _y
        self.x: int = _x
        self.s: Optional[int] = None  # segment

    def compare(self, _n: int) -> Neighbour:
        global pixels
        return Neighbour(
            _n,
            abs(int(self.c[0]) - int(pixels[_n].c[0])),
            abs(int(self.c[1]) - int(pixels[_n].c[1])),
            abs(int(self.c[2]) - int(pixels[_n].c[2])))

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x


class Segment:
    def __init__(self):
        self.a: list[int] = []


# put every pixel in a Pixel class instance
pixels: list[Pixel] = []
for y in range(len(arr)):
    for x in range(len(arr[y])):
        pixels.append(Pixel(arr[y, x], y, x))
print('Loading time:', datetime.now() - loading_time)

# iterate once on all pixels
segmentation_time = datetime.now()
next_seg = 0
segments: dict[int, Segment] = {}
for p in range(len(pixels)):
    if pixels[p].s is not None: continue

    # analyse the neighbours
    neighbours: list[Neighbour] = []
    if pixels[p].x < (dim - 1):  # right
        neighbours.append(pixels[p].compare(Pixel.get_pos(pixels[p].y, pixels[p].x + 1)))
    if pixels[p].y < (dim - 1):  # bottom
        neighbours.append(pixels[p].compare(Pixel.get_pos(pixels[p].y + 1, pixels[p].x)))
    if pixels[p].x > 0:  # left
        neighbours.append(pixels[p].compare(Pixel.get_pos(pixels[p].y, pixels[p].x - 1)))
    if pixels[p].x > 0:  # top
        neighbours.append(pixels[p].compare(Pixel.get_pos(pixels[p].y - 1, pixels[p].x)))

    # iterate on the neighbours
    any_qualified = False
    allowed_regions = set()
    segment_of_any_neighbour: Optional[int] = None
    for n in range(len(neighbours)):
        if neighbours[n].qualified:
            any_qualified = True
            if pixels[neighbours[n].index].s is not None:
                allowed_regions.add(pixels[neighbours[n].index].s)
        if not segment_of_any_neighbour and pixels[neighbours[n].index].s is not None:
            segment_of_any_neighbour = pixels[neighbours[n].index].s

    # determine the segment of this pixel
    allowed_regions = list(allowed_regions)
    if any_qualified:
        if len(allowed_regions) == 0:
            pixels[p].s = next_seg
            segments[next_seg] = Segment()
            next_seg += 1
        else:
            if len(allowed_regions) > 1:  # repair the pixels
                chosen_one = min(allowed_regions)
                for sid in allowed_regions:
                    if sid != chosen_one:
                        for changer in segments[sid].a:
                            pixels[changer].s = chosen_one
                        segments[chosen_one].a.extend(segments[sid].a)
                        segments.pop(sid)
                pixels[p].s = chosen_one
            else:
                pixels[p].s = allowed_regions[0]
    else:
        if segment_of_any_neighbour is not None:
            pixels[p].s = segment_of_any_neighbour
        else:
            pixels[p].s = next_seg
            segments[next_seg] = Segment()
            next_seg += 1
    segments[pixels[p].s].a.append(p)

print('Segmentation time:', datetime.now() - segmentation_time)

# evaluate the segments and colour the biggest ones
segments = dict(sorted(segments.items(), key=lambda item: len(item[1].a), reverse=True))
if colour_model != 'HSV':
    arr = np.asarray(Image.fromarray(arr, colour_model).convert('HSV')).copy()
arr.setflags(write=True)
for big_sgm in list(segments.keys())[:50]:
    for p in segments[big_sgm].a:
        arr[pixels[p].y, pixels[p].x] = np.array([5 + (10 * (big_sgm + 1)), 255, 255])
if colour_model != 'HSV':
    arr = np.asarray(Image.fromarray(arr, 'HSV').convert(colour_model))
print('Biggest segment sizes:', ', '.join(str(len(item.a)) for item in list(segments.values())[:25]))
print('Total segments:', len(segments))

# show the image
plot.imshow(Image.fromarray(arr, colour_model).convert('RGB'))
plot.show()

# save the output
dumping_time = datetime.now()
pickle.dump(pixels, open('segmentation/output/rg2_pixels.pickle', 'wb'))
pickle.dump(segments, open('segmentation/output/rg2_segments.pickle', 'wb'))
print('Dumping time:', datetime.now() - dumping_time)
