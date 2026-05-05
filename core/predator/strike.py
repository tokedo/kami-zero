"""Wraps executor.liquidate(). Returns a structured outcome dict for
runs.jsonl. Imports executor lazily via the same sys.path-prepend
trick as perception.self_state — server.py uses sibling-module
imports.
"""

import time
from typing import Any

from core.perception.self_state import _import_server


async def fire(candidate: dict, account: str) -> dict[str, Any]:
    server = _import_server()

    target = int(candidate["v_idx"])
    striker = int(candidate["striker_idx"])
    hdl = candidate.get("_resolved_handle") or ""

    t0 = time.time()
    result = await server.liquidate(
        target_kami_id=target,
        attacker_kami_id=striker,
        account=account,
        target_handle=hdl,
    )
    duration = time.time() - t0

    return {
        "target": target,
        "striker": striker,
        "owner_handle": hdl,
        "node_id": candidate.get("node_id"),
        "margin_at_fire": candidate.get("margin"),
        "blocked": bool(result.get("blocked")),
        "block_reason": result.get("reason"),
        "tx_hash": result.get("tx_hash"),
        "gas_used": result.get("gas_used"),
        "revert_reason": result.get("revert_reason"),
        "duration_sec": round(duration, 2),
    }
