#!/bin/bash
# kami-zero session runner — triggered by cron every 15 minutes.
# Runs a Claude Code session if memory/next-run-at indicates it's time.
# The agent writes next-run-at at the end of each session.

set -e

KAMI_ZERO="/home/anatolyzaytsev/kami-zero"
NEXT_RUN_FILE="$KAMI_ZERO/memory/next-run-at"
LOG_FILE="/home/anatolyzaytsev/kami-zero-session.log"
LOCK_FILE="/tmp/kami-zero.lock"

# Prevent overlapping sessions (e.g., if a session takes >15min and cron re-fires)
exec 200>"$LOCK_FILE"
if ! flock -n 200; then
    exit 0
fi

# Check schedule — skip if not yet time
if [ -f "$NEXT_RUN_FILE" ]; then
    scheduled=$(cat "$NEXT_RUN_FILE" | tr -d '[:space:]')
    now=$(date +%s)
    if [ -n "$scheduled" ] && [ "$now" -lt "$scheduled" ]; then
        exit 0
    fi
fi

# Run session
cd "$KAMI_ZERO"
{
    echo ""
    echo "=========================================="
    echo "=== Session started: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo "=========================================="

    # 30 minute hard timeout as a safety net against runaway sessions
    timeout 30m claude \
        -p "$(cat session-prompt.md)" \
        --max-turns 200 \
        --model claude-opus-4-7 \
        --effort xhigh \
        --dangerously-skip-permissions \
        2>&1

    echo ""
    echo "=== Session ended: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
    echo ""
} >> "$LOG_FILE"

# Fallback: if agent didn't set next-run-at, default to 6 hours from now
need_default=0
if [ ! -f "$NEXT_RUN_FILE" ]; then
    need_default=1
else
    scheduled=$(cat "$NEXT_RUN_FILE" | tr -d '[:space:]')
    if [ -z "$scheduled" ] || [ "$(date +%s)" -ge "$scheduled" ]; then
        need_default=1
    fi
fi
if [ "$need_default" -eq 1 ]; then
    echo $(($(date +%s) + 21600)) > "$NEXT_RUN_FILE"
fi
