import vuba
import cv2

# Initiate a video for the images
video = vuba.Video("../example_data/raw_images/*.png")

# Initiate a writer for exporting the images to a video
# Note that since we did not supply a codec, the images will be
# encoded using the MJPG codec
writer = vuba.Writer("./test.avi", video, fps=15)

# Create a handler for all the frames found
frames = video.read(start=0, stop=len(video))

# Iterate across the frames and display/export them
for frame in frames:
    cv2.imshow("Multiple frames", frame)
    k = cv2.waitKey(30)

    if k == 27:
        break

    writer.write(frame)

# Lastly, close the handlers
video.close()
writer.close()
