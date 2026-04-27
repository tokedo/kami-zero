# Plan for session 56

## Priority 0: Q44 flush + Q45 + start Q46 grind (~+90min from session 55)

**Context**: Session 55 unblocked the Q43 → Q44 chain after the perception fix landed.
Q43 ✓, Q44 accepted at 2026-04-27 15:18 UTC. Auto_v2 still running on node 16.
The HARVEST_TIME counter for Q44 only counts post-acceptance, only flushes on stop_harvest.
At +90min into Q44 acceptance, expect >1,000 kami-min accumulated (need 720).

### Step 1 — Pre-flush state check (free reads)
- `check_quest_completable(44)` → expect FALSE (counter only flushes on stop). If TRUE, skip steps 2-4 and go straight to complete.
- `get_all_strategies` → confirm auto_v2 still ACTIVE on node 16 strategy `7ce0b4fd-514d-40b9-b6c6-f36d047d357f`.

### Step 2 — Tear down auto_v2 + flush all 20 harvests
- `stop_strategy(43, permanent=True)` (kami_indices[0] = 43, multi-kami strategies use the primary index).
- `get_account_kamis` to enumerate still-HARVESTING kamis.
- `stop_harvest_batch` in ≤5-kami chunks (eth_estimateGas cap on larger sims). Verify each batch by reading state — `executeBatchedAllowFailure` silently skips reverts.
- Repeat until ALL 20 kamis confirmed RESTING. **Migration verify-end-state rule applies (af1cde4 commit).**

### Step 3 — Q44 → Q45 → Q46 chain
- `check_quest_completable(44)` → expect TRUE after flush.
- `complete_quest(44)`. Rewards: 4× Elders Loyalty, 1× Unmarked Data Chip.
- `accept_quest(45)` ("Can't Stop With Just One" — Move to Lost Skeleton).

### Step 4 — Travel to Lost Skeleton (room 25)
- `travel_to_room(25, dry_run=True)` — read path/stamina cost. From session 9 historical data, room 25 is 5-6 hops from current room.
- Account stamina max ~53-61. After ~36h auto_v2 idle on travel, stamina should be near max.
- Execute travel, then `complete_quest(45)`. Rewards: 2× Agency Rep, 2× Booster Pack.

### Step 5 — Accept Q46 + migrate to node 77
- `accept_quest(46)` ("Sweet As Honey" — Scavenge 5 Honeydew Scale).
- **Snapshot-based**: existing 32 Honeydew Scales DON'T count. Need 5 fresh post-Q46-accept scavenges from node 77's droptable.
- `travel_to_room(77, dry_run=True)` from room 25 — likely 5-7 hops.
- May need to use SP+ items from inventory (Ice Cream 78, Better Ice Cream 10, Rock Candyfloss 63 — plenty of stamina restoratives). `travel_to_room` auto-uses these if needed.
- Once at room 77: `get_kami_state_slim(43)` to verify position, then `start_strategy(auto_v2, kami_id=43, node_id=77, all 20 kamis, REST regen, 5% safety)`.

### Step 6 — Q46 economics
- Node 77 droptable: [stems 9 / bone 7 / honeydew 7 / resin 5] sum 28. Honeydew per-roll = 25%.
- Need 5 Honeydew. Expected tier rolls: 5/0.25 = 20 tiers (with variance). At 100 pts/tier = 2,000 scav points needed.
- Node 77 historic rate: ~990 MUSU/h ≈ ~990 scav-pts/hr at 20 kamis (per the new rate model: scav points ≈ harvest output). 2,000 / 990 ≈ 2h. Plus per-tier rng variance — budget 3-5h elapsed before next probe.
- Reschedule next session +4h after Q46 acceptance.

### Step 7 — Optional: harness fix for misleading "claim failed" status
- `scavenge_claim_and_reveal` returns `"error": "claim failed"` when the **reveal** reverts but the **claim** itself succeeded (items granted by claim). Session 55 hit this at node 16 — the response said `"reverted"` but inventory delta confirmed 78-tier success.
- Fix: in the executor, after the wrapper's tx receipts come back, check whether the claim sub-tx logged ItemDroptableCommit (success signal) before deciding error string. Distinguish:
  - claim reverted → "claim failed" (current behavior, correct)
  - claim succeeded + reveal reverted → "items granted by claim, reveal not needed" (current path for some nodes returns this; broken path returns "claim failed")
- Low-priority but fixes a footgun. Defer if time-pressed.

