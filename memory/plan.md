# Plan for session 11

## Priority 0: Get Plastic Bottles for quest 2007

- Auto_v2 running on node 26 (Trash-Strewn Graves, Eerie, scav cost 100, drops "Stone Bottle Burger" = Stone + Plastic Bottle + Cheeseburger).
- Need 5 Plastic Bottles. Have 7 Pine Cones (sufficient).
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(26) → check inventory for Plastic Bottles.
- If >= 5 Plastic Bottles: complete_quest(2007) → accept_quest(2008 already active, accept 2009 if available).
- If < 5: restart auto_v2 on node 26, schedule short session (+3h).
- Plastic Bottle has tier 7 in droptable (7/22 ≈ 32% chance per roll). With scav cost 100 and ~500 MUSU/hr output, expect ~5 tiers/hr = ~1.6 Plastic Bottles/hr. In 6h: ~30 rolls, ~10 Plastic Bottles.

## Priority 1: Quest 10 — Scavenge in 3 Normal-type rooms

Objective: SCAV_CLAIM_NODE in 3 rooms with Normal affinity.
Best Normal nodes that also serve quest 2008:
- Node 79 (Abandoned Campsite, Normal, "Butt Stems Shroom Pansy", scav 100) → Sanguine Shroom
- Node 55 (Shady Path, Normal, "Stick Stone Daffodil", scav 200) → Daffodil
- Any 3rd Normal node: 33 (Forest Entrance), 35 (Elder Path), 37 (Hollow Path), 57 (River Crossing)

## Priority 2: Quest 2008 — Scavenge specific items

Need: 1 Pine Cone (may already count from session 10 scavenge), 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles.
Overlaps with quest 10 plan (Normal nodes 79 and 55 provide Shroom + Daffodil).
Plastic Bottles from node 26 scavenging should count.

## Priority 3: Quest 2009+ planning

Quest 2009: Craft 500 Pine Pollen (need 1 Pine Cone + Grinder). We have 7 Pine Cones and Spice Grinder.
Quest 2010: Craft 1 XP Potion (need 1 Plastic Bottle + 250 Pine Pollen + Burner). We have Portable Burner.
Quest 2011: Craft 1 Bless Potion (needs 2007 + 2010 complete).
Crafting quests can be done quickly once we have materials.

## Priority 4: SQ 3003 — Level up a kami (DEFERRED)

All kamis level 33-37. XP cost too high. Revisit after XP potions become available via crafting quest line.

## Priority 5: Quest 6 — Liquidate a kami (DEFERRED)

Destructive action. Waiting for user review.

## Active quests
- Quest 6 — liquidate kami — deferred
- Quest 10 — scavenge in 3 Normal rooms — not started
- Quest 2007 — Give 5 Plastic Bottle + 5 Pine Cone — IN PROGRESS (have Pine Cones, need Bottles)
- Quest 2008 — scavenge specific items — partially progressed (Pine Cone from node 25 may count)
- SQ 3003 — level up kami — deferred

## Active strategies
- auto_v2 on node 26, 20 kamis, REST regen, 5% safety. 20/21 slots used.
