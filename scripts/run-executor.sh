#!/bin/bash
# Executor cron entry. Runs the deterministic predator tick.
# No LLM. Logs to /home/anatolyzaytsev/kami-zero-executor.log.
set -e

KAMI_ZERO="/home/anatolyzaytsev/kami-zero"
LOG_FILE="/home/anatolyzaytsev/kami-zero-executor.log"
LOCK_FILE="/tmp/kami-zero-executor.lock"

exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    exit 0
fi

cd "$KAMI_ZERO"
{
    echo "=== executor tick: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    "$KAMI_ZERO/executor/.venv/bin/python3" -m core.loop 2>&1
    echo ""
} >> "$LOG_FILE"
