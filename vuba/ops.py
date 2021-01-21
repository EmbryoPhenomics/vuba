import cv2
import numpy as np

cv_vers = int(cv2.__version__[0])


def _channel_check(img, type_):
    """
    Convenience function for raising an exception if the input image is not
    of the correct format.

    """
    exc_info = {2: "grayscale", 3: "BGR"}

    channels = len(np.asarray(img).shape)
    if channels != type_:
        raise ValueError(
            f"Input image needs to be {exc_info[type_]} or have {type_} channels. Instead an image with {channels} channels was provided."
        )


def find_contours(img, *args, **kwargs):
    """
    Convenience function for contour detection.

    This function accounts for the OpenCV version supplied and executes
    accordingly.

    Parameters
    ----------
    img : ndarray
        Grayscale image to perform contour detection on.
    *args : tuple
        Additional arguments `cv2.findContours` will require.
    *kwargs : tuple
        Additional keyword arguments `cv2.findContours` will require.

    Returns
    -------
    contours : ndarray
        An array of contours detected.
    hierarchy : ndarray
        Corresponding hierarchy information to the contours detected.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale or has greater than 2 channels.

    """
    _channel_check(img, 2)

    if cv_vers == 4:
        contours, hierarchy = cv2.findContours(img, *args, **kwargs)
    else:
        _, contours, hierarchy = cv2.findContours(img, *args, **kwargs)
    return contours, hierarchy


def fit_circles(contours):
    """
    Fit minimum enclosing circles to contour(s).

    Parameters
    ----------
    contours : ndarray or list
        Contour(s) to fit circles to.

    Returns
    -------
    circles : ndarray or list
        An array or list corresponding to dimensions to circles fitted.

    """
    if isinstance(contours, list):
        ret = [cv2.minEnclosingCircle(c) for c in contours]
    else:
        ret = cv2.minEnclosingCircle(contours)
    return ret


def fit_rectangles(contours, rotate=False):
    """
    Fit bounding boxes to contour(s).

    Parameters
    ----------
    contours : ndarray or list
        Contour(s) to fit circles to.
    rotate : bool
        Whether to fit rotated bounding boxes, default is False.

    Returns
    -------
    rectangles : ndarray or list
        An array or list corresponding to dimensions to bounding boxes fitted.

    """
    if isinstance(contours, list):
        if rotate:
            ret = [cv2.minAreaRect(c) for c in contours]
        else:
            ret = [cv2.boundingRect(c) for c in contours]
    else:
        if rotate:
            ret = cv2.minAreaRect(contours)
        else:
            ret = cv2.boundingRect(contours)
    return ret


def fit_ellipses(contours):
    """
    Fit ellipses to contour(s).

    Parameters
    ----------
    contours : ndarray or list
        Contour(s) to fit ellipses to.

    Returns
    -------
    ellipses : ndarray or list
        An array or list corresponding to dimensions to ellipses fitted.

    """
    if isinstance(contours, list):
        ret = [cv2.fitEllipse(c) for c in contours]
    else:
        ret = cv2.fitEllipse(c)
    return ret


def draw_contours(img, contours, *args, **kwargs):
    """
    Convenience function for drawing contour(s) on an image.

    Parameters
    ----------
    img : ndarray
        Image to draw contours on.
    contours : ndarray or list
        Contour(s) to draw on the supplied image.
    *args : tuple
        Additional arguments `cv2.drawContours` will require.
    *kwargs : tuple
        Additional keyword arguments `cv2.drawContours` will require.

    See Also
    --------
    draw_rectangles
    draw_circles
    draw_ellipses

    """
    if isinstance(contours, list):
        for c in contours:
            cv2.drawContours(img, [c], *args, **kwargs)
    else:
        cv2.drawContours(img, [contours], *args, **kwargs)


def draw_rectangles(img, dims, *args, **kwargs):
    """
    Convenience function for drawing rectangle(s) on an image.

    Parameters
    ----------
    img : ndarray
        Image to draw contours on.
    dims : tuple or list
        Rectangle(s) to draw on the supplied image. Note these should be
        supplied in (x,y,w,h) format.
    *args : tuple
        Additional arguments `cv2.rectangle` will require.
    *kwargs : tuple
        Additional keyword arguments `cv2.rectangle` will require.

    See Also
    --------
    draw_contours
    draw_circles
    draw_ellipses

    """
    def _draw(rect):
        x,y,w,h = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), *args, **kwargs)

    if isinstance(dims, list):
        for r in dims: _draw(r)
    else:
        _draw(dims)

