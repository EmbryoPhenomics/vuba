import vuba
import cv2
import numpy as np


def grab_frames(camera):
    """
    Simple function for creating a generator that will
    continuously retrieve frames from the camera device.

    """
    while True:
        yield camera.read(0)


# Create a handler for capturing images from the camera at '/dev/video0'
camera = vuba.Video(0)

# Initialise the frame grabber
capture_stream = grab_frames(camera)

# Initiate an instance of CameraGUI
gui = vuba.CameraGUI(capture_stream, "Threshold viewer")

# Here we are declaring a main processing method. This is where our code goes for
# thresholding an image and returning it
@gui.process
def threshold(gui):
    frame = gui.frame.copy()  # create a copy of the current frame
    thresh_val = gui["thresh_val"]  # grab the current threshold value

    # Grayscale the current frame
    gray = vuba.gray(frame)

    # Threshold the current frame
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

    # Retrieve contours from the thresholded image
    contours, hierarchy = vuba.find_contours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE
    )

    # Draw the contours found on the current frame
    vuba.draw_contours(frame, contours, -1, (0, 255, 0), 1)

    # Convert the thresholded image to BGR for the horizontal stacking below
    thresh = vuba.bgr(thresh)

    img = np.hstack((frame, thresh))

    return img


# Since we are going to be applying a variable threshold, we can add
# a trackbar for scrolling through those values.
@gui.trackbar("Threshold", id="thresh_val", min=0, max=255)
def on_thresh(gui, val):
    gui["thresh_val"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


# And finally execute the gui
gui.run()

# Lastly, close the handler
camera.close()
