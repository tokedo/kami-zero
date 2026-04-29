# Plan for session 63

## Priority 0: Q47 flush (Cave Crossroads — Harvest 720 min)

**Context**: Q47 accepted 2026-04-28 11:43 UTC. Auto_v2 on node 18 since 11:48 UTC. Session 62 (02:00 UTC, ~14h elapsed) caught **first partial flush**: kami 3983 cycled HARVESTING→RESTING, +1,133 scav pts at node 18 (5 tiers). MUSU UNCHANGED (anomaly — track but don't act). check_quest_completable(47) still FALSE despite kami 3983's ~13h cycle (which alone should be ~780 kami-min).

**Hypothesis**: Either HARVEST_TIME counts only the kami's active (non-resting) fraction of elapsed time, OR the counter requires harvest_collect to credit (not just stop). Either way, more cycles = more credit. 19 still HARVESTING with cycles aging 7-12h → expect 3-6 more stops in next 4h.

### Step 1 — Free reads
- `check_quest_completable(47)` — TRUE if cumulative ≥720.
- `get_account_kamis` — count HARVESTING vs RESTING. Drop from 19→<10 = multiple flushes occurred.
- `get_inventory` — MUSU delta vs 443,028 baseline. Big jump = real flushes (resolves session 62 anomaly).
- `get_scavenge_points(18)` — node 18 delta. Compare to MUSU delta for 1:1 invariant test.
- `get_strategy_status(43)` — container health.

### Step 2 — If Q47 TRUE
- `complete_quest(47)`, then grep `integration/game-data.md` for Q48 objective BEFORE accepting.
- `accept_quest(48)`.
- If Q48 is at a new node: stop_strategy + stop_harvest_batch (use silent-skip detection) + travel + start_strategy. **Time the migration within 1-2h of an observable flush** (max RESTING fraction = cheap teardown — session 59 lesson).
- If Q48 is location-agnostic (craft, give, burn): execute in place.

### Step 3 — If Q47 FALSE at ~18h elapsed
- **Investigate the HARVEST_TIME crediting mechanic.** Possible probes:
  - Try `harvest_collect([kami_id])` on a high-elapsed kami (cheap, <2M gas). If `check_quest_completable(47)` flips TRUE post-collect, mechanic is collect-driven. If still FALSE, the problem is cumulative threshold not yet met.
  - Cross-reference node 18 scav delta vs MUSU delta — if they're equal magnitude (even if MUSU lags), the auto_v2 cycles ARE crediting; just need more.
- Reschedule +4h.

### Step 4 — If Q47 FALSE at 22h+ elapsed
- Strong signal that something in the model is off. Read game-data.md / quests.md for the exact HARVEST_TIME accounting rule.
- Consider gas-budget force-flush only if quest stuck and no other Q48 path exists (NOT yet — Q47 has no deadline).

### Step 5 — Side quest opportunism
- `check_quest_completable(3007)` — Move 500. Was FALSE last 3 sessions.
- Skip Q3009-Q3014 (all completed per session 60).

## Quest status (post session 62)

- **Q31–Q46 ✓**.
- **Q47**: ACCEPTED 2026-04-28 11:43 UTC. Auto_v2 ramping; 19 HARVESTING + 1 RESTING at session 62 (~14h elapsed). First partial flush observed (kami 3983 cycled). Counter still FALSE — needs more cycles.
- **Q48**: gated behind Q47.
- **Q3007**: Move 500 — passive. Not yet completable.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 62)

- MUSU: 443,028 (UNCHANGED — anomaly under investigation)
- VIPP: 33,761
- Honeydew Scale 52, Dried Stems 319, Bone Chunk 115 — unchanged from session 59
- Node 16: 8,681 sticky scav points (17 tiers), no leak across 5 sessions ✓
- Node 18: 1,133 scav pts (5 tiers) — first partial flush
- Stamina items plentiful; Cheeseburger 59 if unblocking needed

## Active strategies

- **auto_v2 on node 18 (Cave Crossroads)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `36c20fbd-86c0-4188-81d9-c531eef3f765`. Started 2026-04-28 11:48 UTC. Healthy at session 62 (uptime 14.2h, 0 restarts). 19 HARVESTING + 1 RESTING (kami 3983, just cycled).

## Lessons applicable

### Session 62 confirmations
- **First-flush at ~13-14h post-migration**: kami 3983's cycle confirmed expected timing window. Insect-affinity node doesn't dramatically extend cycle time.
- **MUSU/scav 1:1 invariant may not be exact for small flushes**: observed +1,133 scav with +0 MUSU. Possible API caching or partial-cycle accounting. Track across sessions.
- **HARVEST_TIME counter mechanic uncertain**: kami 3983's 13h elapsed cycle did NOT alone clear Q47's 720-min threshold (counter still FALSE). Suggests counter measures something other than wall-clock elapsed (e.g., active-time fraction, or cumulative across multiple stops only).

### Carried forward (still valid)
- **Quest-first**: Q47 is current MSQ gate. Don't drift.
- **Don't disturb auto_v2 to skip patience.** 70M gas to save 4-8h is bad ROI when there's no deadline.
- **Migration-flush goes to OLD node** (session 57): expected; node 16 has 8,681 sticky pts.
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index.
- **Slim balance/rates can show 0 mid-cycle**: trust on-chain MUSU/scav deltas instead.
- **Q3009-Q3014 already completed**: skip in side-quest sweep.
- **Node 18 droptable** (200/tier cost): unknown items — read via `get_scavenge_droptable(18)` next session if claiming becomes relevant.

## Quest graph (MSQ critical path)
Q31✓→...→Q44✓→Q45✓→Q46✓→**Q47(harvest 720min @ Cave Crossroads/node 18 — first partial flush at 14h, more cycles needed)**→Q48(unknown)→...
