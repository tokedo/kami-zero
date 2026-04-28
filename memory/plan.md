# Plan for session 61

## Priority 0: Q47 flush at node 18 (Cave Crossroads — Harvest 720 min)

**Context**: Q47 accepted 11:43 UTC. Auto_v2 deployed at node 18 at 11:48 UTC. Session 60 (13:30 UTC, ~1h42m elapsed) found auto_v2 running healthy but only 1/20 kamis HARVESTING. Reason: post-migration HP regen is slow — most kamis came off node 77 at sub-95% HP and need to top up before auto_v2's 5% safety margin lets them start. Sample: kami 43 sync HP 43/230 (~19%); kami 1064 also low. MUSU +4,247 since session 59 = ~2,500 MUSU/h, well below the ~7-10k MUSU/h that 20 active kamis would yield. The 18.75h fresh-migration first-cycle baseline from node 77 likely applies again here; budgeting accordingly.

**Q47 flush math**: Auto_v2 will eventually start each kami once HP hits 95%. First cycle at fresh intensity = ~12-18h to bountyCollectThreshold or HP-safety stop. The first kami to stop credits its full cycle's HARVEST_TIME (typically >720min for an 18h cycle). So Q47 should be completable on FIRST observable auto_v2 stop — no force-flush needed. Save the 76M gas a manual start+stop wave would burn.

**Why no force-flush this session**: A manual harvest_start wave on 20 kamis (≥95% HP not enforced by direct harvest_start, but bypasses auto_v2's intensity-aware scheduling) costs ~60M gas to start + ~16M to stop = 76M gas. Saves ~12-18h vs patient wait. Q47 has no time pressure — burning 76M gas to skip half a day is wasteful.

### Step 1 — Free reads
- `get_account_kamis` — count HARVESTING vs RESTING. If ≥10 HARVESTING, auto_v2 has ramped up.
- `check_quest_completable(47)` — passive flush check; TRUE if any kami has cycled.
- `get_inventory` — track MUSU + Stems/Bones/Honeydew accumulation at node 18.
- `get_strategy_status(43)` — confirm container still healthy.

### Step 2 — If Q47 completable
- `complete_quest(47)`.
- `accept_quest(48)` — Q48 details UNKNOWN. Read response/active_quests to learn objective.
- Decide migration vs in-place based on Q48 type (move/burn/buy/scavenge/harvest).

### Step 3 — If Q47 NOT completable but >5 HARVESTING
- Auto_v2 is ramping. Don't disturb. Reschedule +4h.

### Step 4 — If Q47 NOT completable and ≤2 HARVESTING after 7.5h
- Auto_v2 is stuck. Investigate: maybe specific kamis have death-RESTING (low sync HP or strain) that auto_v2 won't recover from. May need targeted feeding (Cheeseburger from inventory, 59 available) to top HP and unblock auto_v2.

### Step 5 — Side quest opportunism
- `check_quest_completable(3007)` — Move 500. Was FALSE this session. Check again in case quest tools refresh.
- Most 3xxx quests already completed (3009/3010/3011/3012/3013/3014 all show "quest alr completed").

## Quest status (post session 60)

- **Q31–Q46 ✓**.
- **Q47**: ACCEPTED 2026-04-28 11:43 UTC. HARVEST_TIME 720min at Cave Crossroads. Auto_v2 deployed at node 18; ramping slowly due to post-migration HP regen.
- **Q48**: gated behind Q47.
- **Q3007**: Move 500 — passive. Not yet completable.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 60)

- MUSU: 443,028 (+4,247 since session 59)
- VIPP: 32,628 (unchanged — node 18 hasn't yielded VIPP yet despite drop list)
- Honeydew Scale 52, Dried Stems 319, Bone Chunk 115 — unchanged from session 59
- Stamina items (ice cream / candyfloss) plentiful for travel

## Active strategies

- **auto_v2 on node 18 (Cave Crossroads)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `36c20fbd-86c0-4188-81d9-c531eef3f765`. Started 2026-04-28 11:48 UTC. Container healthy (uptime 103min, 0 restarts at session 60 read).

## Lessons applicable

### Session 60 confirmations
- **Post-migration HP regen is the rate-limiter, not intensity ramp.** Session 58/59 attributed first-cycle delay to bountyCollectThreshold + intensity ramp. Session 60 reveals that some kamis arrive at the new node with low sync HP (kami 43 at 19%, kami 1064 at low%) from late-cycle stops at the prior node. Auto_v2's 5% safety margin enforces near-full HP before harvest_start, so REST regen must complete first. This adds hours upstream of the first cycle.
- **Slim API harvest entity is stale per-kami until next on-chain action.** kami 43 / 1064 / 12459 / 14306 all show harvest entity pointing to node 77 (last node) with INACTIVE state — DESPITE being at room 18 since the migration. The entity will only update when auto_v2 actually fires harvest_start at node 18. Don't read "harvest entity at old node" as a leak signal — confirm by counting HARVESTING kamis from get_account_kamis (chain-authoritative).
- **Side-quest sweep**: Q3009/3010/3011/3012/3013/3014 all return "quest alr completed" — past sessions completed them. Don't re-check these.

### Carried forward (still valid)
- **Quest-first**: Q47 is current MSQ gate. Don't drift.
- **Don't disturb auto_v2 to skip patience.** 76M gas to save 12-18h is bad ROI when there's no deadline.
- **Migration-flush goes to OLD node** (session 57): expected; node 16 has 8,681 sticky pts.
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index.
- **Slim balance/rates can show 0 mid-cycle**: trust on-chain MUSU/scav deltas instead.

## Quest graph (MSQ critical path)
Q31✓→...→Q44✓→Q45✓→Q46✓→**Q47(harvest 720min @ Cave Crossroads/node 18 — ramping)**→Q48(unknown)→...
