# Plan for session 30

## Priority 1: Complete Q18 — Harvest >720 min at Scrap Confluence (node 12)

- 20 kamis HARVESTING on node 12 since ~13:55 UTC (session 29).
- Auto_v2 running with REST regen, 5% safety.
- 720 kami-min / 20 kamis = ~36 min real time. Should be done by ~14:31 UTC.
- **Action**: stop auto_v2, stop all kamis (to flush HARVEST_TIME), check_quest_completable(18).
- If met: complete_quest(18), accept_quest(19).
- If NOT met: restart auto_v2 on node 12, schedule +1h.

## Priority 2: Accept Q19 + prepare for it

- Q19: "Harvesting Data II" — Harvest >720 min at Labs Entrance (node 6, room 6).
- After completing Q18, travel from room 12 to room 6.
- Manually start harvests on node 6 (new node = manual start needed), then auto_v2.

## Priority 3: Scavenge node 12

- Node 12 = Scrap Confluence (Scrap type, scav cost 500).
- Droptable: Scrap Metal (9), Cheeseburger (8), Holy Dust (6), Screwdriver (2).
- Holy Dust is useful (needed for naming kamis). Scavenge if points available.

## Quest overview

- **Q18** (MSQ): Harvest >720 min at Scrap Confluence (node 12) — IN PROGRESS
- **Q19** (MSQ, next): Harvest >720 min at Labs Entrance (node 6)
- **Q20** (MSQ): Harvest >720 min at Hollow Path
- **Q6**: Liquidate kami — deferred
- **Q3007** (side): Move 500 times — accumulates naturally
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ is sequential: ...->Q17(done)->Q18->Q19->Q20->Q21->...->Q30 (gates Mina Q2014)->...->Q108
- Q18 IN PROGRESS (harvest at node 12)
- Q19 = harvest at node 6
- Q20 = harvest at Hollow Path (need to find node index)
- Q21+ = scavenge-based quests

## Active strategies
- auto_v2 on node 12, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## CRITICAL LESSON: Always verify quest node before harvesting
- Q18 requires Scrap Confluence (node 12), NOT Scrapyard Exit (node 31).
- Sessions 27-29 wasted gas harvesting on wrong node because plan.md had wrong node.
- Always cross-reference quest objectives against game-data.md before starting harvests.
- Auto_v2 cannot start harvests on a new node (Kamibots gas issue) — always manual start first.

## Inventory notes
- MUSU: ~184,959
- Ice Cream: 81
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Scrap Metal: 35
- Stone: 325
