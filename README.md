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

- **[Region-growing methods](https://en.wikipedia.org/wiki/Region_growing) (succeeded)**
- [Clustering methods](https://en.wikipedia.org/wiki/Cluster_analysis) (unsuitable)

I implemented 2 kinds of region-growing methods and the latter worked adequately.
The first method focused on a pixel and analysed its neighbours, which didn't work fine.
The second one focused on a **neighbour** then determined if it fits in the same segment.
Clustering methods though aren't suited for this kind of job.

#### 3. /tracing/: [**Image Tracing**](https://en.wikipedia.org/wiki/Image_tracing)

Trying to interpret segments of images in terms of [vector graphics](https://en.wikipedia.org/wiki/Vector_graphics)
instead of [raster images](https://en.wikipedia.org/wiki/Raster_graphics); but the vectors must be able to be easily
compared to others of their kind. It must:

- Detect Shapes: for now we collect coordinates of border pixels.
- Detect Gradients: for now we get an average colour of all pixels.

#### 4. /storage/

We can put comparable features of the **Shape**s in a [**multidimensional database**](
https://en.wikipedia.org/wiki/Multidimensional_analysis).

#### 5. /comparison/ (not yet implemented)

It must search a *Shape* in our multidimensional database.

#### 6. /grouping/ (not yet implemented)

Shapes related to an object will be stored in another kind of database as a **Visual Object**.
Visual objects along with *auditory objects* and *touch patterns* will be related to an ultimate
**Object** which the brain addresses as an entity.

#### + /practices/

Testing miscellaneous codes...
