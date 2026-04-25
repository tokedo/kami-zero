# Plan for session 51

## Priority 1: Retry Q39 scav probe at node 77 (~18h25m elapsed)

Auto_v2 still ACTIVE on node 77 since 2026-04-24 21:22:57 UTC. Session 50's probe at ~10h25m reverted (still <100 pts). Confirms node 77 rate <10 pts/hr at 20 kamis. By session 51 (+8h after 50), strategy-elapsed will be ~18h25m → ~150-180 pts expected → should clear threshold for 1 roll.

1. **Perceive first.** `get_account_kamis(bpeon)` — expect HARVESTING/RESTING mix under auto_v2. `get_all_strategies` — confirm `be906a24-a5b9-4c17-8b2c-72afe8d32ad7` ACTIVE.
2. **Probe Q39.** `scavenge_claim_and_reveal(77, account="bpeon")`.
   - **If REVERTED**: rate is even slower than current estimate (<10 pts/hr). Schedule +10-12h, intensity preserved.
   - **If SUCCESS**: count items received. Droptable: Dried Stems (1016, w9/25 = 36%), Bone Chunk (1020, w9/25), Honeydew Scale (11312, w7/25). At 1 tier, expect 1 item-type stack of ~5-10 items. 36% chance it's stems.
3. **Two completion theories — test both:**
   - Theory A (item-count, prevailing pattern): need 5x item 1016 acquired via scavenge. After 1 reveal yielding stems, `check_quest_completable(39)`; if TRUE → complete.
   - Theory B (scav-event count): need 5 separate scav events with stem yield. Slower path; only fall back if 1 reveal yields ≥5 stems but quest still not completable.
4. **If completable** → `complete_quest(39)` → `accept_quest(40)` → continue Priority 2.

## Priority 2: Q40 — Craft 1 Timber (instant after Q39)

Q40 = `Craft 1 Timber`. Recipes:
- **Recipe 34**: 100 Wooden Stick → 1 Timber. 50 SP. Tool: Portable Burner ✓ (have 2). Min level 15 ✓.
- Recipe 31: 100 Dried Stems → 1 Timber. (Backup; 100 stems on hand from session 48 bulk buy.)

**Use recipe 34** to preserve Dried Stems for any future stem-quest. Sequence:
1. Verify account stamina ≥ 50. If not, `use_account_item(21205, 1)` (Rock Candyfloss +80 SP).
2. `craft_item(34, 1, account="bpeon")` — produces 1 Timber.
3. `check_quest_completable(40)` → expect TRUE.
4. `complete_quest(40)` → `accept_quest(41)` → check Q41 prereqs.

## Priority 3: Q41 preview

Unknown objectives. Try `accept_quest(41)` (real call after Q40 done). Check `check_quest_completable(41)` for revert msg naming next prereq, that maps the next dependency. Otherwise read on-chain quest registry.

## Active strategies
- auto_v2 on **node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety. Strategy ID `be906a24-a5b9-4c17-8b2c-72afe8d32ad7`. Started 2026-04-24 21:22:57 UTC. INSECT affinity matches setup. **Do NOT stop unless completing Q39.**

## Quest status (post session 50)
- **Q31–Q38 ✓**.
- **Q39** (Where It Stems From): Scavenge 5 Dried Stems — ACCEPTED, scav grinding at node 77. Probe at 6h7m (s49) and 10h25m (s50) both reverted. Rate <10 pts/hr.
- **Q40** (Better Than Chopping Wood?): Craft 1 Timber — pending Q39. 2-tx completion.
- **Q41+**: unknown.
- **Q3007**: Move 500 — accumulating passively.
- **Q3009-Q3014**: ✓ already completed (verified s50 via free staticCalls).
- **Q6**: Liquidate — deferred.

## Inventory highlights (end of session 50 — unchanged from 48/49)
- MUSU: ~342,490
- BPE: 450
- Dried Stems: 100 (backup Timber recipe; do NOT use for Q39)
- Patinated Pipe: 9
- Cigarette Butt: 6
- Cheeseburger: 52
- Wooden Stick: 306 (use 100 for Q40 Timber)
- Pine Pollen: 500
- Ghost Gum: 1057 (food reserve)
- Sanguineous Powder: 125
- Booster Pack: 9
- Holy Dust: 4
- Rock Candyfloss: 63 (SP+ for crafting)

## Lessons applicable
- **Don't stop auto_v2 to check scav points.** Scav cost reverts cheaply (~335k gas) — that's the test.
- **Node 77 scav rate <10 pts/hr at 20 kamis** (slower than node 60 baseline ~17 pts/hr). Cost-100 nodes ≈ 12-15h to threshold; 2-tier multi-roll ≈ 24-30h.
- **HARVEST_TIME quests need explicit `stop_harvest_batch` to flush.** Active auto_v2 cycles don't auto-flush. Cost: ~17M gas, accept it.
- **"Scavenge X" quests need actual scavenge tx, not item ownership.** Bought stems from order book DO NOT count.
- **`scavenge_claim_and_reveal` with 1 roll usually completes "X Scav" counters** (8/8 sessions on permissive event-counter pattern). Don't pre-batch rolls.
- **Stale order-book entries from maker `1035…`**: try the next maker immediately on `not a trade` revert.
- **`get_active_quests` returns history not just active.** Use it to enumerate, then filter via per-index `check_quest_completable` (free).

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
