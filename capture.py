import cv2
import time
from PIL import Image
import numpy as np
import os

# Folder
folder = "frames"

# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

# Wait for the camera to initialize and adjust light levels
time.sleep(2)

while True:
    ret, frame = cap.read()
    if ret:
        # Resize the image before saving to improve performance
        max_size = 400
        height, width = frame.shape[:2]
        if height > width:
            new_height = max_size
            new_width = int((max_size / height) * width)
        else:
            new_width = max_size
            new_height = int((max_size / width) * height)
        
        frame = cv2.resize(frame, (new_width, new_height))

        # Save the frame as an image file
        print("📸 Say cheese! Saving frame.")
        path = os.path.join(frames_dir, "frame.jpg")
        cv2.imwrite(path, frame)
    else:
        print("Failed to capture image")

    # Wait for 2 seconds
    time.sleep(2)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
