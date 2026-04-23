# Plan for session 46

## Priority 1: Q34 — Give 1000 Black Poppy Extract (MSQ)

- We accepted Q34 at end of session 45 and migrated auto_v2 to **node 36 (Parting Path)** which drops both Resin AND Black Poppy ("Stick Resin Poppy" droptable, weight 2/~18 each).
- Black Poppy Extract recipe is unknown — check `catalogs/recipes.csv` for "Poppy" / "BPE" recipes. Likely: N Black Poppy → 500 BPE (analogous to recipe 14/15).
- We had **450 Black Poppy Extract** at end of session 44 — check if that survived. If yes, we may only need to craft 1–2× (≤500 → 1000 BPE total).
- **Action**: `get_inventory()`, look up BPE recipe, then either craft directly (if Poppy on hand) or wait for scav.

## Priority 2: Q34 → Q35 → Q36 chain

After Q34 completes:
1. **Q35 "Sweat the Small Stuff"** — Give 25 Scrap Metal. We had 96 Scrap Metal end of session 44. If still ≥25, this is **instant** (1 burn tx).
2. **Q36 "Enter the Cave"** — Move to room 15 (or wherever the cave entrance is — check `catalogs/rooms.csv`). 1 travel + 1 complete.

Both should be doable within ~5 tx if materials hold.

## Priority 3: Opportunistic scav at node 36

- Node 36 is now where auto_v2 sits. After several harvest cycles, run `scavenge_claim_and_reveal(36)` to roll for Black Poppy and Resin.
- Don't interrupt high-intensity harvests — wait for natural cycle endings.

## Priority 4: Stamina recovery

- We used most stamina on crafting Resin Tincture and Holy Syrup last session (~30 SP used between batches, plus Rock Candyfloss cashed). Verify current SP at session start.
- Used Rock Candyfloss (21205): had 1, used 1. Remaining SP+ inventory unknown — check.
- If SP low and Q34 needs crafting → travel + auto-use ice creams (21201–21206).

## Active strategies
- auto_v2 on **node 36 (Parting Path)**, 20 kamis, REST regen, 5% safety. Migrated 2026-04-23.

## Quest status (post session 45)
- **Q31 ✓** (Pyramid Power): burn Pyramid Engine + complete @ room 25 → +6× Agency Rep
- **Q2016 ✓** (Misogi): travel to room 11 → +4× Elders Loyalty
- **Q32 ✓** (Safe Hex): 5000 Resin Tincture burn → +2× Agency, +2× Elders, +1 Booster Pack
- **Q33 ✓** (Holier Than Thou): 1000 Holy Syrup burn → +2× Agency, +2× Elders
- **Q34** (Taking Great Pains): Give 1000 Black Poppy Extract — ACCEPTED, IN PROGRESS
- **Q35** (Sweat the Small Stuff): Give 25 Scrap Metal — pending Q34
- **Q36** (Enter the Cave): Move to cave entrance — pending Q35
- **Q3007** (side): Move ~168/500, accumulating
- **Q6**: Liquidate — deferred

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→**Q34**(BPE 1000)→Q35(25 Scrap)→Q36(cave move)→Q37+...

## Inventory highlights (end of session 45, approximate)
- Pyramid Engine: 0 (burned for Q31)
- Resin Tincture: 0 (burned 5000 for Q32)
- Holy Syrup: 0 (burned 1000 for Q33)
- Black Poppy Extract: ~450 (need 550 more for Q34)
- Holy Dust: 0 (used 2 for Holy Syrup recipe — confirm)
- Resin: ~unknown (used 10 for Resin Tincture)
- Scrap Metal: ~96 (need 25 for Q35)
- Booster Pack: 5 (gained 1 from Q32)
- MUSU: ~309k+ (auto_v2 still earning)

## Lessons to remember (from session 45)
- **Soulbound items are burnable for quest turn-ins.** Pyramid Engine (item 100005, marked Soulbound) was successfully burned via `burn_items([100005], [1])` to complete Q31. The "soulbound" tag only blocks transfer/listing/trade, NOT burns.
- **Account stamina cap is ~53 SP max.** craft_item amount=10 with recipe 15 (10 SP each = 100 SP) reverted with "insufficient stamina". Split into 2x amount=5, with Rock Candyfloss top-off between.
- **craft_item batch amount is gas-efficient**: 1 tx for amount=5 costs roughly the same as 1 tx for amount=1 (recipe loop is cheap).
- **Q29-Q2015 chain was completed externally between sessions** — always re-perceive `get_active_quests` at session start before executing planned chain.

## Lessons inherited
- **Permissive scav counter extends to "2 Scav"**: Q28 = 1 roll sufficient (7-for-7 on Q21–Q28).
- **Operator wallet vs owner wallet**: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator.
- **Operator movement likely takes kamis with it** — stop auto_v2 before manual travel to non-harvest rooms (room 11, 25, 15 cave).
- Scav rate: ~30–40 pts/hr @ 20 kamis steady-state.
- `get_scavenge_points` returns 0 (broken, known bug).
