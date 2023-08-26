from functools import cmp_to_key

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

colours: list[list[int]] = [
    [250, 255, 250],
    [200, 255, 200],
    [150, 255, 150],
    [100, 255, 100],
    [50, 255, 50],
    [0, 255, 0],
]


def cluster(a: list[int], b: list[int]) -> int:
    dif = a[0] - b[0]
    if dif < 0:
        return -1
    elif dif > 0:
        return 1
    else:
        return 0


colours.sort(key=cmp_to_key(cluster))  # sorted(colours, key=cmp_to_key(cluster))

plot.imshow(Image.fromarray(np.array([colours], dtype=np.uint8), 'HSV').convert('RGB'))
# plot.imshow(colours)
plot.show()