## Quest status (post session 55)
- **Q31–Q43 ✓**.
- **Q44**: ACCEPTED 2026-04-27 15:18 UTC. Counter accumulating since.
- **Q45**: gated behind Q44, location-only.
- **Q46**: gated behind Q45, scav 5 Honeydew at node 77 (post-acceptance).
- **Q47**: Harvest 720 min at Cave Crossroads — different node from 77, will need migration.
- **Q3007**: Move 500 — accumulating passively.
- **Q6**: Liquidate — deferred.
- **Mina Q2014–Q2016**: ALL completed (verified session 55).

## Inventory highlights (end of session 55)
- MUSU: 412,444 / VIPP: 32,628
- **Essence of Hearing 2 (NEW)** — Q43 turn-in path.
- Patinated Pipe 65 / Cigarette Butt 6 / Cheeseburger 59 / Pine Cone 59
- Ashlar 1 / Timber 1 / Bone Chunk 37 / Dried Stems 236 / Honeydew Scale 32 / Resin 25
- Pine Pollen 500 / Daffodil 8 / Sanguine Shroom 2 / Mint 2 / Chalkberry 13
- Black Poppy Extract 450 / Sanguineous Powder 125 / Resin Tincture 375 / Essence of Daffodil 300
- Booster Pack 10 / Holy Dust 4 / Stone 686 / Wooden Stick 206 / Scrap Metal 71 / Plastic Bottle 11
- Ice Cream 78 / Better Ice Cream 10 / Rock Candyfloss 63 (stamina restoratives)
- Maple Ghost Gum 1057 / Red Ribbon Gummy 99
- Aetheric Sextant ✓ / KW Maps Data Chip ✓

## Active strategies
- **auto_v2 on node 16 (Techno Temple)** — 20 kamis, REST regen, 5% safety. Strategy ID `7ce0b4fd-514d-40b9-b6c6-f36d047d357f`. Started 2026-04-25 22:20 UTC.
- **Will be torn down in session 56** to flush Q44 counter; then migrated to node 77 for Q46.

## Lessons applicable

### NEW — `scavenge_claim_and_reveal` response can mislead
- When the **claim** sub-tx succeeds but **reveal** reverts (because items were granted directly by the claim itself, e.g. node 16 path), the wrapper returns `"status": "reverted"` and `"error": "claim failed"`. **This is wrong — items DID arrive.** Always verify by inventory delta + `get_scavenge_points` (point drop = successful consumption).
- The session 21 fix (commit 493681a) was supposed to handle this with `reveal_skipped: "..."` messaging. Session 55's node 16 hit a different code path that didn't return that field. Harness needs another pass.

### Carried forward (still valid)
- **`get_scavenge_points` is now reliable** (commit a0c190b + f2966bd). Use it as ground truth before any scav decision. Drop the rate model from sessions 49-54.
- **Quest introspection by docs grep beats on-chain read** — `integration/game-data.md` Q1-Q53 explicit. Always grep first.
- **Snapshot-based progress for "Scavenge X" quests** — counter resets on acceptance. Pre-accept items don't count.
- **HARVEST_TIME counter only flushes on stop_harvest** (session 48). Active auto_v2 cycles do NOT auto-flush.
- **Migration verify-end-state**: `stop_strategy` does NOT halt in-flight harvests. After stop, READ kami states; `stop_harvest_batch` any still-HARVESTING; verify ALL RESTING before `start_strategy` at new node. Otherwise gas waste from operator retries.
- **`stop_harvest_batch` 5-kami safe upper bound** (eth_estimateGas cap).
- **`executeBatchedAllowFailure` silently skips reverts** — always read state after batch.
- **Travel `dry_run=True` first** — free read of path + stamina + items.
- **Account stamina max ~53-61 SP** — top off via Ice Cream / Better Ice Cream if path needs more.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Cross-droptable amortization**: stack scav-objective quests on the same node when possible (Q46 honeydew + Q49+ stems/bones at node 77).
- **Operator vs owner wallet**: trade.execute = owner; listing_buy/burn/craft/scav_claim = operator; auction_buy = owner.
- **Cron forced-fire**: orchestrator can override `next-run-at` to fire immediately. Don't rely on long delays staying long.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→...→Q42✓→Q43✓→**Q44(this session 55+, flush in session 56)**→Q45(move room 25)→Q46(scav node 77 honeydew)→Q47(harvest Cave Crossroads, new node)→Q48+...
