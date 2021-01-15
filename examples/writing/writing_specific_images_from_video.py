import vuba
import cv2

# Initiate a video for the images
video = vuba.Video("../example_data/raw_video/test.avi")

# Initiate a writer for exporting the image
writer = vuba.Writer(["./first.png"], video)

# Read in the first frame
first = video.read(index=0)

# Display it
cv2.imshow("First frame", first)
cv2.waitKey()

# Export it
writer.write(first)

# Lastly, close the handlers
video.close()
writer.close()
