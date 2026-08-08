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

### Using a Local Model (LM Studio)

To run with a local LM Studio model (e.g., Qwen3-VL), set these environment variables:

```bash
# Point to your LM Studio local server (default port is 1234)
export OPENAI_BASE_URL=http://localhost:1234/v1

# Set your local model name (use the exact name from LM Studio)
export LOCAL_MODEL_NAME=qwen3-vl-8b-instruct

# API key can be any string for local servers
export OPENAI_API_KEY=local-model
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

## Run it!

In one terminal, run the webcam capture:
```bash
python capture.py
```
In another terminal, run the narrator:

```bash
python narrator.py
```
