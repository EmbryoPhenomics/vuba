.. _installing:

Installation
============

Required dependencies
---------------------

- NumPy_
- OpenCV_ (opencv-python)
- dataclasses_ (for Python <= 3.7)
- tqdm_
- natsort_

.. _NumPy: https://github.com/numpy/numpy
.. _OpenCV: https://github.com/opencv/opencv
.. _dataclasses: https://github.com/ericvsmith/dataclasses
.. _tqdm: https://github.com/tqdm/tqdm
.. _natsort: https://github.com/SethMMorton/natsort

Instructions
------------

vuba is a pure Python package and can be installed from PyPi_ using ``pip``::

    $ pip install vuba

Note that for some Linux distributions such as Ubuntu you may need to install OpenCV using ``apt`` prior to installing vuba. Using the above command will install all of the required dependencies by default. 

If you would like to install the latest development version, you will need to clone the repository on GitHub and install it as follows::

    $ git clone https://github.com/EmbryoPhenomics/vuba.git
    $ cd vuba
    $ pip install .

Like above, this will install all the required dependencies for vuba.

.. _Pypi: https://pypi.org/