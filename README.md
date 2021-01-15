# vuba 

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

**vuba** (formerly **cvu**) is an easy to use library for constructing [`OpenCV`](https://opencv.org/) HighGUI interfaces. 

* **Documentation**: 
* **Example scripts**: [`https://github.com/EmbryoPhenomics/vuba/examples`](https://github.com/EmbryoPhenomics/vuba/tree/main/examples)
* **Installation**: 
* **Contributing**:
* **Source code**: [`https://github.com/EmbryoPhenomics/vuba/vuba`](https://github.com/EmbryoPhenomics/vuba/tree/main/vuba)

We developed this library to make coding up computer vision interfaces fast and efficient, allowing users to focus on their given application and bypass the challenges associated with developing a working user interface. We have since extended this to other areas of the [`OpenCV`](https://opencv.org/) library, writing wrappers where we feel the reduction in code verbosity improves both readability and reduces complexity in codebases. 

Currently the library is split up into three modules:

* [**gui**](https://github.com/EmbryoPhenomics/vuba/blob/main/vuba/gui.py) - [`OpenCV`](https://opencv.org/) HighGUI constructors, for both individual/multiple images and video sequences. These all share the same base constructor class, where the interfaces are constructed through a series of decorators. This enables users to create complex interfaces through a simple, declarative API.
* [**imio**](https://github.com/EmbryoPhenomics/vuba/blob/main/vuba/imio.py) - Image readers and writers for handling various image formats. Note that regardless of format, the handlers share the same API.
* [**ops**](https://github.com/EmbryoPhenomics/vuba/blob/main/vuba/ops.py)- Image operations, from simple drawing functions to contour filters and mask constructors.

This library is still in active development and so we welcome feedback on any aspect of **vuba**.











