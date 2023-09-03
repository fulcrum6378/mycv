import colorsys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.base import BaseEstimator
import sklearn.cluster as skc
from sklearn.feature_selection import SelectFromModel  # feature-weighted clustering

# https://www.w3schools.com/python/python_ml_hierarchial_clustering.asp
# https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html

#    red, blu, lgr,red, dgr, orn
h = [255, 175, 81, 250, 100, 20]
s = [255, 255, 128, 255, 255, 200]
v = [255, 255, 255, 250, 100, 255]
data = list(zip(h, s, v))

# from scipy.cluster.hierarchy import linkage
# linkage_data = linkage(data, method='ward', metric='euclidean')

weights = np.array([100, 1, 1])
estimator: BaseEstimator = skc.KMeans(n_clusters=3)
selector = SelectFromModel(estimator, max_features=3, importance_getter=lambda _estimator: weights)
selector.fit(data)
print("Labels:", selector.estimator_.labels_)

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
ax.set_zlabel('Brightness')
plt.show()

# THIS APPROACH FAILED TOO!!! Hue must be taken far more important than saturation and value!
# Is there some kind of "Weighted Clustering" just like Weighted Mean?
