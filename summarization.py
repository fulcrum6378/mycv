import matplotlib.pyplot as plot
import numpy as np
from PIL import Image
import sqlite3 as sql

# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV'))
dim = 1088

# Learning methods:
# 1. Reinforcement Learning (organisms, slow, dangerous!)
# 2. Autonomous Learning (as a machine, fast)
#   2.1. Learning everything just-in-time (consumes much energy)
#   2.2. Learning things randomly
#   2.3. Learning specific kinds of things (stupid!)
# In either way except 2.1, there can be a stress factor which boosts learning as well as draining energy.

# Database:
# Shape: 1. (colour/gradient/pattern), 2. [shape](BREAK THIS)
# Vector: 1. array of shapes and probabilistic positions
# Object (from all senses, PROBABILISTICALLY)

# Colour is more important than shape.
# We can also instead, collect raster images in the storage and create Shapes summaries of them, which is a bad idea!
# we could also store a simplified version of those images!
# Forgetting can be accomplished by setting a last modified timestamp on each shape/vector/object.

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
plot.show()
