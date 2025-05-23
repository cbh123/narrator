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

Next, make accounts with [OpenAI](https://beta.openai.com/) and [ElevenLabs](https://elevenlabs.io/) and set your API key environment variables. The Python libraries used in this project will automatically detect and use these environment variables for authentication.

```bash
export OPENAI_API_KEY=<your-openai-api-key>
export ELEVENLABS_API_KEY=<your-elevenlabs-api-key>
export ELEVEN_VOICE_ID=<your-elevenlabs-voice-id> # Optional, see note below
```

**Note on API Keys and Voice ID:**
*   `OPENAI_API_KEY`: Your API key from OpenAI, used for the vision and language model.
*   `ELEVENLABS_API_KEY`: Your API key from ElevenLabs, used for text-to-speech.
*   `ELEVEN_VOICE_ID`: This environment variable allows you to specify a custom voice from your ElevenLabs account. If this variable is not set, the application will default to using the voice ID "21m00Tcm4TlvDq8ikWAM". You can find your available voice IDs using the ElevenLabs [voices API](https://elevenlabs.io/docs/api-reference/voices) or by checking your account on their website. To use a custom voice, make a new voice in your ElevenLabs account and get its voice ID.

## Run it!

```bash
python capture.py
```
In one terminal. In the other, run the narrator:

```bash
python narrator.py
```

