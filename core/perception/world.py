"""Reads world_targets.json (produced by the existing watcher cron) and
exposes candidates as plain dicts. Pure parsing — no filtering, no
business logic.
"""

import json
from pathlib import Path
from typing import Any


def load_world(path: Path | str) -> dict[str, Any]:
    """Load the full watcher snapshot. Raises FileNotFoundError if the
    watcher hasn't run yet — callers should treat that as a fatal anomaly.
    """
    with open(path) as f:
        return json.load(f)


def candidates(world: dict[str, Any]) -> list[dict]:
    """Return killable_v3 entries (the rates-aware filtered superset).
    Empty list if absent.
    """
    return list(world.get("killable_v3") or [])


def parked_rates_by_idx(parked_rates_path: Path | str) -> dict[int, dict]:
    """Load parked_rates_state.by_idx — used as fallback owner attribution
    when world_targets owner_handle is null (regression noted in old
    ideas_to_founder.md item 7).
    """
    p = Path(parked_rates_path)
    if not p.exists():
        return {}
    with open(p) as f:
        state = json.load(f)
    by_idx = state.get("by_idx") or {}
    return {int(k): v for k, v in by_idx.items()}


def resolve_handle(candidate: dict, by_idx: dict[int, dict]) -> str:
    """Return the owner handle for a candidate, falling back to
    parked_rates_state.by_idx if the watcher's `v_acct` is null.
    The chain liquidate() resolves account_id internally if not passed,
    so we only need handle for our own archetype gate.
    """
    hdl = (candidate.get("v_acct") or "").strip()
    if hdl:
        return hdl
    fallback = by_idx.get(int(candidate["v_idx"]), {})
    return str(fallback.get("v_acct") or "").strip()
