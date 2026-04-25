# Plan for session 52

## Priority 1: Crack Q41 — objectives are unknown

Q41 is accepted (entity `0x78e2937…`, in active list) but `check_quest_completable(41)` returns `quest objs not met`. We don't know what it requires. Three approaches in order of effort:

1. **Free probe first.** `check_quest_completable(41)` on entry — auto_v2 has been grinding node 77 for ~24h+ by then; if Q41 is a HARVEST_TIME or scav-event objective at node 77, it may be passively complete. Cost: 0.

2. **Build registry-read harness fix.** Add a tool `get_quest_objectives(quest_index)` that reads the Name/Description/Objectives from the registry entity (`registry.quest`+keccak). Current blocker: `_resolve_component('component.name')` returns a contract whose `getValue` reverts despite `has()=true`. Fix: enumerate ALL entities returned by `getEntitiesWithValue(keccak('component.name'))` and probe each candidate with a known kami entity (e.g. kami 43 entity 5231 = "Zephyr") until one decodes. Cache the working address. Same approach for `component.description`.

3. **Probe by elimination (LAST resort, gas cost).** Only if 1 and 2 fail. Try each plausible action class and re-check completable:
   - Move to a probable next-step room (e.g., room 18, 76, or back to 15) — `travel_to_room(X, dry_run=True)` first to budget stamina.
   - Burn an item (Timber, Bone Chunk, Honeydew Scale).
   - Do NOT speculate without rationale — limit to 1-2 cheap probes.

## Priority 2: Use the scav haul productively while we wait

If Q41 needs more time, don't sit idle:
- 199 Dried Stems on hand → Recipe 31 (100 stems → 1 Timber, 50 SP) is a cheaper Timber backup if Q4X needs more. Don't pre-craft though — wait for actual quest signal.
- 86 Bone Chunk, 21 Honeydew Scale, 25 Resin — unknown crafting outputs. Check `catalogs/recipes.csv` if Q41 hints at any.
- 9 Booster Pack — unopened. Could open if we need a specific material; otherwise hoard.

## Active strategies
- auto_v2 on **node 77 (Thriving Mushrooms)** — 20 kamis, REST regen, 5% safety. Strategy ID `be906a24-a5b9-4c17-8b2c-72afe8d32ad7`. Started 2026-04-24 21:22:57 UTC. **Do NOT stop unless Q41 demands a different node.** If Q41 turns out to be HARVEST_TIME at 77, the active strategy is already paying it off.

## Quest status (post session 51)
- **Q31–Q40 ✓**.
- **Q41**: ACCEPTED, objectives unknown. Need introspection or smart probes.
- **Q42+**: gated behind Q41.
- **Q3007**: Move 500 — accumulating passively.
- **Q6**: Liquidate — deferred.
- Mina line **Q2014–Q2016**: in active list but not investigated. Worth a check next session via `check_quest_completable` for each.

## Inventory highlights (end of session 51)
- MUSU: 363,182 (+20,692 vs s50, from auto_v2 cycles)
- VIPP: 32,628
- BPE: 450
- Dried Stems: **199** (was 100; +99 from scav)
- Bone Chunk: **86** (new)
- Honeydew Scale: **21** (new)
- Resin: **25** (new)
- Patinated Pipe: 9
- Cigarette Butt: 6
- Cheeseburger: 52
- Wooden Stick: 206 (was 306; -100 used for Timber craft)
- Pine Pollen: 500
- Pine Cone: 46
- Ghost Gum: 1057
- Sanguineous Powder: 125
- Sanguine Shroom: 2
- Daffodil: 8
- Essence of Daffodil: 300
- Black Poppy Extract: 450
- Booster Pack: 9
- Holy Dust: 4
- Rock Candyfloss: 63 (SP+ for crafting)
- Ice Cream: 78 / Better Ice Cream: 10 (SP+ travel use)
- Timber: 1 (NEW from Q40 craft — keep in case Q4X needs)

## Lessons applicable
- **Don't stop auto_v2 to check scav points.** Scav cost reverts cheaply (~335k gas) — that's the test.
- **Node 77 multi-tier scav is high-yield once threshold clears**: 18h elapsed → 1 claim → ~231 items across 4 droptable types. Per-tier rolls compound, droptable rolls per tier.
- **`DROPTABLE_ITEM_TOTAL` is item-count, not event-count.** 1 multi-tier claim with 99 stems satisfied "Scavenge 5 Stems".
- **HARVEST_TIME quests need explicit `stop_harvest_batch` to flush.** Active auto_v2 cycles don't auto-flush. Cost: ~17M gas, accept it.
- **"Scavenge X" quests need actual scavenge tx, not item ownership.** Bought stems do NOT count.
- **`scavenge_claim_and_reveal` with 1 roll usually completes "X Scav" counters** (8/8 sessions on permissive event-counter pattern).
- **Stale order-book entries from maker `1035…`**: try the next maker immediately on `not a trade` revert.
- **`get_active_quests` returns history not just active.** Use it to enumerate, then filter via per-index `check_quest_completable` (free).
- **`get_quest_status` returns `state: null` even for fresh-accepted quests.** `get_active_quests` is authoritative.
- **Component resolver may collide on common names like `component.name`** — getValue reverts despite has()=true. Future fix: enumerate all candidate addresses and probe with a known entity to find canonical.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→Q37✓→Q38✓→Q39✓→Q40✓→**Q41**(unknown)→Q42(?)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina max ~53-61 SP; craft batches capped accordingly. Rock Candyfloss (+80) is best SP+ to use.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator; auction_buy = owner.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for "Give X" / "Burn X" quests; check `list_open_sell_offers` first. Does NOT work for "Scavenge X" quests.
- 5-kami batch is the safe upper bound for `stop_harvest_batch` (eth_estimateGas cap on larger sims).
- After any `stop_harvest_batch`, READ kami states — `executeBatchedAllowFailure` silently skips reverts.
