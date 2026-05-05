#!/bin/bash
# Executor cron entry. Sonnet 4.6, ≤15 turns, 5-min timeout.
set -e

KZ="/home/anatolyzaytsev/kami-zero"
LOG="/home/anatolyzaytsev/kami-zero-executor.log"
LOCK="/tmp/kami-zero-executor.lock"

exec 200>"$LOCK"
if ! flock -n 200; then exit 0; fi

cd "$KZ"
{
    echo "=== executor tick: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    timeout 5m claude \
        -p "$(cat executor-prompt.md)" \
        --max-turns 15 \
        --model claude-sonnet-4-6 \
        --dangerously-skip-permissions \
        2>&1
    echo
} >> "$LOG"
