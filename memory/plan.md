# Plan for session 15

## Priority 1: Scavenge node 53 for Red Amber Crystal (quest 2012)

- Auto_v2 running on node 53 (Blooming Tree, Eerie, Z=1, scav cost 300, "Stick Cone Amber" droptable).
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(53).
- Red Amber Crystal drop rate: 20% (weight 4 out of 20). May need multiple scavenge cycles.
- If Red Amber obtained: burn_items([1007], [1]) → check_quest_completable(2012) → complete_quest(2012).
- This scavenge also counts as Eerie scavenge 1/3 for quest 11.

## Priority 2: Quest 11 — Scavenge in 3 Eerie-type rooms

- Quest 11 accepted session 12. Need 3 Eerie scavenges with quest active.
- Scavenging node 53 = 1/3.
- After Red Amber, travel to cheap Eerie nodes for quest 11 (2/3, 3/3):
  - Node 1 (Misty Riverside, cost 100) — closest cheap Eerie
  - Node 6 (Labs Entrance, cost 100)
  - Node 26 (Trash-Strewn Graves, cost 100) — also quest 2013 location
- Strategy: travel to Eerie node, start auto_v2, next session scavenge. Or if scav points from node 53 cycle are enough for a single scavenge at a low-cost node, do it inline.

## Priority 3: Quest 2013 — Move to Trash-Strewn Graves, Give 15 Daffodil

- Blocked: only have 3 Daffodils, need 15. Need to farm more Daffodils.
- Daffodil sources: node 55 (Shady Path, Normal, scav cost 200, ~31% drop rate).
- After quest 11 Eerie scavenges, return to node 55 to farm Daffodils.
- Quest 2013 also requires being in room 26 (Trash-Strewn Graves).

## Priority 4: Quest 3012 — Spend 15000 MUSU at Mina's Shop

- Need to travel to room 13 (Mina's shop). Deferred until convenient.
- Have ~142k MUSU. Buy Ghost Gum or other useful items.

## Quest 2012-2016 chain overview

- 2012: Give 1 Red Amber Crystal — IN PROGRESS (need scavenge at node 53)
- 2013: Move to Trash-Strewn Graves, Give 15 Daffodil — blocked (have 3/15)
- 2014: Give 2 Wooden Sticks + 125 Sanguineous Powder + 125 Resin Tincture — need crafting
- 2015: Give 9999 MUSU — have enough
- 2016: Go to Temple by the Waterfall — need MSQ 31

## Deferred quests
- Quest 6 — liquidate kami — waiting for user review
- Quest 11 — main line — IN PROGRESS (need 3 Eerie scavenges, 0/3)
- Quest 2012 — Red Amber Crystal — IN PROGRESS
- Quest 3003 — level up kami — deferred (XP too expensive)
- Quest 3012 — spend at Mina's — deferred (need room 13)

## Active strategies
- auto_v2 on node 53, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Reminder: craft_item tool now available
- Added to executor/server.py this session. Will be available as MCP tool after server restart.
- Fallback: call directly via `.venv/bin/python -c "from server import craft_item; ..."`
