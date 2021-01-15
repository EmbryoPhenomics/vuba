# Vuba 

Vuba is an easy to use library for constructing [`OpenCV`](https://opencv.org/) HighGUI interfaces. 

* **Documentation**: 
* **Example scripts**:
* **Installation**: 
* **Contributing**:
* **Source code**:

We developed this library to make coding up computer vision interfaces fast and efficient, allowing users to focus on their given application and bypass the challenges associated with developing a working user interface. We have since extended this to other areas of the [`OpenCV`](https://opencv.org/) library, writing wrappers where we feel the reduction in code verbosity improves both readability and reduces complexity in codebases. 

Currently the library is split up into three modules:

* [**gui**](https://github.com/EmbryoPhenomics/cvu/blob/main/cvu/gui.py) - [`OpenCV`](https://opencv.org/) HighGUI constructors, for both individual/multiple images and video sequences. These all share the same base constructor class, where the interfaces are constructed through a series of decorators. This enables users to create complex interfaces through a simple, declarative API.
* [**io**](https://github.com/EmbryoPhenomics/cvu/blob/main/cvu/io.py) - Image readers and writers for handling various image formats. Note that regardless of format, the handlers share the same API.
* [**ops**](https://github.com/EmbryoPhenomics/cvu/blob/main/cvu/ops.py)- Image operations, from simple drawing functions to contour filters and mask constructors.

This library is still in active development and so we welcome feedback on any aspect of **Vuba**.











