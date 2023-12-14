import os
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa
import errno
from elevenlabs import generate, play, set_api_key, voices
import google.generativeai as genai
import PIL.Image



client = OpenAI()
genai.configure(api_key = os.environ.get("GEMINI_API_KEY"))

set_api_key(os.environ.get("ELEVENLABS_API_KEY"))

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
    audio = generate(text, voice=os.environ.get("ELEVENLABS_VOICE_ID"))

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(audio)

    play(audio)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
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
                "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
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


def main():
    script = []

    model = input("Which model would you like to use? 1. GPT-4 Vision 2. Gemini Pro Vision \n")
    
    if model == "1":
        print("using GPT-4 Vision")
        print("👀 David is watching...")

        while True:
            # path to your image
            image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")


            # getting the base64 encoding
            base64_image = encode_image(image_path)
            analysis = analyze_image(base64_image, script=script)


            print("🎙️ David says:")
            print(analysis)

            play_audio(analysis)

            script = script + [{"role": "assistant", "content": analysis}]

            # wait for 5 seconds
            time.sleep(5)
            
    elif model == "2":
        print("using Gemini Pro Vision")
        print("👀 David is watching...")

        while True:
            # path to your image
            image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

            img = PIL.Image.open(image_path)
            
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content(["""
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
                """+"refer to these previous narrations".join(script), img])

            response_text = response.text


            print("🎙️ David says:")
            print(response_text)

            play_audio(response_text)

            script = script + [response_text]

            # wait for 5 seconds
            time.sleep(5)

    else:
        print("Please enter a valid model number")


if __name__ == "__main__":
    main()
