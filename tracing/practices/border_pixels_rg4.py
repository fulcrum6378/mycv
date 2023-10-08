from typing import Optional

import numpy as np


class Segment:
    def __init__(self, id_: int, _p: list[tuple[int, int]]):
        self.id = id_
        self.p: list[tuple[int, int]] = _p  # pixels
        self.m: list[int] = []  # average colour


# noinspection PyTypeChecker
def is_next_b(org_s: Segment, yy: int, xx: int) -> bool:
    """ Checks if this is a border pixel and not detected before. """
    s_ = status[yy, xx]
    if s_ != org_s.id: return False
    if b_status[yy, xx] is None:
        check_if_border(s_, yy, xx)
        return b_status[yy, xx]
    return False


def check_if_border(s_id: int, yy: int, xx: int) -> None:
    """ Checks if this pixel is in border. """
    if (  # do NOT use "&&" for straight neighbours!
            (yy == 0 or s_id != status[yy - 1, xx]) or  # northern
            ((yy > 0 and xx < (dim - 1)) and s_id != status[yy - 1, xx + 1]) or  # north-eastern
            (xx == (dim - 1) or s_id != status[yy, xx + 1]) or  # eastern
            ((yy < (dim - 1) and xx < (dim - 1)) and s_id != status[yy + 1, xx + 1]) or  # south-eastern
            (yy == (dim - 1) or s_id != status[yy + 1, xx]) or  # southern
            ((yy < (dim - 1) and xx > 0) and s_id != status[yy + 1, xx - 1]) or  # south-western
            (xx == 0 or s_id != status[yy, xx - 1]) or  # western
            ((yy > 0 and xx > 0) and s_id != status[yy - 1, xx - 1])  # north-western
    ):
        b_status[yy, xx] = True
        if s_id not in s_border: s_border[s_id] = []
        s_border[s_id].append((
            (100.0 / s_dimensions[s_id][0]) * (s_boundaries[s_id][1] - xx),  # fractional X
            (100.0 / s_dimensions[s_id][1]) * (s_boundaries[s_id][0] - yy),  # fractional Y
        ))
    else:
        b_status[yy, xx] = False


dim: int = 4
status: np.ndarray = np.array([
    [1, 1, 1, 1, ],
    [1, 1, 1, 1, ],
    [1, 1, 1, 1, ],
    [1, 9, 9, 1, ],
])
segments: list[Segment] = [
    Segment(1, [
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
    1: [0, 0, 3, 3, ],
    9: [2, 1, 3, 2, ],
}
s_dimensions: dict[int, tuple[int, int]] = {  # width, height
    1: (4, 4), 9: (2, 1),
}
seg = segments[1]

# find the first encountering border pixel as a checkpoint
border_checkpoint: Optional[tuple[int, int]] = None
stack: list[list[int, int, int]] = []
y, x = 0, 0
for p in seg.p:
    if b_status[*p] is None: check_if_border(seg.id, *p)
    if b_status[*p]:
        y, x = p
        break

# then start collecting all border pixels using that checkpoint
stack.append([y, x, 0])
while len(stack) > 0:
    y, x, avoid_dir = stack[len(stack) - 1]
    stack.pop()
    print(str(y) + 'x' + str(x), 'from', avoid_dir)
    ny, nx = y, x
    if avoid_dir != 5 and y > 0:  # northern
        ny = y - 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 1])
    if avoid_dir != 6 and y > 0 and x < (dim - 1):  # north-eastern
        ny = y - 1
        nx = x + 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 2])
    if avoid_dir != 7 and x < (dim - 1):  # eastern
        nx = x + 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 3])
    if avoid_dir != 8 and y < (dim - 1) and x < (dim - 1):  # south-eastern
        ny = y + 1
        nx = x + 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 4])
    if avoid_dir != 1 and y < (dim - 1):  # southern
        ny = y + 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 5])
    if avoid_dir != 2 and y < (dim - 1) and x > 0:  # south-western
        ny = y + 1
        nx = x - 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 6])
    if avoid_dir != 3 and x > 0:  # western
        nx = x - 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 7])
    if avoid_dir != 4 and y > 0 and x > 0:  # north-western
        ny = y - 1
        nx = x - 1
        if is_next_b(seg, ny, nx): stack.append([ny, nx, 8])
