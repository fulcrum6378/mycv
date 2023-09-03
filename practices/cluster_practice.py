import colorsys

import matplotlib.pyplot as plt
import sklearn.cluster as skc

# https://www.w3schools.com/python/python_ml_hierarchial_clustering.asp
# https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html

#    red, blu, lgr,red, dgr, orn
h = [255, 175, 81, 250, 100, 20]
s = [255, 255, 128, 255, 255, 200]
v = [255, 255, 255, 250, 100, 255]
data = list(zip(h, s, v))

# from scipy.cluster.hierarchy import linkage
# linkage_data = linkage(data, method='ward', metric='euclidean')

labels = skc.KMeans(n_clusters=3).fit_predict(data, sample_weight=[10, 1, 1])
# sample_weight.shape == (3,), expected (6,)!
print("Results:", labels)


# the rest is all about MatPlotLib
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
ax.set_zlabel('Value')
plt.show()

# THIS APPROACH FAILED TOO!!! Hue must be taken far more important than saturation and value!
# Is there some kind of "Weighted Clustering" just like Weighted Mean?
