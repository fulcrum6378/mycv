## MyCV

This is a subproject of [**Mergen IV**](https://github.com/fulcrum6378/mergen_android)
in Python which helps with faster debugging of computer vision algorithms.
These methods are translated to C++ for the main project.
MyCV was initiated in 10 July 2023 and after a successful image analysis, translations began at 24 September.

The project divides the process of image analysis to the following steps:

### 1. /vis/

Tools for reading output from [**vis/camera.cpp**](
https://github.com/fulcrum6378/mergen_android/blob/master/cpp/vis/camera.cpp)

- [**rgb_to_bitmap.py**](vis/rgb_to_bitmap.py) : extracts RGB image frames from a single big file named "*vis.rgb*",
  and saves them in Bitmap (*.bmp) images with BMP metadata (from */vis/metadata*) at beginning of each file.

@ [test_yuv.py](vis/test_yuv.py) : displays a raw YUV bitmap image (*test.yuv*) using OpenCV and Matplotlib.

=> Output: BMP image frames

***

> [**config.py**](config.py) defines tweaks used in most steps.

### 2. /segmentation/: [Image Segmentation](https://en.wikipedia.org/wiki/Image_segmentation)

- **[Region-growing methods](https://en.wikipedia.org/wiki/Region_growing) (succeeded)**
    - [region_growing_1.py](segmentation/region_growing_1.py) : this method focuses on a pixel and analysed its
      neighbours, I left it incomplete and moved to the 2nd method, but then I realised this method was much better!
    - [region_growing_2.py](segmentation/region_growing_2.py) : this method focuses on a neighbour then determines
      if it fits in the same segment. It is more object-oriented than the previous one, and contains more boilerplate
      code! It takes **~22 seconds** here and ~5 seconds in C++ plus ~3.3 seconds in /tracing/ because data structure
      of "*segments*" is a map rather than a vector, making **~9 seconds** totally!
    - [region_growing_3.py](segmentation/region_growing_3.py) : an improved and completed version of the 1st method;
      it takes **~20 seconds** here.
    - [**region_growing_4.py**](segmentation/region_growing_4.py) : same as the 3rd method, but without recursion
      because of C++ restrictions, and segment IDs start from 0 not -1. It takes **~30 seconds** here,
      but **~2 to ~4 seconds** in C++ with a Samsung Galaxy A50 phone!
    - [region_growing_5.py](segmentation/region_growing_5.py) : same as the 4th method, but it compares colours of all
      pixels of a segment with the very first pixel it finds. The results we like a KMeans filter, which I didn't like!
- [Clustering methods](https://en.wikipedia.org/wiki/Cluster_analysis)
    - [clustering_1d.py](segmentation/clustering_1d.py) : clustering all pixels in a 1-dimensional way...
      left incomplete; not logically suitable!

=> Output: segmentation data extracted using [pickle](https://docs.python.org/3/library/pickle.html) library

***

### 3. /tracing/: [Image Tracing](https://en.wikipedia.org/wiki/Image_tracing)

Trying to interpret segments of images in terms of [vector graphics](https://en.wikipedia.org/wiki/Vector_graphics)
instead of [raster images](https://en.wikipedia.org/wiki/Raster_graphics); but the vectors must be able to be easily
compared to others of their kind. **It must**:

- **Detect Shapes**: it calculates path points in relative percentage-like numbers, just like a vector image.
  Vector paths can be stored in 2 different types:
    1. **8-bit**: position of each point will range from 0 to 256 (uint8_t, unsigned byte).
    2. **16-bit**: position of each point will range from 0 to 65,535 (uint16_t, unsigned short).
- **Detect Gradients**: it temporarily computes an average colour of all pixels.

Because outputs of each segmentation method is not the same, each method must have its own implementation of tracing,
and those implementations will have the suffixes referring to those method (e.g. "*_rg4*").

#### Tracing methods:

- *Surrounder*: finds a random border pixel, then navigates through its neighbours until it detects all border
  pixels of a segment. It messes up when a shape has inner borders.
- **Comprehender**: analyses all pixels if they are border ones.

Because of C++ maximum stack restrictions (stack overflow), [surrounder_rg4.py](tracing/surrounder_rg4.py)
was forked from [surrounder_rg3.py](tracing/surrounder_rg3.py) with no recursion.

=> Output: vector data in JSON files (good for debugging, instead of unreadable pickle dumps)

***

### 4. /storage/

Shapes and their details need to be temporarily stored in a [non-volatile memory](
https://en.wikipedia.org/wiki/Non-volatile_memory) (SSD/hard disk/SD), in a way that it enables super-fast searching
and easily finding similar shapes. This is actually some kind of [Short-Term Memory](
https://en.wikipedia.org/wiki/Short-term_memory). First I wanted to put the data in a 4+ dimensional array, making a
[Datacube](https://en.wikipedia.org/wiki/Data_cube), but it was a bad idea. Then...

1. [feature_database.py](storage/feature_database.py) : I wanted to separate features/details of shapes into separate
   small databases and this code was intended to be a super-fast mini-DBMS, but due to limitations of writing/appending
   into files, I realised this method was not even practical!
2. [sequence_files_1.py](storage/sequence_files_1.py) : in this method we save shapes and their details in storage,
   much more separately than the previous method. Each feature will have a folder (resembling a table in a database),
   and also shapes are stored in a separate folder. Quantities of feature are clustered and IDs of their shapes are
   put into separate files.
3. [**sequence_files_2.py**](storage/sequence_files_2.py) : same as the previous, except that *ratio* index doesn't
   store the exact float number anymore, it just stores mere shape IDs.

- [datacube_1.py](storage/datacube_1.py) : I figured maybe the idea of a Datacube might be useful in terms of a
  [Long-Term Memory](https://en.wikipedia.org/wiki/Long-term_memory) rather than in short-term. But this time,
  our datacube is a 4-dimensional **dict/map** rather than an *array*.

=> Output: data properly and efficiently structured and stored in a persistent memory

***

### 5. /comparison/

It shall extract a shape from /storage/output/ and look for similar items in the same directory,
using the databases of the previous step.
Therefore, every database will have its own implementation of comparison.

***

### 6. /resegmentation/: Object Tracking

Visual objects must be tracked across frames, this method is a continuity of Segmentation and must be integrated to it.
Not to be mistaken with /tracing/, but like that, each method should have its own implementation of Segmentation.

***

### /debug/

This section provides you with server-client tools for easily debugging the C++ implementations over a network.

[**run.ps1**](debug/run.ps1) executes [*main.py*](debug/main.py) which accepts some command codes listed in its header.
Most commands require your Android phone and your PC to be connected to the same network (like Wi-Fi).
Few of them also require your phone to be listed in [*ADB*](https://developer.android.com/tools/adb) [`$ adb devices`].

***

### License

```
Copyright © Mahdi Parastesh - All Rights Reserved.
```
