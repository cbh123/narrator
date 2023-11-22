# Piero Angela racconta la tua vita.

Questo è un fork del repo https://github.com/cbh123/narrator pubblicato per la prima volta da Charlie Bholtz su X (Twitter) con questo [post](https://twitter.com/charliebholtz/status/1724815159590293764)
Thank you Charlie for this simple but very fun iteration using OpenAi and Elevelabs APIs

Essendo un repository indirizzato esclusivamente all'utenza italiana ho deciso di tradurre le istruzioni.

>[!NOTE]
>Per poter usare questo repository dovrai creare una nuova voce narrante su Elevenlabs utilizzando un campione della voce di Piero Angela o del narratore che preferisci. Per comodità ho aggiunto un sample da usare per fare il training nella cartella `assets`

>[!NOTE]
>Non possiedo i diritti di utilizzo della voce di Piero, l'utilizzo di questo repository deve essere inteso esclusivamente per scopi divulgativi. Per me è stato un modo per far rivivere la voce amica che accompagnava i weekend della mia infanzia con SuperQuark. A Piero Angela devo in parte la passione per le scienze e per la cultura. 

## Setup

Clona questo repository, avvia il setup and attiva virtualenv:

```bash
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

Installa le dipendenze:
`pip install -r requirements.txt`

Se non ce li hai crea un account [OpenAI](https://beta.openai.com/) e [ElevenLabs](https://elevenlabs.io), poi recupera i tuoi auth token. Setta poi le variabili del tuo ambiente locale digitando

```
export OPENAI_API_KEY=<token>
export ELEVENLABS_API_KEY=<eleven-token>
```

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

