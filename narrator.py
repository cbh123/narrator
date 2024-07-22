import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
# import json
import time
# import simpleaudio as sa
import errno
from elevenlabs import play, Voice
from elevenlabs.client import ElevenLabs

# Load environment variables from a .env file
load_dotenv()

# Initialize OpenAI and ElevenLabs clients
clientOA = OpenAI()
clientEL = ElevenLabs(
  api_key=os.environ.get("ELEVENLABS_API_KEY")
)

def encode_image(image_path):
    """
    Encodes an image to base64.
    
    Args:
        image_path (str): The path to the image file.
        
    Returns:
        str: Base64 encoded string of the image.
    """
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
    """
    Generates and plays audio from text using ElevenLabs.
    
    Args:
        text (str): The text to be converted to speech.
    """
    # Generate audio from text
    audio_generator = clientEL.generate(text=text, voice=Voice(voice_id=os.environ.get("ELEVENLABS_VOICE_ID")))

    # Create a unique directory for storing the audio file
    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    # Gather audio data from generator
    audio_bytes = b''.join(audio_generator)

    # Save audio to file
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    # Play the generated audio
    play(audio_bytes)

def generate_new_line(base64_image):
    """
    Generates a new line of messages for the OpenAI API call.
    
    Args:
        base64_image (str): Base64 encoded string of the image.
        
    Returns:
        list: A list of messages to be sent to the OpenAI API.
    """
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image as if you are Sir David Attenborough narrating a nature documentary about homo sapiens."},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                    },
                },
            ],
        },
    ]

def analyze_image(base64_image, script):
    """
    Analyzes an image using OpenAI's language model.
    
    Args:
        base64_image (str): Base64 encoded string of the image.
        script (list): List of previous messages to maintain context.
        
    Returns:
        str: The response text from OpenAI.
    """
    response = clientOA.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
                You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
                Be accurate, snarky, and funny. Describe what the human is actually doing. Make it short and concise, within 3 sentences. If the human is doing something remotely interesting, make a big deal about it!
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=150,
        temperature=0.7,
    )
    response_text = response.choices[0].message.content
    return response_text

def main():
    script = []

    while True:
        # Path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # Get the base64 encoding of the image
        base64_image = encode_image(image_path)

        # Analyze the image and generate a narration
        print("👀 David is watching...")
        analysis = analyze_image(base64_image, script=script)

        # Print and play the narration
        print("🎙️ David says:")
        print(analysis)
        play_audio(analysis)

        # Append the analysis to the script for context in future requests
        script.append({"role": "assistant", "content": analysis})

        # wait for 3 seconds
        time.sleep(3)

if __name__ == "__main__":
    main()