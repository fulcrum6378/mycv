import sys
from datetime import datetime

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# read the image
whole_time = datetime.now()
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088
sys.setrecursionlimit(dim * dim)

# TODO

# show the image
plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)
plot.show()
