# Plan for session 9

## Priority 0: Complete quest 2005 — harvest 720 min at node 26

- Auto_v2 running on 20 kamis at node 26 (REST regen, 5% safety).
- ~260 kami-min accumulated before auto_v2 launch. After 8h of auto_v2 cycling, should far exceed 720.
- KEY: auto_v2 stop cycles update HARVEST_TIME counter. Check completability first.
- Steps: check_quest_completable(2005) → complete_quest(2005) → accept_quest(2006).
- Quest 2006: "harvest >720 min at Lost Skeleton Moonside" — check game-data.md for node.

## Priority 1: Quest 10 — Scavenge in 3 Normal-type rooms

Objective: SCAV_CLAIM_NODE in 3 rooms with Normal affinity.
Normal nodes near current area: 35 (Elder Path), 33 (Forest Entrance), 37 (Hollow Path), 55 (Shady Path).
Requires: move to Normal node, harvest to accumulate scavenge points (cost 100-200), claim, repeat 3x.
After quest 2005, plan movement to Normal nodes.

## Priority 2: Quest 2008 — Scavenge specific items

Need: 1 Pine Cone, 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles.
Drops come from scavenge droptables at specific node types. Cross-reference with game-data.md.

## Priority 3: SQ 3003 — Level up a kami (DEFERRED)

All kamis level 33-37. XP cost at these levels: 50k-143k XP per level.
XP source: harvesting (1:1 with MUSU). Need many harvest cycles to accumulate.
Revisit when a kami has naturally accumulated enough XP from auto_v2 harvesting.

## Priority 4: Quest 6 — Liquidate a kami (DEFERRED)

Destructive action. Waiting for user review.

## Active quests
- Quest 6 — liquidate kami — deferred
- Quest 10 — scavenge in 3 Normal rooms — not started
- Quest 2005 — harvest 720 min at node 26 — IN PROGRESS (auto_v2 running)
- Quest 2008 — scavenge specific items — not started
- SQ 3003 — level up kami — deferred (insufficient XP)

## Active strategies
- auto_v2 on node 26, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Key learnings
- HARVEST_TIME quest counter updates on STOP, not COLLECT
- Zombie strategy slots bug FIXED — strategy deletion properly frees slots
- SQ 3003 level-up needs ~143k XP at level 37. Feed + cultivation cards insufficient. Requires many harvest cycles.
- Cultivation II (+1000 XP) was consumed on kami 43 — did not enable level up
