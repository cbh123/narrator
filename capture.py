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

print("📸 Starting image capture... Say cheese!")

while True:
    ret, frame = cap.read()
    if ret:
        # Convert the frame to a PIL image
        pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Resize the image
        max_size = 250
        ratio = max_size / max(pil_img.size)
        new_size = tuple([int(x*ratio) for x in pil_img.size])
        resized_img = pil_img.resize(new_size, Image.LANCZOS)

        # Convert the PIL image back to an OpenCV image
        frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

        # Save the frame as an image file
        tmp_path = os.path.join(frames_dir, "frame.tmp.jpg")
        final_path = os.path.join(frames_dir, "frame.jpg")
        
        try:
            cv2.imwrite(tmp_path, frame)
            os.rename(tmp_path, final_path)
        except cv2.error as e:
            print(f"OpenCV error: Failed to write image: {e}")
        except OSError as e:
            print(f"OS error: Failed to rename image: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file operation: {e}")
            
    else:
        print("Failed to capture image")

    # Wait for 2 seconds
    time.sleep(2)

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
