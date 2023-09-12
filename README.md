## MyCV

This is a subproject of [**Mergen IV**](https://github.com/fulcrum6378/mergen_android)
in Python which helps with faster debugging of computer vision algorithms.
These algorithms are intended to be translated to C++ inside the main project.
MyCV was initiated in 10 July 2023.

It contains the following parts (sorted by precedence of usage):

#### 1. /vis/

This section is dedicated to extraction of Bitmap (*.bmp) images from [**vis/camera.cpp**](
https://github.com/fulcrum6378/mergen_android/blob/master/cpp/vis/camera.cpp)
which outputs raw RGB streams without BMP metadata (*vis.rgb*).

#### 2. /segmentation/: [**Image Segmentation**](https://en.wikipedia.org/wiki/Image_segmentation)

Testing various methods of Image Segmentation:

- [**Region-growing methods**](https://en.wikipedia.org/wiki/Region_growing)
- [Clustering methods](https://en.wikipedia.org/wiki/Cluster_analysis)

#### 3. /interpretation/

Trying to interpret segments of images in terms of [vector graphics](https://en.wikipedia.org/wiki/Vector_graphics)
instead of [raster images](https://en.wikipedia.org/wiki/Raster_graphics)...

#### + /practices/

Testing miscellaneous stuff...
