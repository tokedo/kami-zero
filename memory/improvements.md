# Harness improvements

Append-only. Each entry documents a change you made to the harness so future sessions can use it without rediscovering.

Format:

```
## YYYY-MM-DD — Short title
- **What**: one-line description of the change
- **Why**: the problem it solves
- **Files**: paths changed
- **How to use**: signature or example
- **Commit**: git sha
```

---

## 2026-04-09 — Executor: better error details + optional kami_id/node_id
- **What**: `_api_post` now surfaces API error body instead of swallowing it. `start_strategy` makes `kami_id` and `node_id` optional (default 0) for multi-kami strategies.
- **Why**: 500 errors from Kamibots were opaque ("Server error '500'"). Now the agent sees the actual error message. kami_id/node_id are not needed by callers for auto_v2/rest_v3.
- **Files**: `executor/server.py`
- **How to use**: `start_strategy(strategy_type="auto_v2", config={...}, kami_id=1064, node_id=86)` — kami_id/node_id still required by API even for multi-kami strategies.
- **Commit**: 3b3fbab

## 2026-04-09 — Harvest start/stop/collect + scavenge + droptable tools
- **What**: Added 6 new on-chain tools: `harvest_start`, `harvest_stop`, `harvest_collect`, `scavenge_claim`, `droptable_reveal`, `get_scavenge_points`. Also added `_harvest_entity_id()`, `_scavenge_registry_id()`, `_scavenge_instance_id()` helpers and `_send_batch_tx()` for batch patterns.
- **Why**: No harvest or scavenge tools existed. Couldn't collect MUSU, couldn't scavenge items, couldn't progress quests. These are fundamental game actions.
- **Files**: `executor/server.py`
- **How to use**:
  - `harvest_start([43, 1064], node_index=47)` — batch start
  - `harvest_stop([43, 1064])` — batch stop with auto-collect
  - `harvest_collect([43, 1064])` — collect without stopping
  - `scavenge_claim(47)` — claim scavenge rewards (uses registry entity ID)
  - `droptable_reveal([commit_id])` — reveal droptable commits
  - `get_scavenge_points(47)` — read accumulated points + claimable tiers + tier_cost (FIXED 2026-04-27, see entry below)
- **Commit**: a1d46e9

