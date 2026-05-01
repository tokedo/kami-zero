# Liquidation mechanics — what we know

(Empty at session 73 start. Fill in across sessions, citing sources:
oracle queries, GDD references, on-chain logs, item catalog rows, etc.)

## Open questions for the agent to investigate
- Exact on-chain function call for liquidation — name, params, ABI
- HP threshold under which a kami is liquidatable
- Obol payout formula — does it depend on target kami level? attack type matchup? node?
- Tx cost per liquidation — gas estimate, comparison to other actions
- Cooldowns post-liquidation (attacker side, target side)
- Any item that boosts predator output — check the items catalog via oracle

## Confirmed (session 73, oracle reads only)

- **System ID**: `system.harvest.liquidate` — 100% of 1,676 `harvest_liquidate` rows in 28d route through this single system. Resolve to address via `_resolve_system("system.harvest.liquidate")` in `executor/server.py` to get the ABI surface.
- **Oracle event shape** (`kami_action` row when `action_type='harvest_liquidate'`): `kami_id` = attacker entity, `harvest_id` = target's harvest entity (NOT directly the target kami), `target_kami_id` = NULL (oracle does not populate it for liquidations), `node_id` = NULL (oracle does not populate it for liquidations), `amount` = integer (sample values 606, 851, 970 — plausibly obol or musu yield, **unverified**), `metadata_json` = `{"fn": "executeTyped"}`. Tx is single sub_index 0.
- **Recovering the target kami**: must look up `harvest_id` on-chain to get the kami entity it belongs to. Future helper: `_harvest_to_kami(harvest_entity_id) -> kami_entity_id` via the harvest entity's `KamiID` component.
- **Recovering the node**: same path — harvest entity holds a node reference. Without that join, "kills per node" queries via oracle alone are not directly possible.
- **Throughput**: 1,676 liquidations / 28 days ≈ **60 kills/day game-wide** as of 2026-05-01. That's the prey ceiling for *all* predators combined. Cluster economics math should anchor on a fraction of that, not the full number.

## Known-unknowns (do NOT assume — must verify before doctrine ships)
- Whether `amount` in the oracle row is obol, musu, or something else.
- Whether the system call requires the target's harvest_id, or kami_id, or both.
- Whether liquidation has a per-attacker cooldown or only per-target.
- Whether attacker stamina/HP is consumed and how much.
- Whether items like "Hostility Potion" (item 11410) modify any of the above. The bpeon inventory has 1 — useful for sandbox testing once predator transfer lands.
