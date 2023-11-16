from PIL import ImageGrab
import os
import time

# Create a folder to store the screenshot if it doesn't exist
folder = "screenshots"
if not os.path.exists(folder):
    os.makedirs(folder)

# Constant filename for the screenshot
filename = os.path.join(folder, "screenshot.png")

# Function to take a screenshot
def take_screenshot(filename):
    # Capture the entire screen
    screen = ImageGrab.grab()
    # Save the image file
    screen.save(filename)

try:
    while True:
        take_screenshot(filename)
        print(f"Screenshot saved as {filename}")
        time.sleep(5)  # Wait for 5 seconds before taking the next screenshot
except KeyboardInterrupt:
    print("Stopped taking screenshots")
