import base64
import errno
import os
import shutil
import time

from dotenv import load_dotenv
from elevenlabs import generate, play, set_api_key, stream
from openai import OpenAI
from pynput import (  # Using pynput to listen for a keypress instead of native keyboard module which was requiring admin privileges
    keyboard,
)

# import environment variables from .env file
load_dotenv()

client = OpenAI()

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

# Initializes the variables based their respective environment variable values, defaulting to false
isStreaming = os.environ.get("ELEVENLABS_STREAMING", "false") == "true"
isPhotoBooth = os.environ.get("PHOTOBOOTH_MODE", "false") == "true"

script = []
narrator = "Sir David Attenborough"


def encode_image(image_path):
    while True:
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except IOError as e:
            if e.errno != errno.EACCES:
                # Not a "file in use" error, re-raise
                raise
            # File is being written to, wait a bit and retry
            time.sleep(0.1)


def play_audio(text):
    audio = generate(
        text,
        voice=os.environ.get("ELEVENLABS_VOICE_ID"),
        model="eleven_turbo_v2",
        stream=isStreaming,
    )

    if isStreaming:
        # Stream the audio for more real-time responsiveness
        stream(audio)
        return

    # Save the audio to a file
    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(audio)

    # Copy the image analyzed to the same directory as the audio file
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")
    new_image_path = os.path.join(dir_path, "image.jpg")
    shutil.copy(image_path, new_image_path)

    play(audio)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Describe this image as if you are {narrator}",
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": f"""
                You are {narrator}. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )
    response_text = response.choices[0].message.content
    return response_text


def _main():
    global script

    # path to your image
    image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

    # getting the base64 encoding
    base64_image = encode_image(image_path)

    # analyze posture
    print(f"👀 {narrator} is watching...")
    analysis = analyze_image(base64_image, script=script)

    print("🎙️ David says:")
    print(analysis)

    play_audio(analysis)

    script = script + [{"role": "assistant", "content": analysis}]


def main():
    while True:
        if isPhotoBooth:
            pass
        else:
            _main()

            # wait for 5 seconds
            time.sleep(5)


def on_press(key):
    if key == keyboard.Key.space:
        # When space bar is pressed, run the main function which analyzes the image and generates the audio
        _main()


def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False


# Create a listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# Start the listener
listener.start()

if isPhotoBooth:
    print(f"Press the spacebar to trigger {narrator}")

if __name__ == "__main__":
    main()
