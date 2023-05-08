#!/bin/zsh

# Get the directory path of the script
SCRIPT_DIR="$(dirname "$0")"

# Change to the directory where the script is located
cd "$SCRIPT_DIR"

# Run the Python script
python interface.py