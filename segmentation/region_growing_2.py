from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# read the image
whole_time = datetime.now()
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088


# In the previous method, we focused on a pixel and analysed its neighbours.
# Here we shall focus on a neighbour, and see if it fits anywhere with its own neighbours.
# Using a Dict/Map, it'll eliminate the futile exercise.


class Neighbour:
    def __init__(self, index: int, dh: int, ds: int, dv: int):
        self.index = index
        self.qualified = dh <= 5 and ds <= 50 and dv <= 10
        self.distance: float = (dh * 3.0) + (ds * 1.0) + (dv * 1.0)


class Pixel:
    def __init__(self, _c: np.ndarray, _y: int, _x: int):
        self.c: list[int] = _c.tolist()  # if it is ndarray, sorting won't work!
        self.y: int = _y
        self.x: int = _x
        self.s: Optional[int] = None  # Segment

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


# put every pixel in a Pixel class instance
pixels: list[Pixel] = []
for y in range(len(arr)):
    for x in range(len(arr[y])):
        pixels.append(Pixel(arr[y, x], y, x))

# iterate once on all pixels
segmentation_time = datetime.now()
next_seg = 0
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

    # find the nearest neighbour plus someone with a segment to rely on if no close neighbours were there
    nearest: int = 0
    segment_of_any_neighbour: Optional[int] = None
    for n in range(len(neighbours)):
        if n != 0 and neighbours[n].distance < neighbours[nearest].distance:
            nearest = n
        if not segment_of_any_neighbour and pixels[neighbours[nearest].index].s is not None:
            segment_of_any_neighbour = pixels[neighbours[nearest].index].s

    # determine the segment of this pixel
    if neighbours[nearest].qualified:
        if pixels[neighbours[nearest].index].s is not None:
            pixels[p].s = pixels[neighbours[nearest].index].s
        else:
            pixels[p].s = next_seg
            pixels[neighbours[nearest].index].s = next_seg
            next_seg += 1
    else:
        if segment_of_any_neighbour is not None:
            pixels[p].s = segment_of_any_neighbour
        else:
            pixels[p].s = next_seg
            next_seg += 1

print('Segmentation time:', datetime.now() - segmentation_time)

# assess the segments
segments: dict[int, list[int]] = {}  # size: next_seg
for p in range(len(pixels)):
    if pixels[p].s is None:
        raise Exception("Pixel " + str(p) + " is not grouped: " + str(pixels[p].x) + "x" + str(pixels[p].y))
    if pixels[p].s not in segments:
        segments[pixels[p].s] = list()
    segments[pixels[p].s].append(p)
segments = dict(sorted(segments.items(), key=lambda item: len(item[1]), reverse=True))

# colour the biggest segments
for big_sgm in list(segments.keys())[:25]:
    for p in segments[big_sgm]:
        arr[pixels[p].y, pixels[p].x] = np.array([5 + (10 * (big_sgm + 1)), 255, 255])

# print a summary
for seg in list(segments.values())[:30]:
    print(len(seg))
print('Total segments:', next_seg)

# show the image
plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)
plot.show()
