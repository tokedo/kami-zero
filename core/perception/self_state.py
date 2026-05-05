"""Reads our own state via the existing executor module. This is the
ONLY place that touches the chain/Kamibots; everything else operates on
the dicts returned here.
"""

import sys
from pathlib import Path
from typing import Any

EXECUTOR_DIR = Path(__file__).resolve().parent.parent.parent / "executor"


def _import_server():
    """Add executor/ to sys.path then import server.py as a top-level
    module. server.py uses sibling-module imports (`import rooms_graph`)
    so it must be imported with executor/ on the path, not as
    `executor.server`.
    """
    if str(EXECUTOR_DIR) not in sys.path:
        sys.path.insert(0, str(EXECUTOR_DIR))
    import server  # noqa: WPS433
    return server


async def read_self_state(account: str) -> dict[str, Any]:
    """Return:
        {
          "operator_node": int,
          "kamis": {kami_index: {"node": int|None, "state": str}},
        }

    `node` is None when state != HARVESTING (no node attached).
    Reads each kami's slim state in parallel — one API call per kami.
    """
    import asyncio

    server = _import_server()

    raw = await server._api_get_account(account=account)
    operator_node = raw.get("roomIndex")

    roster = [k.get("index") for k in (raw.get("kamis") or []) if k.get("index")]

    async def _slim(kami_id: int) -> tuple[int, dict]:
        try:
            r = await server.get_kami_state_slim(kami_id=kami_id, account=account)
        except Exception as e:  # noqa: BLE001
            return kami_id, {"node": None, "state": "ERROR", "error": str(e)}
        node = ((r.get("harvest") or {}).get("node") or {}).get("index")
        return kami_id, {"node": node, "state": r.get("state")}

    results = await asyncio.gather(*[_slim(k) for k in roster])
    kamis = {k: v for k, v in results}

    return {
        "operator_node": operator_node,
        "kamis": kamis,
    }