## 2026-04-09 — NPC shop listing_buy tool
- **What**: Added `listing_buy` tool and `_ABI_LISTING_BUY` ABI for buying items from NPC merchants.
- **Why**: Quest 8 required buying from a vendor. No buy tool existed. Also needed for quest 2002 (spend 1000 MUSU at Mina's).
- **Files**: `executor/server.py`
- **How to use**: `listing_buy(merchant_index=1, item_indices=[11301], amounts=[1], account="bpeon")` — buys 1 Ghost Gum from Mina. Merchant indices: 1=Mina (room 13), 2=Vending Machine (room 18). Item indices are global (e.g. 11301, not merchant-local). Must be in the merchant's room.
- **Commit**: aa020bb

## 2026-04-10 — burn_items tool + use_account_item gas fix
- **What**: Added `burn_items` tool for burning/destroying items from inventory. Fixed `use_account_item` and `travel_to_room` item-use gas limit from default (~500k) to 1.5M — the account stamina sync in `system.account.use.item` is gas-intensive and was running out of gas at lower limits.
- **Why**: Quest 9 required burning 3 Scrap Metal (ITEM_BURN objective). Ice cream usage reverted with insufficient gas, blocking stamina restoration.
- **Files**: `executor/server.py`
- **How to use**: `burn_items(item_indices=[1005], amounts=[3], account="bpeon")` — burns 3 Scrap Metal. `use_account_item(item_id=21201, account="bpeon")` — now works reliably with 1.5M gas.
- **Commit**: d56897b

## 2026-04-11 — scavenge_claim returns commit_ids + scavenge_claim_and_reveal combo tool
- **What**: `scavenge_claim` now parses the tx receipt to extract droptable commit entity IDs and returns them in the response. New `scavenge_claim_and_reveal` tool combines claim + wait-for-block + reveal into a single call. Added `_extract_commit_ids` helper and `return_receipt` param to `_send_tx`.
- **Why**: Extracting commit IDs manually from receipt logs was painful and error-prone (required parsing MUD Store events, identifying the ScavengeClaimed event, finding the commit entity in the data payload). This was a 10-minute manual process every scavenge.
- **Files**: `executor/server.py`
- **How to use**:
  - `scavenge_claim(47)` → now returns `{"commit_ids": [12345...], ...}` in addition to tx info
  - `scavenge_claim_and_reveal(47)` → does claim + reveal in one call, returns `{"claim": {...}, "reveal": {...}, "commit_ids": [...]}`
- **Commit**: fa71cab

## 2026-04-12 — craft_item tool
- **What**: Added `craft_item` MCP tool and `_ABI_CRAFT` ABI for on-chain crafting via `system.craft`.
- **Why**: No craft tool existed. Needed to craft Pine Pollen, XP Potion, Essence of Daffodil, and Bless Potion for Mina quest chain (2009-2011).
- **Files**: `executor/server.py`
- **How to use**: `craft_item(recipe_index=6, amount=1, account="bpeon")` — crafts 1x recipe 6 (Extract Pine Pollen: 1 Pine Cone → 500 Pine Pollen). See `catalogs/recipes.csv` for all recipe indices.
- **Commit**: fc8e952

## 2026-04-13 — scavenge_claim_and_reveal handles reveal reverts
- **What**: `scavenge_claim_and_reveal` now returns a clear `reveal_skipped` message when the droptable reveal reverts, instead of propagating a confusing reverted status.
- **Why**: On some nodes (e.g., node 35), items are granted directly by the claim tx. The droptable reveal is unnecessary and reverts, wasting ~185k gas. Session 21 wasted 557k gas on 3 failed reveal retries before discovering this.
- **Files**: `executor/server.py`
- **How to use**: No change to call signature. When reveal reverts, response includes `"reveal_skipped": "reveal reverted — items likely granted directly by claim"` and `"reveal": null`. For nodes where reveal reverts, prefer calling `scavenge_claim()` directly instead.
- **Commit**: 493681a

## 2026-04-14 — name_kami tool
- **What**: Added `name_kami` MCP tool and `_ABI_NAME` ABI for naming/renaming kamis via `system.kami.name`.
- **Why**: Quest 3006 required naming a kami. No naming tool existed. Kami must be in room 11, costs 1 Holy Dust (item 11011).
- **Files**: `executor/server.py`
- **How to use**: `name_kami(kami_id=43, name="Zephyr", account="bpeon")` — names kami 43 "Zephyr". Name must be 1-16 chars, globally unique. Note: MCP server must be restarted to pick up the new tool; alternatively execute via direct Python script.
- **Commit**: 2b61683

## 2026-04-15 — harvest_start gas limit fix for new-node starts
- **What**: Increased `harvest_start` gas_limit from 1.5M to 3M per kami (both single and batch).
- **Why**: Starting a harvest on a NEW node (different from the kami's previous harvest node) requires ~900k+ gas per kami to update the harvest entity's node reference. With the old 1.5M limit, the first node-change tx hit exactly the gas ceiling and reverted as out-of-gas. This caused session 27's auto_v2 to silently fail to harvest on node 31 — it appeared ACTIVE but never started any harvests on the new node. Two hours of harvest time were lost.
- **Files**: `executor/server.py` (lines 1425, 1430)
- **How to use**: No API change. `harvest_start([43], node_index=31)` now works even when kami 43 was previously harvesting on a different node. Note: MCP server must be restarted to pick up the change.
- **Commit**: b209626

## 2026-04-22 — auction_buy tool (Gacha/Reroll Ticket via Dutch auction)
- **What**: Added `auction_buy` MCP tool and `_ABI_AUCTION_BUY` for `system.auction.buy` (GDA-priced global auction for Gacha Tickets and Reroll Tokens).
- **Why**: Q29 ("Computer Blues") requires buying at the Marketplace — room 66's Asphodel machine = the auction system. No auction tool existed; listing_buy (merchants 1 Mina / 2 Vending Machine) doesn't satisfy Q29. Also useful long-term for sustainable Gacha Ticket acquisition.
- **Files**: `executor/server.py`
- **How to use**: `auction_buy(item_index=10, amount=1, account="bpeon")` — buys 1 Gacha Ticket at current GDA price (check via `get_prices()` first; target 32k MUSU, decays ~25%/day when unbought). Item 11 = Reroll Token (paid in Onyx Shards). Uses OWNER wallet, not operator. Note: MCP server must be restarted to pick up the new tool.
- **Commit**: 418f815

## 2026-04-24 — harvest_stop gas limit bumped 2M → 4M
- **What**: Raised `gas_limit` on both single and batch variants of `harvest_stop` (and `harvest_collect` for consistency) from 2_000_000 to 4_000_000.
- **Why**: Session 47 diagnostic: 18-hour-accumulated harvests reverted OOG at exactly 1_999_573 gas (the 2M ceiling). The `system.harvest.stop` path is much more gas-intensive when the harvest has been active a long time and/or the kami has been in "starving" sub-state. 2M was insufficient — the tx reverted on success-path logic, not on a business-logic failure. This is the same failure pattern that 2026-04-15's harvest_start bump fixed (1.5M→3M). The single-call `harvest_stop` uses `executeBatched` (revert-all) so it propagates the OOG clearly; the separate `stop_harvest_batch` tool uses `executeBatchedAllowFailure` which silently skips failures — a starving/OOG kami in that batch is invisible. Session 46's "successful" migration hid behind that silent-skip.
- **Files**: `executor/server.py` (lines 1455, 1459, plus matching harvest_collect lines 1480, 1484)
- **How to use**: No API change. `harvest_stop([id])` and `harvest_stop([ids...])` now complete reliably for long-accumulated harvests. Note: MCP server must be restarted to pick up the change.
- **Commit**: 23b4555

## 2026-04-27 — get_scavenge_points fix: wrong selector + silent swallow + perception model
- **What**: Three-layer fix for the long-standing "scavenge points always 0" bug.
  1. ABI declarations for the on-chain Value/State components (`_STRING_VALUE_ABI`, `_UINT_VALUE_ABI`, `_UINT32_VALUE_ABI`, `_ID_COMPONENT_ABI`) renamed `getValue(uint256)` → `get(uint256)`. The kamigotchi-context docs say `getValue`, but the deployed contracts on Yominet expose `get`. The wrong selector reverted on every call.
  2. `get_scavenge_points` no longer swallows reverts as "0 points". It now reads `tier_cost` from the registry, checks `has()` on the instance, and returns `{points, tier_cost, claimable_tiers, remainder, ...}` so the agent has ground truth, not a model.
  3. `get_quest_status` call site updated to use `.get(...)` instead of `.getValue(...)`.
- **Why**: kami-zero had been flying blind on scavenge points for the entire 50+ session run. To compensate, it built a theoretical model ("~6 pts/hr, first roll at ~83h elapsed") that was off by ~150x — actual rate is "harvest output ≈ MUSU/h", roughly 1,000 pts/hr at node 16. Sessions 49, 50, 53, 54 all *deliberately skipped* cheap probe attempts because the model said they would revert, while in reality bpeon had 78 unclaimed tier rolls sitting at node 16 (and 4 leftover at node 77). The skip-the-probe discipline self-reinforced the hidden bug.
- **Files**: `executor/server.py`
- **How to use**: `get_scavenge_points(16, "bpeon")` → returns `{"points": 39368, "tier_cost": 500, "claimable_tiers": 78, ...}`. Always read this BEFORE deciding whether to scavenge_claim. Drop the "rate model" — it was wrong and is no longer needed.
- **Lesson**: When perception returns a too-clean default value (0, "", null) that masks reverts, the silent default *is* the bug. Failing loud beats failing silent. Also: when an agent's mental model is built on a single-point extrapolation (one observed claim at one node at one elapsed time), suspect the model.


## 2026-04-27 — get_scavenge_droptable: correct exponential drop probabilities
- **What**: New async MCP tool `get_scavenge_droptable(node_index, account)`. Reads on-chain `component.keys` (uint32[]) and `component.weights` (uint32[]) for the node's ITEM_DROPTABLE entity, computes `prob_i = 2^weight_i / sum(2^weight_j)`, returns rich dict with item names, weights, probabilities, and `expected_per_100_tiers`. Also added `_UINT32_ARRAY_ABI` for reading uint32[] arrays via safeGet.
- **Why**: The on-chain "weights" field for droptables uses an exponential rarity model, NOT linear-pick. kami-zero (and the kamigotchi-context CSV/API surface) treated `[9,7,7,5]` as linear shares totaling 28, predicting Hearing at 5/28 = 18%. Reality: `2^5 / (2^9 + 2^7 + 2^7 + 2^5) = 32/800 = 4%`. Founder verified the 4% number in-game. Same multi-x error applied to every prior scav-rate estimate (Honeydew, Bone Chunk, Resin, etc.). Discovery context: session 55 returned only 2 Hearings from 78 rolls (vs 14 expected at 18%), prompting investigation that led to this fix.
- **Files**: `executor/server.py` — new helper + new tool placed next to get_scavenge_points.
- **How to use**: `get_scavenge_droptable(16, "bpeon")` → returns droptable with each item's correct probability. Use BEFORE planning any scav grind. Combine with `get_scavenge_points(node)` to compute tier-budget for a target item count: `expected_tiers = items_needed / probability`.
- **Lesson**: When docs/CSV expose a numeric field with an ambiguous label ("weights", "tiers"), verify the implied formula against observed data BEFORE building a multi-day strategy on it. Session 55's empirical 2/78 Hearings was the canary; it took an external signal (founder check) to surface the bug. The kami-oracle-bootstrap docs should add a section explicitly stating "drop weights are exponents of 2".

## 2026-04-27 — stop_harvest_batch: per-kami silent-skip detection
- **What**: After the `executeBatchedAllowFailure` tx commits, `stop_harvest_batch` now reads each kami's `harvest entity` `component.state` via `safeGet` (ACTIVE = still harvesting / silent-skip; INACTIVE = stopped) and returns a `per_kami: {kami_id: {harvest_state, stopped, [error]}}` map plus `stopped_count` and `failed_count`. The status reflects on-chain truth, not just the tx-level success that `executeBatchedAllowFailure` always reports.
- **Why**: Session 46 (2026-04-24) burned ~18 hours of harvest because 15 starving kamis were silently skipped by `executeBatchedAllowFailure` — the wrapper reported "SUCCESS Gas 5.39M+9.60M" while the kamis kept harvesting. The agent had no signal to verify; the next-session inventory check finally exposed it. Session 56 (firing 16:48 UTC) is about to call this tool to flush Q44 across 20 kamis, so a regression here would block the MSQ chain.
- **Files**: `executor/server.py` — extended `stop_harvest_batch` body, kept signature unchanged.
- **How to use**: Call `stop_harvest_batch([kid1, kid2, ...])` as before. Inspect `result["per_kami"]` to find any kami with `stopped: false` and retry just those. `result["failed_count"]` is the quick health-check.
- **Lesson**: Any function using `executeBatchedAllowFailure` (or any other revert-swallowing batch primitive) MUST verify the resulting state. Silent-skip as a UX feature is fine, but undetected silent-skip is a 18-hour bug. Apply this pattern to other `*_batch` tools too.