def draw_circles(img, dims, *args, **kwargs):
    """
    Convenience function for drawing circle(s) on an image.

    Parameters
    ----------
    img : ndarray
        Image to draw contours on.
    dims : tuple or list
        Circle(s) to draw on the supplied image. Note these should be
        supplied in ((x,y),r) format.
    *args : tuple
        Additional arguments `cv2.circle` will require.
    *kwargs : tuple
        Additional keyword arguments `cv2.circle` will require.

    See Also
    --------
    draw_contours
    draw_rectangles
    draw_ellipses

    """
    def _draw(circ):
        (x,y),r = circ
        x,y,r = map(int, (x,y,r))
        cv2.circle(img, (x,y), r, *args, **kwargs)

    if isinstance(dims, list):
        for c in dims: _draw(c)
    else:
        _draw(c)


def draw_ellipses(img, dims, *args, **kwargs):
    """
    Convenience function for drawing ellipse(s) on an image.

    Parameters
    ----------
    img : ndarray
        Image to draw contours on.
    dims : tuple or list
        Ellipse(s) to draw on the supplied image. Note these should be
        supplied in ((x,y),(w,h),a) format.
    *args : tuple
        Additional arguments `cv2.ellipse` will require.
    *kwargs : tuple
        Additional keyword arguments `cv2.ellipse` will require.

    See Also
    --------
    draw_contours
    draw_rectangles
    draw_circles

    """

    if isinstance(dims, list):
        for c in dims:
            cv2.ellipse(img, c, *args, **kwargs)
    else:
        cv2.ellipse(img, dims, *args, **kwargs)


def gray(frame):
    """
    Convert a frame to grayscale.

    Parameters
    ----------
    frame : ndarray
        Frame to grayscale.

    Returns
    -------
    frame : ndarray
        Grayscale frame.

    Raises
    ------
    ValueError
        If the supplied image is not of BGR format.

    See Also
    --------
    bgr
    hsv

    """
    _channel_check(frame, 3)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


def bgr(frame):
    """
    Convert a frame to BGR format.

    Parameters
    ----------
    frame : ndarray
        Frame to convert.

    Returns
    -------
    frame : ndarray
        Frame of BGR format.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    gray
    hsv

    """
    _channel_check(frame, 2)
    return cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)


def hsv(frame):
    """
    Convert a frame to HSV format.

    Parameters
    ----------
    frame : ndarray
        Frame to convert.

    Returns
    -------
    frame : ndarray
        Frame of HSV format.

    Raises
    ------
    ValueError
        If the supplied image is not of BGR format.

    See Also
    --------
    gray
    bgr

    """
    _channel_check(frame, 3)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


class Mask:
    """
    Convenience class for performing segmentation to a mask.

    ``Mask`` enables the creation of a callable that will perform
    ``bitwise_and`` on a given frame with the mask supplied at initiation.
    This can be useful for performing the same operation on a series of frames.

    Parameters
    ----------
    mask : ndarray
        Mask to segment frame(s) to.

    Returns
    -------
    mask : Mask
        Class object with ``__call__`` method that performs ``bitwise_and``
        with the mask provided at initiation.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    shrink
    rect_mask
    circle_mask
    contour_mask

    """

    def __init__(self, mask):
        _channel_check(mask, 2)
        self.mask = mask

    def __call__(self, frame) -> "Mask":
        """
        Mask a frame using the pre-defined mask.

        Parameters
        ----------
        frame : ndarray.
            Frame to mask.

        Returns
        -------
        masked_frame : ndarray
            Masked frame.

        Raises
        ------
        ValueError
            If the supplied image is not grayscale.

        """
        _channel_check(frame, 2)
        return cv2.bitwise_and(frame, frame, mask=self.mask)


def cast_contours(contours, x, y):
    """
    Convenience function to cast contour(s) to a given x,y.

    Parameters
    ----------
    contours : list or ndarray
        Contour(s) to cast.
    x : int
        x position to cast to.
    y : int
        y position to cast to.

    Returns
    -------
    contours : list of ndarray
        Contours casted to new coordinates.

    See Also
    --------
    find_contours
    draw_contours

    """
    if isinstance(contours, list):
        for i, c in enumerate(contours):
            c[:, 0, 0] += x
            c[:, 0, 1] += y
            contours[i] = c
    else:
        contours[:, 0, 0] += x
        contours[:, 0, 1] += y
    return contours


