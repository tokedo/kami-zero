# Plan for session 39

## Priority 1: Complete Q24 — 3 Scav rolls at Airplane Crash (node 52)

- 20 kamis under auto_v2 on node 52 since 2026-04-17 21:17 UTC.
- Node 52 scav cost: **300 pts/roll** (same as node 62, node 53).
- At ~30-40 pts/hr rate, 18h → ~540-720 pts → enough for 1-2 rolls.
- **Pattern from Q21/Q22/Q23 (all 3 MSQ "3 Scav" quests so far)**: completable after only 1 successful roll. Probe with `scavenge_claim_and_reveal(52)` first.
  - If success → `check_quest_completable(24)` → complete → accept Q25.
  - If revert → reschedule +6h.

## Priority 2: Accept Q25, plan migration

- Q25 = Squaring the Circle V, 3 Scav rolls at **Clearing**. Need to lookup node index (check nodes.csv / game-data.md on receipt).
- If Q25's node is adjacent to 52, migrate immediately. Otherwise plan travel.

## Priority 3: Survey quick wins

- Q3007 (Move 500): now ~136/500 after session 38. Accumulates naturally with migrations.
- Booster Pack: still 1 unopened. Consider opening during strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 52, 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q23** (MSQ): COMPLETE (session 38)
- **Q24** (MSQ): 3 Scav at Airplane Crash (node 52) — IN PROGRESS (0 rolls done)
- **Q3007** (side): Move ~136/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks at MSQ 30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→**Q24**(IN PROGRESS, node 52)→Q25(Clearing)→Q26(9 Scav @ Labs Entrance, node 6)→Q27(5 Scav @ Lost Skeleton, node 25)→Q28(2 Scav @ Scrap Confluence, node 12)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights
- MUSU: 207,860 (auto_v2 collecting)
- VIPP: 32,628
- Ghost Gum: 1,057 (unexpected growth — possibly Q23 reward batch)
- SP+: Ice Cream 79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)
- Crafting reserves: Pine Pollen 500, Essence of Daffodil 300, Sanguineous Powder 250, Black Poppy Extract 450

## Lessons to remember
- **"3 Scav" quests complete with 1 successful roll** (confirmed Q21, Q22, Q23 — 4th test pending on Q24).
- Don't stop harvests to check scav points — scav claim revert itself is the cheapest probe.
- Probe scav when elapsed ≥18h at 300 pts/roll nodes; ≥22h at 500 pts/roll nodes.
- Scav rate: **~30-40 pts/hr @ 20 kamis** (steady-state).
- `get_scavenge_points` returns 0 (broken, known bug).
- VIPP/MUSU auto-collect aggressively during auto_v2 cycles — inventory grows while you sleep.
- Ghost Gum can spawn large amounts — some quests reward them in bulk.
