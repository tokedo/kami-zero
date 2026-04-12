# Setting Up kami-zero

kami-zero is a fully autonomous Kamigotchi agent. It wakes up on a schedule,
reads its own plan, perceives the game state, acts, documents what it did,
and schedules its next session — no human in the loop.

## Prerequisites

- **Claude Code CLI** (`claude`) — [install guide](https://docs.anthropic.com/en/docs/claude-code)
- **Claude API access** — Max subscription or API key with Opus 4.6
- **Python 3.11+** with pip
- **A VM or always-on machine** (e.g., GCP e2-small, ~$7/mo) — needs to stay on for cron
- **A Kamigotchi account** with kamis, some ETH for gas, and a registered Kamibots account

## Quick setup

```bash
# 1. Clone
git clone https://github.com/tokedo/kami-zero.git
cd kami-zero

# 2. Install executor dependencies
cd executor && pip install -r requirements.txt && cd ..

# 3. Set up keys (OUTSIDE the repo — Claude Code indexes the working directory)
mkdir -p ~/.blocklife-keys
cp env.template ~/.blocklife-keys/.env
# Edit ~/.blocklife-keys/.env: fill in your OPERATOR_KEY and OWNER_KEY

# 4. Configure your account in accounts/roster.yaml
# Set your owner_address and operator_address

# 5. Configure Claude Code MCP
cat > .mcp.json << 'EOF'
{
  "mcpServers": {
    "kamigotchi": {
      "command": "python3",
      "args": ["executor/server.py"],
      "cwd": "/path/to/kami-zero"
    }
  }
}
EOF

# 6. Test manually first
claude -p "$(cat session-prompt.md)" --model claude-opus-4-6

# 7. Set up cron (once you trust it)
crontab -e
# Add: */15 * * * * /path/to/kami-zero/scripts/run-session.sh
```

## How scheduling works

The cron job fires every 15 minutes, but the agent doesn't run every time.
Here's the flow:

```
cron (every 15min)
  → run-session.sh
    → checks flock (prevents overlapping sessions)
    → reads memory/next-run-at (unix timestamp)
    → if now < scheduled: exit (not time yet)
    → if now >= scheduled: run claude session
      → agent plays, documents, commits
      → agent writes new timestamp to memory/next-run-at
      → next cron tick checks again
```

The agent decides its own schedule at the end of each session:
- **10 min** — quick actions still remaining, come back soon
- **1-2 hours** — waiting for a harvest or cooldown
- **6 hours** — routine cycle, nothing urgent
- **12-24 hours** — everything running smoothly

This means the agent is self-scheduling — it adapts its frequency to
what's happening in the game.

## How memory works

The `memory/` directory is the agent's persistent brain between sessions:

| File | Purpose |
|---|---|
| `plan.md` | What to do next session (overwritten each session) |
| `decisions.md` | Append-only log of what happened each session |
| `improvements.md` | Harness changes the agent made (new tools, fixes) |
| `next-run-at` | Unix timestamp for the next session |
| `alerts.md` | Only exists if something went wrong — agent stops and waits |

The agent commits and pushes `memory/` at the end of each session, so you
can review what it did from anywhere via `git log`.

## Customizing

- **CLAUDE.md** — the agent's operating instructions. Edit this to change
  strategy, priorities, or behavior. Keep directives general and
  principle-based — the agent develops its own judgment over time.
- **session-prompt.md** — the prompt that kicks off each session.
- **accounts/roster.yaml** — add more accounts for multi-account play.
- **executor/server.py** — the agent can (and does) modify this itself
  to add new tools. Your improvements and the agent's will coexist.

## Safety

- Keys are stored outside the repo at `~/.blocklife-keys/.env`
- Claude Code deny rules block reading `.env`, `.key`, `.pem` files
- A pre-tool-use hook blocks any tool call referencing secret paths
- `run-session.sh` has a 30-minute hard timeout
- The flock mechanism prevents overlapping sessions
- If the agent detects something wrong, it writes to `alerts.md` and stops

## Reviewing sessions

```bash
# See what the agent did
git log --oneline memory/

# Read the latest session
tail -50 memory/decisions.md

# Watch a live session
tail -f ~/kami-zero-session.log

# Check next scheduled run
cat memory/next-run-at | xargs -I{} date -d @{}
```
