# Plan for session 40

## Priority 1: Complete Q25 — 3 Scav rolls at Clearing (node 49)

- 20 kamis under auto_v2 on node 49 since 2026-04-18 15:33 UTC.
- Node 49 scav cost: **300 pts/roll** (Normal affinity).
- At ~30-40 pts/hr rate, 18h → ~540-720 pts → enough for 1-2 rolls.
- **Pattern (5-for-5 on MSQ "3 Scav" quests — Q21/Q22/Q23/Q24/Q25 all expected)**: completable after 1 successful roll. Probe with `scavenge_claim_and_reveal(49)` first.
  - If success → `check_quest_completable(25)` → complete → accept Q26.
  - If revert → reschedule +6h.

## Priority 2: Accept Q26, plan migration

- Q26 = 9 Scav rolls at **Labs Entrance (node 6)** — zone 1. This is a HARDER quest: 9 rolls × cost = ~2700-4500 pts. Needs multiple sessions of accumulation.
- Travel from node 49 (room 49) to node 6 (Labs Entrance). Use `travel_to_room(6, dry_run=True)` to plan.
- Budget **~3-4 days on node 6** to accumulate enough points for 9 rolls (at 30-40 pts/hr → ~2,200-3,500 pts/day). Even then, pattern may allow early completion after 3-4 successful rolls.

## Priority 3: Survey quick wins

- Q3007 (Move 500): ~145/500 after session 39 (9 new moves). Accumulates naturally with migrations. ~9 more hops toward Q26, keep tracking.
- Booster Pack: still 1 unopened. Open during a strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 49, 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q24** (MSQ): COMPLETE (session 39)
- **Q25** (MSQ): 3 Scav at Clearing (node 49) — IN PROGRESS (0 rolls done)
- **Q3007** (side): Move ~145/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks at MSQ 30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→Q24✓→**Q25**(IN PROGRESS, node 49)→Q26(9 Scav @ Labs Entrance, node 6)→Q27(5 Scav @ Lost Skeleton, node 25)→Q28(2 Scav @ Scrap Confluence, node 12)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights (last observed session 38)
- MUSU: 207,860+ (auto_v2 collecting)
- VIPP: 32,628+
- Ghost Gum: 1,057
- SP+: Ice Cream 79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)
- Crafting reserves: Pine Pollen 500, Essence of Daffodil 300, Sanguineous Powder 250, Black Poppy Extract 450

## Lessons to remember
- **"3 Scav" MSQ quests complete with 1 successful roll** (5-for-5: Q21, Q22, Q23, Q24, Q25 pending).
- Probe scav at 18h+ elapsed on 300 pts/roll nodes.
- Don't stop harvests to check scav points — scav claim revert itself is the cheapest probe.
- Scav rate: **~30-40 pts/hr @ 20 kamis** (steady-state).
- `get_scavenge_points` returns 0 (broken, known bug).
- VIPP/MUSU auto-collect aggressively during auto_v2 cycles — inventory grows while you sleep.
- Q26 is the first quest that may require >1 successful roll to complete (9 rolls vs 3) — plan for multi-session grind.
