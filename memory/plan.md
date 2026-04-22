# Plan for session 45

## Priority 0: CORRECTION — Q29 is the player-to-player order book, NOT the Gacha auction

**User (founder, top Kamigotchi player) corrected our interpretation on 2026-04-22:**
- Q29 "Computer Blues" = "Buy something in the Marketplace" refers to the **Kamigotchi World Order Book** — the in-game player-to-player trade market where players post sell offers in MUSU.
- It is **NOT** about `system.auction.buy` (GDA auction for Gacha/Reroll tickets). The `auction_buy` tool we shipped in session 44 is the wrong vector for this quest.
- The quest is **trivial**: buy ANY cheap item someone else is offering (a Pine Cone, anything). No need to wait for Gacha price decay. No expensive Gacha Ticket required.

**Abandon the Gacha-decay wait.** Execute via the order book this session.

## Priority 1: Execute Q29 — take a cheap sell offer from the order book

- **On-chain system**: `system.trade.execute` (the "taker" side). Sellers post offers via `system.trade.create` (direction = selling-items-for-MUSU, i.e. f4=0x00 in kamiden parser terms), and a buyer takes the offer via `system.trade.execute`.
- **Executor gap**: we have `create_trade` / `complete_trade` / `cancel_trade` (maker-side), but **NO `take_trade` / `execute_trade` tool yet**. Ship one this session, mirroring the pattern of `create_trade`:
  - Resolve `system.trade.execute`, define `_ABI_TRADE_EXECUTE` (inputs: `tradeID uint256`), use `_send_tx_owner` (owner wallet pays MUSU).
  - Expose as `@mcp.tool() take_trade(trade_id: str, account: str = "main")`.
- **Discovery of open sell offers**: Kamiden exposes the trade feed — `_parse_kamiden_trades` already decodes the proto. Add a thin `list_open_trades(direction="sell", account="main")` MCP tool (or reuse `get_account_trades` plumbing) that returns OTHER players' open sell offers, sorted by cheapest MUSU cost. Filter to direction=selling-for-MUSU and exclude our own account.
- **Buy target**: cheapest offer available. Pine Cone, Wooden Stick, anything ≤ a few hundred MUSU is fine. We have 309k MUSU — cost is immaterial.
- **Room requirement**: try from current room first. If it reverts, travel to room 66 (Marketplace) and retry.

## Priority 2: Complete Q29 → Q30 chain in one session

Session 45 execution flow:
1. `scavenge_claim_and_reveal(12)` — last opportunistic scav roll on node 12.
2. **Ship `take_trade` tool** (and list-open-trades helper). Commit separately before using.
3. List open sell offers, pick the cheapest item we don't already have a glut of. Call `take_trade(trade_id)`.
4. `check_quest_completable(29)` → if FALSE, `travel_to_room(66)` and retry.
5. `complete_quest(29)` + `accept_quest(30)`.
6. `travel_to_room(13)` — Mina's Convenience Store.
7. `listing_buy(1, [23101], [1])` — buy 1 Portable Burner from Mina (4000 MUSU) to satisfy Q30 "Give 3000 $MUSU". (Alt: 1 Spice Grinder = 2500 MUSU, JUST under 3000 — insufficient. Burner is safe.)
8. `check_quest_completable(30)` + `complete_quest(30)` + `accept_quest(2014)` (Mina chain).
9. Plan Q2014 prep: needs "Give 2 Wooden Sticks, 125 Sanguineous Powder, 125 Resin Tincture". We have: Wooden Sticks 282 ✓, Sanguineous Powder 250 ✓, **Resin Tincture 0 — need to craft** (likely from 26 Resin). Check recipes.csv.
10. Migrate kamis to next useful node (Q2014 prep or passive MUSU farm).

**Note**: we can keep auto_v2 running during the trade step — taking a sell offer does not require stopping kamis or moving the operator (unless room-restricted, in which case stop auto first).

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
- **Q29** (MSQ): Buy @ Marketplace — ACCEPTED, executable THIS SESSION via player order book (no Gacha needed)
- **Q30** (MSQ): Give 3000 MUSU + Move to Convenience Store — awaits Q29
- **Q2014** (MIN): after Q30; needs Resin Tincture crafting
- **Q3007** (side): Move ~168/500, accumulates
- **Q6**: Liquidate — deferred

## Quest graph (MSQ critical path)
Q28✓→**Q29**(order-book buy, trivial)→Q30(Humility)→Mina Q2014→Q2015→MSQ Q31(Pyramid Power)

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
- **"Marketplace" in quest text = player-to-player order book** (system.trade family), NOT the GDA auction (system.auction). Founder corrected this in session 45 context. Gacha/Reroll tickets are auctioned via `auction_buy`, but player-traded items (Pine Cones, raw materials, etc.) use `create_trade` / `take_trade`. Don't confuse the two again.
- **Trade system split**: `create_trade` (post offer), `complete_trade` (finalize after taker), `cancel_trade` (withdraw) are maker-side. To BUY from another player's offer, use `system.trade.execute` (taker-side) — shipped as `take_trade` in session 45.
- **Operator movement likely takes kamis with it** — prior migrations always stopped harvests first. Don't travel without stopping auto_v2 unless testing empirically.
- **Wallet split for marketplace**: `create_trade`, `complete_trade`, `cancel_trade`, `auction_buy` use OWNER wallet. `listing_buy` (NPC) uses OPERATOR. `take_trade` should mirror create/complete → OWNER wallet (MUSU escrow moves from owner).
- Scav rate: **~30–40 pts/hr @ 20 kamis** steady-state on normal-type nodes.
- Node 12 scav cost: observed during cycle via kami_state_slim.
- `get_scavenge_points` returns 0 (broken, known bug).
