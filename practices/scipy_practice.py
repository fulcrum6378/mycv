import colorsys

import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage
from sklearn.cluster import AgglomerativeClustering

# https://www.w3schools.com/python/python_ml_hierarchial_clustering.asp
# https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html

#   red,blue,green,red,green,orange
h = [255, 175, 81, 250, 100, 20]
s = [255, 255, 128, 255, 255, 200]
v = [255, 255, 255, 250, 100, 255]
# h = [0, 255]
# s = [0, 255]
# v = [0, 255]

ax: plt.Axes = plt.figure().add_subplot(projection='3d')

data = list(zip(h, s, v))
# linkage_data = linkage(data, method='ward', metric='euclidean')

hierarchical_cluster = AgglomerativeClustering(n_clusters=3, metric='euclidean', linkage='ward')
labels = hierarchical_cluster.fit_predict(data)

print(labels)
# print(type(labels), len(labels))

for c in range(len(data)):
    rgb = colorsys.hsv_to_rgb(data[c][0] / 255.0, data[c][1] / 255.0, data[c][2] / 255.0)
    ax.scatter(data[c][0], data[c][1], data[c][2],  # c=labels[c],
               color=rgb)

ax.set_xlabel('Hue')
ax.set_ylabel('Saturation')
ax.set_zlabel('Value')
plt.show()

# THIS APPROACH FAILED TOO!!! Hue must be taken far more important than saturation and value!
# Is there some kind of "Weighted Clustering" just like Weighted Mean?
