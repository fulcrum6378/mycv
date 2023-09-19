from typing import Optional

import numpy as np


class Segment:
    def __init__(self, id_: int, _p: list[tuple[int, int]]):
        self.id = id_
        self.p: list[tuple[int, int]] = _p  # pixels
        self.a, self.b, self.c = 0, 0, 0  # sum of colour values
        self.m: list[int] = []  # mean colour
        self.min_y, self.min_x, self.max_y, self.max_x = -1, -1, -1, -1  # boundaries
        self.w, self.h = -1, -1  # dimensions


# recursively checks if neighbours are border pixels. directions range are 0..7.
def check_neighbours(s_: Segment, yy: int, xx: int, avoid_dir: Optional[int] = None):
    print(s_.id, ':', str(yy) + 'x' + str(xx), 'from', avoid_dir)

    next_ones: list[tuple[int, int, int]] = []
    if avoid_dir != 0 and yy > 0:  # northern
        n = (yy - 1, xx)
        if is_next_b(s_, *n): next_ones.append(n + (0,))
    if avoid_dir != 1 and yy > 0 and xx < (dim - 1):  # north-eastern
        n = (yy - 1, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (1,))
    if avoid_dir != 2 and xx < (dim - 1):  # eastern
        n = (yy, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (2,))
    if avoid_dir != 3 and yy < (dim - 1) and xx < (dim - 1):  # south-eastern
        n = (yy + 1, xx + 1)
        if is_next_b(s_, *n): next_ones.append(n + (3,))
    if avoid_dir != 4 and yy < (dim - 1):  # southern
        n = (yy + 1, xx)
        if is_next_b(s_, *n): next_ones.append(n + (4,))
    if avoid_dir != 5 and yy < (dim - 1) and xx > 0:  # south-western
        n = (yy + 1, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (5,))
    if avoid_dir != 6 and xx > 0:  # western
        n = (yy, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (6,))
    if avoid_dir != 7 and yy > 0 and xx > 0:  # north-western
        n = (yy - 1, xx - 1)
        if is_next_b(s_, *n): next_ones.append(n + (7,))

    for y_, x_, d in next_ones: check_neighbours(s_, y_, x_, d)


# checks if this is a border pixel and not detected before
def is_next_b(s_: Segment, yy: int, xx: int) -> bool:
    self_s = status[yy, xx]
    if self_s != s_.id: return False
    if b_status[yy, xx] is None:
        # noinspection PyTypeChecker
        check_if_border(self_s, yy, xx)
        if b_status[yy, xx]: return True
    return False


# checks if this pixel is in border
def check_if_border(s_, yy: int, xx: int) -> None:
    s_id = s_.id if isinstance(s_, Segment) else s_
    if xx == (dim - 1) or s_id != status[yy, xx + 1]:  # right
        set_is_border(s_, yy, xx)
        return
    if yy == (dim - 1) or s_id != status[yy + 1, xx]:  # bottom
        set_is_border(s_, yy, xx)
        return
    if xx == 0 or s_id != status[yy, xx - 1]:  # left
        set_is_border(s_, yy, xx)
        return
    if yy == 0 or s_id != status[yy - 1, xx]:  # top
        set_is_border(s_, yy, xx)
        return
    b_status[yy, xx] = False


def set_is_border(s_, yy: int, xx: int):
    if not isinstance(s_, Segment):
        s_ = next(s for s in segments if s.id == s_)
    b_status[yy, xx] = True
    s_.border.append([(100 / s_.w) * s_.min_x - xx, (100 / s_.h) * s_.min_y - yy])


dim: int = 4
status: np.ndarray = np.array([
    [0, 0, 0, 0, ],
    [0, 0, 0, 0, ],
    [0, 0, 0, 0, ],
    [0, 9, 9, 0, ],
])
segments: list[Segment] = [
    Segment(0, [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 0), (3, 3),
    ]),
    Segment(9, [
        (3, 1), (3, 2),
    ]),
]
# noinspection PyTypeChecker
b_status: np.ndarray[Optional[bool]] = np.repeat([np.repeat(None, dim)], dim, 0)
seg = segments[0]

# find the first encountering border pixel as a checkpoint
border_checkpoint: Optional[tuple[int, int]] = None
for p in seg.p:
    if b_status[*p] is None: check_if_border(seg, *p)
    if b_status[*p]:
        border_checkpoint = p
        break

# now start collecting all border pixels using that checkpoint
check_neighbours(seg, *border_checkpoint)
