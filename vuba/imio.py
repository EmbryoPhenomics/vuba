from tqdm import tqdm
import cv2
import numpy as np
import glob
import math
import copy
from more_itertools import prepend
from natsort import natsorted, ns
import warnings

from vuba import ops


def take_first(it):
    """
    Retrieve the first value from an iterable object.

    Parameters
    ----------
    it : iterable
        Iterable object to retrieve the first value from.

    Returns
    -------
    first : number or string or ndarray or None
        First value from the iterable object. Will be
        None if ``StopIteration`` is raised.

    """

    it = iter(it)
    try:
        return next(it)
    except StopIteration:
        return None


def fourcc_to_string(fourcc):
    """
    Convert fourcc integer code into codec string.

    Parameters
    ----------
    fourcc : int
        Fourcc integer code.

    Returns
    -------
    codec : str
        Codec string corresponding to fourcc code.

    """
    char1 = str(chr(fourcc & 255))
    char2 = str(chr((fourcc >> 8) & 255))
    char3 = str(chr((fourcc >> 16) & 255))
    char4 = str(chr((fourcc >> 24) & 255))

    return char1 + char2 + char3 + char4


def open_video(video):
    """
    Convenience function for creating a ``Video`` instance.

    Parameters
    ----------
    video : str or cv2.VideoCapture or list.
        Full filename or VideoCapture object to a video (e.g. AVI or MP4),
        or a glob string or series of filenames to a series of individual
        images.

    Returns
    -------
    video : Video
        Instance of ``Video``.
    release : bool
        True if footage was not an instance to ``Video``, else False.

    """
    release = False
    if not isinstance(video, Video):
        video = Video(video)
        release = True

    return video, release


class Frames:
    """
    Container for frames that is used in ``Video.read``.

    Parameters
    ----------
    reader : callable
        Frame reader method supplied from ``Video`` class.
    start : int
        Index of first frame.
    stop : int
        Index of last frame.
    step : int
        Step size.
    low_memory : bool
        Whether to import frames into memory.
    grayscale : bool
        Whether to convert frames to grayscale.

    Returns
    -------
    frames : Frames
        Container for frames.

    Notes
    -----
    Frames are imported into memory at initiation if low_memory=False.

    See Also
    --------
    Video

    """

    def __init__(self, reader, start, stop, step, low_memory, grayscale):
        self._reader = reader
        self.idxs = (start, stop, step)
        self.grayscale = grayscale
        self.in_mem = False
        self._roi = None

        if not low_memory:
            self.import_to_ndarray()

    def import_to_ndarray(self) -> "Frames":
        """
        Import the declared frames into a contiguous numpy array.

        """
        gen_fr = self._reader(*self.idxs, self.grayscale)
        first = take_first(gen_fr)
        self.ndarray = np.ascontiguousarray(
            np.empty((len(self), *first.shape), dtype="uint8")
        )
        gen_fr = prepend(first, gen_fr)

        print("Importing frames into memory...")
        pg = tqdm(len(self))
        for i, frame in enumerate(gen_fr):
            self.ndarray[i, :] = frame[:]
            pg.update(1)
        pg.close()

        self.in_mem = True

    def __len__(self) -> "Frames":
        """
        Retrieve the length of the provided frames without having to iterate
        across them.

        Returns
        -------
        length : int
            Length of the provided frames.

        """
        (start, stop, step) = self.idxs
        return math.floor((stop - start) / step)

    def __iter__(self) -> "Frames":
        """
        Retrieve the frames declared at initiation.

        Returns
        -------
        frames : generator
            Generator that supplies frames.

        """
        if self.in_mem:
            for frame in self.ndarray:
                yield frame
        else:
            for frame in self._reader(*self.idxs, self.grayscale):
                yield frame


