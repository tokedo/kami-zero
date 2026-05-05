#!/bin/bash
# Optimizer cron entry. Opus 4.7, ≤30 turns, 15-min timeout, every 6h.
set -e

KZ="/home/anatolyzaytsev/kami-zero"
LOG="/home/anatolyzaytsev/kami-zero-optimizer.log"
LOCK="/tmp/kami-zero-optimizer.lock"

exec 200>"$LOCK"
if ! flock -n 200; then exit 0; fi

cd "$KZ"
{
    echo "=========================================="
    echo "=== optimizer session: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "=========================================="
    timeout 15m claude \
        -p "$(cat optimizer-prompt.md)" \
        --max-turns 30 \
        --model claude-opus-4-7 \
        --dangerously-skip-permissions \
        2>&1
    echo "=== optimizer ended: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo
} >> "$LOG"
