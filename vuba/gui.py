import functools
import cv2
from typing import Callable, Iterable
from dataclasses import dataclass
import numpy as np

from vuba import imio


@dataclass
class TrackbarMethod:
    """
    Container for a trackbar method and it's associated variables.

    Parameters
    ----------
    id : str
        Identification string of trackbar added in ``BaseGUI.trackbar``.
    min : int
        Minimum limit of trackbar.
    max : int
        Maximum limit of trackbar.
    method : callable
        Trackbar callback as specified in ``BaseGUI.trackbar``.
    current : int
        Current trackbar value.

    Returns
    -------
    container : dataclass
        Mutable container for a trackbar and it's associated variables.

    """

    __slots__ = ["id", "min", "max", "method", "current"]
    id: str  #: Identification string of trackbar added in ``BaseGUI.trackbar``.
    min: int  #: Minimum limit of trackbar.
    max: int  #: Maximum limit of trackbar.
    method: Callable  #: Trackbar callback as specified in ``BaseGUI.trackbar``.
    current: int  #: Current trackbar value.


class BaseGUI:
    """
    The base constructor class for creating HighGUI interfaces.

    Typical usage of this class is through the supplied wrappers around
    this class, although if those are ill-fit for a given application this
    constructor can be addressed directly.

    To use this constructor with single or multiple frames that are in memory,
    use the ``FrameGUI`` or ``FramesGUI`` classes respectively, Conversely, to use
    this constructor with video files or streams, use the ``VideoGUI`` or ``StreamGUI``
    classes respectively.

    Parameters
    ----------
    title : str
        Title of the interface window.

    Returns
    -------
    gui : BaseGUI
        The newly created gui constructor.

    See Also
    --------
    FrameGUI
    FramesGUI
    VideoGUI
    StreamGUI

    """

    def __init__(self, title):
        self.title = title
        self.trackbars = {}
        cv2.namedWindow(self.title)

    def values(self) -> "BaseGUI":
        """
        Retrieve all current trackbar values from the interface.

        Returns
        -------
        values : dict or None
            All current trackbar values, returns None if no
            trackbars declared.

        See Also
        --------
        BaseGUI.__getitem__
        BaseGUI.__setitem__

        """
        if self.trackbars:
            vals = {}
            for k in self.trackbars:
                vals[k] = self.trackbars[k].current
        else:
            vals = None
        return vals

    def __getitem__(self, key) -> "BaseGUI":
        """
        Access a trackbar's current value.

        Parameters
        ----------
        key : str
            Trackbar identification string provided
            when using ``BaseGUI.trackbar``.

        Returns
        -------
        value : int
            Trackbar's current value.

        See Also
        --------
        BaseGUI.values
        BaseGUI.__setitem__

        """
        return self.trackbars[key].current

    def __setitem__(self, key, val) -> "BaseGUI":
        """
        Change a trackbar's current recorded value.

        Parameters
        ----------
        key : str
            Trackbar identification string provided
            when using ``BaseGUI.trackbar``.
        val : int
            Value to record trackbar as.

        Notes
        -----
        ``BaseGUI.__setitem__`` will not change the trackbar value in
        the OpenCV interface and will only change the value recorded
        in the ``BaseGUI`` class instance.

        See Also
        --------
        BaseGUI.values
        BaseGUI.__getitem__

        """
        self.trackbars[key].current = val

    def method(self, func) -> "BaseGUI":
        """
        Add a main processing function to be executed on every trackbar call.

        All trackbar functions should call the function that is wrapped
        in this decorator. As such changes made to a single trackbar, will
        propagate to this main processing function and the changes will be
        returned to the named window.

        Parameters
        ----------
        func : callable
            Main processing function for the interface.

        See Also
        --------
        BaseGUI.trackbar

        Examples
        --------
        To demonstrate this method's usage as a decorator we can construct
        a simple binary threshold viewer for a random binary image:

        >>> import vuba
        >>> import numpy as np
        >>> import cv2
        >>> img = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
        >>> gui = vuba.BaseGUI('Binary threshold viewer')
        >>> @gui.method
        >>> def threshold(gui):
        ...     frame = img.copy()
        ...     thresh_val = gui['thresh_val']
        ...     _, thresh = cv2.threshold(frame, thresh_val, 255, cv2.THRESH_BINARY)
        ...     return thresh
        >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
        >>> gui.run()

        Note that this method does not have to be used as a decorator:

        >>> gui = vuba.BaseGUI('Binary threshold viewer')
        >>> def threshold(gui):
        ...     frame = img.copy()
        ...     thresh_val = gui['thresh_val']
        ...     _, thresh = cv2.threshold(frame, thresh_val, 255, cv2.THRESH_BINARY)
        ...     return thresh
        >>> gui.method(threshold)
        >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
        >>> gui.run()

        Also note that since we are not doing any additional processing on
        each trackbar call in the above two examples, we can supply None to the
        ``BaseGUI.trackbar`` decorator. This will default to using a simple callback
        that will pass the trackbar values to the main processing method
        and display the result in the interactive window.

        """

        @functools.wraps(func)
        def wrap_to_proc():
            img = func(self)
            return img

        self.process = wrap_to_proc
        return wrap_to_proc

    @staticmethod
    def _basic_trackbar_callback(gui, id, val):
        """
        Basic trackbar callback to be used when ``BaseGUI.trackbar`` is not supplied a function.

        """
        gui[id] = val
        img = gui.process()
        cv2.imshow(gui.title, img)

    def trackbar(self, name, id, min, max) -> "BaseGUI":
        """
        Add a trackbar to the interactive window.

        Parameters
        ----------
        name : str
            Name of trackbar to add.
        id : str
            Id of trackbar to add. This will be the key associated with the trackbar.
        min : int
            Minimum limit of trackbar
        max : int
            Maximum limit of trackbar
        func : callable, optional
            Trackbar callback to be called whenever the trackbar is changed. If
            None, then a basic callback will be used that simply passes the trackbar
            value to the ``BaseGUI.method`` method.

        Notes
        -----
        This method can be called in much the same way as ``BaseGUI.method``, either as
        a decorator or as a typical method call.

        Examples
        --------
        For these examples, we will use the same binary threshold viewer as used in
        ``BaseGUI.method``:

        >>> import vuba
        >>> import numpy as np
        >>> import cv2
        >>> def threshold(gui):
        ...     frame = img.copy()
        ...     thresh_val = gui['thresh_val']
        ...     _, thresh = cv2.threshold(frame, thresh_val, 255, cv2.THRESH_BINARY)
        ...     return thresh
        >>> img = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
        >>> gui = vuba.BaseGUI('Binary threshold viewer')
        >>> gui.method(threshold)

        For applications where there is no additional processing on each trackbar call,
        we can simply supply None to ``BaseGUI.trackbar`` as follows:

        >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
        >>> gui.run()

        However, if we wanted to add some further processing, let's say to exclude
        all odd threshold values, we could handle this logic with a custom callback:

        >>> gui = vuba.BaseGUI('Binary threshold viewer')
        >>> gui.method(threshold)
        >>> @gui.trackbar('Threshold', id='thresh_val', min=0, max=255)
        >>> def even_threshold(gui, val):
        ...     if val%2 == 0:
        ...         gui['thresh_val'] = val
        ...         ret = gui.process()
        ...         cv2.imshow(gui.title, ret)
        >>> gui.run()
        """

        def wrap_to_trackbar(func):
            if not func:

                @functools.wraps(self._basic_trackbar_callback)
                def on_exe(val):
                    return self._basic_trackbar_callback(self, id, val)

            else:

                @functools.wraps(func)
                def on_exe(val):
                    return func(self, val)

            self.trackbars[id] = TrackbarMethod(id, min, max, on_exe, min)
            cv2.createTrackbar(name, self.title, min, max, on_exe)

            return on_exe

        return wrap_to_trackbar

    def run(self) -> "BaseGUI":
        """
        Launch the interface.

        Examples
        --------
        Note that you can access any variables from the class that you
        added/manipulated through the trackbars attribute. This contains
        a dict of the trackbars, with each key containing associated
        variables in a dataclass:

        >>> import vuba
        >>> import numpy as np
        >>> import cv2
        >>> img = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
        >>> gui = vuba.BaseGUI('Binary threshold viewer')
        >>> @gui.method
        >>> def threshold(gui):
        ...     frame = img.copy()
        ...     thresh_val = gui['thresh_val']
        ...     _, thresh = cv2.threshold(frame, thresh_val, 255, cv2.THRESH_BINARY)
        ...     return thresh
        >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
        >>> gui.run()
        >>> name, min, max, method, last_value = gui.trackbars['thresh_val']

        This can be useful for retrieving the ideal parameters for an image analysis
        method after adjusting them in an interface for example.

        """
        # Execute first method to launch the gui
        firstfunc = self.trackbars[[*self.trackbars][0]]
        func = firstfunc.method
        min = firstfunc.min
        func(min)

        cv2.waitKey()
        cv2.destroyAllWindows()


