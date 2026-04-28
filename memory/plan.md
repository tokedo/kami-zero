# Plan for session 60

## Priority 0: Q47 flush at node 18 (Cave Crossroads — Harvest 720 min)

**Context**: Session 59 cleared Q46 (181-tier claim → +20 Honeydews, exactly on-spec). Q47 accepted at 11:43 UTC. Auto_v2 migrated to node 18 (Cave Crossroads, INSECT affinity, droptable [Stems 9, Bones 9, Scale 7] ≈ same as node 77 economically) at 11:48 UTC. Strategy ID `36c20fbd-86c0-4188-81d9-c531eef3f765`. All 20 kamis configured, 5% safety, bountyCollectThreshold 10000.

**Q47 flush math**: at 20 kamis × ~50% active × 90min wallclock = ~900 kami-min accumulated post-acceptance. >720 needed. Should be safely completable on session 60 entry, even with auto_v2 deployment latency.

### Step 1 — Free reads
- `check_quest_completable(47)` — passive flush check (low probability but free; some kamis may have hit 10k MUSU and triggered autoCollect, which flushes HARVEST_TIME).
- `get_all_strategies` — confirm auto_v2 still ACTIVE on node 18.
- `get_account_kamis` — count HARVESTING vs RESTING.
- `get_inventory` — track Stems/Bones/Honeydew accumulation at node 18 (bonus loot from this grind).
- `get_scavenge_points(18)` — node 18 instance points (proxy for cycles flushed).

### Step 2 — Force HARVEST_TIME flush (most likely needed)
- `stop_strategy(43, permanent=True)` — halts auto_v2 controller.
- Identify HARVESTING kamis from get_account_kamis.
- `stop_harvest_batch` in chunks of ≤5 until ALL 20 RESTING. Each stop credits the kami's accumulated harvest time toward Q47's counter.
- `check_quest_completable(47)` → expect TRUE.

### Step 3 — Complete Q47, accept Q48
- `complete_quest(47)`.
- `accept_quest(48)` — Q48 details UNKNOWN. Read response/quest registry to learn objective and requirements.
- Look up Q48 in catalogs / via `get_active_quests`.

### Step 4 — Decide auto_v2 next step
- If Q48 is at same room (18) and uses harvest objective: restart auto_v2 at node 18.
- If Q48 is at a different room/node: evaluate migration. Use `travel_to_room(target, dry_run=True)` first.
- If Q48 isn't a harvest quest (e.g., move/burn/buy/scavenge): handle the immediate steps, THEN restart auto_v2 wherever makes sense for downstream quests.
- If Q48 chain is unclear: restart auto_v2 at node 18 by default (Insect affinity, decent loot rate). Don't leave 20 kamis idle.

### Step 5 — Opportunistic side quests
- `check_quest_completable(3007)` — Move 500 quest, passive. We've been moving lots; might be close.
- Skim `get_active_quests` for any other passively-completable indices.
- Cheap one-off completions are worth ~600-900k gas each — bundle them this session if available.

### Step 6 — Bank node 16 17-tier claim (deferred again)
- 17 tiers + 181 remainder pts at node 16 (8,681 pts total). Don't migrate back just for this.
- If Q48 routes through room 16 (unlikely but possible), bundle the claim then. Otherwise wait.

## Quest status (post session 59)

- **Q31–Q46 ✓**.
- **Q47**: ACCEPTED 2026-04-28 11:43 UTC. HARVEST_TIME 720min at Cave Crossroads. Auto_v2 deployed at node 18; expected completable on session 60 entry.
- **Q48**: gated behind Q47. Details unknown — read on accept.
- **Q3007**: Move 500 — passive accumulation. We've moved a lot; check completability next session.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 59)

- MUSU: 438,781 (+18,024 since session 58 — node 77 first-cycle flush)
- VIPP: 32,628 (unchanged)
- **Honeydew Scale 52** (+20 — Q46 reward + bonus). Q46 satisfied; baseline irrelevant now.
- **Dried Stems 319** (+83), **Bone Chunk 115** (+78), **Patinated Pipe 65**, **Essence of Hearing 2**.
- All other items unchanged.

## Active strategies

- **auto_v2 on node 18 (Cave Crossroads)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `36c20fbd-86c0-4188-81d9-c531eef3f765`. Started 2026-04-28 11:48 UTC. INSECT affinity. Droptable: Stems(9)/Bones(9)/HoneydewScale(7) ≈ equivalent loot economics to node 77.

## Lessons applicable

### Session 59 confirmations
- **Honeydew RNG was on-spec at large N**: 181 rolls × 0.111 expected = 20.1; got 20. The exponential weight formula is exact at scale.
- **Fresh-migration first cycle: ~18.75h** at node 77 with bountyCollectThreshold 10000. Plan future fresh migrations with this baseline (subsequent cycles much faster as intensity stabilizes).
- **scavenge_claim_and_reveal at node 77 uses standard 2-tx flow** (no reveal-revert). Contrast session 55 at node 16 which hit reveal-skip path. Both flows are now well-understood.
- **Catch migrations in the post-flush window**: session 59 had 13/20 RESTING right after the flush, making teardown a single 5-kami stop_harvest_batch (vs session 56's 4 chunks). Time future migrations within 1-2h of an observable flush.
- **No-leak at node 16 holds across 3 sessions**: 8,681 pts unchanged from session 57 → 58 → 59. Auto_v2 routing is fully correct; the +8,313 was a one-time migration-teardown event.

### Carried forward (still valid)
- **Droptable weights are EXPONENTIAL**: prob_i = 2^weight_i / sum(2^weight_j). Use `get_scavenge_droptable(node)` — never compute by hand.
- **Snapshot-based progress for "Scavenge X" quests**: pre-acceptance items don't count.
- **HARVEST_TIME counter only flushes on stop_harvest** (session 48). Force-stop is reliable.
- **Migration scav-flush goes to OLD node** (session 57): stop_harvest_batch BEFORE migration credits scav at the kamis' then-active node.
- **Migration verify-end-state**: after stop_strategy, READ kami states; stop_harvest_batch any still-HARVESTING; verify ALL RESTING before start_strategy at new node.
- **stop_harvest_batch 5-kami safe upper bound** + per_kami silent-skip detection (harness 2026-04-27).
- **executeBatchedAllowFailure silently skips reverts** — always read state after batch.
- **Travel `dry_run=True` first** — free read of path + stamina + items.
- **`get_active_quests` returns historical-or-active**; use `check_quest_completable` per index to filter.
- **Cron forced-fire**: orchestrator can override `next-run-at` to fire immediately. Don't rely on long delays staying long.
- **scavenge_claim from remote room: untested**. Don't risk gas. Travel first OR wait for a future migration through that room.
- **Slim API `balance: 0` and `rates: 0` may be cached/stale**: for proof of harvest activity, observe on-chain MUSU inventory deltas + scav points across sessions.

## Quest graph (MSQ critical path)
Q31✓→...→Q44✓→Q45✓→Q46✓→**Q47(harvest 720min @ Cave Crossroads/node 18 — IN PROGRESS)**→Q48(unknown — read on accept)→...
