# Plan for session 27

## Priority 0: Quest graph analysis (READ CLAUDE.md FIRST)

CLAUDE.md has a new "Quest graph analysis" section. Before acting on any other priority, analyze the quest dependency tree:

1. For all known quest indices (main 1-108, Mina 2001-2016, side 3001-3024), query the quest registry on-chain to map prerequisites and chains.
2. Identify which of your active/available quests are **critical path** (gate many downstream quests) vs **leaf** (dead ends).
3. Re-prioritize this plan based on the graph. If Quest 17 (Move 100 times) gates Q18 which gates further MSQ progression, it is critical — complete it now, even if that means grinding moves. 63 moves at ~400k gas each is a known cost; blocking weeks of progression is worse.
4. Document the dependency tree in this plan for future sessions.

## Priority 1: MUSU farming + scavenge node 49

- Auto_v2 running on node 49 (Clearing, Normal, scav cost 300).
- Droptable: Stick(9), Stone(9), Mint(4). Mint useful if another Mint quest appears.
- Stop, scavenge, restart cycle when scavenge points accumulated.

## Priority 2: Quest 17 — Move 100 times

- ~37/100 moves done. **Re-evaluate after Priority 0 graph analysis** — if this is critical path, grind it out.
- After Q17: quest 18 = Harvest >720 min at Scrap Confluence (node 31).
- Unlocks SQ 3007 (Move 500 times).

## Priority 3: Quest 6 — Liquidate kami

- Waiting for user review. Liquidation unlocks quest 3005 (auto-awarded) + potentially Obols.
- Quest 3015 needs 5 Obols (not in any droptable — may come from liquidation or marketplace).

## Quest overview

- **Quest 17** (MSQ): Move 100 times — ~37/100, priority TBD after graph analysis
- **Quest 6**: Liquidate kami — waiting for user review
- **Quest 18** (MSQ, next): Harvest >720 min at Scrap Confluence (node 31) — after Q17

## Side quest status

- All completable side quests done through 3014
- 3005: needs kami liquidation (auto-awarded)
- 3015: needs ≥1 Obol (not farmable)
- 3007: unlocks after Q17

## Active strategies
- auto_v2 on node 49, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Inventory notes
- MUSU: ~168,721
- Wooden Stick: 129
- Stone: 325
- Pine Cone: 12
- Daffodil: 7
- Essence of Daffodil: 300
- Black Poppy Extract: 450
- Pine Pollen: 500
- Sanguineous Powder: 250
- Ghost Gum: 1,057
- Ice Cream: 93
- Better Ice Cream: 10
- Rock Candyfloss: 66
- Mint: 0 (burned for Q3014)
- Respec Potion: 1
- Holy Dust: 1
