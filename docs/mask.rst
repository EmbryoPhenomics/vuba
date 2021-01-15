Creating masks
==============

Vuba provides a number of convenience functions for creating masks for ``bitwise-and`` operations. These are the following: :py:func:`~vuba.rect_mask`, :py:func:`~vuba.circle_mask` and :py:func:`~vuba.contour_mask`. Each of these performs as much as you would expect: you supply coordinates and parameters that describe the corresponding shape(s) and a mask is created that enables one to segment to those shapes in images of the same size. 

