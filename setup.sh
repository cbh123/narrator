#!/bin/bash

# create a virtual environment
python3 -m pip install virtualenv
python3 -m virtualenv venv

# source the virtual environment to install dependencies
source venv/bin/activate

# install the dependencies
pip install -r requirements.txt

echo -e "\n\n\nSetup complete. Run $(source venv/bin/activate) to activate the virtual environment.\n\nAlso, please ensure your environment variables are set correctly in the .env file."
