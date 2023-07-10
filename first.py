import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# noinspection PyTypeChecker
arr = np.asarray(Image.open('vis/2/1689005849386887.bmp'))

arr

plot.imshow(arr)
plot.show()