class Video:
    """
    Wrapper around various image readers that provides a simple API
    to achieve the same functions regardless of format.

    Parameters
    ----------
    footage : str or ``cv2.VideoCapture`` or list.
        Full filename or VideoCapture object to a video (e.g. AVI or MP4),
        or a glob string or series of filenames to a series of individual
        images. Note that series of all individual filenames will be sorted
        prior to being read if a glob string is supplied.

    Returns
    -------
    video : Video
        Video handler for footage supplied.

    See Also
    --------
    open_video
    Frames
    Writer

    Examples
    --------
    For example usage of this handler please see example scripts located
    at ``examples/reading``.

    """

    def __init__(self, footage):
        def open_videocv(footage):
            self.video = footage
            self.video_release = False
            if not isinstance(self.video, cv2.VideoCapture):
                self.video = cv2.VideoCapture(self.video)
                self.video_release = True
            self.filenames = None

        if isinstance(footage, list):
            self.filenames = footage
            self.video = self.video_release = None
        else:
            try:
                # Somewhat hacky but provides consistent behaviour
                if "*" in footage:
                    files = glob.glob(footage)
                    self.filenames = natsorted(files, alg=ns.IGNORECASE)
                    self.video = self.video_release = None
                else:
                    open_videocv(footage)
            except TypeError:
                open_videocv(footage)
            except:
                raise

        self._grab_info()

    def __len__(self) -> "Video":
        """
        Retrieve the length of the provided footage without having to iterate
        across it.

        Returns
        -------
        length : int
            Length of the provided footage.

        """
        if self.video:
            return int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        else:
            return len(self.filenames)

    def _grab_info(self):
        """
        Grab summary footage information.

        This method is called on initiation of ``Video``.

        """
        if self.video:
            self.fps = round(self.video.get(cv2.CAP_PROP_FPS))

            width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
            height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self.resolution = (self.width, self.height) = tuple(
                map(round, (width, height))
            )

            self.fourcc_code = int(self.video.get(cv2.CAP_PROP_FOURCC))
            self.codec = fourcc_to_string(self.fourcc_code)
        else:
            first_frame = self.read(0)
            width = first_frame.shape[1]
            height = first_frame.shape[0]
            self.resolution = (self.width, self.height) = tuple(
                map(round, (width, height))
            )

            self.fps = self.codec = self.fourcc_code = None

    def read(self, *args, **kwargs) -> "Video":
        """
        Read single or multiple frames from the provided footage.

        Note that reading multiple frames follows slice behaviour,
        whereby there is a 'start', 'stop' and 'step'. However steps will
        only give a performance uplift for reading images stored as
        individual files (e.g. multiple pngs). If you are reading from
        videos, the read time will be the same as if you were reading
        all the frames between 'start' and 'stop'. This is because it is
        faster to pass on frames that don't match the step size, than it is
        to repeatedly locate the correct frames by index in the video file.

        Parameters
        ----------
        * For single frames:
            index : int
                Index of frame in footage to read.
            grayscale : bool
                Whether to convert frame to grayscale.

        * For multiple frames:
            start : int
                Index of frame to start reading from.
            stop : int
                Index of frame to stop reading at.
            step : int
                Step size.
            low_memory : bool
                Whether to import frames into RAM, default is True i.e. not to.
            grayscale
                Whether to convert frames to grayscale.

        Returns
        -------
        For single frames:
            frame : ndarray
                Frame at the given index.

        For multiple frames:
            frames : Frames
                Container that will either supply the frames from
                an ndarray or from a generator. Note that this
                container contains both a len and iter method. For the
                latter, a new generator is created upon calling the
                method if the frames have not been imported into memory.
                This is to maintain implementation parity with the
                in-memory container.

        Raises
        ------
        ValueError
            If the supplied indices are not within the available range of the
            selected footage, or if there is a missing required argument.

        Examples
        --------
        For example usage of this method please see example scripts located
        at ``examples/reading``.

        """
        try:
            frame = self._read_single(*args, **kwargs)
            return frame
        except TypeError:
            args = self._prep_args_kwargs(*args, **kwargs)
            frames = Frames(self._read_multi, *args)
            return frames
        except:
            raise

    def _prep_args_kwargs(
        self, start=None, stop=None, step=1, low_memory=True, grayscale=False
    ):
        """
        Prep any args and kwargs supplied from Video.read().

        """

        def check_indexes(index):
            if index is not None:
                if index < 0 or index > len(self):
                    raise IndexError(
                        "Indices out of available range for provided footage."
                    )
            else:
                raise ValueError(f"Missing required argument.")

        check_indexes(start)
        check_indexes(stop)

        return (start, stop, step, low_memory, grayscale)

    def _read_single(self, index, grayscale=False):
        """
        Read a single frame at a given location in the requested footage.

        """
        if self.video:
            self.video.set(1, index)
            success, frame = self.video.read()
        else:
            frame = cv2.imread(self.filenames[index])

        if grayscale:
            frame = ops.gray(frame)

        return frame

    def _read_multi(self, start, stop, step, grayscale):
        """
        Read multiple frames from the requested footage at the given indices.

        """
        if self.video:
            self.video.set(1, start)

            if step:
                if step > 1:
                    # Floor is used here to stop out-of-range indices being created
                    number = math.floor((stop - start) / step)
                    frames_to_yield = [round((step * n) + start) for n in range(number)]
                    steps = True
                else:
                    steps = False

            for fr in range(start, stop):
                success, frame = self.video.read()
                if not success:
                    break

                if grayscale:
                    frame = ops.gray(frame)

                if steps:
                    if fr in frames_to_yield:
                        yield frame
                    else:
                        pass
                else:
                    yield frame
        else:
            for fn in self.filenames[slice(start, stop, step)]:
                frame = cv2.imread(fn)
                if grayscale:
                    frame = ops.gray(frame)
                yield frame

    def close(self) -> "Video":
        """
        Close/teardown attached video handlers.

        """
        if self.video:
            self.video.release()
        elif self.filenames:
            self.filenames = None


