import vuba
import cv2

# Initiate a handler for the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Read in the first frame
first = video.read(index=0)

# And display it
cv2.imshow("First frame", first)
cv2.waitKey()

# Lastly, close the handler
video.close()
