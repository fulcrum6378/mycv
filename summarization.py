import matplotlib.pyplot as plot
import numpy as np
from PIL import Image

# noinspection PyTypeChecker
arr: np.ndarray = np.asarray(Image.open('vis/2/1689005849386887.bmp').convert('HSV'))
dim = 1088

# WE DON'T NEED 90%+ OF THE DATA WE GET FROM THE CAMERA!
# Humans' caring has a percentage that changes by the amount of stress they have!
# We should later be able to tweak the "attention to details"!
# We may even be able to avoid storing images! We just need a summary!
# CREATE A SIMPLE SUMMARY OF THE IMAGE!
# So should it be either ... ?!?!?
#   - SIMPLIFICATION
#   - SUMMARIZATION  (I CHOOSE THIS, for the great extra performance)

# Summarization shouldn't detect objects, because it would be a mess!
# Summarization should only summarize and then let the next stage decide if anything is an object.
# Maybe all those vectors are 1 single object.
# We must forget all about the Object Detection shit! It's not how it works.
# MANY SPECIFIC DETAILS ALSO SHOULD BE OMITTED!
# Colour is more important than shape.
# We humans don't process most of the things we see. Everything is reward-based here!
# What we're programming has no specific target!

# TODO HOW SHOULD MERGEN LEARN THEN?
# What should Mergen look for? What purpose? Where to start?!?
# It can also try to learn everything UNLIKE organisms! It might consume much energy but it'll grow knowledge
# so faster than human beings.
# Our options:
#   1. Learn everything
#   2. Learn based on rewards
#   3. Learn specific things?!? (based on certain criteria)
#   4. Learn randomly
# It cannot figure out which things it needs to learn which will be useful for [e.g. helping human beings]
# while it knows absolutely nothing!
# The third option can only be used in these ways: for example, learn only about red things or loud noises,
# or hard touch events! which sounds crazy!

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
plot.show()

# Vector Index Database (VID):
# It stores references to vectors and the vectors will reside in the persistent memory.
# I think we should make some kind of database, whose searching can be accomplished by either ...
#   - shapes
#   - colours
# We'll have to sort shapes and colours. Well sorting colours is piece of cake!
# But sorting SHAPES...!!
# We can break down shapes by their attributes.

# Summarization must detect shapes and their (colour/gradient/pattern).
# Shapes will be related to Visionary Objects (vectors) with probabilistic positions.
# Vectors will be related to Global Objects (which can relate to audios and touch events),
# but everything must be PROBABILISTIC!
