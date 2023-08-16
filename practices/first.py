from datetime import datetime

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp'))
dim = 1088
maxDif = 20


def is_the_same(a: np.ndarray, b: np.ndarray) -> bool:
    return abs(int(a[0]) - int(b[0])) <= maxDif \
        and abs(int(a[1]) - int(b[1])) <= maxDif \
        and abs(int(a[2]) - int(b[2])) <= maxDif


time = datetime.now()
out = np.zeros((dim, dim, 3), dtype=np.uint8)
for y in range(dim):
    for x in range(dim):
        # out[y, x] = arr[y, x]
        this = arr[y][x]
        frontier = False
        if y >= 0 and not is_the_same(this, arr[y - 1, x]): frontier = True
        if y < dim and not is_the_same(this, arr[y + 1, x]): frontier = True
        if x >= 0 and not is_the_same(this, arr[y, x - 1]): frontier = True
        if x < dim and not is_the_same(this, arr[y, x + 1]): frontier = True

        if frontier:
            out[y, x] = 255, 0, 0
        else:
            out[y, x] = 255, 255, 255

print('Took', datetime.now() - time)

plot.imshow(out)
plot.show()
