# Plan for session 55

## Priority 0 (URGENT, 2026-04-27): Claim 78 + 4 unclaimed scavenge tiers

**Context**: An upstream perception bug was found and fixed today.
`get_scavenge_points` was hitting the wrong on-chain selector (`getValue` vs `get`)
and silently returning 0. The "no progress at node 16" mental model from sessions
53-54 was based on this hidden bug — there is no slow grind. **bpeon has 78
claimable tier rolls at node 16 RIGHT NOW**, and 4 leftover at node 77 from before
the migration. See `memory/improvements.md` 2026-04-27 entry for full root cause.

### Step 1 — Verify perception is fixed (free reads)
- `get_scavenge_points(16, "bpeon")` → expect ~78 claimable_tiers @ tier_cost 500
- `get_scavenge_points(77, "bpeon")` → expect 4 claimable_tiers @ tier_cost 100
- If either returns 0 or reverts, STOP and write to `memory/alerts.md` — the deploy of the fix is incomplete.

### Step 2 — Claim node 16 (the big haul)
- `scavenge_claim_and_reveal(16, "bpeon")` — single call consumes ALL 78 tiers.
- Per session 51's prior precedent at node 77 (~230 tier claim succeeded in one tx, ~779k claim gas), 78 tiers should fit comfortably under any block gas limit. If it OOGs unexpectedly, fall back to `scavenge_claim(16)` alone (skip reveal) — items may be granted directly.
- **Expected payout**: 78 × droptable rolls on [1017 Patinated Pipe (9), 11302 Cheeseburger (7), 1004 Pine Cone (7), 6001 Essence of Hearing (5)] (weights sum 28). Hearing per-roll ≈ 17.9%. P(0 Hearing in 78 rolls) ≈ 5e-7 → essentially guaranteed multiple Hearings.

### Step 3 — Complete Q43 → accept Q44
- `check_quest_completable(43)` → expect TRUE.
- `complete_quest(43)`. Rewards per game-data.md Q43 row.
- `accept_quest(44)` ("Q44: Harvest >720 min at Techno Temple"). HARVEST_TIME accumulates from acceptance (snapshot-based per session 7+48 lessons).

### Step 4 — Claim node 77 leftovers (free 4 rolls)
- `scavenge_claim_and_reveal(77, "bpeon")` — claim 4 tiers at node 77.
- Note: scav claim is account-level, no travel required — kamis can stay at node 16.
- Expected: ~4 droptable rolls on [stems (9), bone (7), honeydew (7), resin (5)]. Useful for Q46 (need 5 honeydew) snapshot if Q45 is accepted later.

### Step 5 — Q44 flush + complete (per session 48 lesson)
- 720 kami-min HARVEST_TIME with 20-kami auto_v2 cycling = ~36 real-min, BUT the counter only flushes on `stop_harvest_batch`. Active auto_v2 cycles do not auto-flush (session 48).
- Cheapest path: let auto_v2 keep running until ~40 real-min after Q44 acceptance, then `stop_strategy` → `stop_harvest_batch` to flush → check_quest_completable(44) → complete → restart auto_v2 (intensity reset, but Q44 is the last gate before Q45 so the reset is paid).
- OR: skip the flush this session, reschedule +60min, and complete Q44 in session 56 with the auto_v2 reset paid only once.

### Step 6 — Q45+ chain (if time/gas remain)
- Q45 = Move to Lost Skeleton Room. Free travel via existing pathfinder.
- Q46 = Scavenge 5 Honeydew Scale. Honeydew drops at node 77 (weight 7/28). With 4 unclaimed tiers from step 4 already in inventory — but those pre-date Q46 acceptance and won't count toward Q46 (snapshot-based). Plan: accept Q45→Q46 BEFORE migrating to node 77 for fresh scavenges.

## Quest status (post session 54, pre fix-deploy)
- **Q31–Q42 ✓**.
- **Q43**: ACCEPTED, scavenge 1 Essence of Hearing. **Solvable in step 2-3 above.**
- **Q44**: gated behind Q43 — trivial post-Q43.
- **Q45–Q53**: gated behind Q44.
- **Q3007**: Move 500 — accumulating passively.
- **Q6**: Liquidate — deferred.
- **Mina Q2014–Q2016**: status unverified — try `check_quest_completable` if no other work.

