Reading images
==============

Vuba provides a convenience wrapper - :py:class:`vuba.Video` - around the decoders in OpenCV_ but with an additional level of abstraction. It has the exact same API regardless of the footage format, whether it is separate images or movies. Below we will demonstrate it's usage with both images and movies, and also in creating in-memory and out-of-core frame containers for subsequent image processing. 

.. _OpenCV: https://opencv.org/

Initiation
----------

As mentioned above, :py:class:`vuba.Video` has an equivalent API regardless of footage format. The following code demonstrates a couple of ways one can initiate this wrapper with separate images:

.. code-block:: python

	import vuba

	# Using a glob pattern
	video = vuba.Video('../examples/example_data/raw_images/*.png')

	# Using a list of filenames
	video = vuba.Video([f"../examples/example_data/raw_images/{i}.png" for i in range(100)])

and then with movies:

.. code-block:: python

	video = vuba.Video('../examples/example_data/raw_video/test.avi')

At initiation, a number of attributes describing the footage will also be filled:

.. code-block:: python

	print(f"Resolution: {video.resolution}")
	print(f"Width: {video.width}, Height: {video.height}")
	print(f"Frame-rate: {video.fps}")
	print(f"Fourcc code: {video.fourcc_code}")
	print(f"Codec: {video.codec}")
	print(f"Number of frames: {len(video)}")
	print(f"Handler type: {type(video.video)} \n")

Note that since OpenCV is used under the hood, any type of footage that is compatible with OpenCV is also compatible with Vuba. Second to this, it is important to bear in mind that this wrapper has been designed with usage of videos or continuous sequences of frames in mind. Thus, even though you could in theory use this wrapper with individual images, it is recommended to use ``cv2.imread`` instead as this will be much simpler.

Reading in frames
-----------------

All reading operations are handled by :py:meth:`Video.read <vuba.Video.read>`. This method encapsulates decoders associated with reading in both individual frames and multiple frames. Reading single frames is as simple as the following:

.. code-block:: python

	# Read in the first frame
	first_frame = video.read(index=0)

The methods for multiple frames follow slice behaviour, whereby there is a start, stop and step. This allows us to easily import specific frames (by using a start and stop) and subsample them further (by using a step):

.. code-block:: python

	# Read in the first 50 frames, skipping every second frame.
	frames = video.read(start=0, stop=50, step=2)

We can also optionally grayscale frames read in using either operation by supplying ``True`` to the ``grayscale`` argument:

.. code-block:: python

	first_frame = video.read(index=0, grayscale=True)

	frames = video.read(start=0, stop=50, step=2, grayscale=True)

In addition to this, we can also optionally import frames into memory by supplying ``False`` to the ``low_memory`` argument:

.. code-block:: python

	# In-memory grayscale frames
	frames = video.read(start=0, stop=50, step=2, grayscale=True, low_memory=False)

Note that the frames are imported into a contiguous NumPy array and this can be accessed directly if you so choose:

.. code-block:: python

	# Retrieve the contiguous frame array
	frames_array = frames.ndarray

Because any reading operation involving multiple frames uses the :py:class:`vuba.Frames` container, we can also import the frames after our ``read`` operation:

.. code-block:: python

	frames = video.read(start=0, stop=50, step=2, grayscale=True)
	in_memory_frames = frames.import_to_ndarray()

Regardless of whether you imported your frames into memory or not, they are accessible through a generator via :py:meth:`Frames.__iter__ <vuba.Frames.__iter__>`:

.. code-block:: python

	import cv2

	# Iterate across the frames and display them
	for frame in frames:
	    cv2.imshow("Frames", frame)
	    k = cv2.waitKey(30)

	    if k == 27:
	        break

See also
--------

For additional example scripts that cover usage of this module in more depth, see the following:

* examples/reading/
* examples/reading/
* examples/reading/
* examples/reading/
* examples/reading/
* examples/reading/

to be filled.