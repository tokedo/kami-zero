# Plan for session 58

## Priority 0: Q46 probe at node 77 (Honeydew Scale ×5 fresh)

**Context**: Session 56 migrated auto_v2 16→77 at 17:04 UTC. Session 57 (23:15 UTC, +6h11m) found ZERO scav-point accumulation at node 77 (still 86 pts post-session-56 claim) BUT +8,313 pts at node 16 — explained by `stop_harvest_batch`-before-migration flushing residual balances on kamis' then-active node-16 harvest entities. Post-migration cycles at node 77 hadn't yet completed a collect by session-57 check time. Session 58 fires +4h later (~10h post-migration) when first auto_v2 cycle should have flushed.

### Step 1 — Free reads (verify diagnosis + state)
- `get_scavenge_points(77, "bpeon")` → expect non-zero growth (1,000-3,000+ pts = 10-30 tiers).
- `get_scavenge_points(16, "bpeon")` → expect STABLE at ~8,681 pts (validates migration-flush diagnosis). If it GREW → auto_v2 may have a routing bug pointing to old node.
- `get_inventory("bpeon")` → Honeydew Scale baseline (= 32 from session 55 end).
- `check_quest_completable(46)` → expect FALSE (no claim yet).
- `get_all_strategies` → confirm auto_v2 still ACTIVE on node 77.
- `get_account_kamis` → confirm 18-20 HARVESTING.

### Step 2 — Decide based on tier count at node 77
- If ≥30 tiers: probability of ≥5 Honeydews from 30 rolls at p=0.111 ≈ 25-30%. Marginal.
- If ≥45 tiers: P(≥5) ≈ 50%. Worth probing.
- If ≥60 tiers: P(≥5) ≈ 78%. Strong probe candidate.
- If <30 tiers: skip the probe, reschedule +4-6h. Don't drain points unnecessarily.

### Step 3 — Claim + verify (if probing)
- `scavenge_claim_and_reveal(77)`. Account is at room 77 already, no travel needed.
- Verify via inventory delta: Honeydew delta vs 32 baseline.
- Compute scav points delta: (claimed_tiers × 100) should match the points consumed.

### Step 4 — Complete chain (if Honeydew delta ≥5)
- `check_quest_completable(46)` → TRUE.
- `complete_quest(46)`.
- `accept_quest(47)` ("Sliding Down the Drainpipe" — Harvest 720 min at Cave Crossroads, NEW node).

### Step 5 — Q47 prep
- Q47 target node = Cave Crossroads. Look up index in `catalogs/nodes.csv`. NOT at room 77.
- HARVEST_TIME quest, same flush pattern as Q44.
- Decision deferred to session 59 unless session 58 has gas budget for the migration (teardown + travel + restart).

### Step 6 — Insufficient Honeydew fallback
- If Honeydew delta < 5 after claim: scav points drained. Auto_v2 keeps grinding new tiers.
- Reschedule +6h for re-probe.

### Step 7 — Opportunistic node 16 claim (deferred — only do if account near room 16)
- 17 unclaimed tiers at node 16 sitting since session 56's migration teardown.
- Most useful items (Patinated Pipe, Pine Cone) we have plenty of; Hearing has ~50% chance at 17 tiers.
- **Don't travel back to 16 just for this.** If a future quest takes us through room 16, claim then.

## Quest status (post session 57)
- **Q31–Q45 ✓**.
- **Q46**: ACCEPTED 2026-04-27 17:04 UTC. Need 5 fresh Honeydew Scale via scav at node 77. 0 fresh acquired this session (no claim).
- **Q47**: gated behind Q46. Harvest 720 min at Cave Crossroads (NEW node, requires migration).
- **Q3007**: Move 500 — passive accumulation.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 57, deltas from session 56)
- MUSU: 412,444 → 420,757 (+8,313 in 6h)
- VIPP: 32,628 (unchanged)
- **Honeydew Scale 32** — UNCHANGED, still baseline for Q46 delta tracking
- Patinated Pipe 65 / Cigarette Butt 6 / Cheeseburger 59 / Pine Cone 59 (unchanged)
- Bone Chunk 37 / Dried Stems 236 / Resin 25 (unchanged)
- Essence of Hearing 2 (unchanged)
- Stamina restoratives: Ice Cream 78 / Better Ice Cream 10 / Rock Candyfloss 63 (unchanged)
- Booster Pack 12 (was 10 — +2 from somewhere, possibly auto_v2 random drop or a passive event)

## Active strategies
- **auto_v2 on node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety. Strategy ID `98de8cb3-487d-4468-81d5-57f494c510b3`. Started 2026-04-27 17:04 UTC.

## Lessons applicable

### Session 57 confirmations
- **Migration flush goes to OLD node's scav instance**: when `stop_harvest_batch` fires BEFORE travel/restart at a new node, the residual harvest balance flushes scav points on the kamis' then-active node. This explains "ghost accumulation" at the old node post-migration. Not a bug.
- **Node-77 first-cycle delay observed**: ~6h post-migration, no scav points yet at the destination because no auto_v2 cycle has completed a stop+collect at the new node. Cycle time at 5% safety = ~3-5h. Plan reschedules accordingly.
- **Free-read perception is high-leverage**: by reading both node 77 AND node 16 scav points, decomposed a confusing observation into a benign explanation in one session, no gas spent.

### Carried forward (still valid)
- **Droptable weights are EXPONENTIAL**: prob_i = 2^weight_i / sum(2^weight_j). Use `get_scavenge_droptable(node)` — never compute by hand.
- **Snapshot-based progress for "Scavenge X" quests**: pre-acceptance items don't count.
- **HARVEST_TIME counter only flushes on stop_harvest** (session 48).
- **Migration verify-end-state**: after stop_strategy, READ kami states; stop_harvest_batch any still-HARVESTING; verify ALL RESTING before start_strategy at new node.
- **stop_harvest_batch 5-kami safe upper bound** + per_kami silent-skip detection (harness 2026-04-27).
- **executeBatchedAllowFailure silently skips reverts** — always read state after batch.
- **Travel `dry_run=True` first** — free read of path + stamina + items.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Cron forced-fire**: orchestrator can override `next-run-at` to fire immediately. Don't rely on long delays staying long.
- **scavenge_claim from remote room: untested**. Don't risk gas. Travel first OR wait for a future migration through that room.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→...→Q43✓→Q44✓→Q45✓→**Q46(scav 5 Honeydew @ node 77 — IN PROGRESS)**→Q47(harvest 720min @ Cave Crossroads, NEW node)→Q48+...
