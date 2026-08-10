import os
from openai import OpenAI
import base64

import time
import errno
import requests

# Local LM Studio server (default: http://localhost:1234/v1)
# Set OPENAI_BASE_URL env var to override, or edit this line directly.
# For MLX LM server: http://localhost:8080/v1
client = OpenAI(
    base_url=os.environ.get("OPENAI_BASE_URL", "http://localhost:1234/v1"),
    api_key=os.environ.get("OPENAI_API_KEY", "local-model"),  # Any string works for local servers
)

# Local Piper TTS server (default: http://127.0.0.1:5001)
TTS_URL = os.environ.get("TTS_URL", "http://127.0.0.1:5001")

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
    if not text.strip():
        print("⚠️ Empty text passed to play_audio, skipping")
        return

    voice = os.environ.get("TTS_VOICE", "en_GB-alan-medium")

    # Get available voices from the Piper server (returns a dict, not a list)
    target_voice = None
    try:
        voices_resp = requests.get(f"{TTS_URL}/voices")
        voices_resp.raise_for_status()
        all_voices = voices_resp.json()

        # Piper returns a dict like {"en_GB-alan-medium": {...}, ...}
        if voice in all_voices:
            target_voice = voice
        elif all_voices:
            first_voice = list(all_voices.keys())[0]
            print(f"⚠️ Voice '{voice}' not found, using first available voice: {first_voice}")
            target_voice = first_voice

        if not all_voices:
            print("⚠️ No voices returned from Piper server, proceeding without voice selection")

    except Exception as e:
        print(f"⚠️ Could not fetch voices from Piper server: {e}")

    # Piper's /synthesize endpoint returns raw WAV bytes directly (not a URL)
    payload = {"text": text}
    if target_voice:
        payload["voice"] = target_voice

    print(f"🔊 Calling Piper TTS: {TTS_URL}/synthesize (voice={target_voice or 'default'})")
    response = requests.post(f"{TTS_URL}/synthesize", json=payload)
    print(f"🔊 Piper TTS status: {response.status_code}")
    response.raise_for_status()

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(response.content)

    # Play the audio file using afplay (macOS)
    import subprocess

    subprocess.run(["afplay", file_path], check=True)


def generate_new_line(base64_image):
    return [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this image"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        },
    ]


def analyze_image(base64_image, script):
    response = client.chat.completions.create(
        # Use the exact model name from LM Studio (e.g., "qwen3-vl-8b-instruct")
        model=os.environ.get("LOCAL_MODEL_NAME", "qwen3-vl-8b-instruct"),
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

    while True:
        # path to your image
        image_path = os.path.join(os.getcwd(), "./frames/frame.jpg")

        # getting the base64 encoding
        base64_image = encode_image(image_path)

        # analyze posture
        print("👀 David is watching...")
        analysis = analyze_image(base64_image, script=script)

        print("🎙️ David says:")
        print(analysis)

        if not analysis.strip():
            print("⚠️ LLM returned empty text, skipping TTS")
        else:
            play_audio(analysis)

        # Save both the user message and assistant response to build full conversation history
        script = script + [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            },
            {"role": "assistant", "content": analysis},
        ]

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    main()