class FrameGUI(BaseGUI):
    """
    Class for creating interfaces for individual image manipulation.

    Parameters
    ----------
    frame : ndarray
        Frame(s) to manipulate within the interface.
    title : str
        Title of the interface window.

    Returns
    -------
    gui : FrameGUI
        Class object for creating the interactive window.

    See Also
    --------
    BaseGUI
    FramesGUI
    VideoGUI
    StreamGUI

    Notes
    -----
    This class does not impose any restrictions on the types/formats of the images
    you supply upon initiation. As such, we can supply a tuple or list of images
    that we want to manipulate at the same time for example (see examples below).

    Examples
    --------
    As in other single image examples, we will use a series of randomly generated
    binary images with a variable binary threshold in the interfaces below:

    >>> import vuba
    >>> import numpy as np
    >>> import cv2
    >>> img = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
    >>> gui = vuba.FrameGUI(img, 'Binary threshold viewer')
    >>> @gui.method
    >>> def threshold(gui):
    ...     frame = gui.frame.copy()
    ...     thresh_val = gui['thresh_val']
    ...     _, thresh = cv2.threshold(frame, thresh_val, 255, cv2.THRESH_BINARY)
    ...     return thresh
    >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
    >>> gui.run()

    As mentioned above, we can supply a series of images for simultaneuous
    manipulation as well:

    >>> img1 = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
    >>> img2 = np.random.randint(low=0, high=255, size=(500, 500), dtype=np.uint8)
    >>> gui = vuba.FrameGUI((img1, img2), 'Binary threshold viewer')
    >>> @gui.method
    >>> def threshold(gui):
    ...     frame1, frame2 = gui.img
    ...     thresh_val = gui['thresh_val']
    ...     _, thresh1 = cv2.threshold(frame1.copy(), thresh_val, 255, cv2.THRESH_BINARY)
    ...     _, thresh2 = cv2.threshold(frame2.copy(), thresh_val, 255, cv2.THRESH_BINARY)
    ...     return np.hstack((thresh1, thresh2))
    >>> gui.trackbar('Threshold', id='thresh_val', min=0, max=255)(None)
    >>> gui.run()

    For an extension of this type of interface with drawing in addition, see
    ``/examples/interfaces/binarythreshod_viewer_with_drawing_video.py``.

    """

    def __init__(self, frame, *args, **kwargs):
        self.frame = frame
        super(FrameGUI, self).__init__(*args, **kwargs)


