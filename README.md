## MyCV

This is a subproject of [**Mergen IV**](https://github.com/fulcrum6378/mergen_android)
in Python which helps with faster debugging of computer vision algorithms.
These algorithms are intended to be translated to C++ inside the main project.
MyCV was initiated in 10 July 2023.

It contains the following parts (sorted by precedence of usage):

### 1. /vis/

This section is dedicated to extraction of Bitmap (*.bmp) images from [**vis/camera.cpp**](
https://github.com/fulcrum6378/mergen_android/blob/master/cpp/vis/camera.cpp)
which outputs raw RGB streams without BMP metadata (*vis.rgb*).

=> Output: BMP image frames

***

### 2. /segmentation/: [Image Segmentation](https://en.wikipedia.org/wiki/Image_segmentation)

- **[Region-growing methods](https://en.wikipedia.org/wiki/Region_growing) (succeeded)**
    - [region_growing_1.py](segmentation/region_growing_1.py) : this method focuses on a pixel and analysed its
      neighbours, I left it incomplete and moved to the 2nd method, but then I realised this method was much better!
    - [region_growing_2.py](segmentation/region_growing_2.py) : this method focuses on a neighbour then determines
      if it fits in the same segment. It is more object-oriented than the previous one, and contains more boilerplate
      code! It takes **~22 seconds**.
    - [region_growing_3.py](segmentation/region_growing_3.py) : an improved and completed version of the 1st method;
      it takes **~7 to ~8 seconds**.
    - [region_growing_3.py](segmentation/region_growing_3.py) : same as the 3rd method, but without recursion,
      and it uses YCbCr instead of YUV as in the Android version. It takes **~11 seconds**.
- [Clustering methods](https://en.wikipedia.org/wiki/Cluster_analysis)
    - [clustering_1d.py](segmentation/clustering_1d.py) : clustering all pixels in a 1-dimensional way...
      left incomplete; not logically suitable!

=> Output: segmentation data extracted using [pickle](https://docs.python.org/3/library/pickle.html) library

***

### 3. /tracing/: [Image Tracing](https://en.wikipedia.org/wiki/Image_tracing)

Trying to interpret segments of images in terms of [vector graphics](https://en.wikipedia.org/wiki/Vector_graphics)
instead of [raster images](https://en.wikipedia.org/wiki/Raster_graphics); but the vectors must be able to be easily
compared to others of their kind. It must:

- Detect Shapes
- Detect Gradients: for now we get an average colour of all pixels.

Since segmentation output is not always the same, each segmentation method must have its own tracing implementation.
Methods used:

- **Surrounder**: it finds a random border pixel, then navigates through its neighbours until it detects all border
  pixels of a segment.

=> Output: vector data in JSON files (good for debugging, instead of pickle dumps)

***

### 4. /storage/

Shapes and their details need to be temporarily stored in a [non-volatile memory](
https://en.wikipedia.org/wiki/Non-volatile_memory) (SSD/hard disk/SD), in a way that it enables super-fast searching
and easily finding similar shapes. First I wanted to put the data in a 4+ dimensional [datacubes](
https://en.wikipedia.org/wiki/Data_cube), but it was a bad idea. Then...

1. [feature_database.py](storage/feature_database.py) : I wanted to separate features/details of shapes into separate
   small databases and this code was intended to be a super-fast mini-DBMS, but due to limitations of writing/appending
   into files, I realised this method was not even practical!
2. [**sequence_files.py**](storage/sequence_files.py) : in this method we save shapes and their details in storage,
   much more separately than the previous method. Each feature will have a folder (resembling a table in a database),
   and also shapes are stored in a separate folder. Quantities of feature are clustered and IDs of their shapes are
   put into separate files.

=> Output: data properly and wisely structured and stored in a persistent memory

***

### 5. /comparison/

It shall extract a shape from databases made in /storage/ and look for similar items.

***

### 6. /grouping/ (to be implemented)

Shapes related to an object will be stored in another kind of database as a **Visual Object**.
Visual objects along with *auditory objects* and *touch patterns* will be related to an ultimate
**Object** which the brain addresses as an entity.

***

### License

```
Copyright © Mahdi Parastesh - All Rights Reserved.
```
