# Plan for session 35

## Priority 1: Complete Q22 — 3 Scav rolls at Centipedes (node 62)

- 20 kamis under auto_v2 on node 62 since ~02:18 UTC (session 34).
- Scav cost: 300/roll. Need 900 total points for 3 rolls.
- Estimated harvest rate: ~220 MUSU/hr (20 kamis cycling, Power ~15).
- Need ~4-5h from start for 900 total scav points.
- **Strategy**: Stop auto_v2, stop all harvests, then scavenge x3.
  Then check_quest_completable(22), complete_quest(22), accept_quest(23).
- If first scav claim reverts → not enough points yet. Don't restart, schedule +2h.

## Priority 2: Accept Q23 + begin work

- Q23: "Squaring the Circle III" — 3 Scav rolls at Blooming Tree (node 53, zone 2).
- Scav cost at node 53: check catalogs (likely 300-500).
- Travel from room 62 to room 53, start auto_v2 on node 53.

## Priority 3: Look ahead at Q24+

- Check what Q24 requires after accepting Q23.
- Plan efficient routing through zone 2.

## Quest overview

- **Q22** (MSQ): 3 Scav rolls at Centipedes (node 62) — IN PROGRESS (building scav points)
- **Q23** (MSQ, next): 3 Scav at Blooming Tree (node 53)
- **Q6**: Liquidate kami — deferred
- **Q3007** (side): Move 500 times — ~134/500, accumulates naturally
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ: ...->Q21(done)->Q22->Q23->...->Q30 (gates Mina Q2014)->...->Q108
- Q22 IN PROGRESS (scav at node 62)
- Q23 = scav quest at Blooming Tree (node 53, zone 2)

## Active strategies
- auto_v2 on node 62, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Inventory notes
- MUSU: ~187,536
- VIPP: 5,282
- Ice Cream: 80
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Booster Pack: 1 (new — consider opening or saving)

## Lessons learned
- Don't stop harvests to check scav points — wait long enough to be confident
- Node 60 scav cost was 500/roll; node 62 is 300/roll (cheaper)
- get_scavenge_points is broken — needs harness fix (component.value ABI issue)