class FramesGUI(BaseGUI):
    """
    Class for creating interfaces for manipulating a sequence of frames.

    Parameters
    ----------
    frames : list or ndarray
        Images to manipulate within the interface.
    title : str
        Title of the interface window.

    Returns
    -------
    gui : FramesGUI
        Class object for creating the interactive window.

    See Also
    --------
    BaseGUI
    FrameGUI
    VideoGUI
    StreamGUI

    Notes
    -----
    Any gui created with this class will by default have a frame trackbar and
    corresponding callback for retrieving frames from the sequence provided
    at initiation (see ``FramesGUI.read``).

    Examples
    --------
    Since the API for creating an interface is the same regardless of footage format,
    we will demonstrate a basic frame viewer here.

    First, let's create a sequence of binary images that gradually increase
    in their grayscale value:

    >>> import numpy as np
    >>> frames = [np.full((500, 500), i, dtype=np.uint8) for i in range(1, 255)]

    Now let's pass these to our basic frame viewer to view the result:

    >>> import vuba
    >>> import cv2
    >>> gui = vuba.FramesGUI(frames, 'Frame viewer')
    >>> @gui.method
    >>> def blank(gui):
    ...     # Here we are not doing any image processing as we simply
    ...     # want to view the individual frames
    ...     frame = gui.frame.copy()
    ...     return frame
    >>> gui.run()

    """

    def __init__(self, frames, *args, **kwargs):
        self.frames = frames
        super(FramesGUI, self).__init__(*args, **kwargs)
        self.trackbar("Frames", "frames", 0, len(self.frames))(self.read)

    @staticmethod
    def read(gui, val) -> "FramesGUI":
        """
        Callback for reading and displaying a frame from the provided frames.

        Parameters
        ----------
        val : int
            Frame index in the requested frames.

        Notes
        -----
        Any image processing in the main method will be executed prior
        to displaying the frame.

        """
        gui.frame = gui.frames[val]
        frame_proc = gui.process()
        cv2.imshow(gui.title, frame_proc)


