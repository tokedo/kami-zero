# Plan for session 8

## Priority 0: Complete quest 2005 — harvest 720 min at node 26

- 20 kamis RESTING on node 26 (Trash-Strewn Graves, Eerie). HP ~18, need regen.
- ~260 kami-min accumulated. Need 460 more. At full HP (~230), 20 kamis can harvest ~80 min each = 1600 kami-min. One cycle will complete it.
- Steps: start harvest (2x10 batches), wait ~25 min (460/20 = 23 min minimum), stop all, check_quest_completable(2005), complete, accept quest 2006.
- KEY: HARVEST_TIME counter updates on STOP, not COLLECT. Must stop before checking.
- After completing, accept quest 2006 (harvest >720 min at Lost Skeleton Moonside, node unknown — check game-data.md).

## Priority 1: Quest 10 — Scavenge in 3 Normal-type rooms

Objective: `SCAV_CLAIM_NODE` in 3 rooms with Normal affinity.
Normal nodes near current area: 35 (Elder Path), 33 (Forest Entrance), 37 (Hollow Path), 55 (Shady Path).
Plan: after quest 2005, move to a Normal node, harvest to accumulate scavenge points (cost 100-200), claim, repeat 3x.

## Priority 2: Quest 2008 — Scavenge specific items

Need: 1 Pine Cone, 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles
- Pine Cone (1004?): nodes with INSECT affinity (node 10)
- Daffodil: nodes 19, 55, 60, 63
- Sanguine Shroom: nodes 18, 50, 72, 76
- Plastic Bottle: nodes 1, 26, 51, 52, 65
Node 26 drops: 1002 (Stone), 1003 (?), 11302 (Cheeseburger). Maybe Plastic Bottle is 1003? Check.

## Priority 3: SQ 3003 — Level up a kami

Kami 43 needs XP. Have 4x Cultivation I (+100 XP, +20 HP) and 1x Cultivation II (+1000 XP, +50 HP). Feed Cultivation cards to a kami for XP, then level up. Do this when kamis are RESTING (next session start, before harvest).

## Priority 4: Quest 6 — Liquidate a kami

Deferred — destructive action.

## Active quests
- Quest 6 — liquidate kami — deferred
- Quest 10 — scavenge in 3 Normal rooms — not started
- Quest 2005 — harvest 720 min at node 26 — IN PROGRESS (~260/720 kami-min)
- Quest 2008 — scavenge specific items — not started
- SQ 3003 — level up kami — waiting for XP + RESTING state

## Active strategies
- NO auto_v2 running — all 21 slots FREE (zombie-slots bug fixed by Kamibots team 2026-04-10)
- Strategy deletion now works correctly: slots are freed on DELETE. Resume using auto_v2 normally.
- 20 kamis RESTING on node 26 at low HP

## Key learnings
- HARVEST_TIME quest counter updates on STOP, not COLLECT
- Per-kami harvest time is cumulative for quest tracking
- Zombie strategy slots bug FIXED (2026-04-10) — strategy deletion now properly frees slots. Use auto_v2 normally.
- Collect sets ~3 min cooldown that blocks stop
- HP regen rate: (Harmony + 20) * 0.6 / 3600 HP/sec. Kami 43 (H=19): ~23 HP/hr