def shrink(img, by=50):
    """
    Mask an image to a new roi.

    Parameters
    ----------
    img : ndarray
        Grayscale image to reduce the roi for.
    by : int
        Number of pixels to reduce roi by, default is 50.

    Returns
    -------
    img : ndarray
        Image with reduced roi.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    Notes
    -----
    This function will shrink the roi by a uniform amount on all four
    sides of an image, and not to a specific region within the image.

    See Also
    --------
    Mask
    rect_mask
    circle_mask
    contouer_mask

    """
    _channel_check(img, 2)

    mask = np.zeros_like(img)
    w, h = map(int, tuple(np.asarray(img.shape) - by))
    cv2.rectangle(mask, (by, by), (w, h), 255, -1)
    img = cv2.bitwise_and(img, img, mask=mask)
    return img


def rect_mask(img, dims):
    """
    Create a rectangular mask.

    Parameters
    ----------
    img : ndarray
        Grayscale image to produce the rectangular mask for.
    dims : tuple or list
        Rectangle(s) to base mask on. Note these should be
        supplied in (x,y,w,h) format.

    Returns
    -------
    mask : ndarray
        Rectangular mask.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    Mask
    shrink
    circle_mask
    contour_mask

    """
    _channel_check(img, 2)

    rect_mask_ = np.zeros_like(img)
    draw_rectangles(rect_mask_, dims, 255, -1)
    return rect_mask_


def circle_mask(img, dims):
    """
    Create a circular mask.

    Parameters
    ----------
    img : ndarray
        Grayscale image to produce circular mask for.
    dims : tuple or list
        Circle(s) to base mask on. Note these should be
        supplied in ((x,y),r) format.

    Returns
    -------
    mask : ndarray
        Circular mask.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    Mask
    shrink
    rect_mask
    contour_mask

    """
    _channel_check(img, 2)

    circle_mask_ = np.zeros_like(img)
    draw_circles(circle_mask_, dims, 255, -1)
    return circle_mask_

def ellipse_mask(img, dims):
    """
    Create an ellipse mask.

    Parameters
    ----------
    img : ndarray
        Grayscale image to produce elliptical mask for.
    dims : tuple or list
        Ellipse(s) to base mask on. Note these should be
        supplied in ((x,y),(w,h),a) format.

    Returns
    -------
    mask : ndarray
        Elliptical mask.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    Mask
    shrink
    rect_mask
    circle_mask
    contour_mask

    """
    _channel_check(img, 2)

    ell_mask_ = np.zeros_like(img)
    draw_ellipses(ell_mask_, dims, 255, -1)
    return ell_mask_

def contour_mask(img, contours):
    """
    Create a contour mask at the dimensions of contour(s).

    Parameters
    ----------
    img : ndarray
        Grayscale image to produce circular mask for.
    contours : list or ndarray
        Contour(s) to create mask with.

    Returns
    -------
    mask : ndarray
        Contour mask at the dimensions of the contour(s) supplied.

    Raises
    ------
    ValueError
        If the supplied image is not grayscale.

    See Also
    --------
    Mask
    shrink
    rect_mask
    circle_mask

    """
    _channel_check(img, 2)

    cnt_mask = np.zeros_like(img)
    draw_contours(cnt_mask, contours, -1, 255, -1)
    return cnt_mask


# Contour filters ----------------------------------------------------------------------------


def _contours_area(contours):
    """Convenience function for computing the area of contour(s). """
    if isinstance(contours, np.ndarray):
        areas = cv2.contourArea(contours)
    else:
        areas = [cv2.contourArea(c) for c in contours]
    return areas


def smallest(contours):
    """
    Contour filter that returns the smallest contour by area.

    Parameters
    ----------
    contours : list or ndarray
        Contour(s) to filter.

    Returns
    -------
    contour : ndarray
        Smallest contour by area.

    See Also
    --------
    largest
    parents
    Area
    Eccentricity
    Solidity

    """
    areas = _contours_area(contours)
    return contours[np.argmin(areas)]


def largest(contours):
    """
    Contour filter that returns the largest contour by area.

    Parameters
    ----------
    contours : list or ndarray
        Contour(s) to filter.

    Returns
    -------
    contour : ndarray
        Largest contour by area.

    See Also
    --------
    smallest
    parents
    Area
    Eccentricity
    Solidity

    """
    areas = _contours_area(contours)
    return contours[np.argmax(areas)]


def parents(contours, hierarchy):
    """
    Contour filter that returns only parent contours.

    Parameters
    ----------
    contours : list or ndarray
        Contour(s) to filter.
    hierarchy : ndarray
        Corresponding hierarchy information for contours.

    Returns
    -------
    contour : ndarray
        All parent contours.

    See Also
    --------
    smallest
    largest
    Area
    Eccentricity
    Solidity

    """
    parentLvl = hierarchy[0, :, 3].tolist()
    return [contours[i] for i, e in enumerate(parentLvl) if e == -1]


