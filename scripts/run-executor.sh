#!/bin/bash
# Executor cron entry. Sonnet 4.6, ≤25 turns, 10-min timeout
# (allowing for 90s post-deploy cooldown wait + tx times).
set -e

KZ="/home/anatolyzaytsev/kami-zero"
LOG="/home/anatolyzaytsev/kami-zero-executor.log"
LOCK="/tmp/kami-zero-executor.lock"

exec 200>"$LOCK"
if ! flock -n 200; then exit 0; fi

cd "$KZ"
{
    echo "=== executor tick: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    timeout 10m claude \
        -p "$(cat executor-prompt.md)" \
        --max-turns 25 \
        --model claude-sonnet-4-6 \
        --dangerously-skip-permissions \
        2>&1
    echo
} >> "$LOG"
