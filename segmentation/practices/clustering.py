import colorsys

import matplotlib.pyplot as plt
import sklearn.cluster as skc

#    red, blu, lgr,red, dgr, orn
h = [255, 175, 81, 250, 100, 20]
s = [255, 255, 128, 255, 255, 200]
v = [255, 255, 255, 250, 100, 255]
data = list(zip(h, s, v))

for i in range(len(s)):
    s[i] *= 0.3
    v[i] *= 0.3  # maximum should be 0.3
weighted_data = list(zip(h, s, v))
print("Labels:", skc.KMeans(n_clusters=4).fit_predict(weighted_data))
# correct is 1 2 0 1 0 3
# TODO COMPUTE n_clusters, BUT HOW?!?!?!?!?!?

#

# the rest is all about MatPlotLib
# https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html
# prepare the points in the plot
ax: plt.Axes = plt.figure().add_subplot(projection='3d')
for c in range(len(data)):
    rgb = colorsys.hsv_to_rgb(data[c][0] / 255.0, data[c][1] / 255.0, data[c][2] / 255.0)
    ax.scatter(data[c][0], data[c][1], data[c][2],  # c=labels[c],
               color=rgb)

# show the points in the plot
ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
# noinspection PyUnresolvedReferences
ax.set_zlabel('Brightness')
plt.show()

# THIS APPROACH FAILED TOO!!! Hue must be taken far more important than saturation and value!
# Is there some kind of "Weighted Clustering" just like Weighted Mean?
