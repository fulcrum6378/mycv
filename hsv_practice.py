import matplotlib.pyplot as plot
from PIL import Image

plot.imshow(Image.new(mode='HSV', size=(100, 100), color=(255, 255, 255)))
plot.show()
