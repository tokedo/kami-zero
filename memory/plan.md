# Plan for session 7

## Priority 0: Check quest 2004 + restart auto_v2

- check_quest_completable(2004) — should be done (720 min / 20 kamis = 36 min)
- If completable: complete, accept quest 2005 (harvest >720 min on Trash-Strewn Graves, node 26)
- Retry auto_v2 on current node — zombie strategy slots should have cleared by now
- If slots still stuck: alert in alerts.md, harvest manually

## Priority 1: Quest 10 — Scavenge in 3 Normal-type rooms

Objective: `SCAV_CLAIM_NODE` in 3 rooms with Normal affinity.
Normal nodes (closest to node 10): 35 (Elder Path), 33 (Forest Entrance), 37 (Hollow Path), 55 (Shady Path), 57 (River Crossing)
Plan: move to a Normal node, harvest enough to accumulate scavenge points (cost 100-200), claim, repeat for 3 nodes. This takes multiple sessions — each node needs harvest time for scav points.

## Priority 2: Quest 2008 — Scavenge specific items

Need: 1 Pine Cone, 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles
- Pine Cone: node 10 drops "Stick Cone Rename" — scavenge here while harvesting for quest 2004
- Daffodil: nodes 19, 55, 60, 63
- Sanguine Shroom: nodes 18, 50, 72, 76
- Plastic Bottle: nodes 1, 26, 51, 52, 65
Multi-node effort. Plan around quest 10 Normal-room movement.

## Priority 3: SQ 3003 — Level up a kami

Need kami in RESTING state. Auto_v2 cycles kamis through REST. When auto_v2 is running, check for RESTING kami and level it up. Kami 43 has enough XP (level 37, skill points invested).

## Priority 4: Quest 6 — Liquidate a kami

Deferred — destructive action.

## Active quests
- Quest 6 — liquidate kami — deferred
- Quest 10 — scavenge in 3 Normal rooms — not started
- Quest 2004 — harvest 720 min at node 10 — IN PROGRESS (20 kamis harvesting)
- Quest 2008 — scavenge specific items — not started
- SQ 3003 — level up kami — waiting for RESTING state

## Active strategies
- NO auto_v2 running (Kamibots slot bug — 20/21 slots occupied by zombie strategy)
- 20 kamis harvesting directly on node 10 (Forest: Insect Node)

## Key data from game-data.md
- Quest objectives now known — game-data.md has full quest table
- Quest 2005 (next Mina): harvest 720 min at Trash-Strewn Graves (node 26, Eerie)
- Quest 11 (next main): scavenge in 3 Eerie rooms
- Quest 2008 branches from 2003 (parallel to 2004)

## Key learnings
- After harvest_stop, there's a ~3 min cooldown before harvest_start works
- Kamibots stop_strategy returns DELETED but may not free slots (platform bug)
- Quest 2003 auto-completed from session 5's scrap metal activity
- game-data.md has full quest catalog — always check before planning
