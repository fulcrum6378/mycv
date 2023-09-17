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
# TODO ignored bug; it works like this:
# 0, 1, 2, 3, 7, 11, 15, 10, 9, (SKIPS 12) and goes to 8, then comes back to 12, then GETS CONFUSED!!!!!!
s_id = 0
seg = Segment([
    0, 1, 2, 3,
    4, 5, 6, 7,
    8, 9, 10, 11,
    12, 15,  # 13, 14,
])

# find the first encountering border pixel as a checkpoint
opposites = {
    0: 4, 1: 5, 2: 6, 3: 7,
    4: 0, 5: 1, 6: 2, 7: 3
}
border_checkpoint: Optional[Pixel] = None
for p in seg.p:
    _p = pixels[p]
    if _p.b is None: _p.check_if_in_border()
    if _p.b:
        border_checkpoint = _p
        break
print(border_checkpoint.__dict__)

# now start collecting all border pixels using that checkpoint
direction: int = 0  # 0..7
avoid_dir: Optional[int] = None
this_b: Optional[Pixel] = None  # we could use do...while
i = 0
while this_b is None or this_b.y != border_checkpoint.y or this_b.x != border_checkpoint.x:
    print('while1')
    if this_b is None: this_b = border_checkpoint
    this_dir = direction
    next_b = None
    while next_b is None:
        print('while2 at', this_dir)
        if this_dir == avoid_dir: raise Exception("KIR")

        # look at the only 1 direction each turn
        if this_dir == 0 and this_b.y > 0:  # northern
            next_b = pixels[Pixel.get_pos(this_b.y - 1, this_b.x)]
        elif this_dir == 1 and this_b.y > 0 and this_b.x < (dim - 1):  # north-eastern
            next_b = pixels[Pixel.get_pos(this_b.y - 1, this_b.x + 1)]
        elif this_dir == 2 and this_b.x < (dim - 1):  # eastern
            next_b = pixels[Pixel.get_pos(this_b.y, this_b.x + 1)]
        elif this_dir == 3 and this_b.y < (dim - 1) and this_b.x < (dim - 1):  # south-eastern
            next_b = pixels[Pixel.get_pos(this_b.y + 1, this_b.x + 1)]
        elif this_dir == 4 and this_b.y < (dim - 1):  # southern
            next_b = pixels[Pixel.get_pos(this_b.y + 1, this_b.x)]
        elif this_dir == 5 and this_b.y < (dim - 1) and this_b.x > 0:  # south-western
            next_b = pixels[Pixel.get_pos(this_b.y + 1, this_b.x - 1)]
        elif this_dir == 6 and this_b.x > 0:  # western
            next_b = pixels[Pixel.get_pos(this_b.y, this_b.x - 1)]
        elif this_dir == 7 and this_b.y > 0 and this_b.x > 0:  # north-western
            next_b = pixels[Pixel.get_pos(this_b.y - 1, this_b.x - 1)]

        # now check if that neighbour is a border one
        if next_b is not None:
            if next_b.b is not None:
                next_b = None
            else:
                next_b.check_if_in_border()
                if not next_b.b or next_b.s != s_id:
                    next_b = None
                else:
                    print(next_b.y, next_b.x)
                    break

        this_dir += 1
        if avoid_dir is not None and this_dir == avoid_dir: this_dir += 1
        if this_dir > 7: this_dir = this_dir - 7
    if next_b is None: raise Exception("KIR")
    this_b = next_b
    direction = this_dir
    avoid_dir = opposites[direction]
    # print('Border pixels:', len(seg.border))
    print(this_b.__dict__, 'to', direction)
    if i == 10:
        quit()
    i += 1
