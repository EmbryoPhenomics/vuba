import vuba
import cv2

# Initiate a handler for the images
video = vuba.Video("../example_data/raw_images/*.png")

# Create a handler for all the frames found
frames = video.read(start=0, stop=len(video))

# Iterate across the frames and display them
for frame in frames:
    cv2.imshow("Multiple frames", frame)
    k = cv2.waitKey(30)

    if k == 27:
        break

# Lastly, close the handler
video.close()
