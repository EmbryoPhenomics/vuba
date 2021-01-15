Contour filters
===============

Many image analysis workflows contain methods that extract shapes that satisfy specific critera. These criteria can be simply based on the corresponding areas of the shapes, through to more complex characteristics such as their associated solidity and eccentricity. 

vuba provides a series of contour filters that allow one to extract contour shapes that satisfy some of the aforementioned criteria. These can be serially combined to allow the combination of a variety of criteria and also come built-in with pre-defined limits for more fine-scale tuning.

Here, we will cover the basic filters first followed by the more complex filters that are dependent on additional parameters. 

Basic filters
-------------

The basic filters that vuba provides are currently limited to the following: :py:func:`~vuba.smallest`, :py:func:`~vuba.largest` and :py:func:`~vuba.parents`. 

To demonstrate their usage, we need to first generate some contours to filter:

.. code-block:: python

	import vuba
	import cv2
	import numpy as np

	# Create a handler for the reading from the video
	video = vuba.Video('../examples/example_data/raw_video/test.avi')

	# Read in the first frame and grayscale it 
	first = video.read(index=0, grayscale=True)

	# Threshold the grayscaled frame to a binary threshold (n=50, to=255)
	_, thresh = cv2.threshold(first, 50, 255, cv2.THRESH_BINARY)

	# Find all the contours in the thresholded image
	contours, hierarchy = vuba.find_contours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

The above code has consisted of importing the first frame of the supplied example video and grayscaling it. We then applied a binary threshold to it with a threshold of 50. Note that the threshold applied here is arbitrary and only serves to enable us to generate a variety of shapes. Lastly, we applied contour detection to the thresholded image to generate arrays describing both the coordinates associated with each shape, but also their hierarchial information relative to the other shapes in the image.

Now that we have our contours, we can apply our contour filters and visualise the results! 

We can retrieve the smallest contour (by area):

.. code-block:: python

	smallest = vuba.smallest(contours)

but also the largest contour (also by area):

.. code-block:: python

	largest = vuba.largest(contours)

and finally retrieve all parent contours:

.. code-block:: python

	parents = vuba.parents(contours, hierarchy)

Note that here we needed to supply the hierarchical information in addition. This is because :py:func:`~vuba.parents` retrieves all the contours which are not a child of a larger contour. This can be useful for removing nested contours for example. 

To visualise the results, we now need draw the results on blank canvases and stitch them together. 

First we need to generate the canvases:

.. code-block:: python

	all_ = vuba.bgr(first)
	l = all_.copy()
	p = all_.copy()
	s = all_.copy()

Note that we needed to convert the grayscale frame back to BGR format to enable us to draw coloured shapes. Next we can draw our contours on each of these canvases:

.. code-block:: python

	vuba.draw_contours(p, parents, -1, (0,0,255), 2)
	vuba.draw_contours(l, largest, -1, (255,0,0), 2)
	vuba.draw_contours(s, smallest, -1, (0,255,0), 2)
	vuba.draw_contours(all_, contours, -1, (0,255,0), 2)

Here we can take advantage of the wrapper :py:func:`~vuba.draw_contours` which accepts both lists and single numpy arrays. This avoids us having to write ``for`` loops for each list of contours. Finally, lets stitch our resultant images together and visualise them:

.. code-block:: python

	# Stack the frames so we can view them all at once
	img1 = np.hstack((all_, p))
	img2 = np.hstack((l, s))
	img = np.vstack((img1, img2))

	# Resize the final image to a reasonable resolution
	img = cv2.resize(img, video.resolution)

	# And display it
	cv2.imshow('All contours/Parents/Largest/Smallest:', img)
	cv2.waitKey()

This should give us an image that looks like the following:

* Add an asset here

Complex filters
---------------

In addition to the basic contour filters mentioned above, vuba also supplies several more complex contour filters: :py:class:`~vuba.Area`, :py:class:`~vuba.Solidity` and :py:class:`~vuba.Eccentricity`. Each of these filters permits additional fine-tuning via the use of pre-defined limits, supplied at initiation. This enables us to select specific characteristics for the types of shapes we'd like extracted from a previous set of images. 

To demonstrate their usage, we will continue the script started above and add some additional filtering to retrieve small elliptical shapes.

First, let's create our filters, we will need an area and eccentricity filter:

.. code-block:: python

	# Initiate a relatively small area filter
	area_filter = vuba.Area(min=50, max=300)

	# Initiate an eccentricity filter that filters anything out with an eccentricity value greater than 1
	circle_filter = vuba.Eccentricity(max=1)

Now that we have our filters, we can apply them to the contours we created above:

.. code-block:: python

	# Serially combine the filters to extract our shapes
	small_elliptical = area_filter(circle_filter(contours))

Finally, let's visualise our results to see what we extracted:

.. code-block:: python

	# Draw the shapes on the frame used previously (note the format conversion)
	elliptical_img = vuba.bgr(first)
	vuba.draw_contours(elliptical_img, small_circles, -1, (0,255,0), 1)

	# And display the output
	cv2.imshow('Small elliptical shapes', elliptical_img)
	cv2.waitKey()

This should give us an image that looks like the following:

* Add image

Now, these aren't much but hopefully show you how you can combine some more complex contour filters to select shapes that satisfy specific criteria.

See also
--------

For additional example scripts that cover these filters in more complex applications see the following:

* examples/image_operations/contour_filters.py
* exampes/image_operations/contours_filter_with_gui.py