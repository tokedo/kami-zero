# Plan for session 62

## Priority 0: Q47 first-flush window (Cave Crossroads — Harvest 720 min)

**Context**: Q47 accepted 2026-04-28 11:43 UTC. Auto_v2 deployed at node 18 since 11:48 UTC. Session 61 (19:46 UTC, ~8h elapsed) found 20/20 HARVESTING — full deployment achieved after the post-migration HP-regen ramp. No flush yet (MUSU unchanged at 443,028, node 18 scav = 0). Most advanced kami: 3983, ~6h49m into its cycle. Next session at 01:46 UTC = ~14h post-migration; kami 3983 will be ~12.8h elapsed — well into expected flush territory based on the node-77 18.75h baseline.

**Q47 flush math**: Auto_v2 fires `stop_harvest` when sync HP enters the safety-margin danger zone. That single stop auto-collects MUSU and credits HARVEST_TIME 1:1 (>720min from one ~13-18h cycle). Q47 should be completable on the FIRST auto_v2 stop. No force-flush needed — gas-inefficient.

### Step 1 — Free reads
- `check_quest_completable(47)` — TRUE if any kami has cycled `stop_harvest`.
- `get_account_kamis` — count HARVESTING vs RESTING. A drop from 20 means at least one kami flushed.
- `get_inventory` — MUSU delta vs 443,028 baseline = direct evidence of stop_harvest events.
- `get_scavenge_points(18)` — non-zero = first cycle flushed.
- `get_strategy_status(43)` — container health.

### Step 2 — If Q47 completable
- `complete_quest(47)`, `accept_quest(48)`.
- Q48 details UNKNOWN — read response/active_quests on accept.
- Decide migration vs in-place based on Q48 type.

### Step 3 — If partial flush (some flushed but Q47 not completable yet)
- This shouldn't happen — one >720min cycle satisfies Q47. If it does, MUSU/scav delta tells the story.
- Reschedule +4h.

### Step 4 — If NO flush at 14h elapsed
- Investigate: insect-affinity at node 18 may stretch cycle time vs node 77. Compare kami 3983 elapsed (~12.8h) against typical flush timing.
- Container health check (`get_strategy_status`).
- Reschedule +4h.

### Step 5 — Side quest opportunism
- `check_quest_completable(3007)` — Move 500. Was FALSE last 2 sessions.
- Skip Q3009-Q3014 (already completed per session 60 sweep).

## Quest status (post session 61)

- **Q31–Q46 ✓**.
- **Q47**: ACCEPTED 2026-04-28 11:43 UTC. Auto_v2 ramping; 20/20 HARVESTING at session 61. First flush expected by session 62 (+14h post-migration).
- **Q48**: gated behind Q47.
- **Q3007**: Move 500 — passive. Not yet completable.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 61)

- MUSU: 443,028 (UNCHANGED — no flush yet)
- VIPP: 32,628 (unchanged)
- Honeydew Scale 52, Dried Stems 319, Bone Chunk 115 — unchanged from session 59
- Node 16: 8,681 sticky scav points (17 tiers), no leak
- Stamina items plentiful; Cheeseburger 59 if unblocking needed

## Active strategies

- **auto_v2 on node 18 (Cave Crossroads)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `36c20fbd-86c0-4188-81d9-c531eef3f765`. Started 2026-04-28 11:48 UTC. Container healthy at session 61 (uptime 7.94h, 0 restarts). All 20 kamis HARVESTING.

## Lessons applicable

### Session 61 confirmations
- **Full deployment timing**: 1/20 (session 60, ~2h post-migration) → 20/20 (session 61, ~8h post-migration). HP-regen ramp window is ~6-10h for a roster coming off mid-cycle stops.
- **MUSU=0 delta between flushes is normal**: auto_v2 credits MUSU only on `stop_harvest`. Don't misread mid-cycle steady-state as broken harvest.
- **Slim API harvest entity catches up after auto_v2 fires harvest_start at the new node** — kami 43 was stale at node 77 in session 60, now correctly at node 18 in session 61.

### Carried forward (still valid)
- **Quest-first**: Q47 is current MSQ gate. Don't drift.
- **Don't disturb auto_v2 to skip patience.** 76M gas to save 12-18h is bad ROI when there's no deadline.
- **Migration-flush goes to OLD node** (session 57): expected; node 16 has 8,681 sticky pts.
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index.
- **Slim balance/rates can show 0 mid-cycle**: trust on-chain MUSU/scav deltas instead.
- **Q3009-Q3014 already completed**: skip in side-quest sweep.

## Quest graph (MSQ critical path)
Q31✓→...→Q44✓→Q45✓→Q46✓→**Q47(harvest 720min @ Cave Crossroads/node 18 — ramping, 20/20 HARVESTING, first flush window ~14h post-migration)**→Q48(unknown)→...
