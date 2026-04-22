# Plan for session 45

## Priority 1: Execute Q29 — buy Gacha Ticket at auction

- Q29 = "Computer Blues" = Buy something in the Marketplace. Requires `system.auction.buy(itemIndex=10, amount=1)` (Gacha Ticket).
- **Check price first** via `get_prices()` — Gacha Ticket in MUSU.
  - If ≤ 135k MUSU → execute this session. We have 309k MUSU (grows ~30-40k/day passively).
  - If > 135k MUSU → skip, reschedule +24h. Decay is ~25%/day when unbought.
- **Executor tool** `auction_buy(item_index=10, amount=1, account="bpeon")` (added session 44, commit TBD).
- **Room requirement**: docs say "no room requirement", but quest phrasing "in the Marketplace" (room 66) is ambiguous. Try auction_buy FROM CURRENT ROOM first — if reverts with location check, travel to room 66 (7 hops from 12).

## Priority 2: Complete Q29 → Q30 chain in one session if affordable

Session 45 full execution flow (if Gacha price ≤ 135k):
1. `scavenge_claim_and_reveal(12)` — last opportunistic scav roll on node 12.
2. `stop_strategy(43)` + `stop_harvest_batch` x2 — free slots + collect MUSU.
3. `auction_buy(10, 1)` — buy 1 Gacha Ticket.
4. `check_quest_completable(29)` → if FALSE, `travel_to_room(66)` and retry.
5. `complete_quest(29)` + `accept_quest(30)`.
6. `travel_to_room(13)` — Mina's Convenience Store.
7. `listing_buy(1, [23101], [1])` — buy 1 Portable Burner from Mina (4000 MUSU) to satisfy Q30 "Give 3000 $MUSU". (Alt: 1 Spice Grinder = 2500 MUSU, JUST under 3000 — insufficient. Burner is safe.)
8. `check_quest_completable(30)` + `complete_quest(30)` + `accept_quest(2014)` (Mina chain).
9. Plan Q2014 prep: needs "Give 2 Wooden Sticks, 125 Sanguineous Powder, 125 Resin Tincture". We have: Wooden Sticks 282 ✓, Sanguineous Powder 250 ✓, **Resin Tincture 0 — need to craft** (likely from 26 Resin). Check recipes.csv.
10. Migrate kamis to next useful node (Q2014 prep or passive MUSU farm).

## Priority 3: After Q30 — Mina Q2014 prep

- Check `catalogs/recipes.csv` for Resin Tincture recipe. Craft 125.
- If we can't craft enough, farm Resin (Wisteria node or wherever Resin drops).
- Q2014 unlocks Q2015 (Give 9999 MUSU, rewards Pyramid Engine), which unlocks MSQ 31 (Pyramid Power).

## Priority 4: Quick wins survey (opportunistic only)

- Q3007 (Move 500): ~168/500 after session 43 (~8 hops per migration). Will accumulate during Q29/Q30 migrations.
- Booster Packs: 4 unopened. Defer to strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 12 (Scrap Confluence), 20 kamis, REST regen, 5% safety. 20/21 slots. Running since 2026-04-21 16:33 UTC.

## Quest status
- **Q29** (MSQ): Buy @ Marketplace — ACCEPTED, blocked on Gacha price decay
- **Q30** (MSQ): Give 3000 MUSU + Move to Convenience Store — awaits Q29
- **Q2014** (MIN): after Q30; needs Resin Tincture crafting
- **Q3007** (side): Move ~168/500, accumulates
- **Q6**: Liquidate — deferred

## Quest graph (MSQ critical path)
Q28✓→**Q29**(ACCEPTED, awaits Gacha buy)→Q30(Humility)→Mina Q2014→Q2015→MSQ Q31(Pyramid Power)

## Inventory highlights (session 44 perception)
- MUSU: 309,380 (growing ~1-2k/hr via auto_v2)
- VIPP: 32,628
- Ghost Gum: 1,057
- Wooden Stick: 282, Scrap Metal: 53, Pine Cone: 46
- Sanguineous Powder: 250, Black Poppy Extract: 450
- Booster Pack: 4
- Holy Dust: 1 (for future naming/soul bonding)
- "KW Maps" Data Chip: 1 (key item)

## Lessons to remember
- **Permissive scav counter extends to "2 Scav"**: Q28 = 1 roll sufficient (7-for-7 on Q21–Q28).
- **Gacha Ticket auction (item 10, via system.auction.buy)**: target 32k MUSU, current ~180k. Decay ~25%/day. Waiting 1-2 days saves 45-90k MUSU.
- **Operator movement likely takes kamis with it** — prior migrations always stopped harvests first. Don't travel without stopping auto_v2 unless testing empirically.
- **auction_buy uses OWNER wallet** (not operator). Other tools like listing_buy use operator.
- Scav rate: **~30–40 pts/hr @ 20 kamis** steady-state on normal-type nodes.
- Node 12 scav cost: observed during cycle via kami_state_slim.
- `get_scavenge_points` returns 0 (broken, known bug).
