"""Hunt: full strike sequence with pre-strike viability check, migration,
liquidation, and stand-down to RESTING. The hunt is an alternative to
strike.fire() that handles non-co-located targets autonomously.

Sequence:
  A. verify_target_fresh()  — slim read; abort if HP ≥ kill_zone
                              (target was fed/revived since watcher snapshot)
  B. migrate.prepare_at()   — get striker HARVESTING at target's node
  C. liquidate()            — the actual strike
  D. migrate.stand_down()   — return striker to RESTING (always, even on failure)

Each step's result is captured in the returned outcome dict, which is
written to history/runs.jsonl. The optimizer reads this to learn which
gates need adjusting.
"""

import time
from typing import Any

from core.movement import migrate
from core.perception.self_state import _import_server


async def verify_target_fresh(
    target_idx: int,
    kill_zone: float | None,
    account: str,
) -> tuple[bool, int | None, str]:
    """Read target's slim state right before strike. Returns
    (viable, observed_hp, reason). Free read — no gas."""
    server = _import_server()
    try:
        slim = await server.get_kami_state_slim(kami_id=target_idx, account=account)
    except Exception as e:  # noqa: BLE001
        return False, None, f"slim_read_failed: {e}"

    health = (slim.get("stats") or {}).get("health") or {}
    hp = health.get("sync")
    state = slim.get("state")

    if hp is None:
        return False, None, "hp_unreadable"

    if state != "HARVESTING":
        return False, hp, f"target_state_{state}"

    if kill_zone is not None and hp >= kill_zone:
        return False, hp, "hp_above_kill_zone"

    return True, hp, "ok"


async def hunt(candidate: dict, account: str) -> dict[str, Any]:
    """Execute a full hunt against candidate. Returns structured outcome.

    On success: ends with striker RESTING with operator at target node.
    On any failure: attempts stand_down so striker isn't left in a
    half-broken state.
    """
    striker_idx = int(candidate["striker_idx"])
    target_idx = int(candidate["v_idx"])
    target_node = int(candidate["node_id"])
    kill_zone = candidate.get("kill_zone")
    handle = candidate.get("_resolved_handle") or ""

    outcome: dict[str, Any] = {
        "target": target_idx,
        "striker": striker_idx,
        "owner_handle": handle,
        "node_id": target_node,
        "margin_at_filter": candidate.get("margin"),
        "kill_zone": kill_zone,
        "steps": [],
        "total_gas": 0,
        "success": False,
    }

    # --- A. Verify target still fireable ---
    viable, observed_hp, reason = await verify_target_fresh(target_idx, kill_zone, account)
    outcome["observed_hp_pre_strike"] = observed_hp
    outcome["steps"].append(
        {"action": "verify", "viable": viable, "hp": observed_hp, "reason": reason}
    )
    if not viable:
        outcome["aborted_at"] = "verify"
        outcome["abort_reason"] = reason
        return outcome

    # --- B. Migrate striker to target node ---
    mig = await migrate.prepare_at(striker_idx, target_node, account)
    outcome["steps"].extend(mig["steps"])
    outcome["total_gas"] += mig.get("total_gas") or 0
    if not mig["ok"]:
        outcome["aborted_at"] = mig.get("aborted_at") or "migrate"
        # Cleanup attempt — best-effort, don't fail outcome on cleanup failure
        sd = await migrate.stand_down(striker_idx, account)
        outcome["steps"].append({"action": "stand_down_after_migrate_fail", "result": sd})
        outcome["total_gas"] += sd.get("gas") or 0
        return outcome

    # --- C. Strike ---
    server = _import_server()
    t0 = time.time()
    strike_result = await server.liquidate(
        target_kami_id=target_idx,
        attacker_kami_id=striker_idx,
        account=account,
        target_handle=handle,
    )
    duration = time.time() - t0
    strike_gas = strike_result.get("gas_used") or 0
    outcome["total_gas"] += strike_gas
    outcome["steps"].append(
        {
            "action": "liquidate",
            "result": strike_result,
            "duration_sec": round(duration, 2),
            "gas": strike_gas,
        }
    )

    if strike_result.get("blocked"):
        outcome["aborted_at"] = "liquidate_blocked"
        outcome["abort_reason"] = strike_result.get("reason")
    elif strike_result.get("status") != "success":
        outcome["aborted_at"] = "liquidate_reverted"
        outcome["abort_reason"] = strike_result.get("revert_reason")
    else:
        outcome["success"] = True
        outcome["tx_hash"] = strike_result.get("tx_hash")

    # --- D. Stand down (always — strikers default to RESTING) ---
    sd = await migrate.stand_down(striker_idx, account)
    outcome["steps"].append({"action": "stand_down", "result": sd})
    outcome["total_gas"] += sd.get("gas") or 0

    return outcome
