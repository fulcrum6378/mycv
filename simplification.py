import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp'))
dim = 1080

# Don't create another image, just alter the existing image.
# WE DON'T NEED 90%+ OF THE DATA WE GET FROM THE CAMERA!

# TODO

plot.imshow(arr)
plot.show()

# After Simplification, we should recognise patterned objects too and finally group every object.
# Then we will either ...
#   - Store the objects separately.
#   - Store the separate objects in ONE file.
#   - Do no object separation; just store the vector!
# I think we should make some kind of database, whose searching can be accomplished by either ...
#   - shapes
#   - colours
# We'll use the Binary Search for this!
# We'll have to sort shapes and colours. Well sorting colours is piece of cake!
# But sorting SHAPES...!!
