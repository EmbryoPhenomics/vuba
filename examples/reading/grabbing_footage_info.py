import vuba

# Create a handler for reading in the video
video = vuba.Video("../example_data/raw_video/test.avi")

# Here we're going to display some of the associated properties of the video
# These can be useful for passing to other methods that are dependent on them
print(f"Resolution: {video.resolution}")
print(f"Width: {video.width}, Height: {video.height}")
print(f"Frame-rate: {video.fps}")
print(f"Fourcc code: {video.fourcc_code}")
print(f"Codec: {video.codec}")
print(f"Number of frames: {len(video)}")
print(f"Handler type: {type(video.video)} \n")

# Lastly, we need to close the handler
video.close()

# Note that this is different for handling individual images, with
# not all the above properties being available:
video = vuba.Video("../example_data/raw_images/*.png")

print(f"Resolution: {video.resolution}")
print(f"Width: {video.width}, Height: {video.height}")
print(f"Frame-rate: {video.fps}")
print(f"Fourcc code: {video.fourcc_code}")
print(f"Codec: {video.codec}")
print(f"Number of frames: {len(video)}")
print(f"Individual images: {video.filenames[:5]}")  # display the first 5 paths

video.close()
