# Harness improvements

Append-only. Each entry documents a change you made to the harness so future sessions can use it without rediscovering.

Format:

```
## YYYY-MM-DD — Short title
- **What**: one-line description of the change
- **Why**: the problem it solves
- **Files**: paths changed
- **How to use**: signature or example
- **Commit**: git sha
```

---

## 2026-04-09 — Executor: better error details + optional kami_id/node_id
- **What**: `_api_post` now surfaces API error body instead of swallowing it. `start_strategy` makes `kami_id` and `node_id` optional (default 0) for multi-kami strategies.
- **Why**: 500 errors from Kamibots were opaque ("Server error '500'"). Now the agent sees the actual error message. kami_id/node_id are not needed by callers for auto_v2/rest_v3.
- **Files**: `executor/server.py`
- **How to use**: `start_strategy(strategy_type="auto_v2", config={...}, kami_id=1064, node_id=86)` — kami_id/node_id still required by API even for multi-kami strategies.
- **Commit**: 3b3fbab

## 2026-04-09 — Harvest start/stop/collect + scavenge + droptable tools
- **What**: Added 6 new on-chain tools: `harvest_start`, `harvest_stop`, `harvest_collect`, `scavenge_claim`, `droptable_reveal`, `get_scavenge_points`. Also added `_harvest_entity_id()`, `_scavenge_registry_id()`, `_scavenge_instance_id()` helpers and `_send_batch_tx()` for batch patterns.
- **Why**: No harvest or scavenge tools existed. Couldn't collect MUSU, couldn't scavenge items, couldn't progress quests. These are fundamental game actions.
- **Files**: `executor/server.py`
- **How to use**:
  - `harvest_start([43, 1064], node_index=47)` — batch start
  - `harvest_stop([43, 1064])` — batch stop with auto-collect
  - `harvest_collect([43, 1064])` — collect without stopping
  - `scavenge_claim(47)` — claim scavenge rewards (uses registry entity ID)
  - `droptable_reveal([commit_id])` — reveal droptable commits
  - `get_scavenge_points(47)` — read accumulated points (NOTE: currently returns 0, may have component ID issue)
- **Commit**: a1d46e9
