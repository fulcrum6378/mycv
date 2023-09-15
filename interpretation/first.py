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


# load the segmentation outputs
whole_time = datetime.now()
pixels: list[Pixel] = pickle.load(open('segmentation/output/rg2_pixels.pickle', 'rb'))
segments: dict[int, Segment] = pickle.load(open('segmentation/output/rg2_segments.pickle', 'rb'))
colour_model: str = 'YCbCr'
dim = 1088

# detect the boundaries of the cadre
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
blank = {
    'HSV': [0, 0, 255],
    'YCbCr': [255, 127, 127],
    'RGB': [255, 255, 255],
}[colour_model]
for y in range(min_y, max_y + 1):
    xes: list[list[int]] = []
    for x in range(min_x, max_x + 1):
        p = pixels[Pixel.get_pos(y, x)]
        if p.s == seg[0]:
            xes.append(p.c)
        else:
            xes.append(blank)
    arr.append(xes)

# show the testing sample
plot.imshow(cv2.cvtColor(np.array(arr, dtype=np.uint8), cv2.COLOR_YUV2RGB))
# from PIL import Image
# plot.imshow(Image.fromarray(np.array(arr, dtype=np.uint8), colour_model).convert('RGB'))
print('Whole time:', datetime.now() - whole_time)
plot.show()
