# Plan for session 33

## Priority 1: Complete Q21 — 2 Scav rolls at Scrap Trees (node 60)

- 20 kamis under auto_v2 on node 60 since ~17:49 UTC (session 32).
- Kamis were RESTING with ~65% HP; auto_v2 will start harvests when HP recovers (~30-60 min).
- Scav cost: 500/roll. Need 1000 total points (points = harvest output).
- **Action**: check scav points via get_scavenge_points(60). If >= 1000:
  - Stop auto_v2 (kami_indices[0] = 43)
  - Stop all harvests (2x10 batch) to flush final output to scav bar
  - Recheck scav points
  - scavenge_claim_and_reveal(60) x2
  - check_quest_completable(21), complete_quest(21)
  - accept_quest(22)
- If points < 1000: restart auto_v2 on node 60, schedule +1h.

## Priority 2: Accept Q22 + begin work

- Q22: "Squaring the Circle II" — 3 Scav rolls at Centipedes (node 62, room 62, zone 2).
- Scav cost at node 62: check catalogs. Room 62 should be near room 60 in zone 2.
- Travel to room 62, start auto_v2 on node 62.

## Priority 3: Look ahead at Q23

- Q23: 3 Scav at Blooming Tree (node 53, zone 2)
- Plan efficient route: 60 → 62 → 53

## Quest overview

- **Q21** (MSQ): 2 Scav rolls at Scrap Trees (node 60) — IN PROGRESS
- **Q22** (MSQ, next): 3 Scav at Centipedes (node 62)
- **Q23** (MSQ): 3 Scav at Blooming Tree (node 53)
- **Q6**: Liquidate kami — deferred
- **Q3007** (side): Move 500 times — ~131/500, accumulates naturally
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ: ...->Q20(done)->Q21->Q22->Q23->...->Q30 (gates Mina Q2014)->...->Q108
- Q21 IN PROGRESS (scav at node 60)
- Q22-Q23 = scavenge quests at zone 2 nodes (62, 53)

## Active strategies
- auto_v2 on node 60, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Inventory notes
- MUSU: ~186,738
- Ice Cream: 80 (used 1 this session)
- Better Ice Cream: 10
- Rock Candyfloss: 66
