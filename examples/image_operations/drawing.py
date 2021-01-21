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

# Create a series of image copies for drawing the shapes
none = vuba.bgr(first)
cnts = none.copy()
rects = none.copy()
circs = none.copy()

# Find all bounding boxes for the contours detected
bboxs = vuba.fit_rectangles(contours)

# Compute circle dimensions based on contour moments
circles = vuba.fit_circles(contours)

# Draw all the shapes on each of the corresponding tiles
vuba.draw_contours(cnts, contours, -1, (0, 255, 0), 1)
vuba.draw_rectangles(rects, bboxs, (0, 255, 0), 1)
vuba.draw_circles(circs, circles, (0, 255, 0), 1)

# Stack the tiles so we can view them all at once
img1 = np.hstack((none, cnts))
img2 = np.hstack((rects, circs))
img = np.vstack((img1, img2))

# Resize the final image to a reasonable resolution
img = cv2.resize(img, video.resolution)

# And display it
cv2.imshow("Different drawing functions:", img)
cv2.waitKey()

video.close()
