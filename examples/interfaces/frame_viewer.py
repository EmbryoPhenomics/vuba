import vuba

# Create a handler for reading in the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Read in the frames to an in-memory container
frames = video.read(0, len(video), low_memory=False)

# Initiate an instance of FramesGUI with the in-memory frames array
gui = vuba.FramesGUI(frames.ndarray, title='Basic')

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
