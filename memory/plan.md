# Plan for session 53

## Priority 1: Q43 — Scavenge 1 Essence of Hearing at node 16

Q43 = "Sound of One Hand Clapping" — Scavenge 1 Essence of Hearing. Only drops at node 16 (Techno Temple, droptable: Pipe/Burger/Cone/Hearing weights 9/7/7/5). Hearing per-tier-roll probability ~5/28 ≈ 18%.

Scav threshold at node 16 is **500 pts/roll** (vs node 77's 100/roll, 5x harder). At ~10 pts/hr w/ 20 kamis, expect first roll ~50h elapsed. Auto_v2 started 2026-04-25 22:20 UTC.

Approach:
1. **Free probe** `check_quest_completable(43)` first — costs nothing.
2. If false, single `scavenge_claim_and_reveal(16)` probe — if reverts ("no pts"), 335k gas wasted; reschedule longer. Don't double-roll.
3. If succeeds without yielding Hearing (per Theory: 18% per tier, multi-tier compounds), keep auto_v2 running and probe again next cycle.

## Priority 2: Q44 — Harvest >720 min at Techno Temple (node 16)

Q44 unlocks AFTER Q43. Once Q43 completes:
- accept_quest(44)
- HARVEST_TIME accumulates from acceptance (snapshot-based)
- Auto_v2 already cycling on node 16 → 720 kami-min in ~36 min real-time @ 20 kamis
- stop_strategy + stop_harvest_batch to flush HARVEST_TIME → check_quest_completable(44) → complete

Don't accept Q44 prematurely (snapshot won't include pre-acceptance harvest time per session 48 lessons).

## Priority 3: Stack Q46 with current node 77 droptable IF migrating back

Q46 = Scavenge 5 Honeydew Scale. Honeydew drops at node 77 (weight 7/25 = 28%). If we ever migrate back to node 77 between Q44 and Q47, accept Q46 BEFORE scavenging there.

But Q46 prereq is Q45 (Move to Lost Skeleton) which is Q44 prereq → Q45 → Q46. So Q46 chain: Q44 done → accept Q45 → move to Lost Skeleton (room ~46?) → complete Q45 → accept Q46. This is a separate migration from node 16 — defer planning until Q44 complete.

## Active strategies
- auto_v2 on **node 16 (Techno Temple)** — 20 kamis, REST regen, 5% safety. Strategy ID `7ce0b4fd-514d-40b9-b6c6-f36d047d357f`. Started 2026-04-25 22:20 UTC. **Do NOT stop unless Q43 completes** — node 16 scav points accumulate slowly and any reset wastes 50h of accumulation.

## Quest status (post session 52)
- **Q31–Q42 ✓**.
- **Q43**: ACCEPTED, need 1 Essence of Hearing scav at node 16. Long grind.
- **Q44**: gated behind Q43. Trivial once accepted.
- **Q45–Q53**: gated.
- **Q3007**: Move 500 — accumulating passively. Travel from session 52 added 4 moves (~52 lifetime moves). Far from done.
- **Q6**: Liquidate — deferred.
- Mina line **Q2014–Q2016**: still in active list, status unverified — worth a `check_quest_completable` pass next session.

## Inventory highlights (end of session 52)
- MUSU: ~370,000 (up from 363k pre-session)
- VIPP: 32,628
- BPE: 450
- Dried Stems: **235** (199→235, +36 from scav)
- Bone Chunk: **34** (was 86, +48 from scav, -100 to craft Ashlar)
- Honeydew Scale: **32** (21→32, +11 from scav)
- Resin: 25
- Timber: 1 (kept)
- Ashlar: 0 (consumed by Q42 turn-in via complete_quest — verify next session via inventory read; NOT explicitly burned)
- Pine Pollen: 500 / Pine Cone: 46 / Daffodil: 8
- Black Poppy Extract: 450 / Sanguineous Powder: 125 / Resin Tincture: 375
- Booster Pack: 9-10 (Q41 reward +1)
- Holy Dust: 4 / Cigarette Butt: 6 / Patinated Pipe: 9
- Stone: 686 (backup for recipe 36 Ashlar)
- Wooden Stick: 206 (recipe 34 backup for Timber if needed)
- Cheeseburger: 52 (HP recovery)
- Rock Candyfloss: 63 (SP+ for crafting)
- Ice Cream: 78 / Better Ice Cream: 10 (SP+ travel)

## Lessons applicable
- **`integration/game-data.md` is the quest catalog.** Lines 393-471 cover Q1-Q53 + Mina Q2001-Q2016 with title, prerequisite, objective, rewards. ALWAYS grep this BEFORE building registry-read harness fixes.
- **Snapshot-based progress**: scavenge counters reset on acceptance. Pre-accept items don't count. Plan: accept the quest BEFORE the scav, or accept-then-rescavenge.
- **Q42 turn-in semantics**: `Craft 1 Ashlar` was satisfied by the craft tx itself (no `burn_items` needed). `complete_quest` did NOT explicitly burn the Ashlar — but inventory may show 0 Ashlar after, suggesting craft-counter is event-based, not item-ownership-based. Verify next session.
- **Multi-droptable nodes amortize across quests.** Node 77 satisfies Q39 (stems), Q41 (bones), and could satisfy Q46 (honeydew). Plan accept timings to maximize hits per migration.
- **Node 16 has 5x scav cost vs node 77.** Plan for 2-3x longer between probes. ~50h to first roll @ 20 kamis.
- **Don't stop auto_v2 to check scav points.** `scavenge_claim_and_reveal` reverts cheaply (~335k gas) — that IS the test.
- **Stopping strategies migration discipline** (per CLAUDE.md): stop_strategy → stop_harvest_batch on still-HARVESTING kamis → verify ALL RESTING → travel → start_strategy. Confirmed working session 52.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→Q39✓→Q40✓→Q41✓→Q42✓→**Q43**(scav node 16)→Q44(harvest node 16)→Q45(move)→Q46(scav node 77)→Q47(harvest Cave Crossroads)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina max ~53-61 SP; plan craft batches accordingly.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for "Give X" / "Burn X" quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- 5-kami batch is the safe upper bound for `stop_harvest_batch` (eth_estimateGas cap on larger sims). 4-kami batch session 52 worked fine at 7M gas.
- After any `stop_harvest_batch`, READ kami states — `executeBatchedAllowFailure` silently skips reverts.
- Travel `dry_run=True` before `dry_run=False` — free read of path/stamina/items.
