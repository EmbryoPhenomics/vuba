.. currentmodule:: vuba

################
Image operations
################

This section covers the API to the supplied low-level image operations. For more examples and information, refer to the relevant guides in the User Guide.

Format conversion
-----------------

.. autosummary::
   :toctree: generated/

   gray
   bgr
   hsv

Drawing
-------

.. autosummary::
   :toctree: generated/

   draw_contours
   draw_rectangles
   draw_circles

Mask constructors
-----------------

.. autosummary::
   :toctree: generated/

   Mask
   shrink
   rect_mask
   circle_mask
   contour_mask

Contour filters
---------------

.. autosummary::
   :toctree: generated/

   smallest
   largest
   parents
   Area
   Eccentricity
   Solidity

Additional contour functions
----------------------------

.. autosummary::
   :toctree: generated/

   find_contours
   cast_contours
