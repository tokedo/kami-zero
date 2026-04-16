# Plan for session 36

## Priority 1: Complete Q22 — 3 Scav rolls at Centipedes (node 62)

- 20 kamis under auto_v2 on node 62 since 2026-04-16 02:18 UTC.
- Scav cost: 300/roll at node 62. Need 900 total points for 3 rolls.
- By next session start (~12:30 UTC) that's ~10h accumulated — should safely cover 3 rolls.
- **Steps**: stop_strategy(kami 43) → stop_harvest_batch (2x10) → scavenge_claim_and_reveal(62) x3 → check_quest_completable(22) → complete_quest(22) → accept_quest(23).
- If 3rd scav reverts → complete Q22 anyway if `check_quest_completable(22)` returns TRUE (2 rolls may be enough if prior session's 1 roll counted).
- If <2 rolls succeed → restart auto_v2 on node 62, schedule +3h, try again.

## Priority 2: Accept Q23 + begin work

- Q23: "Squaring the Circle III" — 3 Scav rolls at Blooming Tree (node 53, zone 2).
- Travel from room 62 to room 53 via travel_to_room(53, dry_run=True) first.
- Manually start harvests on new node 53 (auto_v2 can't start cross-node). Then start auto_v2.

## Priority 3: Look ahead

- Check Q24 prereqs after accepting Q23.
- Continue MSQ critical path toward Q30 (unlocks Mina Q2014).

## Active strategies
- auto_v2 on node 62, 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q22** (MSQ): 3 Scav at Centipedes node 62 — IN PROGRESS
- **Q23** (MSQ, next): 3 Scav at Blooming Tree node 53
- **Q6**: Liquidate kami — deferred (don't want to kill a harvester)
- **Q3007** (side): Move 500 — ~134/500, accumulates naturally
- **Q2001-2013** (Mina): all show "alr completed" — completed but still in active list (harmless)
- **Mina Q2014** unlocks at MSQ 30

## Quest graph (critical path)
MSQ: Q21(done)→Q22(IN PROGRESS)→Q23→…→Q30 (unlocks Mina Q2014)→…→Q108

## Inventory notes
- MUSU: 187,536
- VIPP: 5,282
- Ice Cream: 80, Better Ice Cream: 10, Rock Candyfloss: 66 (SP+ stock is healthy)
- Booster Pack: 1 (still unopened — consider opening when session is slow)
- Pine Pollen: 500, Essence of Daffodil: 300 (crafting reserves from prior Mina chain)

## Lessons to remember
- Don't stop harvests to check scav points — trust the time accumulated (~80-100 pts/hr @ 20 kamis).
- Node 60 scav = 500/roll; node 62 scav = 300/roll (cheaper).
- get_scavenge_points is broken — harness improvement opportunity when time allows.
- Session 35 was a no-op session (0 tx) — correct call given insufficient scav accumulation and intensity preservation concerns.