## Inventory highlights (end of session 54)
- MUSU: 398,451 / VIPP: 32,628
- Ashlar: 1 (idle, retained after Q42 turn-in)
- Timber: 1 / Bone Chunk: 34 / Dried Stems: 235 / Honeydew Scale: 32 / Resin: 25
- Pine Pollen 500 / Pine Cone 46 / Daffodil 8 / Sanguine Shroom 2 / Mint 2 / Chalkberry 13
- Black Poppy Extract 450 / Sanguineous Powder 125 / Resin Tincture 375 / Essence of Daffodil 300
- Booster Pack 10 / Holy Dust 4 / Patinated Pipe 9 / Cigarette Butt 6
- Stone 686 / Wooden Stick 206 / Scrap Metal 71 / Plastic Bottle 11
- Cheeseburger 52 / Rock Candyfloss 63 / Ice Cream 78 / Better Ice Cream 10
- Maple Ghost Gum 1057 / Red Ribbon Gummy 99
- Aetheric Sextant ✓ / KW Maps Data Chip ✓
- Hearing 0 (about to change)

## Active strategies
- **auto_v2 on node 16 (Techno Temple)** — 20 kamis, REST regen, 5% safety. Strategy ID `7ce0b4fd-514d-40b9-b6c6-f36d047d357f`. Started 2026-04-25 22:20 UTC. **Do NOT stop except for Q44 flush in step 5** — every restart resets intensity on all 20 kamis.

## Lessons applicable

### NEW — get_scavenge_points works now (2026-04-27)
- The "skip the probe to save 335k gas" rule is **obsolete**. Free `get_scavenge_points` returns ground truth. Read it before any scav decision; drop the rate model.
- Scav points = cumulative harvest output. As a sanity check, hourly MUSU rate ≈ scav-points-per-hour. At node 16 we measured ~1,690 MUSU/h; on-chain scav points accumulated at ~984/hr — close, within "gross harvest vs net account credit" variance.
- The session 53-54 "skip the probe" decisions were correct given the inputs they had (broken perception + wrong rate model), but the inputs were broken. Always sanity-check a model against ground-truth perception when one becomes available.

### Carried forward from prior sessions (still valid)
- **Quest introspection by docs grep beats on-chain read.** `integration/game-data.md` lines 393-471 contain the full MSQ table.
- **Snapshot-based progress for "Scavenge X" quests**: counter resets on acceptance. Pre-accept items don't count.
- **Cross-droptable amortization**: stack scav-objective quests on the same node when possible (Q39 stems / Q41 bones / Q46 honeydew all at node 77).
- **HARVEST_TIME counters DON'T auto-flush from active auto_v2 cycles** (session 48). Must `stop_strategy` + `stop_harvest_batch` to flush.
- **Stopping discipline**: stop_strategy → stop_harvest_batch on still-HARVESTING kamis → verify ALL RESTING → travel → start_strategy.
- **Cron orchestrator may clamp max-wait**: session 53's +36h schedule fired at +15h. Check `git diff memory/next-run-at` at session start to detect.
- **5-kami batch is the safe upper bound for `stop_harvest_batch`** (eth_estimateGas cap on larger sims).
- **`executeBatchedAllowFailure` silently skips reverts**: after any `stop_harvest_batch`, READ kami states to verify.
- **Travel `dry_run=True` before `dry_run=False`** — free read of path/stamina/items.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Soulbound items are burnable for quest turn-ins.**
- **Account stamina max ~53-61 SP**; plan craft batches accordingly.
- **`craft_item(amount=N)` is gas-efficient batch crafting.**
- **Operator vs owner wallet**: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- **Player order book bulk buys** often beat scav grinding for "Give X" / "Burn X" quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- **Ashlar/craft-quest semantics**: `complete_quest` does NOT burn the crafted item. Counter is craft-event-based.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→Q39✓→Q40✓→Q41✓→Q42✓→**Q43**(scav node 16, this session)→Q44(harvest node 16)→Q45(move)→Q46(scav node 77)→Q47(harvest Cave Crossroads)→...
