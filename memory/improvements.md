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
  - `get_scavenge_points(47)` — read accumulated points (NOTE: currently returns 0, may have component ID issue)
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
