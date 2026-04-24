# Plan for session 48

## Priority 1: Verify + complete Q37 (Harvest >720 min at Temple Cave, node 15)

Priority 0 (stranded kamis) was resolved in session 47 — all 20 kamis now RESTING/HARVESTING under a single clean auto_v2 at node 15. When session 48 opens:

1. **Perceive first.** `get_account_kamis(bpeon)` — expect most/all 20 in HARVESTING state at node 15. Any still RESTING hours after session 47's launch is suspicious: check HP + whether auto_v2 has attempted to deploy them. `get_strategy_logs` is useful here.
2. **Check Q37 completable.** `check_quest_completable(37, account="bpeon")`. With 20 kamis harvesting for 6h, HARVEST_TIME counter should be ~7200+ kami-min — way past the 720 threshold. If not completable, diagnose *why*:
   - Does HARVEST_TIME accumulate only while actively harvesting (not resting)? If so, a fresh-launch scenario with 15 kamis at low HP means their productive harvest only began 1-3h in.
   - Is the objective keyed to a specific node? Verify the quest targets node 15 specifically.
3. **Complete Q37, accept Q38.** Both small tx. Then stop + restart auto_v2 isn't necessary for Q38 — Q38 is scav-based, not harvest-based. Auto_v2 keeps running.
4. **Q38 = 7 Scav at Temple Cave (node 15).** Node 15 cost = 100/roll (cheap). Run `scavenge_claim_and_reveal(15)` as soon as points accumulate (likely 1-3 rolls possible per session). Test counter permissiveness with first roll.

## Priority 2: Q39 preview (5 Dried Stems via scavenge)

Q39 "Where It Stems From" accepts after Q38. Node 15 droptable: [1017, 1018, 11302] — **Dried Stems is item 1017 or 1018**; check `catalogs/items.csv` to confirm. If node 15 drops it, Q38 + Q39 may grind simultaneously. If not, need to find a Dried Stems node.

## Priority 3: Q40 preview (Craft 1 Timber)

Check `catalogs/recipes.csv` for Timber. Likely needs Wooden Sticks (we have 306) + other inputs. If all inputs are already in inventory, Q40 is a 2-tx finish (craft + complete).

## Active strategies
- auto_v2 on **node 15 (Temple Cave)**, 20 kamis, REST regen, 5% safety. Started 2026-04-24 15:03 UTC. Strategy ID `a0f98a64-dbba-407f-bc5e-40008550c33f`.

## Quest status (post session 47)
- **Q31–Q36 ✓** (prior sessions).
- **Q37** (Into the Depths): Harvest >720 min at Temple Cave — ACCEPTED, auto_v2 running, expected completable within ~1-3h.
- **Q38** (Feeling in the Dark): 7 Scav at Temple Cave — pending Q37.
- **Q39** (Where It Stems From): Scavenge 5 Dried Stems — pending Q38.
- **Q40** (Better Than Chopping Wood?): Craft 1 Timber — pending Q39.
- **Q3007** (side): Move accumulating passively on travel.
- **Q6**: Liquidate — deferred.

## Inventory highlights (end of session 47)
- MUSU: 319,657
- BPE: 450 (unchanged)
- Cheeseburger: 46 (was 61 — used 15 for starving-kami rescue)
- Wooden Stick: 306
- Pine Pollen: 500
- Ghost Gum: 1057 (food reserve)
- Sanguineous Powder: 125
- Booster Pack: 8 (unchanged, still unopened)
- Holy Dust: 4

## Lessons from session 47 — do not repeat
- **`stop_harvest_batch` uses `executeBatchedAllowFailure` — it silently skips failures.** After any batch stop that matters (migration, quest turn-in), read kami states to confirm each actually transitioned. Session 46 trusted the batch's "SUCCESS" return and left 15 kamis stranded for 18h.
- **`harvest_stop` needs ≥3M gas for long-accumulated harvests.** Bumped to 4M in this session (commit 23b4555). MCP server must be restarted to pick it up.
- **Starving kamis (HP=0 while HARVESTING) block `harvest_stop` with `revert: kami starving`.** Feed each (Cheeseburger 11302 = 50 HP, one is enough to clear the precondition) before attempting stop. Feed must be issued from the kami's current room.
- **5 is the max safe batch size for `stop_harvest_batch`** — ~8M gas per call fits under the RPC's eth_estimateGas simulation cap. 15-kami batches hit OOG in simulation.
- **On account wallet at start of session**: 80 stamina. Stamina regenerates over time; full travel loop (36→15, 4 hops) costs 20.

## Quest graph (MSQ critical path)
Q31✓→Q32✓→Q33✓→Q34✓→Q35✓→Q36✓→**Q37**(720 min cave, accepted)→Q38(7 Scav cave)→Q39(5 Dried Stems)→Q40(Timber)→...

## Inherited harness lessons
- Soulbound items are burnable for quest turn-ins.
- Account stamina cap ~53-61 SP; craft/travel capped accordingly.
- `craft_item(amount=N)` is gas-efficient batch crafting.
- Operator wallet vs owner wallet: trade.execute = owner; listing_buy = operator; burn = operator; craft = operator.
- `get_scavenge_points` returns 0 (broken, known bug).
- Player order book bulk buys often beat scav grinding for BPE-class items; check `list_open_sell_offers` first.
