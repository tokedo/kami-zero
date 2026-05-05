"""Striker migration: get a kami into HARVESTING state at a target node.

Each step is revert-checked. On first failure the sequence aborts and
returns a structured result — the caller (hunt.py) decides whether to
clean up via stand_down().

Sequence (idempotent):
  1. If kami HARVESTING at non-target: harvest_stop  (~4M gas)
  2. If operator not at target room:    travel_to_room  (~1M/hop, uses items)
  3. If kami not HARVESTING at target:  harvest_start  (~3M gas)
"""

from typing import Any

from core.perception.self_state import _import_server


def _tx_failed(result: dict | None) -> bool:
    """A tx is considered failed if status != "success". Travel returns
    a different shape — handled by caller."""
    if not isinstance(result, dict):
        return True
    return result.get("status") != "success"


async def prepare_at(striker_idx: int, target_node: int, account: str) -> dict[str, Any]:
    """Get the striker into HARVESTING state at target_node.
    Returns:
        {
          "ok": bool,
          "steps": [{"action": str, "result": dict, ...}],
          "total_gas": int,
          "aborted_at": str | None,
        }
    """
    server = _import_server()
    steps: list[dict] = []
    total_gas = 0

    # --- Read striker state ---
    try:
        slim = await server.get_kami_state_slim(kami_id=striker_idx, account=account)
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "steps": [{"action": "read_striker", "error": str(e)}],
            "total_gas": 0,
            "aborted_at": "read_striker",
        }

    striker_state = slim.get("state")
    striker_node = ((slim.get("harvest") or {}).get("node") or {}).get("index")

    # --- 1. harvest_stop if HARVESTING at wrong node ---
    if striker_state == "HARVESTING" and striker_node != target_node:
        result = server.harvest_stop(kami_ids=[striker_idx], account=account)
        gas = result.get("gas_used") or 0
        total_gas += gas
        steps.append({"action": "harvest_stop", "result": result, "gas": gas})
        if _tx_failed(result):
            return {"ok": False, "steps": steps, "total_gas": total_gas, "aborted_at": "harvest_stop"}

    # --- 2. travel operator to target (RESTING kami follows) ---
    try:
        raw = await server._api_get_account(account=account)
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "steps": steps + [{"action": "read_account", "error": str(e)}],
            "total_gas": total_gas,
            "aborted_at": "read_account",
        }
    operator_room = raw.get("roomIndex")

    if operator_room != target_node:
        travel = await server.travel_to_room(target_room=target_node, account=account)
        # travel returns: {"reached_target": bool, "hops": [...], "stamina_remaining": ...}
        gas = sum((h.get("gas_used") or 0) for h in (travel.get("hops") or []) if isinstance(h, dict))
        total_gas += gas
        steps.append({
            "action": "travel",
            "from": operator_room,
            "to": target_node,
            "reached": travel.get("reached_target"),
            "hops_count": len(travel.get("hops") or []),
            "stamina_remaining": travel.get("stamina_remaining"),
            "gas": gas,
        })
        if not travel.get("reached_target"):
            return {"ok": False, "steps": steps, "total_gas": total_gas, "aborted_at": "travel"}

    # --- 3. harvest_start at target if not already HARVESTING there ---
    # Re-read state — steps 1-2 changed it.
    try:
        slim2 = await server.get_kami_state_slim(kami_id=striker_idx, account=account)
    except Exception as e:  # noqa: BLE001
        return {
            "ok": False,
            "steps": steps + [{"action": "reread_striker", "error": str(e)}],
            "total_gas": total_gas,
            "aborted_at": "reread_striker",
        }
    state2 = slim2.get("state")
    node2 = ((slim2.get("harvest") or {}).get("node") or {}).get("index")

    if not (state2 == "HARVESTING" and node2 == target_node):
        result = server.harvest_start(
            kami_ids=[striker_idx], node_index=target_node, account=account
        )
        gas = result.get("gas_used") or 0
        total_gas += gas
        steps.append({"action": "harvest_start", "result": result, "gas": gas})
        if _tx_failed(result):
            return {"ok": False, "steps": steps, "total_gas": total_gas, "aborted_at": "harvest_start"}

    return {"ok": True, "steps": steps, "total_gas": total_gas, "aborted_at": None}


async def stand_down(striker_idx: int, account: str) -> dict[str, Any]:
    """Return striker to RESTING. Called after strike (success OR failure).
    No-op if already RESTING.
    """
    server = _import_server()
    try:
        slim = await server.get_kami_state_slim(kami_id=striker_idx, account=account)
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "noop": False, "error": str(e)}
    if slim.get("state") != "HARVESTING":
        return {"ok": True, "noop": True, "gas": 0}
    result = server.harvest_stop(kami_ids=[striker_idx], account=account)
    return {
        "ok": not _tx_failed(result),
        "noop": False,
        "gas": result.get("gas_used") or 0,
        "result": result,
    }
