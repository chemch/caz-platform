#!/bin/sh

cd "$(dirname "$0")"
export FLASK_APP=cashman.index
export FLASK_ENV=development
export PYTHONPATH=$(pwd)
python3 -m flask run --host=0.0.0.0 --port=5000

