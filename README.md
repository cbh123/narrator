# David Attenborough narrates your life

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

Make a [Replicate](https://replicate.com), [OpenAI](https://beta.openai.com/), and [ElevenLabs](https://elevenlabs.io) account and set your tokens:

```bash
export OPENAI_API_KEY=<token>
export ELEVENLABS_API_KEY=<eleven-token>
```

Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API, or by clicking the flask icon next to the voice in the VoiceLab tab.

```bash
export ELEVENLABS_VOICE_ID=<voice-id>
```

## Run it!

In on terminal, run the webcam capture:

```bash
python capture.py
```

In another terminal, run the narrator:

```bash
python narrator.py
```

## Options

### Setup

#### Script

Alternative to running the [Setup](#setup) commands above individually, one can use the `setup.sh` script to facilitate getting the two required shell envs ready to rock.

_Note: may have to manually run `source source venv/bin/activate` afterwards depending on shell env._

#### Dotenv

One can set the environment variables via the `.env` file, which is read every time the process starts. It is recommended to copy the `.env.example` file and rename to `.env`.

### Streaming

If you would like the speech to start quicker via a streaming manner set the environment variable to enable. The concession is that the audio and corresponding image is not saved in the `/narration` directory.

```bash
export ELEVENLABS_STREAMING=true
```

### PhotoBooth

The default behavior of this app will continually analyze images. If you would like to use in a mode more similar to a photo booth, set the environment variable. In this mode, the image will only be analyzed when the spacebar key is pressed.

```bash
export PHOTOBOOTH_MODE=true
```
