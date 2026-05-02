# predator/ infrastructure

Cron jobs and background processes the agent owns. Document every entry here so future-you and the founder can see what runs autonomously.

## Cron entries

### Session runner (managed by founder)
```
*/5 * * * * /home/anatolyzaytsev/kami-zero/scripts/run-session.sh >/dev/null 2>&1
```
Triggers an LLM session every 5 minutes. Honors `memory/next-run-at` to gate actual execution.

### World-targets refresher (session 90, 2026-05-02)
```
*/5 * * * * /usr/bin/python3 /home/anatolyzaytsev/kami-zero/predator/scripts/refresh_world_targets.py >/tmp/world_targets_cron.log 2>&1
```
- **What**: Scans HARVESTING victims across hot-list nodes (currently 86, 60, 73, 25, 62, 9, 30, 82). Applies guild + heal-event filters, projects HP via canonical formulas, computes margin against each of bpeon's 6 strikers. Atomic write to `predator/world_targets.json`.
- **Why**: Sessions were re-deriving the same world view at session start (~30-60s of repeated oracle scans). Now sessions read the cached snapshot first; oracle scan is only triggered if the cache is stale (>10 min old).
- **Output**: `predator/world_targets.json` (top 50 clean killable across all hot nodes, plus per-node top 10 with diagnostic flags).
- **Runtime**: ~2-3s per scan. Oracle handles 8 SQL queries cheaply.
- **Failure mode**: oracle 5xx → script raises, atomic write never happens, prior `world_targets.json` stays intact. Sessions detect staleness via `generated_at` timestamp.
- **Hot list update**: edit `HOT_NODES` in `predator/scripts/refresh_world_targets.py`. Recompose when discovering new clusters or operator moves.
- **Striker roster update**: edit `STRIKERS` constant in same file. **Refresh on respec or roster change** — kept inline for tactical-decision speed (avoids an extra oracle round-trip per scan).

## How sessions consume

```python
import json
with open("predator/world_targets.json") as f:
    snapshot = json.load(f)

# Stale check (older than 10 min → re-scan via /tmp/scan89.py or recon90.py).
from datetime import datetime, timezone
gen = datetime.fromisoformat(snapshot["generated_at"].replace("Z", "+00:00"))
age_sec = (datetime.now(timezone.utc) - gen).total_seconds()
if age_sec > 600:
    # snapshot is stale; refresh inline
    ...

killable = snapshot["killable_clean"]  # top 50, sorted by margin desc
```

## Reading the snapshot

- `killable_clean`: top 50 candidates with margin ≥ +5 HP, no guild block, no soft-no-touch (rtvvvvv), no heal event since `harvest_start`. Sorted by margin desc.
- `by_node[<node_id>].top10`: top 10 per node (includes guild-blocked / soft-no-touch / fed for visibility).
- `by_node[<node_id>].killable_count`: count of clean killable on that node — useful for cluster-economic decisions ("is this worth migrating to?").

## Caveats

- The snapshot's `proj_hp` is the canonical formula's projection. It can be wrong by 5-10 HP on edge cases (REVIVE-mid-cycle short-elapsed, dual-affinity slot ambiguity). Use the +5 HP margin gate as the safety buffer.
- A `proj_hp` of 0 with elapsed_h > 10 and no recent action is a structural-surprise signal — either oracle staleness or a defense mechanism we don't model. Spot-check via direct oracle query before striking.
- Snapshot says nothing about counter-predators on the destination node. Run a separate counter-predator scan before deploying.
