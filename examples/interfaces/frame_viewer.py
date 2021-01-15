import vuba

# Create a handler for reading in the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Initiate an instance of VideoGUI
gui = vuba.VideoGUI(video, "Basic viewer")

# Here we do nothing except supply the current frame since we don't want
# to do any image processing on the individual frames
@gui.method
def blank(gui):
    frame = gui.frame.copy()
    return frame


# And finally, execute the gui
gui.run()

# Lastly, close the handler
video.close()
