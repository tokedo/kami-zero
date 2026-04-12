# Plan for session 18

## Priority 1: Quest 13 — Scavenge in 3 Scrap-type rooms (0/3)

- Auto_v2 running on node 47 (Scrap Paths, Z=1, scav cost 100).
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(47) → that's 1/3 Scrap.
- Move to node 31 (Scrapyard Exit, Scrap, scav cost 100). Path: 47→31 (1 hop? check adjacency).
- Start harvesting on 31, accumulate scav points. This may require a short harvest cycle.
- If scav points already > 100 on node 31 after stops (auto_v2 cycles flush points), scavenge immediately.
- Otherwise: start auto_v2 on 31, wait for next session.
- After 31: node 30 (Scrapyard Entrance, Scrap, cost 100, adjacent to 31 via room graph).
- Plan: 47 (scav) → 31 (harvest + scav) → 30 (harvest + scav) → complete quest 13.
- Note: each node needs harvest time to accumulate scav points ≥ cost (100 each).

## Priority 2: Quest 2012 — Give 1 Red Amber Crystal

- Need to scavenge node 53 (Blooming Tree, Eerie, "Stick Cone Amber" droptable, 20% chance).
- Deferred until quest 13 Scrap tour is complete.
- Node 53 is accessible from Scrap cluster via ~8-10 hops.

## Priority 3: Quest 3012 — Spend 15000 MUSU at Mina's Shop

- Need to travel to room 13 (Mina's shop).
- Have 155,994 MUSU. Buy Ghost Gums or other useful items.
- Deferred until convenient (perhaps after quest 13 completion when traveling anyway).

## Priority 4: Quest 14 — Give 5 Wooden Sticks (after quest 13)

- Have 83 Wooden Sticks. Should be instantly completable after quest 13.

## Priority 5: Quest 2013 — Move to Trash-Strewn Graves, Give 15 Daffodil

- Blocked: only have 3 Daffodils, need 15.
- Daffodil sources: node 55 (Shady Path, Normal, scav cost 200, ~31% drop rate), node 60 (Scrap Trees, Scrap, scav cost 500).
- After Scrap tour, consider farming Daffodils at node 55 or 60.

## Quest overview

- **Quest 13** (MSQ): Scavenge 3 Scrap rooms — IN PROGRESS (0/3)
- **Quest 2012** (Mina): Give 1 Red Amber Crystal — need scavenge at node 53
- **Quest 2013** (Mina): Give 15 Daffodil — blocked (have 3/15)
- **Quest 3012** (side): Spend 15000 at Mina's — deferred (need room 13)
- **Quest 6**: Liquidate kami — waiting for user review
- **Quest 3003**: Level up kami — deferred (XP too expensive)

## Active strategies
- auto_v2 on node 47, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Scrap node routing
- Node 47 (current, scav cost 100) → node 31 (1 hop?, cost 100) → node 30 (adjacent to 31, cost 100)
