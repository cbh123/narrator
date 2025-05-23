import os
from dotenv import load_dotenv
from openai import OpenAI
import base64
import json
import time
import simpleaudio as sa
import errno
from elevenlabs.client import ElevenLabs
from elevenlabs import play

# Load environment variables from .env file
load_dotenv()

client = OpenAI()
elevenlabs_client = ElevenLabs(
    api_key=os.environ.get("ELEVENLABS_API_KEY")
)


def encode_image(image_path, retries=3, delay=0.1):
    for attempt in range(retries):
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")
        except FileNotFoundError:
            print(f"Error: Image file not found at {image_path}. Retrying...")
            time.sleep(delay)
        except IOError as e:
            # Handles other I/O errors, including permission errors if they still occur
            print(f"IOError when trying to read {image_path}: {e}. Retrying...")
            time.sleep(delay)
        except Exception as e:
            print(f"An unexpected error occurred while encoding image {image_path}: {e}")
            return None # Or raise, depending on desired behavior for unexpected errors
    print(f"Failed to encode image {image_path} after {retries} retries.")
    return None


def play_audio(text):
    try:
        voice_id = os.environ.get("ELEVEN_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        # Generate audio using the new ElevenLabs client API
        audio = elevenlabs_client.generate(
            text=text,
            voice=voice_id,
            model="eleven_turbo_v2"
        )
    except Exception as e: # Replace with specific ElevenLabs APIError if available
        print(f"Error generating audio with ElevenLabs: {e}")
        return

    try:
        unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
        dir_path = os.path.join("narration", unique_id)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, "audio.wav")

        with open(file_path, "wb") as f:
            f.write(audio)
        
        play(audio) # Assuming play() is blocking; if not, ensure file is written before next step
    except IOError as e:
        print(f"IOError saving or playing audio file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during audio playback: {e}")


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    },
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    if not base64_image:
        return "Error: Could not encode image for analysis."
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
            {
                "role": "system",
                "content": """
                Narrate the picture in the style of a nature documentary. Be observational, insightful, and use vivid language. Maintain a respectful and engaging tone. Keep it concise. If anything interesting or unusual is observed, highlight it with a sense of wonder or intrigue.
                Also do not exceed 300 characters.
                take a deep breath and do this step by step.
                """,
            },
        ]
        + script
        + generate_new_line(base64_image),
        max_tokens=500,
    )
        response_text = response.choices[0].message.content
        return response_text
    except Exception as e:
        if "APIConnectionError" in str(type(e)):
            print(f"OpenAI API Connection Error: {e}")
            return "Error: Could not connect to OpenAI API."
        elif "RateLimitError" in str(type(e)):
            print(f"OpenAI API Rate Limit Error: {e}")
            return "Error: OpenAI API rate limit exceeded."
        elif "AuthenticationError" in str(type(e)):
            print(f"OpenAI API Authentication Error: {e}")
            return "Error: Invalid OpenAI API key. Please check your .env file."
        elif "APIStatusError" in str(type(e)):
            print(f"OpenAI API Status Error: {e}")
            return f"Error: OpenAI API returned an error status."
        else:
            print(f"An unexpected error occurred during OpenAI API call: {e}")
            return "Error: An unexpected error occurred during image analysis."


def main():
    script = []

    while True:
        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        if base64_image:
            # analyze posture
            print("👀 David is watching...")
            analysis = analyze_image(base64_image, script=script)

            if analysis and not analysis.startswith("Error:") : # Check if analysis produced valid output
                print("🎙️ David says:")
                print(analysis)
                play_audio(analysis)
                script = script + [{"role": "assistant", "content": analysis}]
            else:
                print(analysis) # Print error message from analyze_image or if it's None
        else:
            print("Skipping analysis due to image encoding failure.")

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    main()