class VideoGUI(BaseGUI):
    """
    Class for creating interfaces for manipulating a sequence of frames.

    Parameters
    ----------
    video : vuba.Video
        Video to manipulate within the interface.
    title : str
        Title of the interface window.

    Returns
    -------
    gui : VideoGUI
        Class object for creating the interactive window.

    See Also
    --------
    BaseGUI
    FrameGUI
    FramesGUI
    StreamGUI

    Notes
    -----
    Any gui created with this class will by default have a frame trackbar and
    corresponding callback for retrieving frames from the video provided
    at initiation (see ``VideoGUI.read``).

    Examples
    --------
    Please see the following example scripts for some typical applications of this
    class:

    * examples/interfaces/frame_viewer.py
    * examples/interfaces/binary_threshold_viewer_with_drawing_video.py

    """

    def __init__(self, video, *args, **kwargs):
        self.video, self.release = imio.open_video(video)
        super(VideoGUI, self).__init__(*args, **kwargs)
        self.trackbar("Frames", "frames", 0, len(self.video))(self.read)

    @staticmethod
    def read(gui, val) -> "VideoGUI":
        """
        Callback for reading and displaying a frame from the requested video.

        Parameters
        ----------
        val : int
            Frame index in the requested video.

        Notes
        -----
        Any image processing in the main method will be executed prior
        to displaying the frame.

        """
        gui.frame = gui.video.read(val, grayscale=False)
        frame_proc = gui.process()
        cv2.imshow(gui.title, frame_proc)

    def run(self) -> "VideoGUI":
        """
        Launch the interactive video interface.

        Notes
        -----
        After running the interface, this function will close/teardown the
        video handler supplied if it was created at initiation.

        """
        try:
            super().run()
        finally:
            if self.release:
                self.video.close()


class StreamGUI(BaseGUI):
    """
    Class for creating interfaces for manipulation of images from video feeds.

    Parameters
    ----------
    stream : Iterable
        An iterator to a camera stream. This can be a generator
        that will continuously pull frames from a capture device
        for example.
    title : str
        Title of the interface window.

    Returns
    -------
    gui : StreamGUI
        Class object for creating the interactive window.

    See Also
    --------
    BaseGUI
    FrameGUI
    FramesGUI
    VideoGUI

    Notes
    -----
    Upon execution of the interface through ``StreamGUI.run``, this interface
    will continuously pull frames from the provided stream and display them in
    the interactive window.

    Examples
    --------
    Please see the following example scripts for some typical applications of this
    class:

    * examples/interfaces/binary_threshold_viewer_with_drawing_camera.py

    """

    def __init__(self, stream, *args, **kwargs):
        self.stream = stream
        super(StreamGUI, self).__init__(*args, **kwargs)

    def run(self) -> "StreamGUI":
        """
        Launch the interactive window.

        Notes
        -----
        Whilst this class overrides ``BaseGUI.run``, exiting the interface is the same
        as other wrappers in that any key press will cause the interface to close.

        If you provide an iterable that has a limit, the interface created will exit
        once it has reached the end of the iterable. As such, we would recommend
        using ``FramesGUI`` when using limited sequences of footage rather streams
        or feeds.

        """
        while True:
            try:
                self.frame = next(self.stream)
            except StopIteration:
                break
            except:
                raise

            frame_proc = self.process()
            cv2.imshow(self.title, frame_proc)

            k = cv2.waitKey(1)
            if k > 0:
                break
