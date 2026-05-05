# kami-zero-rewrite

Executor / optimizer architecture for kami-zero. Replaces the
LLM-drives-every-tick model that ended in the s163–s184 dead-loop.

## The two roles

**Executor** — deterministic Python. Runs every 5 min via cron. No LLM.
Reads `world_targets.json` (already produced by existing watcher cron),
applies filter from `config.yaml`, picks a candidate, calls
`executor.liquidate()` if anything qualifies, logs structured outcome to
`history/runs.jsonl`. Emits `history/anomalies.jsonl` events when it sees
something it can't handle.

**Optimizer** — LLM session. Runs every 6h (or on-demand when the
anomaly queue exceeds a threshold). Reads `history/runs.jsonl` and
`history/anomalies.jsonl`. Proposes ≤1 change to `core/` (config,
rules, or code). Commits or exits with no change. ≤30 turns.

The artifact that compounds is `core/`. Prose does not.

## Directory layout

```
core/
  loop.py              # tick orchestrator
  config.yaml          # gates, floors, thresholds — every tunable param
  rules.py             # archetype rejects, hard limits, guild gate adapter
  anomaly.py           # structured event emitter
  
  perception/
    world.py           # parses world_targets.json
    self_state.py      # reads account state via existing executor
  
  predator/
    filter.py          # the gate stack (config-driven)
    targeting.py       # candidate ranking
    strike.py          # wraps executor.liquidate()

history/               # append-only, machine-readable, optimizer reads
  runs.jsonl
  anomalies.jsonl
  core_changes.jsonl

scripts/
  run-executor.sh      # cron entry: `python -m core.loop`
  run-optimizer.sh     # cron entry: claude -p session-prompt.md

CLAUDE.md              # ~100 lines — editor agent role + invariants
session-prompt.md      # ~30 lines — optimizer prompt
```

## Run flow (executor tick)

```
1. perception.world.load()       → killable_v3 candidates + metadata
2. perception.self_state.read()  → operator node, striker positions, gas budget
3. predator.filter.apply(...)    → drop candidates failing any gate
4. predator.targeting.pick(...)  → top survivor (or None)
5. if pick:
     predator.strike.fire(...)   → await liquidate(...)
     log to runs.jsonl with structured outcome
   else:
     log to runs.jsonl with reason=defer + filter rejection counts
6. anomaly.emit(...) if any data-quality issues this tick
```

## Run flow (optimizer session)

```
1. read history/runs.jsonl (last 24h)
2. read history/anomalies.jsonl (unresolved)
3. read core/ source
4. propose ≤1 change:
     - tweak config.yaml param
     - add/remove a rule in rules.py
     - fix a bug in any module
     - mark an anomaly resolved
5. commit (or exit with no change)
```

That's it. No plan.md, no decisions.md, no strategic-experiments.md.
The diff log of `core/` IS the decision history. Inspect with `git log core/`.

## Hard invariants (executor refuses to run if violated)

1. Guild gate freshness — predator/guild-no-touch.csv must exist and have
   `Updated:` line ≤7 days old (enforced inside `executor.liquidate()`).
2. Single concurrent tick (flock).
3. Per-tick gas budget cap (config.yaml).

## What this does NOT do (out of scope for v0)

- Crafting (paused, defer to v1)
- Counter-predator (defer)
- Quests, harvesting, leveling (paused for predator mode)
- Operator/striker movement (v0 only fires when already co-located;
  emits anomaly if a high-margin candidate would require migration)

## Migration from old kami-zero

When this is approved and deployed:
1. Old prose archived to `archive/2026-05-pre-rewrite/` on the VM
2. Old `~/kami-zero/` becomes `~/kami-zero-old/` (kept for reference)
3. New tree (this directory) becomes `~/kami-zero/`
4. Watcher crons (refresh_world_targets, refresh_parked_rates,
   fetch-discord-liquidations) keep running unchanged
5. New crons:
   - `*/5 * * * *  scripts/run-executor.sh`   # Python, no LLM
   - `0 */6 * * *  scripts/run-optimizer.sh`  # LLM, ≤30 turns
