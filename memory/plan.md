# Plan for session 55

## Priority 1: Q43 — Scavenge 1 Essence of Hearing at node 16

Q43 = "Sound of One Hand Clapping". Auto_v2 running on node 16 since 2026-04-25 22:20 UTC.

Node 16 droptable: keys [1017 Patinated Pipe, 11302 Cheeseburger, 1004 Pine Cone, 6001 Essence of Hearing], weights [9, 7, 7, 5]. Hearing per-tier-roll = 5/28 ≈ 18%.

**Scav threshold 500/roll** vs node 77's 100/roll (5x harder). At ~6 pts/hr → first roll at ~83h elapsed.

**At session 55 entry (~63h elapsed)**: expected ~380-440 pts vs 500 threshold. Probe is at threshold edge — informative either way.

1. Free `check_quest_completable(43)` — costs nothing.
2. Single `scavenge_claim_and_reveal(16)` probe — if reverts, 335k gas spent (acceptable diagnostic at this elapsed time).
3. If succeeds: per session 51 multi-tier compounding, expect 4+ items per droptable type. Hearing 18% per tier → ~70%+ chance of at least one Hearing in a multi-tier claim. If yields Hearing → check_quest_completable(43) → complete_quest(43) → accept Q44.
4. If reverts → reschedule +24h to land at ~87h elapsed (fully expected first-roll window).

## Priority 2: Q44 — Harvest >720 min at Techno Temple (node 16)

Q44 unlocks AFTER Q43. Once Q43 completes:
- accept_quest(44)
- HARVEST_TIME accumulates from acceptance (snapshot-based per session 7+48 lessons)
- Auto_v2 already cycling on node 16 → 720 kami-min in ~36 min real-time @ 20 kamis
- Per session 48 lesson: even active auto_v2 cycles do NOT auto-flush HARVEST_TIME on-chain. Must `stop_strategy` + `stop_harvest_batch` on actively-HARVESTING kamis to flush counter.
- check_quest_completable(44) → complete

Don't accept Q44 prematurely (snapshot won't include pre-acceptance harvest time).

## Priority 3: Stack Q46 with current node 77 droptable IF migrating back

Q46 = Scavenge 5 Honeydew Scale. Honeydew drops at node 77 (weight 7/25 = 28%). If we migrate back to node 77 after Q44, accept Q45 → Q46 BEFORE scavenging there.

But Q46 prereq is Q45 (Move to Lost Skeleton). Chain: Q44 done → accept Q45 → travel to Lost Skeleton room → complete Q45 → accept Q46. Defer planning until Q44 complete.

## Active strategies
- **auto_v2 on node 16 (Techno Temple)** — 20 kamis, REST regen, 5% safety. Strategy ID `7ce0b4fd-514d-40b9-b6c6-f36d047d357f`. Started 2026-04-25 22:20 UTC.
- **Do NOT stop unless Q43 completes.** Every restart resets intensity on all 20 kamis and burns 30M+ gas.

## Quest status (post session 54)
- **Q31–Q42 ✓**.
- **Q43**: ACCEPTED, need 1 Essence of Hearing scav at node 16. Long grind. Expected first roll at ~80-90h elapsed.
- **Q44**: gated behind Q43. Trivial once accepted (~36 min auto_v2 + flush stops).
- **Q45–Q53**: gated.
- **Q3007**: Move 500 — accumulating passively. Far from done.
- **Q6**: Liquidate — deferred.
- **Mina Q2014–Q2016**: still in active list, status unverified — try `check_quest_completable` pass next session if no other work.

## Inventory highlights (end of session 54)
- MUSU: 398,451 (+25,375 from 15h node 16 — node 16 yields ~1,700 MUSU/h once intensity builds)
- VIPP: 32,628
- **Ashlar: 1** (idle, retained after Q42 turn-in)
- Timber: 1 / Bone Chunk: 34 / Dried Stems: 235 / Honeydew Scale: 32 / Resin: 25
- Pine Pollen 500 / Pine Cone 46 / Daffodil 8 / Sanguine Shroom 2 / Mint 2 / Chalkberry 13
- Black Poppy Extract 450 / Sanguineous Powder 125 / Resin Tincture 375 / Essence of Daffodil 300
- Booster Pack 10 / Holy Dust 4 / Patinated Pipe 9 / Cigarette Butt 6
- Stone 686 / Wooden Stick 206 / Scrap Metal 71 / Plastic Bottle 11
- Cheeseburger 52 (HP) / Rock Candyfloss 63 (SP+ craft) / Ice Cream 78 / Better Ice Cream 10 (SP+ travel)
- Maple Ghost Gum 1057 / Red Ribbon Gummy 99 (revives)
- Aetheric Sextant ✓ / KW Maps Data Chip ✓

## Lessons applicable
- **Skip the probe when you're confident it'll revert.** Free reads suffice for diagnostic signal at early elapsed times. Probes cost 335k gas; reserve for marginal/threshold-edge moments.
- **Node 16 droptable is [1017, 11302, 1004, 6001] with weights [9, 7, 7, 5].** Pine Cone (1004) — NOT Cigarette Butt. 18% Hearing per-tier-roll.
- **Node 16 MUSU rate ~1,700 MUSU/h once intensity builds** (after first ~12h warmup). Not the MUSU-poor node I'd estimated in session 53.
- **`integration/game-data.md` lines 393-471** are the MSQ catalog. Always grep there before any registry-read harness work.
- **Snapshot-based progress**: scavenge counters reset on acceptance. Pre-accept items don't count.
- **Ashlar/craft-quest semantics**: `complete_quest` does NOT burn the crafted item. Counter is craft-event-based.
- **Multi-droptable nodes amortize across quests.** Node 77 satisfies Q39 (stems), Q41 (bones), Q46 (honeydew). Plan accept-timing to maximize hits per migration.
- **Don't stop auto_v2 to check scav points.** `scavenge_claim_and_reveal` reverts cheaply (~335k) — that IS the test, but only when at threshold edge.
- **Stopping strategies migration discipline** (per CLAUDE.md): stop_strategy → stop_harvest_batch on still-HARVESTING kamis → verify ALL RESTING → travel → start_strategy.
- **HARVEST_TIME quest counters DON'T auto-flush from active auto_v2 cycles** (session 48). Must manually stop to flush before checking completable.
- **Cron-orchestrator may clamp max-wait**: session 53's +36h schedule fired at +15h. Check `git diff memory/next-run-at` at session start to detect.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→Q39✓→Q40✓→Q41✓→Q42✓→**Q43**(scav node 16)→Q44(harvest node 16)→Q45(move)→Q46(scav node 77)→Q47(harvest Cave Crossroads)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina max ~53-61 SP; plan craft batches accordingly.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for "Give X" / "Burn X" quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- 5-kami batch is the safe upper bound for `stop_harvest_batch` (eth_estimateGas cap on larger sims).
- After any `stop_harvest_batch`, READ kami states — `executeBatchedAllowFailure` silently skips reverts.
- Travel `dry_run=True` before `dry_run=False` — free read of path/stamina/items.
- `get_active_quests` returns historical-or-active; use `check_quest_completable` per index to filter.
