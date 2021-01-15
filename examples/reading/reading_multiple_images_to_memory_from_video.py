import vuba
import cv2

# Initiate a handler for the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Create a handler for all the frames found and import them into memory
# Note that this instance of frames now contains a contiguous numpy array
# that holds the imported frames
frames = video.read(start=0, stop=len(video), low_memory=False)

# Iterate across the frames and display them
for frame in frames:
    cv2.imshow("Multiple frames", frame)
    k = cv2.waitKey(30)

    if k == 27:
        break

# Lastly, close the handler
video.close()
