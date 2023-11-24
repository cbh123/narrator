import os
import time
from playsound import playsound

def find_latest_folder(base_path):
    all_folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    latest_folder = max(all_folders, key=os.path.getmtime)
    return latest_folder

def main():
    base_path = 'narration'  # Base path to the narration folder
    last_played_folder = None

    while True:
        latest_folder = find_latest_folder(base_path)
        audio_file = os.path.join(latest_folder, 'audio.wav')

        if os.path.exists(audio_file) and latest_folder != last_played_folder:
            print(f"Playing audio from {audio_file}")
            playsound(audio_file)
            last_played_folder = latest_folder
            # After the audio finishes, wait for a short period before checking for new folders
            # time.sleep(2)

if __name__ == "__main__":
    main()
