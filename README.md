# sarcastic narrator
Sarcastic David Attenborough narrates what you are doing based on your screen


Forked from this project:
https://github.com/cbh123/narrator
David Attenborough narrates your life.
https://twitter.com/charliebholtz/status/1724815159590293764

## Setup

Clone this repo, and setup and activate a virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Then, install the dependencies:
`pip install -r requirements.txt`

Make an OpenAI and ElevenLabs (https://elevenlabs.io) account and set your tokens:

```
export OPENAI_API_KEY=<token>
export ELEVENLABS_API_KEY=<eleven-token>
```

Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API.

## Run it!

```bash
python capture.py
```
In one terminal. In the other, run the narrator:

```bash
python narrator.py
```

