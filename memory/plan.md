# Plan for session 14

## Priority 1: Scavenge node 55 for Daffodil (quest 2008)

- Auto_v2 running on node 55 (Shady Path, Normal, Z=1, scav cost 200, "Stick Stone Daffodil" droptable).
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(55).
- Daffodil drop rate: ~31% (weight 8 out of 26). May need multiple scavenge cycles if unlucky.
- If Daffodil obtained: check_quest_completable(2008). If completable, complete it.

## Priority 2: Complete quest 2008 → accept quest 2009

- Quest 2008 items: Pine Cone (have 2), Daffodil (need 1), Sanguine Shroom (have 2), Plastic Bottle (have 4). Only missing Daffodil.
- Quest 2009: Craft 500 Pine Pollen (need 1 Pine Cone + Grinder). Have both.
- Quest 2010: Craft 1 XP Potion (need Plastic Bottle + 250 Pine Pollen + Burner). Have Burner.
- Quest 2011: Craft 1 Bless Potion.

## Priority 3: Quest 11 — Scavenge in 3 Eerie-type rooms

- Quest 11 accepted session 12. Need 3 Eerie scavenges with quest active.
- Accessible Eerie nodes at Z=1: 1 (Misty Riverside, cost 100), 6 (Labs Entrance, cost 100), 25 (Lost Skeleton, cost 200), 26 (Trash-Strewn Graves, cost 100), 52 (Airplane Crash, cost 300), 53 (Blooming Tree, cost 300).
- After getting Daffodil, travel to cheap Eerie nodes (1, 6, 26) for quest 11.
- Need to harvest at each node long enough to accumulate scavenge cost, then scavenge. Low-cost nodes (100) are fastest.

## Priority 4: Quest 2009+ chain (blocked on 2008)

- Quest 2009: Craft 500 Pine Pollen (recipe 7: 1 Pine Cone → 500 Pine Pollen, Grinder, 10 musu, 25 craft time)
- Quest 2010: Craft 1 XP Potion (recipe 2: 1 Plastic Bottle + 250 Pine Pollen → 1 XP Potion, Burner)
- Quest 2011: Craft 1 Bless Potion (recipe 5: 1 Plastic Bottle + 100 Essence of Daffodil → 1 Bless Potion, Burner)

## Deferred quests
- Quest 6 — liquidate kami — waiting for user review
- Quest 11 — main line — IN PROGRESS (need 3 Eerie scavenges)
- Quest 2008 — scavenge Daffodil — IN PROGRESS (need Daffodil only)
- SQ 3003 — level up kami — deferred (XP too expensive)

## Active strategies
- auto_v2 on node 55, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Reminder: run pre-logout checklist before ending session
See CLAUDE.md "Pre-logout checklist" — scan all quests for resource-ready completions before scheduling next session.
