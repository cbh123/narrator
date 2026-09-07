# David Attenborough narrates your life. 

https://twitter.com/charliebholtz/status/1724815159590293764

## Want to make your own AI app?
Check out [Replicate](https://replicate.com). We make it easy to run machine learning models with an API.

## Setup

Clone this repo, and setup and activate a virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Then, install the dependencies:
`pip install -r requirements.txt`

### Using LM Studio with Piper TTS (Local)

This project is set up to run locally with LM Studio for vision/language and Piper TTS for speech.

#### 1. Set up Piper TTS

Run piper1-gpl (https://github.com/OHF-voice/piper1-gpl) and download an appropriate model:

```bash
mkdir local-piper
uv venv --python 3.12
source .venv/bin/activate
uv pip install piper-tts
uv pip install piper-http
uv python -m piper.download_voices en_GB
uv run python -m piper.http_server -m en_GB-alan-medium --port 5001
```

Leave this running in a terminal. The server will serve Piper TTS at http://127.0.0.1:5001 by default. You can set `TTS_URL` and `TTS_VOICE` if needed:
```bash
export TTS_URL=http://127.0.0.1:5001
export TTS_VOICE=en_GB-alan-medium
```

#### 2. LM Studio setup

Start LM Studio and load a vision-capable model (e.g., qwen3.6-35b-a3b-nvfp4 for capture, meta/muse-glimmer for narrator).

Set environment variables for local inference:

```bash
export OPENAI_BASE_URL=http://localhost:1234/v1
export OPENAI_API_KEY=lmstudio
```

## Run it!

In one terminal, run the webcam capture with LM Studio:
```bash
OPENAI_BASE_URL=http://localhost:1234/v1 LOCAL_MODEL_NAME=qwen3.6-35b-a3b-nvfp4 OPENAI_API_KEY=lmstudio python capture.py
```

In another terminal, run the narrator with LM Studio:
```bash
OPENAI_BASE_URL=http://localhost:1234/v1 LOCAL_MODEL_NAME=meta/muse-glimmer OPENAI_API_KEY=lmstudio python narrator.py
```

### Using the Cloud API (Replicate / OpenAI)

Make a [Replicate](https://replicate.com), [OpenAI](https://beta.openai.com/), and [ElevenLabs](https://elevenlabs.io) account and set your tokens:

```
export OPENAI_API_KEY=<token>
export ELEVENLABS_API_KEY=<eleven-token>
```

Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API, or by clicking the flask icon next to the voice in the VoiceLab tab.

```
export ELEVENLABS_VOICE_ID=<voice-id>
```
