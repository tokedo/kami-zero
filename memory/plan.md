# Plan for session 10

## Priority 0: Complete quest 2006 — harvest 720 min at Lost Skeleton (Moonside)

- Auto_v2 running on 20 kamis at node 25 (REST regen, 5% safety).
- "(Moonside)" may mean harvest time only counts during MOONSIDE phase (12h window per 36h cycle).
- MOONSIDE started ~2h after session 9 launch. By session 10 (+8h), one full MOONSIDE window should have passed.
- Steps: stop all kamis → check_quest_completable(2006) → complete_quest(2006) → accept_quest(2007).
- If NOT completable: check if phase-gating is the issue. May need to time harvest cycles to MOONSIDE windows.
- Quest 2007: "Give 5 Plastic Bottle, 5 Pine Cone" — need to find scavenge sources for these items.

## Priority 1: Quest 10 — Scavenge in 3 Normal-type rooms

Objective: SCAV_CLAIM_NODE in 3 rooms with Normal affinity.
Normal nodes near current area: 35 (Elder Path), 33 (Forest Entrance), 37 (Hollow Path), 55 (Shady Path).
Requires: move to Normal node, harvest to accumulate scavenge points (cost 100-200), claim, repeat 3x.
Plan movement to Normal nodes after quest 2006.

## Priority 2: Quest 2008 — Scavenge specific items

Need: 1 Pine Cone, 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles.
Drops come from scavenge droptables at specific node types. Cross-reference with game-data.md.
Overlaps with quest 2007 needs (5 Pine Cone, 5 Plastic Bottle).

## Priority 3: SQ 3003 — Level up a kami (DEFERRED)

All kamis level 33-37. XP cost at these levels: 50k-143k XP per level.
Revisit when a kami has naturally accumulated enough XP from auto_v2 harvesting.

## Priority 4: Quest 6 — Liquidate a kami (DEFERRED)

Destructive action. Waiting for user review.

## Active quests
- Quest 6 — liquidate kami — deferred
- Quest 10 — scavenge in 3 Normal rooms — not started
- Quest 2006 — harvest 720 min at Lost Skeleton (Moonside) — IN PROGRESS (auto_v2 on node 25)
- Quest 2008 — scavenge specific items — not started
- SQ 3003 — level up kami — deferred (insufficient XP)

## Active strategies
- auto_v2 on node 25, 20 kamis, REST regen, 5% safety. 20/21 slots used.
