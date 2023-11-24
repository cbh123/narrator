import os
import time
import pyautogui
from PIL import Image

# Folder
folder = "frames"
frames_dir = os.path.join(os.getcwd(), folder)
os.makedirs(frames_dir, exist_ok=True)

while True:

    # Wait for Chrome to activate
    time.sleep(2)

    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Convert screenshot to RGB (JPEG does not support RGBA)
    screenshot_rgb = screenshot.convert('RGB')

    # Optional: Resize the image
    max_size = 250
    ratio = max_size / max(screenshot_rgb.size)
    new_size = tuple([int(x * ratio) for x in screenshot_rgb.size])
    resized_img = screenshot_rgb.resize(new_size, Image.LANCZOS)

    # Save the frame as an image file
    print("📸 Captured Chrome tab. Saving frame.")
    path = f"{frames_dir}/frame.jpg"
    resized_img.save(path)
