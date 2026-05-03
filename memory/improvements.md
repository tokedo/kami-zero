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

## 2026-04-30 — Tier-1 quest tooling: quest_state + get_expected_objective + get_active_quests fix
- **What**: Three additions, one fix.
  1. `quest_state(quest_index, account)` — discriminated read returning `state` ∈ {`not_accepted`, `active_blocked`, `active_ready`, `completed`} plus `revert_kind` ∈ {`none`, `objs_not_met`, `not_active`, `other`} plus raw `revert_reason`. Uses `component.id.quest.owns.safeGet`, `component.is.complete.has`, and the `system.quest.complete` staticCall. Replaces the stale-string-only `get_quest_status`.
  2. `get_expected_objective(quest_index)` — reads `catalogs/quests/quests.csv` + `objectives.csv` (loaded at module init), returns the catalog-expected objective list ({description, type, delta_type, operator, index, value}) plus title and rewards. Surfaces the catalog as a *hypothesis*, not chain truth — explicitly so a future agent can compare and detect drift.
  3. `get_active_quests` now reads `component.is.complete.has(qid)` for each owned quest and returns `owned_count`, `completed_count`, `truly_active_count`, with per-quest `completed: bool`. `active_quest_count` kept as a back-compat alias (== `owned_count`); future callers should prefer `truly_active_count`.
  4. `_classify_revert(reason)` helper for substring → category mapping (used by `quest_state` and reusable by future quest tools).
- **Why**: Q49 has been blocked for 4 sessions. Gas-based hypothesis testing was costing ~2-18M gas per session with no progress. The new tools shift Q49 (and any future stuck quest) from "burn gas to probe objective type" to "compare catalog vs chain in zero gas — if catalog-expected objective is already-satisfied per local state but chain disagrees, escalate". Founder authored the plan; implementation matches plan verbatim.
- **Files**: `executor/server.py` (catalog loader + 2 new tools + 1 rewritten tool), `executor/tests/test_quest_state.py`, `executor/tests/test_expected_objective.py`, `CLAUDE.md` (added "Quest debugging discipline" + "Force-flush gas budgeting" sections).
- **How to use**:
  - `quest_state(49, "bpeon")` → state="active_blocked", revert_kind="objs_not_met" (Q49 baseline this session).
  - `get_expected_objective(49)` → DROPTABLE_ITEM_TOTAL[1018]≥15.
  - Compare: catalog says ≥15 butts; inventory has 134 butts; chain still rejects → escalation territory per the new CLAUDE.md discipline rule.
  - **MCP server must be restarted to expose the new tools.** Until restart, reach them via direct python: `executor/.venv/bin/python -c "import sys; sys.path.insert(0,'.'); import server; print(server.quest_state(49,'bpeon'))"` (already used this session for Priority 0b verification).
- **Tests**: `cd executor && .venv/bin/python -m unittest tests.test_quest_state tests.test_expected_objective` — 6/6 pass against bpeon's known Q48/49/50 state.
- **Commit**: b22935c

## 2026-05-01 — Predator-mode tooling gaps (session 73) — proposal-only

This is a tooling inventory for the new PREDATOR chapter. **No code changes this session** — just an audit of what's missing and what building each gap would require. Founder reviews and authorizes builds in a future session prompt.

Audit basis: read of `executor/server.py` MCP tool surface. Existing tools relevant to predator mode are read-only:
- `get_killer_ranking` — top predators by kill count (cached 1h, kamibots playwright endpoint)
- `get_all_kamis` — full population with violence/attack bonuses/equipment for threat modeling
- `get_nodes` — all nodes with kami counts
- `get_kami_state_slim` / `get_kami_state` — per-kami HP/stats/skills
- `oracle_sql` — historical action stream including `harvest_liquidate` rows (mentioned in oracle_sql docstring as ~13% no-op; the action exists)
- `oracle_kami_summary` — per-kami action histogram
- `oracle_top_nodes` — node activity ranking

