# Plan for session 29

## Priority 1: Complete Q18 — Harvest >720 min at Scrapyard Exit (node 31)

- 20 kamis now HARVESTING on node 31 (started session 28, ~12:35 UTC).
- Auto_v2 running with REST regen, 5% safety.
- 720 kami-min / 20 kamis = ~36 min real time. Should be well past threshold.
- **Action**: stop auto_v2, stop all kamis (to flush HARVEST_TIME), check_quest_completable(18).
- If met: complete_quest(18), accept_quest(19).
- If NOT met: restart auto_v2 on node 31, schedule +2h.

## Priority 2: Accept Q19 + check objectives

- Q19 objectives unknown — check completability after accepting.
- Continue MSQ chain as far as possible.

## Priority 3: Scavenge node 31

- Node 31 = Scrapyard Exit (Scrap type, scav cost 100).
- Droptable: Stone (9), Scrap Metal (7), Cheeseburger (6).
- Scavenge after stopping kamis for Q18.

## Quest overview

- **Q18** (MSQ): Harvest >720 min at Scrapyard Exit (node 31) — IN PROGRESS (kamis actively harvesting since ~12:35 UTC)
- **Q6**: Liquidate kami — deferred (waiting for user review)
- **Q3007** (side): Move 500 times — ~98/500, accumulates naturally
- **Mina line**: Q2014 unlocks at MSQ 30 — many MSQs to go

## Quest graph (critical path)

MSQ is sequential: ...->Q17->Q18->Q19->...->Q30 (gates Mina Q2014)->...->Q108
- Q17 DONE (session 27)
- Q18 IN PROGRESS (harvest 720 min at node 31 — kamis now correctly on node 31)
- Q19+ unknown objectives — advance as fast as possible

Side quests (leaf, low priority):
- Q3007: Move 500 times (natural accumulation)
- Q6: Liquidate kami (needs user decision)

## Active strategies
- auto_v2 on node 31, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Known issues
- harvest_start gas limit was too low for new-node starts (fixed: 1.5M -> 3M in server.py)
- MCP server needs restart to pick up gas limit fix (or use direct Python scripts)

## Inventory notes
- MUSU: ~184,176
- Ice Cream: 82
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Scrap Metal: 35
- Stone: 325
