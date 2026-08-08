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

# Local TTS server (default: http://127.0.0.1:7860)
TTS_URL = os.environ.get("TTS_URL", "http://127.0.0.1:7860")

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
    voice = os.environ.get("TTS_VOICE", "David2")

    # Get available voices from the TTS server
    try:
        voices_resp = requests.get(f"{TTS_URL}/api/voices")
        voices_resp.raise_for_status()
        all_voices = voices_resp.json()

        # Find the voice name matching our desired voice
        target_voice = None
        for v in all_voices:
            if v.get("name") == voice:
                target_voice = v["name"]
                break

        # If we didn't find an exact match, try the first voice as fallback
        if target_voice is None and all_voices:
            print(f"⚠️ Voice '{voice}' not found, using first available voice: {all_voices[0].get('name', 'unknown')}")
            target_voice = all_voices[0]["name"]

        if not all_voices:
            print("⚠️ No voices returned from TTS server, proceeding without voice selection")

    except Exception as e:
        print(f"⚠️ Could not fetch voices from TTS server: {e}")
        target_voice = None

    # Generate audio via the /api/generate endpoint (POST with JSON body)
    payload = {"text": text}
    if target_voice:
        payload["voice"] = target_voice

    print(f"🔊 Calling TTS: {TTS_URL}/api/generate (voice={target_voice or 'default'})")
    response = requests.post(f"{TTS_URL}/api/generate", json=payload)
    print(f"🔊 TTS status: {response.status_code}")

    # The /api/generate endpoint returns JSON with a 'url' field pointing to the audio file
    if response.headers.get("content-type", "").startswith("application/json"):
        result = response.json()
        audio_url = result.get("url")
        # The URL may be relative (e.g., "/clips/..."), prepend the TTS base URL
        if audio_url and not audio_url.startswith("http"):
            audio_url = f"{TTS_URL}{audio_url}"
        if not audio_url:
            raise RuntimeError(f"TTS generation failed: {result.get('error', 'unknown error')}")
        print(f"🔊 Downloading audio from: {audio_url}")
        response = requests.get(audio_url)
        response.raise_for_status()

    print(f"🔊 TTS status: {response.status_code}")
    response.raise_for_status()

    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(response.content)

    # Play the audio file using afplay (macOS) or a fallback
    import subprocess

    # Save the audio to disk first, then play it with afplay
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

        play_audio(analysis)

        script = script + [{"role": "assistant", "content": analysis}]

        # wait for 5 seconds
        time.sleep(5)


if __name__ == "__main__":
    main()
