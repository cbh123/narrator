import cv2
import time
from PIL import Image, ImageGrab
import numpy as np
import os
import glob
from datetime import datetime

# Folder
folder = "frames"
MAX_IMAGES = 10

# Create the frames folder if it doesn't exist
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)

def cleanup_old_images():
    """Keep only the 10 most recent frame images"""
    frame_files = glob.glob(os.path.join(frames_dir, "frame_*.jpg"))
    frame_files.sort(key=os.path.getctime, reverse=True)  # Sort by creation time, newest first
    
    # Remove older files if we have more than MAX_IMAGES
    for old_file in frame_files[MAX_IMAGES:]:
        try:
            os.remove(old_file)
            print(f"Removed old frame: {os.path.basename(old_file)}")
        except OSError as e:
            print(f"Error removing old frame {old_file}: {e}")

def get_latest_frame_path():
    """Get the path of the most recent frame file"""
    frame_files = glob.glob(os.path.join(frames_dir, "frame_*.jpg"))
    if frame_files:
        return max(frame_files, key=os.path.getctime)
    return None

print("📸 Starting screenshot capture... Capture is watching your screen!")

while True:
    try:
        # Take a screenshot
        screenshot = ImageGrab.grab()
        
        # Resize the image
        max_size = 250
        ratio = max_size / max(screenshot.size)
        new_size = tuple([int(x*ratio) for x in screenshot.size])
        resized_img = screenshot.resize(new_size, Image.LANCZOS)

        # Convert the PIL image to an OpenCV image for saving
        frame = cv2.cvtColor(np.array(resized_img), cv2.COLOR_RGB2BGR)

        # Generate timestamped filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        frame_filename = f"frame_{timestamp}.jpg"
        tmp_path = os.path.join(frames_dir, f"frame_{timestamp}.tmp.jpg")
        final_path = os.path.join(frames_dir, frame_filename)
        
        try:
            cv2.imwrite(tmp_path, frame)
            os.rename(tmp_path, final_path)
            
            # Also create/update a symlink to the latest frame for backward compatibility
            latest_link = os.path.join(frames_dir, "frame.jpg")
            if os.path.exists(latest_link) or os.path.islink(latest_link):
                os.remove(latest_link)
            os.symlink(frame_filename, latest_link)
            
            # Clean up old images
            cleanup_old_images()
            
        except cv2.error as e:
            print(f"OpenCV error: Failed to write image: {e}")
        except OSError as e:
            print(f"OS error: Failed to rename image: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during file operation: {e}")
            
    except Exception as e:
        print(f"Failed to capture screenshot: {e}")

    # Wait for 2 seconds
    time.sleep(2)

# Cleanup
cv2.destroyAllWindows()
