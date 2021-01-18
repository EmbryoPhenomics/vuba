.. _writing-images:

Writing images
==============

Similar to the wrapper for decoding images, Vuba also provides a convenience wrapper for enconding footage in addition: :py:class:`vuba.Writer`. Just like :py:class:`vuba.Video`, this wrapper has the same API for all footage formats.

Initiation
----------

Similar to :py:class:`vuba.Video`, :py:class:`vuba.Writer`  has an equivalent API regardless of footage format. The following code demonstrates a couple of ways one can initiate this wrapper:

To encode to a movie:

.. ipython:: python

	import vuba

	# Initiate with minimal parameters
	writer = vuba.Writer('./output.avi', fps=15, resolution=(1000, 1000))

.. ipython:: python
    :suppress:

    writer.close()

.. ipython:: python

	# Custom codec (default is MJPG)
	writer = vuba.Writer('./output.avi', fps=15, resolution=(1000,1000), codec='MPNG')

.. ipython:: python
    :suppress:

    writer.close()

.. ipython:: python

	# Encode video in grayscale format
	writer = vuba.Writer('./output.avi', fps=15, resolution=(1000,1000), grayscale=True)	

To encode to individual images:

.. ipython:: python

	# Write to individual images 
	writer = vuba.Writer([f"./{i}.png" for i in range(100)], resolution=(1000, 1000))

.. ipython:: python
    :suppress:

    writer.close()

Note that you can also supply an instance of :py:class:`vuba.Video` if you wish to encode footage in the same format as the source video:

.. ipython:: python

	# Write to an AVI of the same format as the input video
	video = vuba.Video('../examples/example_data/raw_video/test.avi')
	writer = vuba.Writer('./output.avi', video)

.. ipython:: python
    :suppress:

    writer.close()

.. ipython:: python

	# Write to individual images from multiple images
	video = vuba.Video([f"../examples/example_data/raw_images/{i}.png" for i in range(100)])
	writer = vuba.Writer([f"./{i}.png" for i in range(len(video))], video)

.. ipython:: python
    :suppress:

    writer.close()

Also note that these are interchangeable, i.e. you can supply a 'movie' instance of :py:class:`vuba.Video` to an 'individual images' instance of :py:class:`vuba.Writer`.

Writing frames
--------------

.. ipython:: python
    :suppress:

    import tempfile

    tempdir = tempfile.TemporaryDirectory()
    writer = vuba.Writer(f'{tempdir.name}/output.avi', video, fps=15)

All writing operations are handled by :py:meth:`Writer.write <vuba.Writer.write>`. This method encapsulates encoders that enable writing to individual images and movies. Moreover, it will also resize and convert supplied frames to the resolution and format declared at initiation, if needed. Attempting to write frames in the wrong colour space or resolution has been one of the most common failure points in our own applications, and the error messages supplied by OpenCV are not of much use when debugging these scenarios. Thus, we have provided built-in operations and warnings in :py:meth:`Writer.write <vuba.Writer.write>` to help in this particular case. 

Now, when it actually comes to writing images to a given output, the syntax is the same regardless of the input or output footage format: 

.. ipython:: python

	# Read the first frame
	frame = video.read(index=0)

	# And write it
	writer.write(frame)

And that's it!

.. ipython:: python
    :suppress:

    import os

    os.remove('./output.avi')

    writer.close()
    video.close()
    tempdir.cleanup()

See also
--------

For additional example scripts that cover usage of this module in more depth, see the following:

- `examples/writing/writing_multiple_images_from_images.py`_
- `examples/writing/writing_multiple_images_from_video.py`_
- `examples/writing/writing_specific_images_from_images.py`_
- `examples/writing/writing_specific_images_from_video.py`_
- `examples/writing/writing_to_video_from_images.py`_
- `examples/writing/writing_to_video_from_video.py`_

.. _examples/writing/writing_multiple_images_from_images.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_multiple_images_from_images.py

.. _examples/writing/writing_multiple_images_from_video.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_multiple_images_from_video.py

.. _examples/writing/writing_specific_images_from_images.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_specific_images_from_images.py

.. _examples/writing/writing_specific_images_from_video.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_specific_images_from_video.py

.. _examples/writing/writing_to_video_from_images.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_to_video_from_images.py

.. _examples/writing/writing_to_video_from_video.py: https://github.com/EmbryoPhenomics/vuba/tree/main/examples/writing/writing_to_video_from_video.py
