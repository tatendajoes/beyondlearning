import cv2
import glob
import os

# Parameters
img_dir = r"C:\Users\taten\Downloads\activity\content\new-student-classroom-activity-3-2\train\images"
out_file = 'output.mp4'
# Use fewer frames for quicker test
max_frames = 200
# Lower FPS for slower playback
fps = 10.0  

# Get sort ed list of image files, limit to first max_frames
all_images = sorted(glob.glob(os.path.join(img_dir, '*.jpg')))
images = all_images[:max_frames]
if not images:
    raise ValueError(f"No images found in {img_dir}")

# Read first image to get frame size
first = cv2.imread(images[0])
height, width = first.shape[:2]

# Define the codec and create VideoWriter
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(out_file, fourcc, fps, (width, height))
if not out.isOpened():
    raise RuntimeError(f"Cannot open VideoWriter for '{out_file}'")

# Write each frame
for img_path in images:
    img = cv2.imread(img_path)
    if (img.shape[1], img.shape[0]) != (width, height):
        img = cv2.resize(img, (width, height))
    out.write(img)

out.release()

# Playback the result at the reduced speed
cap = cv2.VideoCapture(out_file)
if not cap.isOpened():
    raise RuntimeError(f"Cannot open video file '{out_file}'")

delay_ms = int(10000 / fps)  # controls speed between frames
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv2.imshow('Playback (press q to quit)', frame)
    if cv2.waitKey(delay_ms) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
