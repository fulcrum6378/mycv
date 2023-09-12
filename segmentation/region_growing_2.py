import pickle
from datetime import datetime
from typing import Optional

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# read the image
loading_time = datetime.now()
# red pillow: 1689005849386887, shoes: 1689005891979733
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005891979733.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088
min_seg = 100  # changed by stress!?
max_skipped_seg_pixels = 5  # 90 goes with no problem with min_seg:200


# In the previous method, we focused on a pixel and analysed its neighbours.
# Here we shall focus on a neighbour, and see if it fits anywhere with its own neighbours.
# This can be easily translated to work using Vulkan.


class Neighbour:
    def __init__(self, index: int, dh: int, ds: int, dv: int):
        self.index = index
        self.qualified = dh <= 10 and ds <= 20 and dv <= 5
        # self.distance: float = (dh * 3.0) + (ds * 1.0) + (dv * 1.0)


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


def find_a_segment_to_dissolve_in(this_seg: int, _p_ids: list[int]) -> Optional[int]:
    ranges_starts = [
        pixels[_p_ids[0]],
        pixels[_p_ids[0]],
        pixels[_p_ids[len(_p_ids) - 1]],
        pixels[_p_ids[len(_p_ids) - 1]],
    ]
    ranges: list[range] = [
        range(ranges_starts[0].y, 0, -1),
        range(ranges_starts[1].x, 0, -1),
        range(ranges_starts[2].y + 1, dim - 1),
        range(ranges_starts[3].x + 1, dim - 1),
    ]
    ranges_dim = [False, True, False, True]  # False=>Y, True=>X
    this_range, i = 0, 0
    point: Optional[int]
    while len(ranges) > 0 and i < max_skipped_seg_pixels:
        try:
            point = ranges[this_range][i]
            this_range += 1
        except IndexError:
            point = None
            ranges_starts.pop(this_range)
            ranges.pop(this_range)
            ranges_dim.pop(this_range)
        if this_range == len(ranges): this_range = 0
        if point is not None:
            seg_ = pixels[
                Pixel.get_pos(point, ranges_starts[this_range].x)
                if not ranges_dim[this_range]
                else Pixel.get_pos(ranges_starts[this_range].y, point)
            ].s
            if seg_ != this_seg:
                if len(segments[seg_].a) >= min_seg:
                    return seg_
        i += 1
    # raise Exception('Ran out of allowed skipped pixels for dissolving small segments')
    return None


# dissolve the small segments
removal: dict[int, int] = {}
for sid, seg in segments.items():
    if len(seg.a) < min_seg:
        absorber = find_a_segment_to_dissolve_in(sid, seg.a)
        if absorber is None: continue
        segments[absorber].a.extend(segments[sid].a)
        removal[sid] = absorber
rem_keys = removal.keys()
for p in pixels:
    if p.s in rem_keys:
        p.s = removal[p.s]
for reg in rem_keys:
    segments.pop(reg)

print('Segmentation time:', datetime.now() - segmentation_time)

# evaluate the segments and colour the biggest ones
segments = dict(sorted(segments.items(), key=lambda item: len(item[1].a), reverse=True))
for big_sgm in list(segments.keys())[:25]:
    for p in segments[big_sgm].a:
        arr[pixels[p].y, pixels[p].x] = np.array([5 + (10 * (big_sgm + 1)), 255, 255])
print('Biggest segment sizes:', ', '.join(str(len(item.a)) for item in list(segments.values())[:25]))
print('Total segments:', len(segments))

# show the image
plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
plot.show()

# save the output
dumping_time = datetime.now()
pickle.dump(pixels, open('segmentation/output/rg2_pixels.pickle', 'wb'))
pickle.dump(segments, open('segmentation/output/rg2_segments.pickle', 'wb'))
print('Dumping time:', datetime.now() - dumping_time)
