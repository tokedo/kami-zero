# Plan for session 17

## Priority 1: Quest 12 — Scavenge in 3 Insect-type rooms (1/3 done)

- Auto_v2 running on node 10 (Forest: Insect Node, Z=1, scav cost 200).
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(10) → that's 2/3 Insect.
- Move to node 51 (2 hops: 10→50→51, Insect, scav cost 300), start auto_v2.
- Session 18: scavenge node 51 (3/3), complete quest 12, accept next MSQ.

## Priority 2: Quest 2012 — Give 1 Red Amber Crystal

- Need to scavenge node 53 (Blooming Tree, Eerie, "Stick Cone Amber" droptable, 20% chance).
- Node 53 is 1 hop from node 51 — convenient after quest 12 completion.
- After Insect scavenge cycle: return to node 53, harvest, scavenge for Red Amber.
- If Red Amber obtained: burn_items([1007], [1]) → complete_quest(2012).

## Priority 3: Quest 3012 — Spend 15000 MUSU at Mina's Shop

- Need to travel to room 13 (Mina's shop). ~14 hops from node 10 cluster.
- Have 151,418 MUSU. Buy Ghost Gums or other useful items.
- Deferred until convenient (perhaps after quest 12 completion when traveling anyway).

## Priority 4: Quest 2013 — Move to Trash-Strewn Graves, Give 15 Daffodil

- Blocked: only have 3 Daffodils, need 15.
- Daffodil sources: node 55 (Shady Path, Normal, scav cost 200, ~31% drop rate).
- After quest 2012, will need to farm Daffodils.

## Quest overview

- **Quest 12** (MSQ): Scavenge 3 Insect rooms — IN PROGRESS (1/3)
- **Quest 2012** (Mina): Give 1 Red Amber Crystal — need scavenge at node 53
- **Quest 2013** (Mina): Give 15 Daffodil — blocked (have 3/15)
- **Quest 3012** (side): Spend 15000 at Mina's — deferred (need room 13)
- **Quest 6**: Liquidate kami — waiting for user review
- **Quest 3003**: Level up kami — deferred (XP too expensive)

## Active strategies
- auto_v2 on node 10, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Insect node routing (remaining)
- Node 10 (current) → node 50 (1 hop) → node 51 (1 hop from 50) → node 53 (1 hop from 51)
