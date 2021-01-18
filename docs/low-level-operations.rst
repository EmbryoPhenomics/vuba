.. _low-level-operations:

Low-level operations
====================

In addition to contour filters, vuba also provides a number of wrappers and convenience functions around some of the lower level image operations provided with OpenCV_. These can be grouped in the following categories:

- Format conversion: wrappers that permit conversion between colour spaces.
- Drawing: functions related to drawing different shapes on images that have an equivalent API regardless of whether single or multiple shapes are requested to be drawn.
- Mask contructors: convenience functions for both creating masks and performing segmentation based on masks created.

Here, we will demonstrate their usage in several examples. There are links at the end of this guide to more in-depth example scripts that are hosted on github.

.. _OpenCV: https://opencv.org/

For these examples, the following imports are required:

.. ipython:: python

	import numpy as np
	import matplotlib.pyplot as plt
	import cv2
	import vuba

Format conversion
-----------------

There are several format conversion wrappers provided by vuba:

- :py:func:`~vuba.gray`
- :py:func:`~vuba.bgr`
- :py:func:`~vuba.hsv`

These all have the exact same behaviour as the corresponding **OpenCV** functions:

.. ipython:: python

	video = vuba.Video('../examples/example_data/raw_video/test.avi')
	frame = video.read(0)

	# Grayscale a BGR frame
	gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray_frame = vuba.gray(frame)

	# Convert grayscale frame to BGR
	bgr_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
	bgr_frame = vuba.bgr(gray_frame)

	# Convert BGR frame to HSV
	hsv_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2HSV)
	hsv_frame = vuba.hsv(bgr_frame)

Note that these functions also contain additional exceptions that provide more explicit error messages:

.. ipython:: python
	:okexcept:

	vuba.bgr(bgr_frame)

	cv2.cvtColor(bgr_frame, cv2.COLOR_GRAY2BGR)

For more information on these wrappers, please see the following API documentation: :py:func:`~vuba.gray`, :py:func:`~vuba.bgr`, :py:func:`~vuba.hsv`.

Drawing
-------

Currently, vuba provides three drawing wrappers:

- :py:func:`~vuba.draw_contours`
- :py:func:`~vuba.draw_rectangles`
- :py:func:`~vuba.draw_circles`

These wrappers support usage with both single and multiple shapes. This can remove the sometimes cumbersome series of ``for`` loops one has to write when drawing multiple shapes. Below, we will demonstrate their usage using a simple binary threshold applied to our example video:

.. ipython:: python

	# Read in the first frame and grayscale it
	first = video.read(index=0, grayscale=True)

	# Threshold the grayscaled frame to a binary threshold (n=50, to=255)
	_, thresh = cv2.threshold(first, 50, 255, cv2.THRESH_BINARY)

	# Find all the contours in the thresholded image
	contours, hierarchy = vuba.find_contours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

Next, let's draw the resultant polygons on the frame we grabbed:

.. ipython:: python

	# Convert to bgr for drawing below
	frame = vuba.bgr(first)

	# Draw all contours
	vuba.draw_contours(frame, contours, -1, (0,255,0), 1)

	# Draw the largest contour
	vuba.draw_contours(frame, vuba.largest(contours), -1, (0,0,255), 2)

	@savefig simple_drawing.png width=8in
	plt.imshow(frame)

Note that because this is a wrapper, the arguments for colour, line thickness etc. are equivalent to those used in the corresponding OpenCV function. For a more in-depth example, see the following script_.

.. _script: https://github.com/EmbryoPhenomics/vuba/blob/main/examples/image_operations/drawing.py

Creating masks
--------------

Vuba provides a number of convenience functions for creating masks for ``bitwise-and`` operations: 

* :py:func:`~vuba.rect_mask`
* :py:func:`~vuba.circle_mask`
* :py:func:`~vuba.contour_mask`

Each of these performs much as you would expect: you supply coordinates and parameters that describe the corresponding shape(s), and a mask is created that enables one to segment to those shapes in images of the same size. Because each of these contructors uses the above drawing functions under the hood, you can supply multiple shapes and construct a mask that corresponds to them:

.. ipython:: python

	# Using the above contours to find multiple bounding boxes
	bboxs = [cv2.boundingRect(c) for c in contours]
	mask = vuba.rect_mask(first, bboxs)

	out = vuba.bgr(mask)

	@savefig multi_rect_mask.png width=8in
	plt.imshow(out)

Using this mask, we can use :py:func:`~vuba.Mask` to perform segmentation on an image of the same size:

.. ipython:: python

	segm = vuba.Mask(mask)
	ret = segm(first)
	ret = vuba.bgr(ret)

	# Visualise our segmentation
	vuba.draw_rectangles(ret, bboxs, (0, 255, 0), 2)

	@savefig simple_segmentation.png width=8in
	plt.imshow(ret)

See also
--------

For additional example scripts that cover these functions in more depth, see the following:

- `examples/image_operations/drawing.py`_
- `examples/image_operations/contour_filters.py`_
- `examples/image_operations/contour_filter_with_gui.py`_

.. _examples/image_operations/drawing.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/image_operations/drawing.py

.. _examples/image_operations/contour_filters.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/image_operations/contour_filters.py

.. _examples/image_operations/contour_filter_with_gui.py: https://github.com/EmbryoPhenomics/vuba/blob/main/examples/image_operations/contour_filters_with_gui.py