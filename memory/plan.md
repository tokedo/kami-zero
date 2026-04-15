# Plan for session 31

## Priority 1: Complete Q19 — Harvest >720 min at Labs Entrance (node 6)

- 20 kamis HARVESTING on node 6 since ~15:20 UTC (session 30).
- Auto_v2 running with REST regen, 5% safety.
- 720 kami-min / 20 kamis = ~36 min real time. Should be done by ~15:56 UTC.
- **Action**: stop auto_v2, stop all kamis (to flush HARVEST_TIME), check_quest_completable(19).
- If met: complete_quest(19), accept_quest(20).
- If NOT met: restart auto_v2 on node 6, schedule +1h.

## Priority 2: Accept Q20 + prepare for it

- Q20: "Harvesting Data III" — Harvest >720 min at Hollow Path (node 37, room 37).
- After completing Q19, travel from room 6 to room 37.
- Node 37 is Normal type, scav cost 200 (drops Wooden Stick, Pine Cone, Poppy).
- Manually start harvests on node 37 (new node = manual start needed), then auto_v2.

## Priority 3: Scavenge node 6

- Node 6 = Labs Entrance (Eerie type, scav cost 100).
- Droptable: only Stone (weight 9). Low value — skip unless points are high.

## Quest overview

- **Q19** (MSQ): Harvest >720 min at Labs Entrance (node 6) — IN PROGRESS
- **Q20** (MSQ, next): Harvest >720 min at Hollow Path (node 37)
- **Q21+** (MSQ): likely scavenge-based quests
- **Q6**: Liquidate kami — deferred
- **Q3007** (side): Move 500 times — accumulates naturally (~107/500 after session 30)
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ is sequential: ...->Q17(done)->Q18(done)->Q19->Q20->Q21->...->Q30 (gates Mina Q2014)->...->Q108
- Q19 IN PROGRESS (harvest at node 6)
- Q20 = harvest at Hollow Path (node 37)
- Q21+ = TBD (check game-data.md after Q20)

## Active strategies
- auto_v2 on node 6, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## CRITICAL LESSON: Always verify quest node before harvesting
- Q18 required Scrap Confluence (node 12), NOT Scrapyard Exit (node 31).
- Always cross-reference quest objectives against game-data.md before starting harvests.
- Auto_v2 cannot start harvests on a new node (Kamibots gas issue) — always manual start first.
- Cooldown after harvest_stop is ~3 min — wait before harvest_start to avoid reverted tx.

## Inventory notes
- MUSU: ~184,959
- Ice Cream: 81
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Scrap Metal: 35
- Stone: 325
