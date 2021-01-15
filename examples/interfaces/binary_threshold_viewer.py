import vuba
import cv2

# Create a handler for reading in the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Read in the first frame for the viewer
first = video.read(index=0)

# Initiate an instance of FrameGUI
gui = vuba.FrameGUI(first, "Threshold viewer")

# Here we are declaring a main processing method. This is where our code goes for
# thresholding the image and returning it
@gui.method
def threshold(gui):
    frame = gui.frame.copy()  # create a copy of the current frame
    thresh_val = gui["thresh_val"]  # grab the current threshold value

    # Grayscale the current frame
    gray = vuba.gray(frame)

    # Threshold the current frame
    _, thresh = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)

    return thresh


# Since we are going to be applying a variable threshold, we can add
# a trackbar for scrolling through those values. Note that every
# gui class contains getters and setters for retrieving and setting
# trackbar values.
@gui.trackbar("Threshold", id="thresh_val", min=0, max=255)
def on_thresh(gui, val):
    gui["thresh_val"] = val
    img = gui.process()
    cv2.imshow(gui.title, img)


# And finally execute the gui
gui.run()

# Lastly, close the handler
video.close()
