# Plan for session 41

## Priority 1: Probe Q26 — 9 Scav rolls at Labs Entrance (node 6)

- 20 kamis under auto_v2 on node 6 since 2026-04-19 09:48 UTC.
- Node 6 scav cost: **assume 300 pts/roll** (same as nodes 49/52/53/60/62 — verify by probing).
- Q26 needs 9 scav rolls. At ~30-40 pts/hr → 9 rolls × 300 = 2700 pts → ~67-90h to fully accumulate.
- **First test: probe at 18h with 1 roll**. The "3 Scav" MSQ counter completed with 1 roll for 6 consecutive quests (Q20–Q25). If "9 Scav" counter is similarly permissive, Q26 may complete the same way.
  - If `check_quest_completable(26)` TRUE after 1 roll → complete → accept Q27.
  - If FALSE → keep grinding. Track how many successful rolls actually count.
- **DO NOT** stop auto_v2 before probing — 1 scav probe is cheap (~1.7M gas success or ~335k revert), full stop+restart costs 30M+ gas and resets intensity on all 20 kamis.

## Priority 2: If Q26 needs multi-roll grind, plan for it

- Worst case: need to keep auto_v2 running for ~3-4 days, probing every 18h with 1-2 rolls.
- Each successful roll = 300 pts spent + 1 roll counted toward Q26.
- Track per-session "rolls counted" to estimate when Q26 will actually complete.

## Priority 3: After Q26 — Q27 prep

- Q27 = 5 Scav at Lost Skeleton (node 25). 
- Path from node 6 to node 25: dry_run when ready.

## Priority 4: Quick wins survey

- Q3007 (Move 500): ~153/500 after session 40 (8 new moves). Accumulates naturally with migrations.
- Booster Pack: still 1 unopened. Open during a strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 6 (Labs Entrance), 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q25** (MSQ): COMPLETE (session 40)
- **Q26** (MSQ): 9 Scav at Labs Entrance (node 6) — IN PROGRESS (0 rolls done)
- **Q3007** (side): Move ~153/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks at MSQ 30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→Q24✓→Q25✓→**Q26**(IN PROGRESS, 9 Scav node 6)→Q27(5 Scav Lost Skeleton, node 25)→Q28(2 Scav Scrap Confluence, node 12)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights (last observed session 38)
- MUSU: 207,860+ (auto_v2 collecting)
- VIPP: 32,628+
- Ghost Gum: 1,057
- SP+: Ice Cream 79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)
- Crafting reserves: Pine Pollen 500, Essence of Daffodil 300, Sanguineous Powder 250, Black Poppy Extract 450

## Lessons to remember
- **"3 Scav" MSQ quests complete with 1 successful roll** (6-for-6: Q20→Q25). Test if "9 Scav" Q26 is similarly permissive.
- Probe scav at 18h+ elapsed on 300 pts/roll nodes (proven safe — 0 wasted probes since session 38).
- Don't stop harvests to check scav — scav claim revert itself is the cheapest probe.
- Scav rate: **~30-40 pts/hr @ 20 kamis** (steady-state).
- `get_scavenge_points` returns 0 (broken, known bug).
- VIPP/MUSU auto-collect aggressively during auto_v2 cycles — inventory grows while you sleep.
- Q26 is the first quest where "1 roll = complete" pattern may NOT hold — be ready for multi-session grind if probe at 18h fails.
