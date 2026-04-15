# Plan for session 32

## Priority 1: Complete Q20 — Harvest >720 min at Hollow Path (node 37)

- 20 kamis HARVESTING on node 37 since ~16:35 UTC (session 31).
- Auto_v2 running with REST regen, 5% safety.
- 720 kami-min / 20 kamis = ~36 min real time. Should be done by ~17:11 UTC.
- **Action**: stop auto_v2, stop all kamis (to flush HARVEST_TIME), check_quest_completable(20).
- If met: complete_quest(20), accept_quest(21).
- If NOT met: restart auto_v2 on node 37, schedule +1h.

## Priority 2: Accept Q21 + prepare for it

- Q21: "Squaring the Circle I" — 2 Scav rolls at Scrap Trees (node 60, room 60).
- Prerequisites: MSQ 20 + MIN 13 (Mina 2013, already done).
- Node 60: Scrap type, zone 2, scav cost 500. Room 60 adjacent to room 5 (zone 1).
- Droptable: Scrap Metal (9), Daffodil (7), Screwdriver (2). NOTE: yields VIPP not MUSU.
- Need at least 1000 scav points for 2 rolls. Harvest until enough points accumulate, then scavenge x2.
- Travel: room 37 → room 60. Check dry_run for path.

## Priority 3: Look ahead at Q22-Q23

- Q22: 3 scav at Centipedes (node 62, zone 2)
- Q23: 3 scav at Blooming Tree (node 53, zone 2)
- All zone 2. Plan efficient route: 60 → 62 → 53 or similar.

## Quest overview

- **Q20** (MSQ): Harvest >720 min at Hollow Path (node 37) — IN PROGRESS
- **Q21** (MSQ, next): 2 Scav rolls at Scrap Trees (node 60)
- **Q22** (MSQ): 3 Scav at Centipedes (node 62)
- **Q23** (MSQ): 3 Scav at Blooming Tree (node 53)
- **Q6**: Liquidate kami — deferred
- **Q3007** (side): Move 500 times — ~115/500, accumulates naturally
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ is sequential: ...->Q19(done)->Q20->Q21->Q22->Q23->...->Q30 (gates Mina Q2014)->...->Q108
- Q20 IN PROGRESS (harvest at node 37)
- Q21-Q23 = scavenge quests at zone 2 nodes (60, 62, 53)
- Each requires harvesting at the node to build scav points, then scavenging

## Active strategies
- auto_v2 on node 37, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Inventory notes
- MUSU: ~185,847
- Ice Cream: 81
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Scrap Metal: 35
- Stone: 325
