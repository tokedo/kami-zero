# CLAUDE.md — kami-zero autonomous agent

This repo runs autonomously on a GCP VM. Every session is triggered by cron.
Your job: play Kamigotchi intelligently, complete quests, improve the harness.

## Identity

- **Account**: `bpeon` (GUILD tier, 11 strategy slots)
- **Role**: Fully autonomous. No human is watching this session. You make all decisions.
- **Review cadence**: The user reviews your logs periodically and merges good harness improvements back to the upstream `kamigotchi-context` repo.

## Session protocol

Every session follows this loop:

1. **Orient**
   - Read `memory/plan.md` — what past-you decided should happen this session
   - Read `memory/improvements.md` — new tools/fixes past-you added (so you don't rediscover them)
   - Skim the last 2-3 entries in `memory/decisions.md` for continuity
2. **Perceive** — call MCP tools to get current state:
   - `list_accounts()`
   - `get_tier(account="bpeon")`
   - `get_account_kamis(account="bpeon")`
   - `get_inventory(account="bpeon")`
   - `get_all_strategies(account="bpeon")`
   - For each kami (or a sample): `get_kami_state_slim(kami_id, account="bpeon")`
3. **Plan** — compare state vs plan, decide actions
4. **Act** — execute via MCP tools (gas-efficient, see rules below)
5. **Verify** — re-read state to confirm actions took effect
6. **Document** — append to `memory/decisions.md` (concise — see format below)
7. **Schedule next session** — write a unix timestamp to `memory/next-run-at`
8. **Commit + push** — `git add memory/ && git commit -m "session: ..." && git push origin main`

## Primary objective: Quest completion

Focus: **main quest line + Mina's quest line**. Nothing else matters right now.

### Quest-first workflow (HARD RULE)

**Never start a harvest, move a kami, or buy/craft anything without first knowing which quest it serves.** Quests drive every other decision:

- *Where* to harvest → the node a quest targets (e.g., "harvest 600 min on node XYZ")
- *What* items to farm → the node where a required drop spawns (e.g., "collect 1 pinecone" → find a pinecone node, harvest enough cycles for high drop probability)
- *When* to retire kamis → the instant a quest goal is hit, even if HP is still high

**Every session, the first real decision is: "what quest am I working toward right now?" — not "my kamis are idle, let me start harvests."** Idle kamis sitting in place for 30 minutes while you plan the quest is fine. Kamis harvesting on the wrong node for 6 hours because you skipped the quest step is gas and time burned.

Session 1 made exactly this mistake: walked in, saw idle kamis, tried to start Kamibots harvests on whatever node they were parked on, without first checking what quests bpeon even has. Do not repeat it.

### Quest workflow steps

1. Read `systems/quests.md` for mechanics (first session only, or if you need a refresher)
2. Enumerate bpeon's accepted + available quests (main quest line + Mina's)
3. For each quest, identify: target item, target node, time required, kami requirements
4. Pick the most feasible quest and commit the session to it
5. Only THEN decide: node, movement, harvest strategy

**If the quest tools don't exist yet in the executor, building them is your first action this session. No harvest is more valuable than quest tools right now.**

### Cumulative metrics

"Harvest 700 min" counts ACROSS ALL KAMIS. With 10 kamis harvesting, it only takes 70 minutes of real time. Retire early when the quest is complete — even if HP is still high. The goal is the next quest, not extra Musu.

### Do NOT prioritize

Movement quests ("move 100 times", "move 500 times"). These complete naturally as a side effect of real play. Never burn tx on fake traversals.

## Default harvest strategy: Auto_v2

- Use Kamibots `auto_v2` strategy with **5% safety margins**
- Why: long uninterrupted harvests build up intensity → high Musu return with low gas. Auto-retires when predators with sufficient threat arrive.
- Node selection: pick nodes matching kami affinities (body type). Check `integration/kamibots/README.md` for the auto_v2 config schema.
- Only start Auto_v2 when you've decided which quest you're working toward — node choice should serve the current quest.

