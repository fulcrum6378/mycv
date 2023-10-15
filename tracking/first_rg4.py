import os
from datetime import datetime

import cv2
import matplotlib.pyplot as plot
import numpy as np

from config import bitmap2, bitmap_folder
from segmentation.region_growing_4 import segments, status

print('----------------')

# read the SECOND image
loading_time = datetime.now()
arr: np.ndarray = cv2.cvtColor(cv2.imread(os.path.join('vis', 'output', bitmap_folder, bitmap2 + '.bmp')),
                               cv2.COLOR_BGR2YUV)
print('Loading time:', datetime.now() - loading_time)

# TODO
