# Plan for session 57

## Priority 0: Q46 probe + flush (Honeydew Scale ×5 at node 77)

**Context**: Session 56 chained Q44+Q45 ✓, accepted Q46, migrated auto_v2 16→77.
Strategy `98de8cb3-487d-4468-81d5-57f494c510b3` running at node 77 since 2026-04-27 17:04 UTC.
Q46 needs 5 fresh Honeydew Scale scavenges (snapshot baseline = 32 Honeydew at Q46 acceptance).
Honeydew probability = 11.1% per tier (verified via get_scavenge_droptable(77)).

### Step 1 — Free reads (no gas)
- `get_scavenge_points(77, "bpeon")` → expect ~4,000-6,000 pts at +6h, ~40-60 claimable tiers.
- `get_inventory("bpeon")` → record Honeydew Scale baseline (should still be 32).
- `check_quest_completable(46, "bpeon")` → expect FALSE (no claim yet).
- `get_all_strategies` → confirm auto_v2 ACTIVE on node 77.

### Step 2 — Decide: probe vs wait
- If `claimable_tiers >= 30`: probability of getting ≥5 Honeydews from 30 rolls at p=0.111 ≈ 1 - binomial(<5, 30, 0.111) ≈ 25-30%. Marginal. Better to wait if cheaper.
- If `claimable_tiers >= 45`: P(≥5) ≈ 50%. Worth probing.
- If `claimable_tiers >= 60`: P(≥5) ≈ 78%. Strong probe candidate.
- If `claimable_tiers < 30`: skip the probe entirely, reschedule +3h.

### Step 3 — Claim + verify
- `scavenge_claim_and_reveal(77)`. **Beware response misleading**: at node 77, reveal IS the path (not granted-by-claim like nodes 16/35) — should report normal success. But verify via inventory delta + `get_scavenge_points` regardless.
- Compute Honeydew delta vs 32 baseline. Need ≥5 fresh.

### Step 4 — Complete chain (if Honeydew ≥5)
- `check_quest_completable(46)` → TRUE.
- `complete_quest(46)`. Rewards per game-data Q46 row.
- `accept_quest(47)` ("Sliding Down the Drainpipe" — Harvest 720 min at Cave Crossroads, NEW node).

### Step 5 — Q47 prep (deferred to next session if migration heavy)
- Q47 target node = Cave Crossroads. Look up the node index in catalogs/nodes.csv (room ?). Not at room 77.
- Will require auto_v2 teardown + travel + restart at new node. **If session 57 has gas budget, do it inline. If migration is heavy, schedule session 58 to handle it.**
- Note: Q47 is HARVEST_TIME, so same flush pattern as Q44 will apply. Plan ~2-3h post-acceptance harvest before first flush attempt.

### Step 6 — Insufficient Honeydew fallback
- If Honeydew delta < 5 after the claim: scav points are now drained. Auto_v2 keeps grinding new tiers; new claim available in another ~6h.
- Don't burn another claim until points have re-accumulated to ≥30 tiers.
- Schedule next session +6h for re-probe.

## Quest status (post session 56)
- **Q31–Q45 ✓**.
- **Q46**: ACCEPTED 2026-04-27 17:04 UTC. Need 5 fresh Honeydew Scale via scav at node 77. Counter accumulating since.
- **Q47**: gated behind Q46. Harvest 720 min at Cave Crossroads (NEW node, requires migration).
- **Q3007**: Move 500 — accumulated +10 moves this session (4+6 hops).
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 56, deltas from session 55)
- MUSU: 412,444 → unchanged (~0 collected during session, only stop_harvest balance flushes which I didn't sample post-flush)
- VIPP: 32,628
- **Honeydew Scale 32** — baseline for Q46 delta tracking. Pre-Q46 inventory = 32.
- Patinated Pipe 65 / Cigarette Butt 6 / Cheeseburger 59 / Pine Cone 59
- Bone Chunk 37 / Dried Stems 236 / Resin 25
- Essence of Hearing 2 / Ashlar 1 / Timber 1
- Pine Pollen 500 / Sanguineous Powder 125 / Resin Tincture 375 / Black Poppy Extract 450 / Essence of Daffodil 300
- Booster Pack 10 / Holy Dust 4
- Stamina restoratives: Ice Cream 78 / Better Ice Cream 10 / Rock Candyfloss 63 (untouched this session)

## Active strategies
- **auto_v2 on node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety. Strategy ID `98de8cb3-487d-4468-81d5-57f494c510b3`. Started 2026-04-27 17:04 UTC.

## Lessons applicable

### Session 56 confirmations
- **silent-skip detection works in production**: 1 silent-skip caught (kami 13947, chunk 4 of stop_harvest_batch). Per-kami `harvest_state` returns let agent retry surgically. Use this signal religiously after any `*_batch` call.
- **Q44 flush 90 min after acceptance was sufficient** — 19 kamis × ~50% active × 106 min ≈ 1,000 kami-min. The flush threshold (720) clears faster than the +90min reschedule estimated.
- **Travel auto-pathfinding handled both 25 (4 hops) and 77 (6 hops) flawlessly** — no manual path-reasoning, no item inserts needed at 64+ SP starting stamina.

### Carried forward (still valid)
- **Droptable weights are EXPONENTIAL**: prob_i = 2^weight_i / sum(2^weight_j). Use `get_scavenge_droptable(node)` — never compute by hand.
- **`scavenge_claim_and_reveal` response can mislead** at nodes where items are granted by claim (16, 35, possibly others). Node 77 IS the reveal path, so should report normal success — but verify via inventory delta regardless.
- **Snapshot-based progress for "Scavenge X" quests**: pre-acceptance items don't count.
- **HARVEST_TIME counter only flushes on stop_harvest** (session 48). auto_v2 cycles do NOT auto-flush.
- **Migration verify-end-state**: after stop_strategy, READ kami states; stop_harvest_batch any still-HARVESTING; verify ALL RESTING before start_strategy at new node.
- **stop_harvest_batch 5-kami safe upper bound** (eth_estimateGas cap).
- **executeBatchedAllowFailure silently skips reverts** — always read state after batch (now caught by per_kami map).
- **Travel `dry_run=True` first** — free read of path + stamina + items.
- **Account stamina max ~64-80 SP** observed this session. Top off via Ice Cream / Better Ice Cream if path needs more.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Cross-droptable amortization**: stack scav-objective quests on the same node when possible.
- **Operator vs owner wallet**: trade.execute = owner; listing_buy/burn/craft/scav_claim = operator; auction_buy = owner.
- **Cron forced-fire**: orchestrator can override `next-run-at` to fire immediately. Don't rely on long delays staying long.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→...→Q43✓→Q44✓→Q45✓→**Q46(scav 5 Honeydew @ node 77 — this session 57)**→Q47(harvest 720min @ Cave Crossroads, NEW node)→Q48+...