class _ByLimit:
    """
    Filter values based on pre-defined limits.

    """

    def __init__(self, min=None, max=None):
        if min is None and max is None:
            raise ValueError("Limit(s) required for filtering contours.")

        self.min = min
        self.max = max

    def __call__(self, x):
        """
        Filter x based on  a lower or upper limit, or both. If x is between either
        of the pre-defined limits then it will be returned.

        """
        min, max = (self.min, self.max)
        if min and max:
            if x >= min and x <= max:
                return x
        else:
            if min and not max:
                if x >= min:
                    return x
            elif max and not min:
                if x <= max:
                    return x


class Area:
    """
    Filter contours by area based on a lower or upper limit, or both.

    Parameters
    ----------
    min : int or float
        Lower limit to filter contour areas.
    max: int or float
        Upper limit to filter contour areas.

    Returns
    -------
    filter : Area
        Class object with ``__call__`` method that filters contours based on
        the pre-defined area limits provided at initiation.

    See Also
    --------
    smallest
    largest
    parents
    Eccentricity
    Solidity

    """

    def __init__(self, min=None, max=None):
        self._filter = _ByLimit(min, max)

    def __call__(self, contours) -> "Area":
        """
        Filter contours by area based on pre-defined limits.

        Parameters
        ----------
        contours : list
            List of contours to filter.

        Returns
        -------
        contours : list
            Filtered contours.

        """
        areas = _contours_area(contours)
        _filtered = []

        for i, a in enumerate(areas):
            if self._filter(a):
                _filtered.append(contours[i])

        return _filtered


class Eccentricity:
    """
    Filter contours by eccentricity based on a lower or upper limit, or both.

    Parameters
    ----------
    min : int or float
        Lower eccentricity limit to filter contours.
    max: int or float
        Upper eccentricity limit to filter contours.

    Returns
    -------
    filter : Eccentricity
        Class object with ``__call__`` method that filters contours based on
        the pre-defined eccentricity limits provided at initiation.

    See Also
    --------
    smallest
    largest
    parents
    Area
    Eccentricity

    """

    def __init__(self, min=None, max=None):
        self._filter = _ByLimit(min, max)

    def _eccentricity(self, contours):
        """Convenience method for computing the eccentricity of contours. """
        for i, c in enumerate(contours):
            if c.shape[0] >= 5:  # filter to this size for below calculations
                center, axes, orientation = cv2.fitEllipse(c)
                major, minor = (max(axes), min(axes))
                eccentricity = np.sqrt(1 - (minor / major) ** 2)
                yield (i, eccentricity)

    def __call__(self, contours) -> "Eccentricity":
        """
        Filter contours by eccentricity based on pre-defined limits.

        Parameters
        ----------
        contours : list
            List of contours to filter.

        Returns
        -------
        contours : list
            Filtered contours.

        """
        _filtered = []
        for i, e in self._eccentricity(contours):
            if self._filter(e):
                _filtered.append(contours[i])

        return _filtered


class Solidity:
    """
    Filter contours by solidity based on a lower or upper limit, or both.

    Parameters
    ----------
    min : int or float
        Lower solidity limit to filter contours.
    max: int or float
        Upper solidity limit to filter contours.

    Returns
    -------
    filter : Solidity
        Class object with ``__call__`` method that filters contours based on
        the pre-defined solidity limits provided at initiation.

    Notes
    -----
    Note that here the solidity of a contour is based on its area relative
    to its corresponding convex hull.

    See Also
    --------
    smallest
    largest
    parents
    Area
    Eccentricity

    """

    def __init__(self, min=None, max=None):
        self._filter = _ByLimit(min, max)

    def _solidity(self, contours):
        """Convenience method for computing the solidity of contours. """
        for i, c in enumerate(contours):
            c_area = cv2.contourArea(c)
            hull = cv2.convexHull(c)
            hullarea = cv2.contourArea(hull)

            try:
                yield (i, c_area / hullarea)
            except ZeroDivisionError:
                pass

    def __call__(self, contours) -> "Solidity":
        """
        Filter contours by solidity based on pre-defined limits.

        Parameters
        ----------
        contours : list
            List of contours to filter.

        Returns
        -------
        contours : list
            Filtered contours.

        """
        _filtered = []
        for i, s in self._solidity(contours):
            if self._filter(s):
                _filtered.append(contours[i])

        return _filtered
