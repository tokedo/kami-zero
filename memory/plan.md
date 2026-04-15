# Plan for session 34

## Priority 1: Complete Q21 — 2 Scav rolls at Scrap Trees (node 60)

- 20 kamis under auto_v2 on node 60 since ~20:09 UTC (session 33 restart).
- Scav cost: 500/roll. Need 1000 total points.
- Estimated harvest rate: ~220 MUSU/hr (20 kamis cycling, Power ~15, neutral efficacy).
- Had ~480 scav points before intensity reset. Need ~4.5h from restart for 1000 total.
- **CRITICAL: Do NOT stop harvests preemptively.** Stopping resets intensity and wastes gas.
- **Strategy**: Try `scavenge_claim_and_reveal(60)` directly. If it succeeds → points >= 500.
  Then stop auto_v2, stop all harvests to flush remaining output, scavenge again.
  Then check_quest_completable(21), complete_quest(21), accept_quest(22).
- If claim reverts → not enough points yet. Restart nothing, just schedule +2h.
- get_scavenge_points reader is broken (component.value ABI issue). Don't rely on it.

## Priority 2: Accept Q22 + begin work

- Q22: "Squaring the Circle II" — 3 Scav rolls at Centipedes (node 62, room 62, zone 2).
- Scav cost at node 62: check catalogs. Room 62 should be near room 60 in zone 2.
- Travel to room 62, start auto_v2 on node 62.

## Priority 3: Look ahead at Q23

- Q23: 3 Scav at Blooming Tree (node 53, zone 2)
- Plan efficient route: 60 → 62 → 53

## Quest overview

- **Q21** (MSQ): 2 Scav rolls at Scrap Trees (node 60) — IN PROGRESS (building scav points)
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
- MUSU: ~187,536
- Ice Cream: 80
- Better Ice Cream: 10
- Rock Candyfloss: 66
- VIPP: 121

## Lessons learned
- Don't stop harvests to check scav points — use a claim attempt instead (cheaper than intensity reset)
- get_scavenge_points is broken — needs harness fix (component.value ABI issue)
