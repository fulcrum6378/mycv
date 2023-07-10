import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# noinspection PyTypeChecker
img = np.asarray(Image.open('vis/1687856959415777.bmp'))

plot.imshow(img)
plot.show()

colour = img[80][80]
plot.imshow(Image.fromarray(
    np.repeat(np.array([np.repeat(np.array([colour]), 100, 0)]), 100, 0)))
plot.show()
