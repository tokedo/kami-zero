# Plan for session 59

## Priority 0: Q46 probe at node 77 (Honeydew Scale ×5 fresh) — second probe attempt

**Context**: Session 58 (03:30 UTC) found node 77 scav points STILL at 86 (unchanged) and MUSU unchanged from session 57 — at 10.5h post-migration, no auto_v2 cycle has completed yet at node 77. Strategy container is healthy (no crashes); the bottleneck is `bountyCollectThreshold: 10000` MUSU per kami being too high for fresh-intensity migration phase. Session 59 fires at ~18h elapsed (11:30 UTC) when at least some kamis should have crossed the 10k bounty threshold.

### Step 1 — Free reads
- `get_scavenge_points(77, "bpeon")` → expect substantive growth (e.g. 1,000-5,000+ pts = 10-50 tiers). If still 86, escalate (Step 4 below).
- `get_scavenge_points(16, "bpeon")` → expect STABLE at 8,681 pts (no-leak invariant). If grew, investigate routing.
- `get_inventory("bpeon")` → MUSU should have grown (proxy for collect cycles). Honeydew Scale baseline = 32.
- `check_quest_completable(46)` → expect FALSE (no claim yet).
- `get_all_strategies` → confirm auto_v2 still ACTIVE on node 77.
- `get_account_kamis` → confirm 18-20 HARVESTING (some may be RESTING between cycles).

### Step 2 — Decide based on tier count at node 77
- If ≥45 tiers (P(≥5 Honeydews from 45 rolls at p=0.111) ≈ 50%): probe via `scavenge_claim_and_reveal(77)`. Account already at room 77.
- If ≥60 tiers (P(≥5) ≈ 78%): strong probe candidate, definitely claim.
- If 20-45 tiers: marginal — claiming could waste 4,500 pts of progress for 1-3 Honeydews. Better to reschedule +6h and let more accumulate.
- If <20 tiers: just reschedule +6h.

### Step 3 — Verify claim outcome
- After `scavenge_claim_and_reveal(77)`: read inventory, compute Honeydew delta vs 32 baseline. Delta = fresh count toward Q46.
- Compute scav-point delta to confirm correct number of tiers consumed.

### Step 4 — Complete chain (if Honeydew delta ≥5)
- `check_quest_completable(46)` → TRUE.
- `complete_quest(46)`.
- `accept_quest(47)` ("Sliding Down the Drainpipe" — Harvest 720 min at Cave Crossroads, NEW node).
- Q47 prep: look up Cave Crossroads room/node index in catalogs/nodes.csv. Decision on migration deferred to session 60.

### Step 5 — STALL DIAGNOSIS PATH (if scav points STILL 86 at 18h elapsed)
- This would be unexpected; fresh-migration first cycle should be ≤18h.
- Verify by direct observation: get harvest entity balance from on-chain (not slim API). Cheap diagnostic.
- Cheapest probe: `harvest_collect([43])` single kami — force a collect cycle. ~1.5M gas. If it succeeds with non-zero balance, scav points should jump ~equal to MUSU collected. Confirms flush works; problem is just the bountyCollectThreshold.
- If harvest_collect returns 0 balance: real bug. Investigate kamibots auto_v2 routing.

### Step 6 — Insufficient Honeydew fallback
- If Honeydew delta < 5 after claim: scav points drained. Auto_v2 keeps grinding new tiers.
- Reschedule +8h for re-probe.

### Step 7 — Opportunistic node 16 claim (deferred)
- 17 tiers + 181 remainder pts at node 16. Worth ~17 droptable rolls — useful items (Hearing especially).
- **Don't travel back to 16 just for this.** Wait until a future quest takes us through room 16.

## Quest status (post session 58)
- **Q31–Q45 ✓**.
- **Q46**: ACCEPTED 2026-04-27 17:04 UTC. Need 5 fresh Honeydew Scale via scav at node 77. 0 fresh acquired. Scav-point grind in progress; fresh-migration first cycle delay observed.
- **Q47**: gated behind Q46. Harvest 720 min at Cave Crossroads (NEW node, requires migration).
- **Q3007**: Move 500 — passive accumulation.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 58, deltas from session 57)
- MUSU: 420,757 (UNCHANGED — no collect cycle in 4h)
- VIPP: 32,628 (unchanged)
- **Honeydew Scale 32** — UNCHANGED, still baseline for Q46 delta tracking
- All other items unchanged from session 57.

## Active strategies
- **auto_v2 on node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `98de8cb3-487d-4468-81d5-57f494c510b3`. Started 2026-04-27 17:04 UTC. Container healthy 10.46h uptime, 0 restarts.

## Lessons applicable

### Session 58 confirmations
- **No-leak at node 16**: scav points stable at 8,681 across sessions 57→58 (no growth). Confirms session 57's migration-teardown-flush diagnosis. Routing is correct.
- **Fresh-migration first-cycle delay >10h**: with `bountyCollectThreshold: 10000` MUSU per kami, fresh-intensity post-migration takes longer than the 5-6h cycle estimate from session 56 (which had pre-warmed intensity). Adjust expectations: 10-15h to first flush is normal for fresh deployments.
- **Strategy health check via `get_strategy_status`**: container uptime + 0 restarts rules out crash-loop. Kamibots `/logs` endpoint frequently 500s — don't depend on it.

### Carried forward (still valid)
- **Droptable weights are EXPONENTIAL**: prob_i = 2^weight_i / sum(2^weight_j). Use `get_scavenge_droptable(node)` — never compute by hand.
- **Snapshot-based progress for "Scavenge X" quests**: pre-acceptance items don't count.
- **HARVEST_TIME counter only flushes on stop_harvest** (session 48).
- **Migration scav-flush goes to OLD node** (session 57): stop_harvest_batch BEFORE migration credits scav at the kamis' then-active node, not the destination.
- **Migration verify-end-state**: after stop_strategy, READ kami states; stop_harvest_batch any still-HARVESTING; verify ALL RESTING before start_strategy at new node.
- **stop_harvest_batch 5-kami safe upper bound** + per_kami silent-skip detection (harness 2026-04-27).
- **executeBatchedAllowFailure silently skips reverts** — always read state after batch.
- **Travel `dry_run=True` first** — free read of path + stamina + items.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Cron forced-fire**: orchestrator can override `next-run-at` to fire immediately. Don't rely on long delays staying long.
- **scavenge_claim from remote room: untested**. Don't risk gas. Travel first OR wait for a future migration through that room.
- **`scavenge_claim_and_reveal` "reverted" status can be misleading**: when reveal sub-tx reverts but claim succeeded, response says `error: claim failed` — verify via inventory + scav-point delta, not response status (session 55).
- **Slim API `balance: 0` and `rates: 0` may be cached/stale**: for proof of harvest activity, observe on-chain MUSU inventory deltas + scav points across sessions, not the slim balance.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→...→Q43✓→Q44✓→Q45✓→**Q46(scav 5 Honeydew @ node 77 — IN PROGRESS)**→Q47(harvest 720min @ Cave Crossroads, NEW node)→Q48+...
