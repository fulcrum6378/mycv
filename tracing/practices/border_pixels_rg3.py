from typing import Optional

import numpy as np


class Segment:
    def __init__(self, id_: int, _p: list[tuple[int, int]]):
        self.id = id_
        self.p: list[tuple[int, int]] = _p  # pixels
        self.m: list[int] = []  # average colour


# recursively checks if neighbours are border pixels. directions range are 0..7.
def check_neighbours(s_: Segment, yy: int, xx: int, avoid_dir: Optional[int] = None):
    print(s_.id, ':', str(yy) + 'x' + str(xx), 'from', avoid_dir)

    if avoid_dir != 0 and yy > 0:  # northern
        n = (yy - 1, xx)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 0)
    if avoid_dir != 1 and yy > 0 and xx < (dim - 1):  # north-eastern
        n = (yy - 1, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 1)
    if avoid_dir != 2 and xx < (dim - 1):  # eastern
        n = (yy, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 2)
    if avoid_dir != 3 and yy < (dim - 1) and xx < (dim - 1):  # south-eastern
        n = (yy + 1, xx + 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 3)
    if avoid_dir != 4 and yy < (dim - 1):  # southern
        n = (yy + 1, xx)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 4)
    if avoid_dir != 5 and yy < (dim - 1) and xx > 0:  # south-western
        n = (yy + 1, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 5)
    if avoid_dir != 6 and xx > 0:  # western
        n = (yy, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 6)
    if avoid_dir != 7 and yy > 0 and xx > 0:  # north-western
        n = (yy - 1, xx - 1)
        if is_next_b(s_, *n): check_neighbours(s_, n[0], n[1], 7)


# checks if this is a border pixel and not detected before
# noinspection PyTypeChecker
def is_next_b(org_s: Segment, yy: int, xx: int) -> bool:
    if b_status[yy, xx] is None:
        s_ = status[yy, xx]
        check_if_border(s_, yy, xx)
        if b_status[yy, xx] and s_ == org_s.id:
            return True
    return False
    # s_ = status[yy, xx]
    # if s_ == org_s.id: return False
    # if b_status[yy, xx] is None:
    #    check_if_border(s_, yy, xx)
    #    return b_status[yy, xx]
    # return False


# checks if this pixel is in border
def check_if_border(s_id: int, yy: int, xx: int) -> None:
    if (xx == (dim - 1) or s_id != status[yy, xx + 1] or  # right
            yy == (dim - 1) or s_id != status[yy + 1, xx] or  # bottom
            xx == 0 or s_id != status[yy, xx - 1] or  # left
            yy == 0 or s_id != status[yy - 1, xx]):  # top
        set_is_border(s_id, yy, xx)
        return
    b_status[yy, xx] = False


def set_is_border(s_id: int, yy: int, xx: int):
    b_status[yy, xx] = True
    if s_id not in s_border: s_border[s_id] = []
    s_border[s_id].append((
        (100.0 / s_dimensions[s_id][0]) * (s_boundaries[s_id][1] - xx),  # fractional X
        (100.0 / s_dimensions[s_id][1]) * (s_boundaries[s_id][0] - yy),  # fractional Y
    ))


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
s_border: dict[int, list[tuple[float, float]]] = {}
s_boundaries: dict[int, list[int, int, int, int]] = {  # min_y, min_x, max_y, max_x
    0: [0, 0, 3, 3, ],
    9: [2, 1, 3, 2, ],
}
s_dimensions: dict[int, tuple[int, int]] = {  # width, height
    0: (4, 4), 9: (2, 1),
}
seg = segments[0]

# find the first encountering border pixel as a checkpoint
border_checkpoint: Optional[tuple[int, int]] = None
for p in seg.p:
    if b_status[*p] is None: check_if_border(seg.id, *p)
    if b_status[*p]:
        border_checkpoint = p
        break

# now start collecting all border pixels using that checkpoint
check_neighbours(seg, *border_checkpoint)
