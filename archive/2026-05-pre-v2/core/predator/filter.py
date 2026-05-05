"""The gate stack. Pure function: candidates + state + config → survivors.
Each rejection records a reason so the executor can report rejection
counts in runs.jsonl (the optimizer's primary feedback signal).
"""

from typing import Any

from core import rules
from core.perception.world import resolve_handle


def apply(
    candidates: list[dict],
    by_idx: dict[int, dict],
    self_state: dict[str, Any],
    cfg: dict[str, Any],
) -> tuple[list[dict], dict[str, int]]:
    """Return (survivors, rejection_counts).

    A survivor is a candidate dict augmented with `_resolved_handle` and
    `_striker_state` for downstream use.
    """
    pcfg = cfg["predator"]
    survivors: list[dict] = []
    counts: dict[str, int] = {}

    def rej(reason: str) -> None:
        counts[reason] = counts.get(reason, 0) + 1

    for c in candidates:
        # Owner handle resolution
        hdl = resolve_handle(c, by_idx)
        if pcfg["require_owner_resolved"] and not hdl:
            if pcfg["reject_owner_unknown"]:
                rej("owner_unknown")
                continue

        # Archetype reject
        if hdl and rules.is_archetype_rejected(hdl):
            rej("archetype_rejected")
            continue

        # Margin floor — hunting_mode raises the bar (we pay migration
        # cost, so only chase strong candidates).
        margin = c.get("margin", 0) or 0
        if pcfg["hunting_mode"]:
            if margin < pcfg["hunting_margin_floor"]:
                rej("below_hunting_margin_floor")
                continue
        else:
            if margin < pcfg["margin_floor"]:
                rej("below_margin_floor")
                continue

        # Elapsed
        elapsed = c.get("elapsed_h") or 0
        if elapsed < pcfg["min_elapsed_h"]:
            rej("below_min_elapsed")
            continue

        # Heat
        heat = c.get("heat") or {}
        if pcfg["reject_if_anti_predator_automation"] and heat.get(
            "anti_predator_automation"
        ):
            rej("heat_anti_predator")
            continue
        if pcfg["reject_if_defensive_cycle"] and heat.get("defensive_cycle"):
            rej("heat_defensive_cycle")
            continue

        # Parked-bool requirement (configurable)
        if pcfg["require_parked_bool"]:
            parked = (c.get("parked_rates") or {}).get("parked_bool")
            if not parked:
                rej("not_parked")
                continue

        # Co-location: when hunting_mode is on, the executor migrates
        # the striker to the target's node, so we don't gate on it here.
        # We still verify the striker_idx is in our roster.
        striker_idx = c.get("striker_idx")
        target_node = c.get("node_id")
        striker = self_state["kamis"].get(int(striker_idx) if striker_idx else -1)
        if striker is None:
            rej("striker_not_in_roster")
            continue

        if not pcfg["hunting_mode"] and pcfg["require_colocation"]:
            if striker.get("state") != "HARVESTING":
                rej("striker_not_harvesting")
                continue
            if striker.get("node") != target_node:
                rej("striker_not_colocated")
                continue

        c = dict(c)
        c["_resolved_handle"] = hdl
        c["_striker_state"] = self_state["kamis"].get(int(c["striker_idx"]))
        survivors.append(c)

    return survivors, counts
