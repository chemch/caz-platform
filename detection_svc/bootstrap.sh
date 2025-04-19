#!/bin/sh
set -e  # Exit on error

# Move to the directory of the script
cd "$(dirname "$0")"

# Environment variables
export FLASK_APP=${FLASK_APP:-main}
export FLASK_ENV=${FLASK_ENV:-development}
export PYTHONPATH=$(pwd)

# Allow port override via env or positional arg
PORT=${1:-${PORT:-5004}}
DEBUG="${2:-${DEBUG:-false}}"

# Enable debug flag conditionally
if [ "$DEBUG" = "true" ]; then
  DEBUG_FLAG="--debug"
else
  DEBUG_FLAG=""
fi

echo "[INFO] Starting Flask app: $FLASK_APP on port $PORT (env: $FLASK_ENV, debug: $DEBUG)"
exec python3 -m flask run --host=0.0.0.0 --port="$PORT" $DEBUG_FLAG