import cv2
import time

# Folder
folder = "frames"

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
        # Save the frame as an image file
        print("📸 Say cheese! Saving frame.")
        path = f"{folder}/frame.jpg"
        cv2.imwrite(path, frame)
    else:
        print("Failed to capture image")

    # Wait for 5 seconds
    time.sleep(2)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
