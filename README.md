# kami-zero v2

Two-LLM architecture: Sonnet 4.6 executor (every 5 min) follows
`executor-prompt.md`. Opus 4.7 optimizer (every 6 h) reads tick
history and edits the playbook.

The artifact that compounds is `executor-prompt.md` + `rules/*.md`.
The founder reviews the rules — they ARE the spec.

## Why v2 (vs v1)

v1 made the executor pure Python. The intuition was right
(separation of execution from optimization), but the surface area
of the game has too many edge cases for code-as-spec to capture
cleanly. Each missed edge case (consolidation, cooldowns,
multi-candidate iteration) was a new Python module, a new bug
surface, and a new deploy.

v2 keeps the role separation but makes both roles LLM-driven, with
prose rules as the artifact. Edge cases get expressed as plain
English in the playbook, not as branches in code.

## Why this won't dead-loop like v0 did

v0 (pre-rewrite) was a single LLM session per tick that wrote
freeform decisions, plans, and doctrine. It dead-looped because
LLM was unbounded.

v2 prevents that structurally:

| Mechanism | Effect |
|---|---|
| Forbidden-by-name files (`decisions.md` etc.) | No prose journals |
| JSONL-only outputs | No paragraphs |
| ≤1 rule edit per optimizer session | No doctrine sprawl |
| 200-line cap on `executor-prompt.md` | No accreted bloat |
| ≤15 turn cap on executor | No mid-tick rabbit-holes |
| ≤30 turn cap on optimizer | No mid-session essays |
| Cron circuit breaker (planned) | Slow cadence on prolonged defer |

## Layout

```
~/kami-zero/
  CLAUDE.md                 # shared orientation (anti-patterns)
  executor-prompt.md        # ← THE PLAYBOOK (you review this)
  optimizer-prompt.md       # how the optimizer reviews
  
  rules/
    rejects.md              # archetype reject list
    safety.md               # hard limits
    notes.md                # optimizer change log (≤30 lines)
  
  history/
    runs.jsonl              # one line per executor tick
    anomalies.jsonl         # executor's "I don't know" queue
    rule_changes.jsonl      # optimizer's structured edit log
  
  scripts/
    run-executor.sh         # Sonnet, every 5 min
    run-optimizer.sh        # Opus, every 6 h
    fetch-discord-liquidations.py  # unchanged watcher
  
  executor/                 # MCP tool source (unchanged)
  predator/                 # watcher state + crons (unchanged)
  archive/                  # frozen prior versions
```

## Cost (rough)

- Executor: ~$0.02/tick × 12/h × 24h ≈ **$6/day**
- Optimizer: ~$0.30/session × 4/day ≈ **$1.20/day**
- Total: **~$7-8/day** for autonomous predator ops.

## Deployment

1. Pause executor cron (already paused from prior architecture).
2. Archive `core/` (v1 Python attempt) to `archive/2026-05-pre-v2/`.
3. Copy this tree's contents to `~/kami-zero/`.
4. Manual test: invoke executor once, verify it produces a
   `runs.jsonl` line and no scatter.
5. Resume executor cron (every 5 min).
6. After ~6 h of executor data, enable optimizer cron (every 6 h).