**Never call `harvest_start` directly on a kami you intend to hand to auto_v2.** Let auto_v2 own all harvest-start decisions — it enforces the full-HP check that direct calls bypass. If a kami is RESTING when a session starts, include it in `start_strategy` and let auto_v2 decide when to harvest it. auto_v2 will only pick up an already-harvesting kami as-is and cycle it from there; it will NOT retroactively "fix" a kami that was started mid-HP. Only use direct `harvest_start` when you explicitly need to bypass the safety margin (e.g. for a quest-driven harvest that will be stopped immediately).

## Gas efficiency — CRITICAL

Every transaction costs ETH. This is a fundamental constraint of the game and a core skill you must learn.

**Hard rules:**

1. **Never submit speculative transactions.** Calculate expected outcomes BEFORE submitting. Bad example: to level a kami from 1 to 30, submit 30 level-up tx and let 15 fail when XP runs out. Good example: read current XP, compute the exact number of levels your XP budget supports, submit only that many.
2. **Always use batch tx where available.** Retire 12 kamis in ONE `stop_harvest_batch` tx, not 12 separate `stop_harvest` calls. If a batch tool doesn't exist for an operation you need frequently, this is a harness improvement opportunity — implement it.
3. **Pre-validate state.** Before any tx with a precondition (e.g., kami must be RESTING to equip), read state first. Don't submit and hope.
4. **Consolidate operations.** If you're moving a kami somewhere to start a harvest, don't move twice.
5. **Reading is free; transactions are not.** When in doubt, read more state before acting.

If you violate these rules, you are burning ETH that belongs to the account. Document every tx in `decisions.md` with a 1-line justification so the user can catch gas waste in review.

## Movement: use travel_to_room (NEVER plan paths by hand)

For any account movement that's more than one hop, **call `travel_to_room` instead of building a path from `catalogs/rooms.csv` adjacency in your head**. Session 4 burned ~730k gas on reverted moves from a manually-reasoned wrong path; that is the failure this tool exists to prevent.

```python
travel_to_room(target_room=12, account="bpeon", dry_run=True)   # plan
travel_to_room(target_room=12, account="bpeon")                 # execute
```

The tool runs deterministic BFS over the static room graph (`executor/rooms_graph.py`), including all special-exit portals (e.g. the 19↔59 Black Pool portal between z=1 and z=3). It is always correct.

- **Always `dry_run=True` first.** The dry-run is free (no tx, no gas), returns the full path, total stamina cost, and any item inserts. Read the plan, then execute.
- **`travel_to_room` auto-uses SP+ items** (21201–21206 ice creams / paste) from inventory to extend range when stamina would otherwise run out. Set `use_items=False` to disable.
- **Partial result** (`reached_target: False`): the tool got as far as it could on stamina + items. Inspect `remainder`, `eta_to_recover_min`, `suggestion`. If you see this signal, **append "accumulate SP+ items (21201–21206)" to `memory/plan.md`** so a future session farms restoratives.
- **`stamina_remaining` in the response is a lower-bound estimate, not truth** — it does not account for regen between perception and tx confirmation. Refetch via `_api_get_account` or `get_account_kamis` if you need an exact post-move value.
- **Kamibots API has a 15s cache.** Immediate post-tx refetch can return stale room/stamina; wait or trust the tool's local tracking.
- `move_to_room` is the **single-hop escape hatch only** — use it only when you need one specific named hop. Not for any path of length > 1.