class Writer:
    """
    Create an encoder for exporting frames at a given output.

    Regardless of input format, this encoder can encode footage to both individual
    images and to video files. For encoding to individual images, a sequence of
    filenames needs to be supplied that will match the length of the number of frames
    that need to be encoded. Conversely, for encoding to a video file, a filename to
    the video file needs to be provided.

    Parameters
    ----------
    output : str or list
        Output to export frames.
    footage : Video
        Instance of Video to create writer based on. If this is
        not supplied then you must supply all encoder specific arguments.
    fps : float
        Framerate to export footage at, default is the fps of
        the video supplied. Note that this argument must be supplied
        if working with individual images.
    resolution : tuple
        Width and height to export footage at (both must be supplied
        as integers). Default is the resolution of the footage supplied.
    codec : str
        Codec to encode footage with. Default is to encode with MJPG
        codec or that of the Video instance supplied (if any).
    grayscale : bool
        Whether to export footage as grayscale. Default is False.

    Returns
    -------
    encoder : Writer
        Encoder to export frames to a given output.

    Raises
    ------
    ValueError
        If a frame-rate is not supplied when encoding to a movie using
        individual images.

    See Also
    --------
    Video

    Examples
    --------
    For example usage of this handler please see example scripts located
    at ``examples/writing``.

    """

    def __init__(
        self,
        output,
        footage=None,
        fps=None,
        resolution=None,
        codec=None,
        grayscale=False,
    ):
        self.footage_release = None
        if footage:
            footage, self.footage_release = open_video(footage)

        self.is_color = True
        if grayscale:
            self.is_color = False

        self.resolution = resolution
        if not resolution:
            self.resolution = footage.resolution

        self.encoder_release = False
        if isinstance(output, str):
            if not codec:
                if footage:
                    if footage.video:
                        codec = footage.codec
                    else:
                        codec = "MJPG"
                else:
                    codec = "MJPG"

            fourcc = cv2.VideoWriter_fourcc(*codec)

            if not fps:
                if footage:
                    if footage.fps:
                        fps = footage.fps
                    else:
                        raise ValueError(
                            "When working with individual images you must supply a frame-rate to export footage at."
                        )
                else:
                    raise ValueError(
                        "Integer must be supplied to fps when an instance of vuba.Video is not supplied."
                    )

            self.encoder = cv2.VideoWriter(
                output, fourcc, fps, self.resolution, self.is_color
            )
            self.encoder_release = True
        elif isinstance(output, list):
            self.encoder = iter(output)
            self.fps = self.fourcc = None

    def write(self, frame) -> "Writer":
        """
        Write a frame using the declared encoder.

        Parameters
        ----------
        frame : ndarray
            Frame to export.

        Warns
        -----
        UserWarning
            If the supplied frame is not of the correct resolution or colour space,
            and to notify the user that the frame has been correctly converted so
            encoding is successful.

        Notes
        -----
        For encoding to video, note that if the frames supplied for encoding are not at
        the same resolution as that set for the encoder upon initiation, the frames will
        be resized accordingly. Also note that frames will be converted to the colour
        space set at initiation if they are not the same. These features are built-in so
        that a complete movie is always created, rather than an empty container which
        is not of much use for debugging a failed component of a script.

        Examples
        --------
        For example usage of this method please see example scripts located
        at ``examples/writing``.

        """
        if isinstance(self.encoder, cv2.VideoWriter):
            size = (frame.shape[1], frame.shape[0])
            if size != self.resolution:
                frame = cv2.resize(frame, self.resolution)
                warnings.warn(
                    f"Frame has been resized to ensure successful encoding. Supplied frame vs encoder resolution: {size} , {self.resolution}",
                    UserWarning,
                )

            channels = len(frame.shape)
            if channels > 2 and not self.is_color:
                frame = ops.gray(frame)
                warnings.warn(
                    f"Frame has been grayscaled to ensure successful encoding. Supplied frame vs encoder format: {channels} , {2, self.is_color}",
                    UserWarning,
                )
            elif channels == 2 and self.is_color:
                frame = ops.bgr(frame)
                warnings.warn(
                    f"Frame has been grayscaled to ensure successful encoding. Supplied frame vs encoder format: {channels} , {3, self.is_color}",
                    UserWarning,
                )
            self.encoder.write(frame)
        else:
            cv2.imwrite(next(self.encoder), frame)

    def close(self) -> "Writer":
        """
        Close/teardown declared encoders.

        """
        if self.encoder_release:
            self.encoder.release()
        if self.footage_release:
            self.footage.close()
