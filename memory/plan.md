# Plan for session 1 (initial seed)

> *This is the initial plan written by the human operator. After this session, you will overwrite it with your own plan for the next session.*

## This is your first session

Before you do anything game-related:

1. **Read `CLAUDE.md` fully.** Understand the session protocol, gas rules, quest focus, and improvement mandate.
2. **Read `session-prompt.md`** so you understand what cron will send you each time.
3. **Skim these systems docs** for context:
   - `systems/quests.md` — your primary objective is quest completion
   - `systems/harvesting.md` — Auto_v2 will use nodes; understand node selection
   - `systems/gas-efficiency.md` — if this doesn't exist, that's a harness improvement opportunity (don't create it during this session though, focus on game progress)
   - `integration/kamibots/README.md` — auto_v2 strategy config schema

## Priority 1: Clean up stale state

During the setup session, we noticed 1 strategy slot was reported "in use" but all harvests were INACTIVE. Call `get_all_strategies(account="bpeon")` and investigate. Clean up any zombie strategy records.

## Priority 2: Quest assessment

This is your primary objective going forward.

- Use whatever MCP tools exist to enumerate accepted/available quests for bpeon
- Focus on: **main quest line** and **Mina's quest line**
- For each quest, read its requirements and current progress
- Pick the most feasible quest to work on first

If there is no tool to list quests, this is a high-value harness improvement — read `systems/quests.md` and `integration/api/quests.md`, then add a `get_account_quests(account)` tool to `executor/server.py`. Document it in `memory/improvements.md`.

## Priority 3: Start Auto_v2 harvests (aimed at quest)

Once you know which quest you're working toward:

- Select nodes appropriate for kami affinities AND that advance the chosen quest
- Start `auto_v2` strategies with 5% safety margins
- Batch the kamis you deploy to minimize gas

## Priority 4: Initial state snapshot

Kamis currently on bpeon (as of 2026-04-08):
- 43, 1064, 2553, 6096, 7803, 8745, 10011, 12459, 13235, 13390, 13702, 13857
- All were RESTING with cooldowns expired
- Balances: 108,958 Musu, 365,000 Sanguineous Powder, 100 Red Ribbon Gummies (revives), etc.

Verify this is still accurate at the start of your session.

## At end of session

- Append entry to `memory/decisions.md`
- Overwrite this file (`memory/plan.md`) with the plan for session 2
- Write unix timestamp to `memory/next-run-at` (default: 6h = current + 21600)
- Commit and push
