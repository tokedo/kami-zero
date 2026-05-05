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

### Parked-rates refresher (session 157, 2026-05-04)
```
*/5 * * * * /usr/bin/python3 /home/anatolyzaytsev/kami-zero/predator/scripts/refresh_parked_rates.py >/tmp/parked_rates_cron.log 2>&1
```
- **What**: Reads top-100 from latest `world_targets.json` `killable_v3 ∪ killable_v2` (deduped, v3 first to prioritize fresh non-parked entries — see s160 coverage-gap fix below), calls Kamibots playwright `/api/playwright/kami/{idx}/slim` for each, extracts `harvest.rates.intensity.average` + `harvest.rates.fertility` + `harvest.balance` + `stats.health.{sync,total}` + `harvest.state`, derives `parked_bool`, and atomic-writes `predator/parked_rates_state.json`.
- **Why**: Sessions s152–s156 hit a 5-session 0-kill streak driven by a universal "parked-rates" defensive equilibrium (13/13 across 9 owners / 7 nodes). The watcher's elapsed-based proj_hp is invalid when on-chain `harvest.rates.*` are zero; killable_v2 surfaces phantom margins. The scanner caches the canonical strike-go signal so the watcher can pre-filter (killable_v3) without an LLM-in-the-loop slim probe at session start.
- **Output**: `predator/parked_rates_state.json` keyed by `v_idx` → `{rates_intensity_avg, rates_fertility, balance, sync, total, harvest_state, kami_state, parked_bool, last_checked_ts, v_acct, node_id}`. Schema_version: 1.
- **Runtime**: ~12s for 50 candidates at 50ms politeness pause + 15s timeout. Hard ceiling 240s so the scan never overlaps the next 5-min cron tick.
- **parked_bool** = `rates.intensity.average == 0 AND rates.fertility == 0 AND balance == 0 AND harvest.state == "ACTIVE" AND sync > 0`. (Sync==total dropped from s152's original signal — observed sync<total parked rows on 4444… in s157 dry-run.)
- **Failure mode**: 404 / 429 / network → row skipped, scan continues. Empty `world_targets.json` → empty snapshot written (still atomic). Kamibots API key missing → script aborts before write; previous snapshot stays intact.
- **Hard-rule note**: Kamibots state reads in this scanner are the **sanctioned workaround** per `ideas_to_founder.md § 6.3` until oracle exposes `harvest.rates.*`. Migrate to oracle the moment the field lands. CLAUDE.md hard rule #8 forbids Kamibots reads in predator-decision paths *in-session*; this cron isolates the violation to a single observable surface (`parked_rates_state.json`) so sessions never need to call slim themselves.
- **Coverage-gap fix (session 160, 2026-05-05)**: scanner originally read `world_targets["killable_v2"][:50]`. When all top-50 v2 rows were parked-flagged, v3 published rows beyond rank-50 of internal v2 were rates-unknown (`parked_rates: None`). Filter was partially blind. Fix: scanner now reads `killable_v3 ∪ killable_v2` deduped (v3 first), TOP_N bumped 50 → 100. Validated s160: scanner went 50 → 72 candidates per cycle (within 16-17s, well under the 240s ceiling).

### Watcher integration (session 157)
- `refresh_world_targets.py` reads `parked_rates_state.json` (≤600s old) after computing `killable_v2`. Per-row `parked_rates` field attached, plus two new top-level arrays:
  - `killable_v3` — `killable_v2` minus `parked_bool == True` rows. **The new primary read for clean-strike planning.** Empty when the scanner says everyone is parked.
  - `parked_v2` — only the parked rows. Visibility / heat-window monitoring (a parked row flipping to non-parked is the strike opening).
- Stale or missing `parked_rates_state.json`: watcher emits `parked_rates.applied=false`; `killable_v3` defaults to `killable_v2` (no filter applied, fall back to slim-verify in session).
- Snapshot also exposes `schema_version=2` so consumer code can version-gate the new fields.

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
