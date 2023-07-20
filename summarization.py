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

plot.imshow(Image.fromarray(arr, 'HSV').convert('RGB'))
plot.show()

# After Summarization, we will either ...
#   - Store the objects separately.
#   - Store the separate objects in ONE file.
#   - Do no object separation; just store the vector!
# I think we should make some kind of database, whose searching can be accomplished by either ...
#   - shapes
#   - colours
# We'll have to sort shapes and colours. Well sorting colours is piece of cake!
# But sorting SHAPES...!!
