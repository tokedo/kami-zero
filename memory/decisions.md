# Decision log

Append one entry per session. Newest at the bottom.

---

## 2026-04-08 — session 0 (bootstrap by human operator)

**Setup**: GCP VM (kami-agent-prod, us-central1-a, e2-small). Claude Code authed via Max subscription. MCP executor running. bpeon registered with Kamibots (GUILD tier, 11 slots), operator key stored, 12 kamis transferred, 108,958 Musu seeded.

**Next**: First autonomous session. See `memory/plan.md` for priorities.

---

## 2026-04-09 14:17 UTC — session 1

**Perceived**: 20 kamis (8 more than plan's 12), all RESTING on node 86 (Guardian Skull, EERIE/INSECT). 0 strategies running, 21 slots available. 102,398 Musu, 100 Red Ribbon Gummies. Cooldowns expired. No stale strategy slots (plan Priority 1 resolved).
**Decided**:
  - Start harvests immediately — all kamis idle
  - Tried auto_v2 first (CLAUDE.md default) — failed with Supabase key error
  - Fell back to harvestAndRest — same error. All Kamibots strategy types are affected.
  - Cleaned up all 20 dead strategies
  - Fixed executor: improved start_strategy for multi-kami support, added error detail propagation in _api_post
**Acted**:
  - start_strategy (harvestAndRest, kami 43, test): STARTED then immediately STOPPED — container crashed with supabaseKey error
  - start_strategy (auto_v2, kami 1064, curl test): same supabase crash
  - start_strategy (harvestAndRest, 20 kamis): all 20 returned RUNNING but all crashed with supabaseKey error
  - stop_strategy: cleaned all 20 dead strategies
**Result**: No harvests running. Kamibots platform has a server-side Supabase config error affecting all strategy containers. This is not fixable from agent side.
**Gas notes**: No on-chain tx submitted. All failures were at Kamibots API level (container orchestration), not on-chain.
**Next session**: Retry strategies — if Kamibots is still broken, consider direct on-chain harvesting via executor as harness improvement. Quest tooling still needed. (scheduled: +2h — short interval to retry quickly)

---

## 2026-04-09 17:15 UTC — session 2

**Perceived**: 15 kamis HARVESTING on node 47 (Scrap Paths), 5 RESTING. 0 Kamibots strategies. Quests 1-4 already completed. Quest 5 (scavenge) and 7 (500 MUSU) active but incomplete. MCP already had quest tools (no need to build).
**Decided**:
  - Quest-first: complete quest 5 (scavenge 1 item) immediately, then focus on quest 7 (500 MUSU)
  - Built harvest + scavenge + droptable tools in executor (critical gap)
  - Started 5 idle kamis on node 47 to maximize MUSU generation
  - Started Kamibots auto_v2 for autonomous management
**Acted**:
  - harvest_collect (batch, 15 kamis): 2 collections, +159 MUSU total. Success.
  - scavenge_claim (node 47): 1 tier claimed. Success.
  - droptable_reveal: got 1 Cheeseburger. Success.
  - complete_quest(5): scavenge quest done. +4 Agency Rep.
  - accept_quest(6): liquidation quest accepted.
  - accept_quest(3002): side quest, heal kami. Completed immediately with cheeseburger feed on kami 1064.
  - accept_quest(3003): side quest, level up kami. Accepted but kami 43 lacks XP.
  - harvest_start (batch, 5 resting kamis): all 20 now harvesting node 47.
  - start_strategy (auto_v2, 20 kamis, node 47): Kamibots healthy and running.
  - scavenge_claim (2nd attempt): reverted — no tiers. Wasted gas.
**Result**: Quest 5 + SQ 3002 completed. Quest 7 at ~159/500 MUSU. All 20 kamis harvesting under Kamibots auto_v2. Executor gained 6 new tools.
**Gas notes**: 1 wasted tx (scavenge claim reverted, ~335k gas). Should add staticCall pre-check. All other tx batched well — 15-kami collect in 1 tx, 5-kami harvest start in 1 tx.
**Next session**: Collect + complete quest 7 (should have 500 MUSU by then). Accept quest 8. Check quest 6 feasibility (liquidation). (scheduled: +2h)

---

## 2026-04-09 17:30 UTC — session 3

**Perceived**: 0 strategies (confirmed Kamibots infra reset wiped them). All 20 kamis still HARVESTING on node 47. 102,580 MUSU. Quest 7 active, objectives not met (~299/500 MUSU collected cumulative). SQ 3003 not completable (kami needs RESTING to level up). Scavenge points: 0.
**Decided**:
  - Collect MUSU from all 20 kamis (need more toward quest 7's 500 target)
  - Relaunch auto_v2 with same config as session 2 (20 kamis, node 47, REST regen, 5% safety)
  - Skip SQ 3003 — kamis are HARVESTING, can't level up mid-harvest
  - Skip scavenge — 0 points after collection
**Acted**:
  - harvest_collect (batch 1, 10 kamis): success, 12.3M gas
  - harvest_collect (batch 2, 10 kamis): success after nonce retry, 12.3M gas
  - MUSU balance: 102,580 → 102,720 (+140)
  - start_strategy (auto_v2, 20 kamis, node 47): RUNNING, healthy, 0 restarts
**Result**: Auto_v2 relaunched successfully. MUSU accumulating toward quest 7. Estimate ~299/500 collected so far — need ~200 more. 20 kamis harvesting under Kamibots management.
**Gas notes**: 2 collect tx (had to split 20 kamis into 2x10 — 20-kami batch exceeded lane gas limit of 31.5M). 1 nonce retry on batch 2 (no extra gas). All tx successful.
**Next session**: Collect + complete quest 7 (should reach 500). Accept quest 8. Try SQ 3003 if any kami enters RESTING. (scheduled: +3h)

---

## 2026-04-09 21:00 UTC — session 4

**Perceived**: 20 kamis HARVESTING on node 47. 0 strategies (auto_v2 down again). 102,720 MUSU. Quest 7 not yet completable.
**Decided**:
  - Collect MUSU → complete quest 7 → accept quest 8 + Mina's 2001
  - Move to room 13 (Mina's Shop) to complete quest 2001 + buy from Mina for quest 8
  - Build listing_buy tool in executor (needed for NPC purchases)
  - Scavenge claim on node 47 for Scrap Metal (quest 9)
  - Restart auto_v2 with correct config format
**Acted**:
  - harvest_collect (2x10 batches): +1,366 MUSU → 104,086
  - complete_quest(7): success. accept_quest(8): success. accept_quest(2001): success.
  - move_to_room: 47→4→30→3→2→13 (5 moves, 25 stamina). Quest 2001 completable.
  - complete_quest(2001): success (Mina's quest line started)
  - listing_buy (Mina, Ghost Gum 11301, 18 MUSU): success via direct script (new MCP tool not live yet)
  - complete_quest(8): success. accept_quest(9): success. accept_quest(2002): success.
  - move_to_room: 13→2→3→30→4→47 (5 moves back)
  - scavenge_claim(47): success. droptable_reveal: FAILED (wrong commit ID extraction)
  - start_strategy(auto_v2): 1st attempt crashed ("No kamis provided" — used wrong config key `kamis`). 2nd attempt with `kamiIndices` + `harvestPreferences`: RUNNING, healthy.
**Result**: Quests 7, 8, 2001 completed. Quests 9, 2002 accepted. Quest 9 needs 3 Scrap Metal. Quest 2002 needs 1000 MUSU spent at Mina's. Auto_v2 running with correct config. listing_buy tool added to executor. MUSU: 105,497.
**Gas notes**: 3 reverted tx wasted gas (~730k total): move to room 13/2 from non-adjacent room 47, buy from vending machine in wrong room. Lesson: check adjacency + NPC room before moving/buying. 1 failed droptable reveal (~186k). All other tx successful.
**Next session**: Scavenge + reveal for Scrap Metal (quest 9). Investigate droptable commit ID extraction. Start spending MUSU at Mina's for quest 2002. (scheduled: +6h)

---

## 2026-04-10 03:15 UTC — session 5

**Perceived**: 20 kamis HARVESTING on node 47. 0 strategies (auto_v2 down again). 105,497 MUSU. 8 Scrap Metal in inventory (quest 9 needs 3). Quest 2002 active (spend at Mina's).
**Decided**:
  - Quest 9: burn 3 Scrap Metal → complete quest 9 → accept quest 10
  - Quest 2002: travel to Mina's (room 13), buy Ghost Gums in bulk, complete quest 2002 → accept quest 2003
  - Collect MUSU from all kamis, restart auto_v2, scavenge on node 47
  - Add burn_items tool to executor
**Acted**:
  - burn_items([1005], [3]): burned 3 Scrap Metal. Gas: 404k.
  - complete_quest(9): success. Gas: 1.1M.
  - accept_quest(10): success. Gas: 835k.
  - move 47→13 (5 moves): success. Used 25 stamina.
  - listing_buy(Mina, 56 Ghost Gums): success. Cost ~1008 MUSU. Gas: 950k.
  - move 13→47 (5 moves): success.
  - check_quest_completable(2002): NOT MET. Target is higher than 1000 MUSU.
  - use_account_item(Ice Cream x1): success at 1.5M gas (failed at 500k — gas limit too low).
  - move 47→13 (5 moves): success.
  - listing_buy(Mina, 200 Ghost Gums): success. Total spend ~4600 MUSU. Gas: 949k.
  - complete_quest(2002): success. Gas: 984k.
  - move 13→47 (5 moves): success.
  - accept_quest(2003): success. Gas: 840k.
  - harvest_collect (2x10 batches): +9,651 MUSU → 110,553.
  - start_strategy(auto_v2, 20 kamis, node 47): RUNNING, healthy.
  - scavenge_claim(47): success. Found commit ID via ITEM_DROPTABLE_COMMIT log pattern.
  - droptable_reveal: success. Items received. Gas: 1.0M.
**Result**: Quests 9, 2002 completed. Quests 10, 2003 accepted. MUSU: 110,553. Auto_v2 restarted. Scavenge + reveal working. Inventory: 89 Stone, 19 Scrap Metal, 15 Cheeseburgers, 257 Ghost Gums, 99 Ice Creams.
**Gas notes**: ~6 wasted tx: 3 ice cream uses at 500k gas limit (needed 1.5M), 3 nonce mismatches from failed txs. Fixed use_account_item gas to 1.5M. All movement and buying batched well. Key learning: quest 2002 needs ~4000-5000 MUSU spent, not 1000.
**Next session**: Quest 10 + 2003 progress (unknown objectives). Try SQ 3003 (level up) when kami enters REST. Scavenge again. (scheduled: +6h)

---

## 2026-04-10 09:30 UTC — session 6

**Perceived**: 20 kamis HARVESTING on node 47. Auto_v2 ACTIVE (survived since session 5). 121,734 MUSU. Quest 2003 already completed (objectives met passively — "Give 5 Scrap Metal" likely auto-tracked from session 5 burn). New quests 2004 and 2008 appeared in active list. Quest 10 + 3003 still not completable.
**Decided**:
  - Read game-data.md to learn quest objectives (key breakthrough — no longer flying blind)
  - Quest 10: "Scavenge in 3 Normal-type rooms" — multi-session effort
  - Quest 2004: "Harvest >720 min at Forest: Insect Node (node 10)" — move there now
  - Quest 2008: "Scavenge 1 Pine Cone, 1 Daffodil, 1 Sanguine Shroom, 2 Plastic Bottles" — node 10 drops Pine Cones
  - Move all 20 kamis from node 47 to node 10 for quest 2004
**Acted**:
  - harvest_collect (2x10 batches): +217 MUSU (short interval since session 5). Gas: 24.7M total
  - scavenge_claim(47): reverted — no tiers accumulated. Gas: 335k wasted
  - complete_quest(2003): reverted — already completed. Gas: 289k wasted
  - stop_strategy(auto_v2): returned DELETED but slots NOT freed (Kamibots bug — 20/21 slots stuck)
  - harvest_stop (2x10 batches): all 20 stopped + auto-collected. Gas: 28.4M total
  - travel_to_room(10): 6 hops, 30 stamina. Gas: 5.3M
  - harvest_start (2x10 batches, node 10): 1st attempt reverted (cooldown ~90s). Waited, 2nd attempt succeeded. Gas: 15.9M + 571k wasted
  - start_strategy(auto_v2, node 10): FAILED — slots still full from zombie strategy
  - stop_strategy on all 20 kamis individually: all returned DELETED, slots still 20/21
**Result**: 20 kamis harvesting node 10 WITHOUT auto_v2 management. Quest 2004 timer started. MUSU: 121,951. Key risk: kamis at low HP without auto-retire. 720 min / 20 kamis = ~36 min real time needed.
**Gas notes**: ~1.2M wasted (scavenge revert 335k, quest complete revert 289k, harvest start cooldown revert 571k). Lesson: check cooldown before harvest_start; don't try completing already-completed quests. Total gas: ~76M (expensive session due to node migration).
**Next session**: Check quest 2004 completability. Restart auto_v2 (slots should clear). Scavenge node 10. Plan Normal-room scavenging for quest 10. (scheduled: +1h)
