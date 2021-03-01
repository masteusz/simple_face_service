#!/bin/bash
PORT="${PORT:-8000}"
LOG_LEVEL="${LOG_LEVEL:-INFO}"
NUM_WORKERS=${NUM_WORKERS:-1}
NUM_THREADS=${NUM_THREADS:-1}
GUNICORN_CMD_ARGS="${GUNICORN_CMD_ARGS:-"--bind=0.0.0.0:$PORT --workers=$NUM_WORKERS --threads=$NUM_THREADS --log-level=$LOG_LEVEL --graceful-timeout=2 --timeout=5 --keep-alive=5"}"
GUNICORN_CMD_ARGS="$GUNICORN_CMD_ARGS" LOG_LEVEL="$LOG_LEVEL" exec gunicorn main:app --worker-class sync