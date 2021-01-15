Why vuba?
=========

Early on, we recognised that much of the HighGUI interfaces we were developing had the same core building blocks, and these could easily be captured in constructors to improve the development experience. We have since extended this to other areas of the OpenCV_ library, writing wrappers where we feel the reduction in code verbosity improves both readability and reduces complexity. 

.. _OpenCV: https://opencv.org/

The utility of simple constructors
----------------------------------

Simple computer vision interfaces can be an excellent way of integrating user input into a final application or visualising the variable output of a given method. The current python API to HighGUI provided by OpenCV_ reflects the C++ API, that is to say it provides absolute control over the interfaces one might develop but does not take advantage of many of python's features to improve the developer experience. To overcome this, we have developed a base constructor class which centralises code around a core image processing workflow. This allows users to concentrate their efforts on the image analysis component of their interfaces with minimal ui code required:

.. code-block:: python

    import vuba

    gui = vuba.BaseGUI(title='...')

    @gui.method
    def processing_method(gui):
        # Image analysis code goes here

    @gui.trackbar('Trackbar label', id='trackbar_id', min=0, max=100)
    def on_trackbar(gui, trackbar_val):
        # Here we provide the code we'd like to execute whenever 
        # this trackbar is changed

    gui.run()

For most applications, what you see here is all that is needed to create working interfaces in terms of the ui code required. This can scale to multi-trackbar applications just by declaring additional statements with the ``BaseGUI.trackbar`` decorator. To make working with a variety of footage inputs easier, we have written several additional constructor classes for both individual/multiple frames and video sequences/feeds. These classes inherit the ``BaseGUI`` class and so the API is the same regardless of the type of footage you're working with. 

.. _OpenCV: https://opencv.org/

Consistent API's
-----------------------

From handlers for encoding/decoding images, to drawing functions and more, the API's remain the same regardless of the type of footage you're working with. This allows you to develop software without an additional level of logic for handling application specific footage types, simplifying codebases and making long-term maintenance far easier.

