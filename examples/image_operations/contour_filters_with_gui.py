import vuba
import cv2
import numpy as np

# Create a handler for reading in the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Read in the first frame for the viewer
first = video.read(index=0)

# Initiate an instance of FrameGUI
gui = vuba.FrameGUI(first, "Threshold viewer")

# The main processing method.
@gui.method
def segment(gui):
    frame = gui.frame.copy()  # create a copy of the current frame
    thresh_val = gui["thresh_val"]  # grab the current threshold value
    area_val = gui["area"]
    solid_val = gui["solidity"] / 100  # divide value by 100 to find true value
    ecc_val = gui["eccentricity"] / 100

    # Construct contour filters
    area_filt = vuba.Area(min=area_val)
    solid_filt = vuba.Solidity(min=solid_val)
    ecc_filt = vuba.Eccentricity(max=ecc_val)

    # Grayscale the current frame
    gray = vuba.gray(frame)

    # Threshold the current frame
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

    # Retrieve contours from the thresholded image
    contours, hierarchy = vuba.find_contours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Combine our contour filters to produce the final contours array
    contours = area_filt(contours)
    contours = solid_filt(contours)
    contours = ecc_filt(contours)

    if contours:
        vuba.draw_contours(frame, contours, -1, (0, 255, 0), 1)

    return frame


# Our variable threshold trackbar
@gui.trackbar("Threshold", id="thresh_val", min=0, max=255)
def on_thresh(gui, val):
    gui["thresh_val"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


# Our contour filter trackbars
@gui.trackbar("Area", id="area", min=1, max=10000)
def on_area(gui, val):
    gui["area"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


# Note that for both solidity and eccentricity trackbars we are
# supplying very large ranges so we can have fine scaling
# for the filters above.
@gui.trackbar("Solidity", id="solidity", min=1, max=100)
def on_solidity(gui, val):
    gui["solidity"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


@gui.trackbar("Eccentricity", id="eccentricity", min=0, max=400)
def on_eccentricity(gui, val):
    gui["eccentricity"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


# And finally execute the gui
gui.run()

video.close()
