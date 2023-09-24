#!/bin/zsh

# Create a virtual environment
python -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required packages from req.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