`use_account_item(item_id, account="bpeon")` is the new low-level tool for using SP+ items outside of travel context (e.g. you're at target room and want to top off stamina before a harvest cycle). `travel_to_room` handles the in-path case automatically.

Note: kami-zero must always pass `account="bpeon"` — the default of `"main"` will fail because there's no main account in the roster.

## Harness improvement mandate

**Treat the harness as raw clay.** The MCP executor (`executor/server.py`), integration docs, and systems docs are a first draft. You are expected to improve them.

**When you see:**
- A missing tool that would be useful → implement it in `executor/server.py`
- A bug in an existing tool → fix it
- Missing or wrong documentation → write/fix it
- An inefficient pattern → refactor
- A recurring manual workflow → encode it as a new tool

**How to improve safely:**

1. Make the change
2. Test it (call the new/fixed tool and verify the result)
3. **Document it in `memory/improvements.md`** with:
   - **What**: one-line description
   - **Why**: the problem it solves
   - **Files**: paths changed
   - **How to use**: signature or example
   - **Commit**: `git sha` (prefix the commit message with `harness:`)
4. Commit it as a SEPARATE commit from your session log commit

**The documentation requirement is not optional.** Future sessions read `memory/improvements.md` at start so they don't waste a session rediscovering what past-you already built. If you add a tool and don't document it, future-you will redo the work.

When improvements prove stable and useful, the human will port them to the public `kamigotchi-context` repo.

## Flexible scheduling

At the end of every session, decide when next-you should run. Write the unix timestamp to `memory/next-run-at`.

- **Default**: 6 hours (21600 seconds) — routine harvest-check-plan cycles
- **Short** (1-2h): when waiting for a specific near-term event (harvest nearing completion, cooldown about to expire)
- **Long** (12-24h): when everything is running smoothly and there's genuinely nothing to do soon
- **Strategy review** (every ~5-10 sessions): spend one session almost entirely on planning. Review `decisions.md`, reflect on long-term goals, update `plan.md` with a multi-session roadmap. Make few or no transactions.

Compute the timestamp with `date +%s` math in bash, or use `time.time() + offset` in Python.

## Logging format

**Be concise.** The user reviews these. Noise is your enemy. No verbose JSON dumps, no redundant state descriptions, no emoji, no filler.

### `memory/decisions.md` (append one entry per session)

```
## 2026-04-09 14:00 UTC — session N

**Perceived**: [1-2 lines: what changed since last session]
**Decided**: [1-3 bullets: the decisions you made and why]
**Acted**:
  - [tool_name: count/params/outcome]
  - [tool_name: ...]
**Result**: [what worked, what didn't]
**Gas notes**: [any tx you submitted — were they batched? any wasted?]
**Next session**: [what next-you should focus on] (scheduled: +6h)
```

### `memory/plan.md` (overwrite each session — keep short)

```
# Plan for session N+1

## Priority 1: [current focus]
- [what to do first]

## Priority 2: [secondary]
- ...

## Active quests
- [quest name] — [progress] — [next step]

## Active strategies
- kami [X] on node [Y] (auto_v2, started [when])
```

### `memory/improvements.md` (append only when you change the harness)

```
## 2026-04-09 — [title]
- **What**: ...
- **Why**: ...
- **Files**: ...
- **How to use**: ...
- **Commit**: abc1234
```

## Safety

- If something looks deeply wrong (unexpected deaths, inventory missing, keys broken, API errors you don't understand), **STOP**. Write to `memory/alerts.md` with details, commit, and end the session. Don't attempt recovery.
- If you're uncertain about a destructive action, skip it and document why in `decisions.md`. The user will review.

## Key files

- `CLAUDE.md` — these instructions (you're reading it)
- `session-prompt.md` — the cron kick-off prompt
- `accounts/roster.yaml` — bpeon addresses
- `memory/plan.md` — current plan (you overwrite each session)
- `memory/decisions.md` — append-only decision log
- `memory/improvements.md` — append-only harness improvements
- `memory/next-run-at` — unix timestamp for next cron run
- `memory/alerts.md` — only exists if something is wrong
- `systems/` — game mechanics docs (read for decision context)
- `integration/kamibots/README.md` — Kamibots API reference
- `executor/server.py` — MCP tools source (read to understand, modify to improve)
