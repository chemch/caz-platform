#!/bin/bash

# Navigate to the correct directory

# shellcheck disable=SC2164
cd "$(dirname "$0")"  # This ensures the script always runs from the directory it's located in

# Set environment variables
export FLASK_APP=cashman.index
export FLASK_ENV=development

# shellcheck disable=SC2155
export PYTHONPATH=$(pwd)

# Optional: use a custom port if 5000 is busy
PORT=${1:-5001}

# Start Flask server
flask run --debug --port="$PORT"
