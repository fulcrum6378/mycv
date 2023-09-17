from typing import Optional


class Pixel:
    def __init__(self, y: int, x: int, s: int):
        self.c: list[int] = []
        self.y: int = y
        self.x: int = x
        self.s: int = s
        self.b: Optional[bool] = None

    @staticmethod
    def get_pos(_y: int, _x: int) -> int:
        return (_y * dim) + _x

    # direction is 0..7
    def check_neighbours(self, avoid_dir: Optional[int] = None):
        print(self.__dict__, 'from', avoid_dir)

        next_ones: list[tuple[Pixel, int]] = []
        if avoid_dir != 0 and self.y > 0:  # northern
            n = pixels[Pixel.get_pos(self.y - 1, self.x)]
            if n.is_next_b(): next_ones.append((n, 0))
        if avoid_dir != 1 and self.y > 0 and self.x < (dim - 1):  # north-eastern
            n = pixels[Pixel.get_pos(self.y - 1, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 1))
        if avoid_dir != 2 and self.x < (dim - 1):  # eastern
            n = pixels[Pixel.get_pos(self.y, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 2))
        if avoid_dir != 3 and self.y < (dim - 1) and self.x < (dim - 1):  # south-eastern
            n = pixels[Pixel.get_pos(self.y + 1, self.x + 1)]
            if n.is_next_b(): next_ones.append((n, 3))
        if avoid_dir != 4 and self.y < (dim - 1):  # southern
            n = pixels[Pixel.get_pos(self.y + 1, self.x)]
            if n.is_next_b(): next_ones.append((n, 4))
        if avoid_dir != 5 and self.y < (dim - 1) and self.x > 0:  # south-western
            n = pixels[Pixel.get_pos(self.y + 1, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 5))
        if avoid_dir != 6 and self.x > 0:  # western
            n = pixels[Pixel.get_pos(self.y, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 6))
        if avoid_dir != 7 and self.y > 0 and self.x > 0:  # north-western
            n = pixels[Pixel.get_pos(self.y - 1, self.x - 1)]
            if n.is_next_b(): next_ones.append((n, 7))

        for n, d in next_ones: n.check_neighbours(d)

    def is_next_b(self) -> bool:
        if self.b is None:
            self.check_if_in_border()
            if self.b and self.s == s_id:
                return True
        return False

    def check_if_in_border(self) -> None:
        if self.x < (dim - 1):  # right
            _n = pixels[Pixel.get_pos(self.y, self.x + 1)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.y < (dim - 1):  # bottom
            _n = pixels[Pixel.get_pos(self.y + 1, self.x)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.x > 0:  # left
            _n = pixels[Pixel.get_pos(self.y, self.x - 1)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return
        if self.y > 0:  # top
            _n = pixels[Pixel.get_pos(self.y - 1, self.x)]
            if self.s != _n.s:
                self.set_is_border()
                return
        else:
            self.set_is_border()
            return

    def set_is_border(self):
        seg.border.add((self.y, self.x))
        self.b = True


class Segment:
    def __init__(self, _p: list[int]):
        self.p: list[int] = _p  # pixels
        self.a: list[int] = []  # colour A values
        self.b: list[int] = []  # colour B values
        self.c: list[int] = []  # colour C values
        self.m: list[int] = []  # mean colour
        self.border: set[tuple[int, int]] = set()


dim: int = 4
pixels: list[Pixel] = [
    Pixel(0, 0, 0), Pixel(0, 1, 0), Pixel(0, 2, 0), Pixel(0, 3, 0),
    Pixel(1, 0, 0), Pixel(1, 1, 0), Pixel(1, 2, 0), Pixel(1, 3, 0),
    Pixel(2, 0, 0), Pixel(2, 1, 0), Pixel(2, 2, 0), Pixel(2, 3, 0),
    Pixel(3, 0, 0), Pixel(3, 1, 9), Pixel(3, 2, 9), Pixel(3, 3, 0),
]
s_id = 0
seg = Segment([
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 15,  # 13, 14,
])

# find the first encountering border pixel as a checkpoint
border_checkpoint: Optional[Pixel] = None
for p in seg.p:
    _p = pixels[p]
    if _p.b is None: _p.check_if_in_border()
    if _p.b:
        border_checkpoint = _p
        break

# now start collecting all border pixels using that checkpoint
border_checkpoint.check_neighbours()
