.. currentmodule:: vuba

########
Image IO
########

This section covers the API to the image io handlers. For more examples and information, refer to the relevant guides in the User Guide.

Current handlers
----------------

.. autosummary::
   :toctree: generated/

   Video
   Writer

Reading and writing
-------------------

.. autosummary::
   :toctree: generated/

   Video.read
   Writer.write

Teardown of handlers
--------------------

.. autosummary::
   :toctree: generated/

   Video.close
   Writer.close

Helper functions
----------------

.. autosummary::
   :toctree: generated/

   take_first
   fourcc_to_string
   open_video

Ancillary classes/methods
-------------------------

.. autosummary::
   :toctree: generated/

   Frames
   Frames.import_to_ndarray
   Frames.__len__
   Frames.__iter__
   Video.__len__
