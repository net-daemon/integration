#!/bin/bash

# This is for local development using Python v13 or higher for Home Assistant.

set -e


# Check if we are in a virtual environment for v 1.13 or higher
if [ -z "$VIRTUAL_ENV" ]; then
    # Check if we can source an existing virtual environment or create a new one if not exists
    if [ -d ".python312env" ]; then
        echo "Virtual environment exists, activating it by running: source .python312env/bin/activate and run the script again!" 
    else
        echo "Creating a new virtual environment for python 3.13"
        python3.12 -m venv .python312env
        echo "Activate by using the following command: source .python312env/bin/activate"
        echo "Then run this command again to start Home Assistant"
    fi
    exit 1
else
    # Check if homeassistant is installed
    if ! python3 -m homeassistant --version; then
        echo "Home Assistant is not installed, installing requirements now"
        pip3 install -r requirements.txt
    fi
    # Run the development server script
    echo "Starting Home Assistant server"
    ./scripts/develop
fi
