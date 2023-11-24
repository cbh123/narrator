#!/bin/bash

# create a virtual environment
python3 -m pip install virtualenv
python3 -m virtualenv venv

# source the virtual environment
source venv/bin/activate

# install the dependencies
pip install -r requirements.txt

# set the environment variables
export ELEVENLABS_VOICE_ID=
export OPENAI_API_KEY=
export ELEVENLABS_API_KEY=

export ELEVENLABS_STREAMING=false
