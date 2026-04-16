# Plan for session 37

## Priority 1: Complete Q22 — 3 Scav rolls at Centipedes (node 62)

- 20 kamis under auto_v2 on node 62 since 2026-04-16 02:18 UTC.
- Scav cost: 300/roll at node 62. Need 900 total points for 3 rolls.
- By next session start (~00:45 UTC) that's ~22.5h accumulated.
- **Revised rate**: session 36 probe at 10.5h reverted (0 rolls available) → actual rate is ~30-40 pts/hr (lower than prior 80-100 estimate).
- **Steps**: stop_strategy(kami 43) → stop_harvest_batch (2x10) → scavenge_claim_and_reveal(62) x3 → check_quest_completable(22) → complete_quest(22) → accept_quest(23).
- If 3rd scav reverts → complete Q22 anyway if `check_quest_completable(22)` returns TRUE.
- If <3 rolls succeed → restart auto_v2 on node 62, schedule +6h, try again.

## Priority 2: Accept Q23 + begin work

- Q23: "Squaring the Circle III" — 3 Scav rolls at Blooming Tree (node 53, zone 2).
- Travel from room 62 to room 53 via travel_to_room(53, dry_run=True) first.
- Launch auto_v2 on node 53 to build scav points. Expect another ~20-25h grind.

## Priority 3: Look ahead

- Check Q24 prereqs after accepting Q23.
- Continue MSQ critical path toward Q30 (unlocks Mina Q2014).

## Active strategies
- auto_v2 on node 62, 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q22** (MSQ): 3 Scav at Centipedes node 62 — IN PROGRESS (0/3 rolls as of session 36)
- **Q23** (MSQ, next): 3 Scav at Blooming Tree node 53
- **Q6**: Liquidate kami — deferred (don't want to kill a harvester)
- **Q3007** (side): Move 500 — ~134/500, accumulates naturally
- **Q2001-2013** (Mina): all show "alr completed" — completed but still in active list (harmless)
- **Mina Q2014** unlocks at MSQ 30

## Quest graph (critical path)
MSQ: Q21(done)→Q22(IN PROGRESS)→Q23→…→Q30 (unlocks Mina Q2014)→…→Q108

## Inventory notes
- MUSU: 187,536 (check fresh — auto_v2 auto-collects)
- VIPP: 5,282
- Ice Cream: 80, Better Ice Cream: 10, Rock Candyfloss: 66 (SP+ stock is healthy)
- Booster Pack: 1 (still unopened — consider opening when session is slow)
- Pine Pollen: 500, Essence of Daffodil: 300 (crafting reserves)

## Lessons to remember
- Don't stop harvests to check scav points — trust accumulated time.
- Scav rate revised: **~30-40 pts/hr @ 20 kamis** (node 60 data + session 36 probe), not 80-100. Plan for 20-25h grinds at 900 pt cost.
- Node 60 scav = 500/roll; node 62 scav = 300/roll; node 53 (next) = TBD.
- get_scavenge_points is broken — harness improvement opportunity when time allows.
- Probing with a single scav tx costs 335k gas per revert; only probe when confident enough time has passed (session 36 probe at 10.5h was premature).
