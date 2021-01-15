import vuba
import cv2
import numpy as np

# Create a handler for the reading from the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Read in the first frame and grayscale it
first = video.read(index=0, grayscale=True)
first = vuba.shrink(
    first, by=50
)  # shrink the frame so we clearly see the separate tiles below

# Threshold the grayscaled frame to a binary threshold (n=50, to=255)
_, thresh = cv2.threshold(first, 50, 255, cv2.THRESH_BINARY)

# Find all the contours in the thresholded image
contours, hierarchy = vuba.find_contours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Apply a series of contour filters
smallest = vuba.smallest(contours)  # smallest contour by area
largest = vuba.largest(contours)  # largest contour by area
parents = vuba.parents(contours, hierarchy)  # All parent contours

# Create a series of image copies for drawing the contours found
all_ = vuba.bgr(first)
l = all_.copy()
p = all_.copy()
s = all_.copy()

# Draw the contours on the raw frame
vuba.draw_contours(p, parents, -1, (0, 0, 255), 2)
vuba.draw_contours(l, largest, -1, (255, 0, 0), 2)
vuba.draw_contours(s, smallest, -1, (0, 255, 0), 2)
vuba.draw_contours(all_, contours, -1, (0, 255, 0), 2)

# Stack the frames so we can view them all at once
img1 = np.hstack((all_, p))
img2 = np.hstack((l, s))
img = np.vstack((img1, img2))

# Resize the final image to a reasonable resolution
img = cv2.resize(img, video.resolution)

# And display it
cv2.imshow("All contours/Parents/Largest/Smallest:", img)
cv2.waitKey()

video.close()
