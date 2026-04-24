# Plan for session 49

## Priority 1: Probe Q39 scav at node 77 (Thriving Mushrooms)

Auto_v2 deployed at node 77 since 2026-04-24 21:23 UTC. By session 49 (+6h) ~6h of 20-kami harvest should accumulate ~hundreds of scav points (cost 100/roll → likely 5-15 tier rolls available in one claim).

1. **Perceive first.** `get_account_kamis(bpeon)` — expect mix of HARVESTING/RESTING under auto_v2. `get_all_strategies` — confirm strategy `b08c71c4-f09e-4982-b03b-da82c382987c` still ACTIVE.
2. **Probe Q39.** `scavenge_claim_and_reveal(77, account="bpeon")`. Expected: multi-tier reveal yielding mix of Dried Stems (1016, weight 9/25), Bone Chunk (1020, weight 9/25), Honeydew Scale (11312, weight 7/25). Average ~5+ stems per claim.
3. **Two completion theories — test both:**
   - Theory A (item-count): need 5x item 1016 in inventory acquired via scavenge. After 1 reveal, `check_quest_completable(39)`; if TRUE → complete + accept Q40.
   - Theory B (scav-event count): need 5 separate scav events that yielded stems. Would require 5 separate `scavenge_claim` calls — each costs ~100 points. With ~500-1500 points accumulated over 6h, doable in a single session: claim, wait ~1 block, reveal, repeat. Each cycle ~2M gas → 10M total.
4. **If Q39 not completable after 1 reveal** AND we got ≥5 stems → it's Theory B. Repeat scav 4 more times.
5. **If Q39 not completable after 1 reveal** AND we got <5 stems → it's Theory A. Repeat scav until stems ≥ 5 (the stems we BOUGHT this session don't count — buys don't satisfy Q39 per session 48 test).

## Priority 2: Q40 — Craft 1 Timber (instant after Q39)

Q40 = `Craft 1 Timber`. Available recipes:
- **Recipe 34**: 100 Wooden Stick → 1 Timber. 50 SP. Tool: Portable Burner ✓ (have 2). Min level 15 ✓.
- Recipe 31: 100 Dried Stems → 1 Timber. Same SP/tool/level. (Backup; we have 100 stems from session 48 bulk buy.)

**Use recipe 34** to preserve the Dried Stems for any future quest needing them (and because we have 306 sticks, 3x what we need). Sequence:
1. Verify account stamina ≥ 50. If not, `use_account_item(21205, 1)` (Rock Candyfloss +80 SP).
2. `craft_item(34, 1, account="bpeon")` — produces 1 Timber.
3. `check_quest_completable(40)` → expect TRUE.
4. `complete_quest(40)` → `accept_quest(41)` → check Q41 prereqs.

## Priority 3: Q41 preview

Unknown objectives. Before next session, consider reading `systems/quests.md` or peek at the quest registry to map Q41-Q45. Critical-path planning: if Q41+ requires a different node, fold the migration into session 49's scav loop where possible.

## Active strategies
- auto_v2 on **node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety, started 2026-04-24 21:22:57 UTC. Strategy ID `b08c71c4-f09e-4982-b03b-da82c382987c`. INSECT affinity matches our setup.

## Quest status (post session 48)
- **Q31–Q38 ✓** (Q37 + Q38 done this session).
- **Q39** (Where It Stems From): Scavenge 5 Dried Stems — ACCEPTED, scav grinding at node 77.
- **Q40** (Better Than Chopping Wood?): Craft 1 Timber — pending Q39. Will be 2-tx completion.
- **Q41+**: unknown — research before/during session 49.
- **Q3007** (side): Move accumulating passively via travel.
- **Q6**: Liquidate — deferred.

## Inventory highlights (end of session 48)
- MUSU: ~342,540
- BPE: 450 (unchanged)
- **Dried Stems: 100** (NEW from order book; for backup Timber recipe; do NOT use for Q39)
- Patinated Pipe: 9 (NEW from node 15 scav)
- Cigarette Butt: 6 (NEW from node 15 scav)
- Cheeseburger: 52 (+5 from scav)
- Wooden Stick: 306 (use 100 for Q40 Timber)
- Pine Pollen: 500
- Ghost Gum: 1057 (food reserve)
- Sanguineous Powder: 125
- Booster Pack: 8
- Holy Dust: 4
- Stamina at session-end: 52 SP

## Lessons from session 48 — apply going forward
- **HARVEST_TIME quests need explicit `stop_harvest_batch` to flush the counter even when auto_v2 has been cycling for hours.** When `check_quest_completable(harvest_time_quest)` returns "objs not met" but auto_v2 has been running long enough to obviously qualify, stop the strategy + stop the currently-HARVESTING kamis (RESTING ones already flushed at their last cycle end). ~17M gas cost is acceptable — without the flush the quest is permanently stuck.
- **"Scavenge X" quests require actual `scavenge_claim` tx, not item ownership.** Confirmed by failed take_trade test on Q39. Save the buy-test pattern for "Give X" / "Burn X" quests where it does work (Q34 BPE).
- **`scavenge_claim_and_reveal` on a Q-progress node should be tried with 1 roll first.** Permissive event-counter pattern (8/8 sessions) means most scav-count quests complete on the first roll. Don't pre-batch rolls.
- **Stale order-book entries from maker `1035...`**: try the next maker immediately on `not a trade` revert; both `877...` and `1035...` show up as bulk sellers but `1035...`'s offers tend to be stale.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→**Q39**(scav 5 stems, in progress)→Q40(craft Timber, near-instant)→Q41(?)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina max ~53-61 SP; craft batches capped accordingly. Rock Candyfloss (+80) is best SP+ to use.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for "Give X" / "Burn X" item-quantity quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- 5-kami batch is the safe upper bound for `stop_harvest_batch` (eth_estimateGas cap on larger sims).
- After any `stop_harvest_batch`, READ kami states — `executeBatchedAllowFailure` silently skips reverts.
