import vuba
import cv2

# Initiate a video for the images
video = vuba.Video([f"../example_data/raw_images/{i}.png" for i in range(100)])

# Initiate a writer for exporting the images
writer = vuba.Writer([f"./{i}.png" for i in range(len(video))], video)

# Create a handler for all the frames found
frames = video.read(start=0, stop=len(video))

# Iterate across the frames and display/write them
for frame in frames:
    cv2.imshow("Multiple frames", frame)
    k = cv2.waitKey(30)

    if k == 27:
        break

    writer.write(frame)

# Lastly, close the handlers
video.close()
writer.close()
