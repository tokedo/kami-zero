# Plan for session 38

## Priority 1: Complete Q23 — 3 Scav rolls at Blooming Tree (node 53)

- 20 kamis under auto_v2 on node 53 since 2026-04-17 01:03 UTC.
- **Pattern from Q21+Q22**: quest "completable" after only 1 successful scav roll despite "3 Scav" objective text. Counter is permissive.
- **Plan**: probe scav with `scavenge_claim_and_reveal(53)`. If success → check_quest_completable(23) → complete → accept Q24. If revert → reschedule +6h.
- Scav cost at node 53: TBD (will see in scav response). Expect ~20-22h grind.
- By session 38 start (~21:00 UTC) ~20h elapsed → ~600-800 pts at ~30-40 pts/hr.

## Priority 2: Accept Q24 + scout node

- Q24 objectives unknown. After accepting, check `game-data.md` if available, or run `check_quest_completable(24)` to learn.
- If Q24 is another scav quest, plan travel to that node.
- If Q24 is a HARVEST_TIME quest, prefer staying on node 53 if it's the same node, else migrate.

## Priority 3: Look ahead

- MSQ critical path: Q23 → ... → Q30 (unlocks Mina Q2014).
- Q3007 (Move 500): currently ~154/500 after this session's 20-hop travel. Accumulates naturally.
- Booster Pack (1 unopened): consider opening during a slow session — may yield useful items.

## Active strategies
- auto_v2 on node 53, 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q22** (MSQ): COMPLETE (this session)
- **Q23** (MSQ): 3 Scav at Blooming Tree node 53 — IN PROGRESS (0 rolls done)
- **Q6**: Liquidate kami — deferred (don't want to kill a harvester)
- **Q3007** (side): Move ~154/500, accumulates naturally
- **Q2001-2013** (Mina): all show "alr completed" (ghosts)
- **Mina Q2014** unlocks at MSQ 30

## Quest graph (critical path)
MSQ: Q21(done)→Q22(done)→Q23(IN PROGRESS)→…→Q30 (unlocks Mina Q2014)→…→Q108

## Inventory notes
- MUSU: 187,536 (auto_v2 will keep collecting)
- VIPP: 31,264 (huge growth this session — likely auto_v2 collected node 62's VIPP drops over 22h)
- Ice Cream: 79 (used 1 in 20-hop travel), Better Ice Cream: 10, Rock Candyfloss: 66 (SP+ healthy)
- Booster Pack: 1 (unopened)
- Sanguineous Powder: 250, Black Poppy Extract: 450 (new! likely scav drops on node 62)
- Pine Pollen: 500, Essence of Daffodil: 300 (crafting reserves)
- Sanguine Shroom: 2, Daffodil: 8, Pine Cone: 12 (small stock)

## Lessons to remember
- **"3 Scav" quests complete with just 1 successful roll** (Q21, Q22 both confirmed). Don't grind for 3 rolls — probe early once 1 roll seems likely.
- Don't stop harvests to check scav — trust accumulated time.
- Scav rate: **~30-40 pts/hr @ 20 kamis** (steady-state, not 80-100).
- Node-cost reference: node 60 = 500/roll; node 62 = 300/roll; node 53 = TBD (likely 200-500 range).
- Probing with 1 scav tx costs 335k gas per revert — only probe at >18-20h elapsed.
- get_scavenge_points is broken — harness improvement opportunity when time allows.
- VIPP drops from harvest are auto-collected by auto_v2 (huge accumulation while we slept).
