import tkinter as tk
import subprocess

NARRATOR_DIR = "/Users/charlieholtz/workspace/dev/narrator"


def run_command1():
    applescript_command = f"""
    tell application "Terminal"
        do script "cd {NARRATOR_DIR} && source .env && source venv/bin/activate && python3 capture.py"
        activate
    end tell

    tell application "Terminal"
        do script "cd {NARRATOR_DIR} && source .env && source venv/bin/activate && python3 narrator.py"
        activate
    end tell
    """
    subprocess.run(["osascript", "-e", applescript_command])


# Create the main window
window = tk.Tk()
window.title("AI Narrator")

# Create buttons for each command
button1 = tk.Button(window, text="Start", command=run_command1)
button1.pack(pady=10)

# Start the GUI event loop
window.mainloop()
