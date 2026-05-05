#!/bin/bash
# Optimizer cron entry. LLM session, ≤30 turns. Reads history/, edits core/.
set -e

KAMI_ZERO="/home/anatolyzaytsev/kami-zero"
LOG_FILE="/home/anatolyzaytsev/kami-zero-optimizer.log"
LOCK_FILE="/tmp/kami-zero-optimizer.lock"

exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    exit 0
fi

cd "$KAMI_ZERO"
{
    echo "=========================================="
    echo "=== optimizer session: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "=========================================="
    timeout 15m claude \
        -p "$(cat session-prompt.md)" \
        --max-turns 30 \
        --model claude-opus-4-7 \
        --effort high \
        --dangerously-skip-permissions \
        2>&1
    echo ""
    echo "=== ended: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
} >> "$LOG_FILE"
