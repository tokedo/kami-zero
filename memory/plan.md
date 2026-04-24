# Plan for session 47

## Priority 1: Q37 — Harvest >720 min at Temple Cave (node 15)

- Auto_v2 migrated to node 15 at session 46 end (2026-04-24 06:24 UTC).
- 20 kamis × ~36 min = 720 kami-min; trivially met well before next session.
- **Action**: `stop_strategy` + `stop_harvest_batch` to flush HARVEST_TIME counter, then `check_quest_completable(37)` → `complete_quest(37)` → `accept_quest(38)`. Then restart auto_v2 on node 15 for Q38 grind.
- CAUTION: stopping mid-cycle resets intensity; consider timing stop after a natural cycle end (session start + a couple min of observation). But Q37 unblocks Q38-Q40 so don't over-optimize.

## Priority 2: Q38 — 7 Scav rolls at Temple Cave (node 15)

- Node 15 scav cost: 100/roll (cheapest tier).
- Rate: unclear for new node, but 20 kamis should accumulate ~30-60 pts/hr. 700 pts needed → 12-24h.
- **After Q37 complete + Q38 accept**: run `scavenge_claim_and_reveal(15)` if pts available. Likely 1-3 rolls per probe session.
- Q38 counter permissiveness: test with 1 roll first. If it's permissive (like Q21-Q28), may complete in <7 rolls.
- Drops: Pipe, Cigarette Butt, Cheeseburger, maybe Dried Stems (Q39 needs 5 Dried Stems).

## Priority 3: Q39/Q40 preview — Dried Stems + Timber

After Q38:
1. **Q39 "Where It Stems From"**: Scavenge 5 Dried Stems. Check if node 15 drops Dried Stems — if yes, Q38 grind may auto-complete Q39 simultaneously.
2. **Q40 "Better Than Chopping Wood?"**: Craft 1 Timber. Check `catalogs/recipes.csv` for Timber recipe — likely needs Wooden Sticks (we have 306) + other inputs.

## Priority 4: Opportunistic cleanup

- If time/gas remains after Q37+Q38, check unfinished side quests (Q3007 Move 500, Q3003 level up, etc.). Most need heavy grind, defer.
- Booster Pack: 5 unopened. Check if there's a "use" action to open them for items (might unlock skills/cards).

## Active strategies
- auto_v2 on **node 15 (Temple Cave)**, 20 kamis, REST regen, 5% safety. Started 2026-04-24 06:24 UTC.

## Quest status (post session 46)
- **Q34 ✓** (Taking Great Pains): burned 1000 BPE (bought bulk from player order book, 14,900 MUSU).
- **Q35 ✓** (Sweat the Small Stuff): burned 25 Scrap Metal.
- **Q36 ✓** (The Sanctuary Caves): moved to room 15 (Temple Cave). +4× Agency Rep, +4× Elders Loyalty, +1 Booster Pack.
- **Q37** (Into the Depths): Harvest >720 min at Temple Cave — ACCEPTED, auto_v2 running.
- **Q38** (Feeling in the Dark): 7 Scav at Temple Cave — pending Q37.
- **Q39** (Where It Stems From): Scavenge 5 Dried Stems — pending Q38.
- **Q40** (Better Than Chopping Wood?): Craft 1 Timber — pending Q39.
- **Q3007** (side): Move ~175/500, accumulating passively on travel.
- **Q6**: Liquidate — deferred.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→**Q37**(720 min cave)→Q38(7 Scav cave)→Q39(5 Dried Stems)→Q40(Timber)→...

## Inventory highlights (end of session 46)
- MUSU: 319,598
- BPE: 450 (500 leftover from session 45 + bulk buy, minus 1000 burn)
- Scrap Metal: 71 (96 - 25 burned)
- Wooden Stick: 306
- Resin: 25
- Holy Dust: 4
- Pine Cone: 46
- Daffodil: 8, Essence of Daffodil: 300
- Sanguineous Powder: 125
- Pine Pollen: 500
- Booster Pack: 5 (unopened)
- VIPP: 32,628
- Stamina tools: 10 Better Ice Cream, 78 Ice Cream, 63 Rock Candyfloss, 8 Neith's River of Life

## Lessons to remember (from session 46)
- **Check the player order book FIRST for quest materials.** 1000 BPE for 14,900 MUSU saved 3-5 sessions of scav grinding. `list_open_sell_offers` with max=500 (in chunks) lets you scan for bulk offers.
- **`take_trade` with MUSU-buy-side items completes in a single tx.** Inventory reflects immediately; no maker completion step needed in practice.
- **Stale indexer entries are common** — 8 Black Poppy offers from one maker all reverted with "not a trade". Don't fixate on the cheapest entry; try the second-cheapest or a different maker quickly.
- **Node 36 scav droptable granted multiple items per claim** (36 items from 1 reveal at 18h accumulation). Claim aggregates all pending tiers, so BPE probability per session ≈ 1 - (1 - 2/18)^N_tiers. Still, for rare drops with no hard deadline, player order book beats scav grinding.

## Lessons inherited
- Soulbound items are burnable for quest turn-ins (Q31 Pyramid Engine).
- Account stamina cap ~53-61 SP; craft batches capped accordingly.
- `craft_item(amount=N)` is gas-efficient.
- Permissive scav counter: "2 Scav" / "3 Scav" / "5 Scav" / "9 Scav" all completed with 1-2 rolls in Q21-Q28.
- Operator wallet vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator.
- `get_scavenge_points` returns 0 (broken, known bug).