### Gap 1 — `liquidate(target_kami_id, attacker_kami_id)` MCP tool: NOT PRESENT
- **Closest primitive**: none. No `attack`, `kill`, `liquidate`, or `combat` symbol anywhere in `executor/server.py`. The action *exists on-chain* — oracle records it as `harvest_liquidate` action_type — so a system call must exist (probably `system.harvest.liquidate` or `system.kami.attack`; needs lookup against `integration/ids/systems.json`).
- **Building it requires**: (a) discover the system ID + ABI for the on-chain call (signature, params: attacker_kami_entity_id + target_kami_entity_id at minimum, possibly node_id, possibly more), (b) gas tuning — probably similar order to `harvest_stop` (1.5–4M); the in-flight harvest accumulator settlement is the gas-heavy part, (c) returns a structured result: tx hash, gas used, obols gained, musu gained (if any), counter-strike damage taken (if any), target's post-tx state.
- **Pre-req before build**: fill in `predator/mechanics.md` with the system-name discovery + a successful staticCall against a sandbox target. Doctrine ("data work, not movement") implies we should not ship this tool before we understand the formula it embodies.

### Gap 2 — `scan_node_for_targets(node_index)` read tool: NOT PRESENT but COMPOSABLE
- **Closest primitive**: `get_nodes` lists per-node kami counts but not identities. `get_all_kamis` returns the full population including current room/node. Cross-join is doable.
- **Composable from**: `get_all_kamis` (filter by `node_index` and `state == "HARVESTING"`) + `get_kami_state_slim(kami_id)` per candidate (HP/level/owner) + `oracle_sql` (recent kill counts on node, target's recent activity for "starving" detection — H2 in `predator/targeting.md`) + `predator/guild-no-touch.csv` filter.
- **Building it as a single tool would**: avoid the fan-out cost in main-context tokens, return a ranked list `[{kami_id, kami_index, owner_handle, owner_account_id, hp_pct, level, on_node_minutes, last_owner_action_at, in_guild_no_touch}]`. The ranking is doctrine-laden (which targets are "good"?), so possibly leave ranking to the agent and just return the enriched list.
- **Pre-req before build**: doctrine maturity — once `predator/targeting.md` heuristics are verified, hard-code the safe filters (drop guild members, drop high-counter-attack threats) and let scoring be data-side.

### Gap 3 — `predict_strike(attacker_kami_id, target_kami_id)` predicate: NOT PRESENT
- **Closest primitive**: none. Counter-predator math — "will our HP after the kill stay above their liquidation threshold for our weakest kami on the node?" — has no harness support today.
- **Building it requires**: the obol/damage/HP-cost formula from `predator/mechanics.md`, plus `get_kami_state_slim` reads of attacker + target + "weakest other kami of ours on node". Pure read-side, no tx.
- **Pre-req before build**: `predator/mechanics.md` must contain the verified formula. Until then, this predicate is unbuildable.

### Gap 4 — Guild-roster gate: NOT PRESENT (load-bearing safety)
- **Current state**: `predator/guild-no-touch.csv` exists (founder-shipped, 82 handles, account_ids being resolved this session in P5b). Nothing in `executor/server.py` reads it.
- **Proposed minimum**: a small helper `predator_safety.is_target_protected(account_id, handle, csv_path="predator/guild-no-touch.csv")` that loads the CSV (with mtime cache), checks the file's `Updated:` line is ≤ 7 days old (hard-fail if stale → "deny all"), matches by `account_id` if non-empty else by handle, returns `(blocked: bool, reason: str)`.
- **Wired into**: any future `liquidate(...)` tool — call `is_target_protected` first, abort if `blocked`. Also expose as a standalone tool so the agent can pre-filter scan results.
- **Hard rule per CLAUDE.md**: file missing or stale → deny-all. The wrapper must enforce this — not the agent. This is the bright line; encoding it in code (not memory) is mandatory before the first liquidation tx ever fires.

### Other observations
- `harvest_liquidate` appears in oracle action-type vocabulary, but no oracle helper enriches it (no view, no per-event helper). `get_killer_ranking` is the only existing predator-flavored read and it's a cached aggregate, not raw events. → P3 in `ideas_to_founder.md` (oracle predator views) is the right home for that ask, not the executor.
- `get_guild_members(account)` exists — returns the kamibots-API `friendAccountNames` so guild-mates don't attack each other. **This is a different list** from the founder-curated `guild-no-touch.csv` (which encompasses the broader GUILD-tier alliance, not just the same-account-cluster). Both lists need to filter targets; `is_target_protected` should check both.
- No "obol balance" read exists. `get_inventory` may already include obol if it's an item. Check before building anything obol-specific. (Inventory-fetch attempt deferred to a non-prep session.)

### What this session does NOT do
- Build any of the above. Founder authorizes builds in a future session prompt.
- Touch `harvest_liquidate` or any predator tx — no on-chain action this session.



- **What**: Documented dead-end (NOT a code change). `component.id.parent` (keccak hash `0xbca01f994221da3049c3ee687ab5c6a1ebf40f2011941d5581d9cd500fdf2cd0`, present in `integration/ids/components.json`) is **not registered in the deployed World contract**. `_resolve_component('component.id.parent')` in `executor/server.py` raises "Component not found on-chain". Tried alternative names: `component.parent`, `component.parent.id`, `component.id.holder`, `component.id.from`, `component.id.target`. Of these only `holder`, `from`, `target` resolve, but none of them link objective entities → quest entities (verified by reverse-lookup attempts using `getEntitiesWithValue`).
- **Why**: This blocks reading on-chain quest objective configuration. Session 68 needed to inspect Q49's objective type/target/handler to disambiguate between SCAV_CLAIM_NODE / DROPTABLE_ITEM_TOTAL / ITEM_BURN / ITEM_TOTAL. Forced to fall back on empirical hypothesis testing (burn 15 butts, observe Q49 state — gas cost ~807k just to disprove ITEM_BURN).
- **Status**: Unsolved. Possible causes: (a) the parent component was never deployed at this World instance even though it's in the upstream IDs file; (b) parent linkage uses a different convention here (maybe the registry encodes objective-parent via a string-typed component or via a different naming scheme).
- **Files**: None changed. This is a research note.
- **DO NOT REPEAT**: Future sessions: do not re-spawn the parent-component lookup. If you need objective-config, either (1) try the off-chain indexer (if any becomes available), (2) read open-source MUD system code to find the correct creation pattern, or (3) keep using empirical probes as in session 68.
- **`debug_traceCall` is also unavailable** on the RPC endpoint — can't trace the staticCall revert path.

## 2026-05-02 — Liquidate MCP tool + guild-no-touch gate
- **What**: New `liquidate(target_kami_id, attacker_kami_id, account, target_account_id?, target_handle?)` MCP tool. Submits `system.harvest.liquidate.executeTyped(uint256 victimHarvestID, uint256 killerKamiID)` with the GDD-required 7.5M gas limit. In-code guild gate loads `predator/guild-no-touch.csv`, parses `# Updated: YYYY-MM-DD` header, denies all if missing or > 7 days old, matches by account_id (preferred) else handle (case-insensitive). Cache invalidates on file mtime change.
- **Why**: Predator hard rule #1 — never liquidate guild members. Doctrine says "encode in code, not memory". Also: liquidate is the central PvP action and was completely absent from the executor; nothing else in the predator playbook works without it.
- **Files**: `executor/server.py` (added `_ABI_HARVEST_LIQUIDATE`, `_GUILD_NO_TOUCH_PATH`, `_GUILD_NO_TOUCH_CACHE`, `_load_guild_no_touch()`, `_is_target_protected()`, `liquidate(...)` async tool; added `import datetime`).
- **How to use**:
  - `liquidate(target_kami_id=3764, attacker_kami_id=12649, account="bpeon")` — gate runs, target owner resolved via Kamibots API; tx submitted if unblocked.
  - Pre-resolved owner skips API call: `liquidate(..., target_account_id="538526...", target_handle="rtvvvvv")`.
  - Returns `{tx_hash, status, block, gas_used, blocked?, reason?, target/attacker fields}`. `status` will be `'reverted'` for contract-side denies (e.g. "kami lacks violence (weak)"); inspect via `eth_call` replay to recover the revert reason.
  - Both kamis must be HARVESTING on the same node, attacker not on cooldown, attacker HP > 0, AND the threshold formula must yield `target_current_HP < threshold` (see `predator/mechanics.md`).
- **Restart needed**: yes — running MCP server picks up new tool only after restart. For session 76 the tool was invoked via direct `python -c "import server; asyncio.run(server.liquidate(...))"` to avoid the restart round-trip.
- **Commit**: (this session's harness commit)

## 2026-05-02 — HP projection module + back-fit validator

- **What**: Pure-python HP projection (`executor/hp_projection.py`, 433 LOC) and a back-fit validation script (`executor/scripts/backfit_liquidations.py`).
- **Why**: 8 sessions of guess-at-HP striking burned 70M+ gas with 0 kills. Founder mandate: HP must be COMPUTED from canonical formulas + back-fit-validated against historical liquidations before any strike.
- **Files**:
  - `executor/hp_projection.py` — `compute_current_hp(...)` (HARVESTING/RESTING/DEAD branches), `kill_threshold(...)`, `harvest_efficacy(...)`, `strain_from_bounty(...)`, `projected_recovery(...)`, `max_hp(...)`. No chain dependencies — pure python, suitable for unit testing and back-fitting.
  - `executor/scripts/backfit_liquidations.py` — validates the projection against historical liquidations. Two modes: `formula` (canonical Fert+Int projection) and `empirical` (use actual oracle collect data + per-collect ceil strain).
- **How to use**:
  - Live projection: read victim's `health.sync` and `harvest.bounty.balance` from `get_kami_state`, then `compute_current_hp(state="HARVESTING", sync_hp=..., bounty_pool_now=<live balance>, harmony=v.total_harmony, strain_boost=v.strain_boost, ...)`. The `bounty_pool_now` arg drives confidence to 0.95 (validated path).
  - Kill threshold: `kill_threshold(attacker_violence=..., victim_harmony=..., victim_max_hp=..., atk_threshold_shift=..., def_threshold_shift=..., def_threshold_ratio=...)`. Strike fires only if `compute_current_hp.projected_hp < kill_threshold.kill_zone` by margin ≥ 5 HP.
  - Re-validate certificate: pull a fresh 7d window of liquidations from oracle (template SQL in the back-fit script header), save JSON dump, run `python3 executor/scripts/backfit_liquidations.py <dump.json> empirical 1.0`. If accuracy drops below 90%, formula has gaps — investigate before striking.
- **Validation certificate (session 84)**: N=200, M=199, accuracy 99.5% on 7d window 2026-04-25→2026-05-02. Recorded in `predator/mechanics.md` § "Validated HP projection". Single miss (v_idx=12629, 117s elapsed) consistent with REVIVE mid-cycle entry — out-of-model edge case.
- **Commit**: (this session's harness commit)

## 2026-05-02 — Oracle-only world-state primitives (`oracle_state.py`)

- **What**: New module `executor/oracle_state.py` (615 LOC) implementing oracle-only state-read primitives that replace kamibots playwright reads in the predator-decision path. Founder structural rule (2026-05-02): all world-state reads come from oracle.
- **Why**: kamibots playwright cache returned stale data (sync_hp=220, balance=0) for kami 16479 when ground-truth chain state was HP=29, pool=1674. Founder mandate: kamibots is forbidden for world-state reads in kami-zero — oracle is the single source of truth.
- **Files**:
  - `executor/oracle_state.py` (new) — `oracle_kami_state(kami_index)` composite read; `reconstruct_bounty_pool(kami_index)` live pool projection from action stream; `resolve_target_owner(kami_index)` replaces playwright owner lookup; helpers `oracle_sql_sync`, `_harvest_efficacy`, `_bounty_integral`. Module imports `httpx` directly (does not touch `server.py` to keep dependency acyclic).
- **How to use**:
  - Predator targeting: `from executor.oracle_state import oracle_kami_state; ks = oracle_kami_state(16479)` — returns `KamiState` dataclass with `sync_hp_at_last_touch`, `bounty_pool_now`, `harvest_start_ts`, `n_feeds_since_start`, `node_id`, `node_affinities`, all skill bonuses, `freshness_warnings`, `confidence`. Pipe straight into `compute_current_hp(...)` and `kill_threshold(...)`.
  - Owner gate: `resolve_target_owner(kami_index)` returns `{account_id, handle, ...}` for the no-touch CSV match. No playwright call.
  - Smoke test: `executor/.venv/bin/python executor/oracle_state.py 16479` — prints full `KamiState` JSON.
- **Calibration**: default `strain_calibration=1.5` (×1.5 multiplier on raw formula pool, internalizes the back-fit's ~1.4× under-projection bias). Cross-check on kami 16479: raw pool 1196 MUSU, ×1.5 calibrated 1795, ×1.4 calibrated 1675 (vs founder's chain-truth 1674 — exact match at ×1.4). Default is conservative (stricter strike gate); change to 1.4 if more aggressive striking is desired.
- **Validation certificate (session 87 re-run)**: N=495, M=493, accuracy **99.6%** on 7d window 2026-04-25→2026-05-02 via `executor/scripts/backfit_liquidations.py empirical 1.0`. Beats the ≥99.5% gate. Recorded in `predator/mechanics.md` § "Validated HP projection — Session 87 re-validation". Same miss class as session 84 (REVIVE mid-cycle entry).
- **Commit**: (this session's harness commit)

## 2026-05-02 — Kamibots state-read audit (session 87)

`executor/server.py` audited for `_api_get` call sites (kamibots playwright reads). Classification per session-87 plan:

| Class | Count | Examples | Action |
|---|---|---|---|
| **A — World-state, MIGRATE** | 13 | `get_inventory` (1217), `get_kami_state*` (1227,1234,1238,1245), `get_kamis_progress_batch` (1249,1265), `get_killer_ranking` (1377), `get_leaderboard` (1391), `get_all_kamis` (1402,1413), `get_nodes` (1417,1423), `get_account_kamis` (1427), `liquidate` owner resolution (1710) | Replace with `oracle_state.py` calls. Mark kamibots versions DEPRECATED in code comments next session. |
| **B — Control plane, LEAVE** | 6 | `get_all_strategies` (1308,1314), `get_strategy_status` (1332,1339), `get_strategy_logs` (1343,1353), `get_tier` (1207,1213) | Allowed. Auto_v2 strategy management on harvester accounts is in scope for kamibots. |
| **C — Quest-paused, leave** | 4 | `level_to` (2248), `level_and_allocate_batch` (2336), `get_scavenge_droptable` (3552), `listing_buy` paths | Quest-paused; not predator-decision path. No migration needed. |
| **D — Diagnostic / one-off** | 2 | `get_guild_members` (1318,1328) | Acceptable as fallback for guild roster discovery; not on hot strike path. |

Migration sequence (next session, separate PR scope):
1. Rewrite `liquidate()` pre-flight to use `oracle_state.resolve_target_owner` instead of `_api_get_kami(...)`.
2. Rewrite `get_kami_state` → thin wrapper over `oracle_state.oracle_kami_state` for predator callers (keep raw kamibots version under a `_legacy_*` name for kami-agent control plane).
3. Add a server-level guard: any tool decorated `@predator_only` rejects internal `_api_get*` calls in its call graph.
- **Commit**: (this session's session commit; audit doc-only, no code changes yet)

## 2026-05-02 — Bug 3: harvest_efficacy single-slot constraint (session 88)

- **What**: Fixed `harvest_efficacy()` in both `executor/hp_projection.py` and `executor/oracle_state.py` to enforce **single-slot constraint** on dual-affinity nodes. Both body and hand affinity now check against the SAME single node-affinity slot (the one that maximizes overall efficacy), instead of independently picking their best-matching slot. Previously, on a dual-affinity node like 86 (EERIE-INSECT), a kami with body=EERIE/hand=INSECT would erroneously claim +650 (body match EERIE) AND +350 (hand match INSECT) = 2000, when the canonical rule yields 1550 (body match EERIE + hand mismatch non-NORMAL=-100, picking the EERIE slot).
- **Why**: Cross-check on kami 16479 in session 88 showed harness predicted efficacy=2000 vs founder client truth 1550. Bug was masked in the back-fit cert (99.6%) because the empirical-mode fit uses oracle collect data directly, not the formula path. Bug surfaces in formula-mode HP projection (forward-projection of bounty pool when no live read available).
- **Files**:
  - `executor/hp_projection.py` — `harvest_efficacy()` enumerates each unique node affinity slot, computes `1000 + body_comp(slot) + hand_comp(slot)`, returns the max.
  - `executor/oracle_state.py` — `_harvest_efficacy()` mirrors the same single-slot logic.
- **How to use**: No API change. Existing `compute_current_hp(...)` and `oracle_kami_state(...)` callers benefit transparently.
- **Validation**: Founder cross-check on 5 calibration kamis [16479, 12386, 12293, 12728, 15042] now matches client truth at **mean 0.40 HP / 0.12% pool error** (post Bug 1+2+3 fixes, no `×1.4-1.5` calibration multiplier).
- **Commit**: (this session's harness commit)

## 2026-05-02 — KAMI_LIQ_* on-chain config reader (session 88)

- **What**: Verified KAMI_LIQ_ANIMOSITY = `[_,400,_,3,_]` and KAMI_LIQ_THRESHOLD = `[_,1000,_,3,_]` (packed int32[8] decoded MSB-first from uint256, indices 1 = ratio/base, 3 = precision_exponent). Read via `component.value.safeGet(keccak256("is.config" || configName))`.
- **Why**: Plan Priority 3b required validating empirical kill_threshold formula against canonical formula derived from on-chain config. Result: empirical (99.60%) beats canonical-as-derived (98.18%) on N=495 corpus. Likely a precision-exponent interpretation issue; empirical retained as operational formula.
- **Files**: `predator/mechanics.md` § "Cached on-chain KAMI_LIQ_* config" — cached values + canonical-vs-empirical accuracy table.
- **Reader script** (one-off, kept in /tmp for repro): `/tmp/read_liq_config.py` — `from web3 import Web3; entity = int.from_bytes(Web3.keccak(b"is.config" + name.encode()), "big"); val_comp.functions.safeGet(entity).call()`.
- **Commit**: (this session's session commit; mechanics-doc-only)

## 2026-05-02 — Canonical kill_threshold (session 89, founder calibration 6/6)
- **What**: Replaced `kill_threshold()` in `executor/hp_projection.py` with the canonical formula `animosity × efficacy + atk_shift − def_shift` (where `animosity = Φ(ln(V/H)) × 0.4`). Implemented `_liq_affinity_shift()` with the rock-paper-scissors triangle (EERIE>SCRAP>INSECT>EERIE), NORMAL=+0.2, same=0, strong=+0.5, weak=-0.5. Implemented ratio-bonus gate: `atk_ratio`/`def_ratio` apply only when `affinity_shift ≥ 0` (weak matchups stuck at base 0.5x). Added `animosity_ratio: float = 0.4` parameter.
- **Why**: Empirical formula passed session 84's 99.6% back-fit but had three structural defects (missing × 0.4 on animosity, stubbed `_liq_affinity_shift`, wrong combination topology) that partially canceled for middle-of-the-road stats. Founder cross-checked the canonical formula against the kamigotchi team's official liquidation calculator: 6/6 match across all matchup types. The empirical's apparent accuracy was self-consistent with broken HP projection (which itself got fixed in session 88) — calculator wins over corpus.
- **Files**: `executor/hp_projection.py` (kill_threshold + _liq_affinity_shift + _LIQ_BEATS), `executor/scripts/backfit_liquidations.py` (now passes `attacker_hand`/`victim_body` to kill_threshold).
- **How to use**: `kill_threshold(attacker_violence=34, victim_harmony=22, victim_max_hp=260, atk_threshold_shift=300, atk_threshold_ratio=500, def_threshold_shift=200, def_threshold_ratio=0, attacker_hand="NORMAL", victim_body="EERIE")` → `{"kill_zone": <int>, "animosity": <float>, "efficacy": <float>, ...}`. Strict `<` gate: strike succeeds iff `projected_hp < kill_zone`.
- **Cert**: N=495, M=492, 99.40% on 7d back-fit corpus (down 0.20pp from empirical's 99.60%, but per plan 89 — calculator wins). The 3 misses are floor edge cases on weak matchups with large `def_shift`.
- **Commit**: (this session's harness commit, see git log)

## 2026-05-02 — Calibration regression test (6 founder cases)
- **What**: New file `executor/tests/test_kill_threshold_calibration.py` — 6 test cases mirroring the founder's calibration table. Each asserts exact match on death-below HP ∈ {54, 86, 28, 80, 57, 98}.
- **Why**: The 6 cases span all matchup geometries (weak + atk_ratio gate test, strong unbonused, weak unbonused, special + atk_ratio, special + def_ratio, strong + atk_ratio). Any future kill-formula change must preserve all 6. This is the new regression bar.
- **Files**: `executor/tests/test_kill_threshold_calibration.py` (new).
- **How to use**: `python executor/tests/test_kill_threshold_calibration.py` — exits 0 if all 6 pass, 1 otherwise.
- **Commit**: (this session's harness commit)

## 2026-05-02 — System Thinking doctrine in CLAUDE.md (session 89, founder framing)
- **What**: New doctrine block "System Thinking — you're not a session, you're a system" inserted into CLAUDE.md immediately above "Operational Mode: PREDATOR". Includes founder framing quote, trigger checklist (3+ repeated queries, re-derived answers at session start, etc.), in-scope infrastructure list (background watchers, pre-computed indices, A/B test infra, dashboards), cron access pointer (agent can write its own crontab entries), and the "metric is the regulator" loop.
- **Why**: Founder directive 2026-05-02: formula correctness is necessary but not sufficient; next leverage is for kami-zero to think of itself as a system it owns and improves, not as the operator of any single session. Compute is no longer constrained (Max plan); the 24/7 VM is for persistent processes, indices, caches, watchers.
- **Files**: `CLAUDE.md` (new block above PREDATOR section).
- **How to use**: Read at session start as part of perception phase. Triggers a build whenever a repeated-query / re-derived-answer pattern is detected.
- **Commit**: (this session's session commit)

## 2026-05-02 — world_targets.json background refresher (System Thinking unlock)
- **What**: 5-min cron-driven scanner that snapshots HARVESTING victims across 8 hot-list nodes, applies guild + heal-event + soft-no-touch filters, projects HP via canonical formulas (`executor/hp_projection.py`), computes per-striker margin, atomic-writes to `predator/world_targets.json`.
- **Why**: Sessions were re-deriving the world view at session start (~30-60s of repeated oracle scans). Now a 2-3s background scan precomputes and sessions read the cache. Compounding leverage per System Thinking doctrine — first concrete infra build of the doctrine.
- **Files**: `predator/scripts/refresh_world_targets.py`, `predator/infrastructure.md`, `predator/world_targets.json` (output, regenerated every 5 min).
- **How to use**:
  ```python
  import json
  with open("predator/world_targets.json") as f:
      snap = json.load(f)
  for c in snap["killable_clean"][:10]:  # margin >= +5, no guild, no soft-no-touch, no feed
      print(c["v_idx"], c["v_acct"], c["node_id"], c["margin"], c["striker_idx"])
  ```
  Stale-check via `snap["generated_at"]` (ISO 8601 Z); if older than 10 min, refresh inline.
- **Cron**: `*/5 * * * * /usr/bin/python3 /home/anatolyzaytsev/kami-zero/predator/scripts/refresh_world_targets.py >/tmp/world_targets_cron.log 2>&1`
- **Hot-list update**: edit `HOT_NODES` in script. Striker roster: edit `STRIKERS` constant; refresh on respec.
- **Commit**: 6d346be

## 2026-05-03 — Watcher: dead-kami harvest_id filter
- **What**: Added `killed_harvests` CTE in `predator/scripts/refresh_world_targets.py` that pulls all `harvest_id` from recent `harvest_liquidate` actions, then filters open harvests via `WHERE hs.harvest_id NOT IN (SELECT harvest_id FROM killed_harvests)`.
- **Why**: `harvest_liquidate` rows have NULL `target_kami_id` — only the victim's `harvest_id` is preserved. Victim's own action stream shows no terminating event after kill, so the watcher's `last_actions` CTE incorrectly picked up `harvest_start` as the latest action even after the kami was killed. Session 91 kills (6104, 6505) appeared as alive with margins +94/+51 in session 92's snapshot, almost causing a wasted strike sequence.
- **Files**: `predator/scripts/refresh_world_targets.py`
- **How to use**: Watcher runs every 5 min via cron. No callsite change. Re-validation: post-fix node 73 killable went 6→2 (correctly excluded 4 dead Yeahta kamis from sessions 91+92).
- **Commit**: (this session)

## 2026-05-03 — Watcher heat-check (per-owner defensive-cycle detection)
- **What**: Added `owner_heat_check()` to `predator/scripts/refresh_world_targets.py`. For every owner appearing in the candidate pool, queries oracle for 6h action stream and computes minutes_idle, distinct_kamis_5min, distinct_kamis_60min, bulk_stop_windows_6h. Marks `defensive_cycle: bool` per Plan-104 P0 v2 criteria. Adds `killable_v2` field (heat-check filtered) and per-owner `owner_heat` map.
- **Why**: Sessions 102-104 each ran the same stefan97 6h bulk-stop drill. System Thinking trigger (3+ same-derivation = build). Previously, 17/31 of `killable_clean` was stefan97 noise; the heat-check pre-filters this. Real test: 31 killable → 2 after filter; 15 defensive owners auto-suppressed.
- **Files**: `predator/scripts/refresh_world_targets.py`.
- **How to use**:
  ```python
  import json
  with open("predator/world_targets.json") as f: snap = json.load(f)
  # Use heat-check filtered list (defensive owners removed):
  for c in snap["killable_v2"][:10]:
      print(c["v_idx"], c["v_acct"], c["margin"], c["heat"])
  # Inspect owner heat directly:
  print(snap["owner_heat"]["stefan97"])  # {minutes_idle, bulk_stop_windows_6h, defensive_cycle, ...}
  ```
- **Next session reads**: prefer `killable_v2` over `killable_clean` for first-pass strike candidate selection. Cross-reference `owner_heat` for nuance when needed.
- **Commit**: 86b0fa4

## 2026-05-03 — refresh_world_targets.py: HOT_NODES expansion 8 → 17
- **What**: Expanded the watcher's hot-list scan from 8 nodes to 17 covering more SCRAP/EERIE/INSECT/NORMAL biomes. Dropped dead node 30 (1 row/24h). Added 16, 88, 89, 10, 15, 83, 33, 76, 35, 34.
- **Why**: Plan-106 P4 build-ask. Heat-check noise-suppression (added session 104) makes wider scans cheap. Hypothesis confirmed: a single expansion immediately surfaced 24 above-gate candidates at node 34 (Deeper Into Scrap) that were previously invisible. Session 106 converted +3 kills (margins +97/+87/+85) directly from the build.
- **Files**: `predator/scripts/refresh_world_targets.py` (HOT_NODES list)
- **How to use**: Watcher cron now scans 17 nodes per cycle. Scan duration grew 2.95s → 5.01s — well within the 5-min cron budget. `killable_v2` candidate count expanded 1 → 38 in production-validation run.
- **Commit**: (this session)

## 2026-05-03 — Watcher: sync-stop burst detector (anti-predator automation)
- **What**: Extended `predator/scripts/refresh_world_targets.py` heat-check with `sync_stop_bursts_6h` (count of clusters where 3+ kamis are harvest_stop'd by the same owner within a 5-second window over the last 6h) + `anti_predator_automation` flag (true if `sync_stop_bursts_6h ≥ 1`). Added `ANTI_PREDATOR_WATCH = {aenne, stefan97, stefan96, foden, dias, rtvvvvv}` always heat-checked even when no candidates in pool. Fixed case-mismatch: SQL now LOWER()s both sides (oracle stores 'Aenne' with capital A; lowercase watch-set entry was previously invisible).
- **Why**: Session 110 lost 10.2M gas + 0 kills when Aenne synced-stopped 3 residual kamis within 22s of my deploy at node 34, before strike cooldown opened. The pattern is sub-second atomic batch (span_sec=0); a 5s window catches it cleanly while leaving normal manual cycling untouched (60s window caught vuongdung1198 false-positives).
- **Files**: `predator/scripts/refresh_world_targets.py`
- **How to use**: Run `python3 predator/scripts/refresh_world_targets.py` as before — output JSON at `predator/world_targets.json` now includes `owner_heat[name].sync_stop_bursts_6h` and `anti_predator_automation` per owner. `killable_v2` already filters by `defensive_cycle` which now incorporates the new flag. Validation set: Aenne sync_bursts=2, 3333333333333333=3, foden=26, dias=20, rtvvvvv=2 — all properly flagged. vuongdung1198 sync_bursts=0 (false-positive cleared at 5s threshold).
- **Commit**: (this session)

## 2026-05-03 — Watcher: sync-feed burst detector (anti-predator automation extension)
- **What**: Extended `owner_heat_check()` in `predator/scripts/refresh_world_targets.py` with `sync_feed_bursts_6h` field and corresponding CTEs (`feeds`, `feed_burst_windows`, `feed_burst_islands`, `feed_burst_count`). Mirror of stop-burst detector: 5-second window, ≥3-distinct-kami threshold, gap-based island collapse. `anti_predator_automation` is now True if EITHER stop-bursts OR feed-bursts ≥1. Defensive reasons split into `sync_stop_bursts(xN)` / `sync_feed_bursts(xN)` for diagnostic clarity.
- **Why**: Session 115 — vuongdung1198 fed 15 kamis in 15s using item 11001 (mass-heal defensive cycle response after 14-kill cumulative pressure). Same atomic-batch signature as Aenne's stop-bursts but a different defensive primitive (heal-back-above-threshold vs pull-off-node). Old detector caught vuongdung1198 only via the soft `sync_active(idle<10min, kamis_5min≥3)` heuristic, not the underlying mechanic. New field flags the mechanic explicitly so future similar events bypass human-loop oracle dive.
- **Files**: `predator/scripts/refresh_world_targets.py`
- **How to use**: No API change. Watcher snapshot now exposes `owner_heat[<owner>]['sync_feed_bursts_6h']` and `defensive_reasons` includes `sync_feed_bursts(xN)` when triggered. Validated: vuongdung1198 flagged with feed_bursts=1; 3333333333333333 also picked up 1 feed-burst (reinforces existing stop-burst flag).
- **Commit**: 8813df9
