import sys
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
sys.setrecursionlimit(dim * dim)


# In the previous method, we focused on a pixel and analysed its neighbours.
# Here we shall focus on a neighbour, and see if it fits anywhere with its own neighbours.
# Using a Dict/Map, it'll eliminate the futile exercise.


class Pixel:
    def __init__(self, _c: np.ndarray, _y: int, _x: int):
        self.c: list[int] = _c.tolist()  # if it is ndarray, sorting won't work!
        self.y: int = _y
        self.x: int = _x
        self.s: Optional[int] = None  # Segment

    # returns True if the colours are near, NOT EXACTLY EQUAL
    def __eq__(self, other) -> bool:
        return abs(int(self.c[0]) - int(other.c[0])) <= 5 \
            and abs(int(self.c[1]) - int(other.c[1])) <= 50 \
            and abs(int(self.c[2]) - int(other.c[2])) <= 10

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x


pixels: list[Pixel] = []
for y in arr:
    for x in y:
        pixels.append(Pixel(arr[y, x], y, x))

# Flowchart:
# a neighbour ->
#   grouped & close   -> JOIN
#   !grouped & close  -> skip, if none other was found, NEW GROUP, else recursion?!?!?
#   grouped & !close  ->
#   !grouped & !close ->

n: int
next_seg = 0
req1: bool
req2: bool
for p in range(len(pixels)):
    neighbourhood = list()  # TODO
    n = Pixel.get_pos(pixels[p].y, pixels[p].x + 1)  # right
    req1, req2 = pixels[p] == n, pixels[n].s is not None
    if pixels[p].x < (dim - 1) and req1:
        if pixels[n].s is not None:
            pass
        if pixels[p] == pixels[n]:
            pass
        pixels[p].s = pixels[n].s

    n = Pixel.get_pos(pixels[p].y + 1, pixels[p].x)  # bottom
    req1, req2 = pixels[n].s is not None, pixels[p] == pixels[n]
    if pixels[p].y < (dim - 1) and pixels[n].s is not None and pixels[p] == pixels[n]:
        pixels[p].s = pixels[n].s

    n = Pixel.get_pos(pixels[p].y, pixels[p].x - 1)  # left
    req1, req2 = pixels[n].s is not None, pixels[p] == n
    if pixels[p].x > 0 and pixels[n].s is not None and pixels[p] == n:
        pixels[p].s = pixels[n].s

    n = Pixel.get_pos(pixels[p].y - 1, pixels[p].x)  # top
    req1, req2 = pixels[n].s is not None, pixels[p] == n
    if pixels[p].x > 0 and pixels[n].s is not None and pixels[p] == n:
        pixels[p].s = pixels[n].s

    # if none of the neighbours had any segments
    # if none of the neighbours were close

# show the image
plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)
plot.show()
