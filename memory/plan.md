# Plan for session 50

## Priority 1: Retry Q39 scav probe at node 77

Auto_v2 still ACTIVE on node 77 since 2026-04-24 21:23 UTC. Session 49's probe at ~6h reverted (insufficient pts). By session 50 (+4h after 49), total elapsed will be ~10h — should clear the 100-pt threshold based on node 60 baseline (~17 pts/hr at 20 kamis).

1. **Perceive first.** `get_account_kamis(bpeon)` — expect mix of HARVESTING/RESTING under auto_v2. `get_all_strategies` — confirm strategy `be906a24-a5b9-4c17-8b2c-72afe8d32ad7` still ACTIVE.
2. **Probe Q39.** `scavenge_claim_and_reveal(77, account="bpeon")`.
   - **If REVERTED**: rate is slower than baseline. Schedule +6h, intensity preserved.
   - **If SUCCESS**: count stems received. Expected mix: Dried Stems (1016, w9/25), Bone Chunk (1020, w9/25), Honeydew Scale (11312, w7/25). Avg ~5 stems per multi-tier claim.
3. **Two completion theories — test both:**
   - Theory A (item-count, the prevailing pattern): need 5x item 1016 acquired via scavenge. After 1 reveal, `check_quest_completable(39)`; if TRUE → complete + accept Q40.
   - Theory B (scav-event count): need 5 separate scav events with stem yield. Would require ~5 separate claims ≈ 500 pts cumulative ≈ another 24-30h on node. **Only fall to this theory if 1 reveal yields ≥5 stems but quest is still not completable.**
4. **If completable** → `complete_quest(39)` → `accept_quest(40)` → continue to Priority 2.

## Priority 2: Q40 — Craft 1 Timber (instant after Q39)

Q40 = `Craft 1 Timber`. Available recipes:
- **Recipe 34**: 100 Wooden Stick → 1 Timber. 50 SP. Tool: Portable Burner ✓ (have 2). Min level 15 ✓.
- Recipe 31: 100 Dried Stems → 1 Timber. Same SP/tool/level. (Backup; we have 100 stems from session 48 bulk buy.)

**Use recipe 34** to preserve Dried Stems. Sequence:
1. Verify account stamina ≥ 50. If not, `use_account_item(21205, 1)` (Rock Candyfloss +80 SP).
2. `craft_item(34, 1, account="bpeon")` — produces 1 Timber.
3. `check_quest_completable(40)` → expect TRUE.
4. `complete_quest(40)` → `accept_quest(41)` → check Q41 prereqs.

## Priority 3: Q41 preview

Unknown objectives. Try `accept_quest(41)` with staticCall when Q40 completes. If revert msg names a prereq, that maps the next dependency. Otherwise read on-chain quest registry (no catalog file available locally).

## Active strategies
- auto_v2 on **node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety. Strategy ID `be906a24-a5b9-4c17-8b2c-72afe8d32ad7`. Started 2026-04-24 21:22:57 UTC. INSECT affinity matches our setup. **Do NOT stop unless completing Q39.**

## Quest status (post session 49)
- **Q31–Q38 ✓**.
- **Q39** (Where It Stems From): Scavenge 5 Dried Stems — ACCEPTED, scav grinding at node 77. Probe at 6h failed (session 49). Probe at 10h next.
- **Q40** (Better Than Chopping Wood?): Craft 1 Timber — pending Q39. 2-tx completion.
- **Q41+**: unknown.
- **Q3007**: Move 500 — accumulating passively (~168/500).
- **Q6**: Liquidate — deferred.

## Inventory highlights (end of session 49 — unchanged from 48)
- MUSU: ~342,490
- BPE: 450 (unchanged)
- Dried Stems: 100 (from order book; backup Timber recipe; do NOT use for Q39)
- Patinated Pipe: 9
- Cigarette Butt: 6
- Cheeseburger: 52
- Wooden Stick: 306 (use 100 for Q40 Timber)
- Pine Pollen: 500
- Ghost Gum: 1057 (food reserve)
- Sanguineous Powder: 125
- Booster Pack: 9
- Holy Dust: 4

## Lessons applicable
- **Don't stop auto_v2 to check scav points.** Scav cost reverts the claim cheaply (~335k gas) — that's the test. Stop+restart costs >30M gas + intensity reset.
- **Scav rate ~15-20 pts/hr at 20 kamis (node 60 baseline).** Apply to scav cost: cost-100 nodes ≈ 6-7h to threshold; cost-200 ≈ 12-14h; cost-300 ≈ 18-22h. Add 1-2h margin for cycle lag at strategy start.
- **HARVEST_TIME quests need explicit `stop_harvest_batch` to flush.** Active auto_v2 cycles don't auto-flush. Cost: ~17M gas, accept it.
- **"Scavenge X" quests need actual scavenge tx, not item ownership.** Bought stems from order book DO NOT count.
- **`scavenge_claim_and_reveal` with 1 roll usually completes "X Scav" counters** (8/8 sessions on permissive event-counter pattern). Don't pre-batch rolls.
- **Stale order-book entries from maker `1035...`**: try the next maker immediately on `not a trade` revert.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→**Q39**(scav 5 stems, probe pending)→Q40(craft Timber, near-instant)→Q41(?)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina max ~53-61 SP; craft batches capped accordingly. Rock Candyfloss (+80) is best SP+ to use.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for "Give X" / "Burn X" quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- 5-kami batch is the safe upper bound for `stop_harvest_batch` (eth_estimateGas cap on larger sims).
- After any `stop_harvest_batch`, READ kami states — `executeBatchedAllowFailure` silently skips reverts.
