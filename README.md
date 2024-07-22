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

Make a [Replicate](https://replicate.com), [OpenAI](https://beta.openai.com/), and [ElevenLabs](https://elevenlabs.io) account and set your tokens:

### Setting Up Environment Variables

Instead of setting your tokens directly in the terminal, we'll use a `.env` file to manage them securely. Follow these steps:

1. Create a file named `.env` in the root directory of your project.
2. Add your API keys and voice ID to the `.env` file in the following format:

   ```
   OPENAI_API_KEY=your_openai_api_key
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=your_elevenlabs_voice_id
   ```

   Replace `your_openai_api_key`, `your_elevenlabs_api_key`, and `your_elevenlabs_voice_id` with your actual keys and ID.

3. The python-dotenv package (already included in `requirements.txt`) will load these variables automatically.

**Note:** Ensure that `.env` is listed in your `.gitignore` file to keep your API keys secure.
Make a new voice in Eleven and get the voice id of that voice using their [get voices](https://elevenlabs.io/docs/api-reference/voices) API, or by clicking the flask icon next to the voice in the VoiceLab tab.

```
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

