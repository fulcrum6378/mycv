from datetime import datetime

import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

whole_time = datetime.now()
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV')).copy()
arr.setflags(write=True)
dim = 1088

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
print('Whole time:', datetime.now() - whole_time)  # mere File->Image->RGB->HSV->RGB->Image->ImShow: 0:00:00.430~~480
plot.show()
