"""
Oracle-only world-state primitives for kami-zero.

Replaces kamibots playwright reads in the predator-decision path. All world-
state queries go through kami-oracle (DuckDB tail of every Yominet action).

Founder structural rule (2026-05-02): kamibots state reads are FORBIDDEN in
any predator-decision path. Oracle is the single source of truth.

Public API:
  - resolve_target_owner(kami_index)   -> {account_id, handle, ...}
  - oracle_kami_state(kami_index)      -> KamiState
  - reconstruct_bounty_pool(kami_index, now_ts=None) -> {pool, confidence, ...}

Each function returns plain dicts (or dataclasses) with explicit
`freshness_warnings` lists so callers can apply margin gates.

This module talks to the oracle via raw HTTP (same auth path as
executor/server.py). It does NOT import server.py to keep the dependency
acyclic and to make unit-testing easier.
"""

from __future__ import annotations

import json
import math
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

_REPO = Path(__file__).resolve().parent.parent
_KEYS_PATH = Path.home() / ".blocklife-keys" / ".env"
load_dotenv(_KEYS_PATH)

_ORACLE_URL = os.environ.get("KAMI_ORACLE_URL", "https://136-112-224-147.sslip.io").rstrip("/")
_ORACLE_TOKEN = os.environ.get("KAMI_ORACLE_TOKEN", "")


def _oracle_headers() -> dict:
    if not _ORACLE_TOKEN:
        raise RuntimeError("KAMI_ORACLE_TOKEN missing from ~/.blocklife-keys/.env")
    return {"Authorization": f"Bearer {_ORACLE_TOKEN}"}


def oracle_sql_sync(query: str, limit: int = 1000) -> dict:
    """Synchronous oracle SQL — used by direct-python invocations."""
    with httpx.Client(timeout=30) as c:
        r = c.post(
            f"{_ORACLE_URL}/sql",
            headers=_oracle_headers(),
            json={"q": query, "limit": limit},
        )
        if r.status_code != 200:
            return {"error": "oracle_http", "status": r.status_code, "detail": r.text}
        return r.json()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _q1(query: str) -> dict | None:
    """Run a query expecting at most one row; return as dict or None."""
    res = oracle_sql_sync(query, limit=2)
    if "error" in res:
        raise RuntimeError(f"oracle query failed: {res}")
    cols = res.get("columns") or []
    rows = res.get("rows") or []
    if not rows:
        return None
    return dict(zip(cols, rows[0]))


def _qn(query: str, limit: int = 1000) -> list[dict]:
    res = oracle_sql_sync(query, limit=limit)
    if "error" in res:
        raise RuntimeError(f"oracle query failed: {res}")
    cols = res.get("columns") or []
    return [dict(zip(cols, r)) for r in (res.get("rows") or [])]


def _safe_int(x, default=0) -> int:
    try:
        return int(x) if x is not None else default
    except (TypeError, ValueError):
        return default


def _split_node_affinities(s: str | None) -> list[str]:
    if not s:
        return ["NORMAL"]
    parts = [p.strip().upper() for p in s.split(",") if p.strip()]
    return parts or ["NORMAL"]


# ---------------------------------------------------------------------------
# Owner resolution (replaces playwright lookup in liquidate)
# ---------------------------------------------------------------------------


def resolve_target_owner(kami_index: int) -> dict:
    """Resolve target kami's owner (account_id, handle) from oracle.

    Replaces /api/playwright/kami/{id}/ playwright lookup in the liquidate
    pre-flight (predator-decision path → must come from oracle).

    Returns:
      {"kami_index": int, "kami_id": str, "account_id": str, "handle": str,
       "freshness_warnings": [str, ...]}
    """
    row = _q1(
        "SELECT kami_id, account_id, account_name, last_refreshed_ts "
        f"FROM kami_static WHERE kami_index = {int(kami_index)}"
    )
    warnings: list[str] = []
    if row is None:
        return {
            "kami_index": int(kami_index),
            "kami_id": "",
            "account_id": "",
            "handle": "",
            "freshness_warnings": [
                f"kami_index {kami_index} not in kami_static (populator gap)"
            ],
        }
    return {
        "kami_index": int(kami_index),
        "kami_id": row.get("kami_id") or "",
        "account_id": row.get("account_id") or "",
        "handle": row.get("account_name") or "",
        "last_refreshed_ts": str(row.get("last_refreshed_ts") or ""),
        "freshness_warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Bounty pool reconstruction (load-bearing piece)
# ---------------------------------------------------------------------------


def _harvest_efficacy(body_aff: str, hand_aff: str, node_affinities: list[str]) -> int:
    """Affinity efficacy multiplier (×1000 prec). See hp_projection.py."""
    AFFINITY_BEATS = {("EERIE", "SCRAP"), ("SCRAP", "INSECT"), ("INSECT", "EERIE")}
    body_aff = (body_aff or "").upper()
    hand_aff = (hand_aff or "").upper()
    nodes = [(a or "").upper() for a in node_affinities]
    if len(nodes) == 1:
        nodes = [nodes[0], nodes[0]]
    best = 1000
    for body_node in nodes:
        for hand_node in nodes:
            if body_node == "NORMAL" or body_aff == "NORMAL":
                bc = 0
            elif body_aff == body_node:
                bc = 650
            elif (body_aff, body_node) in AFFINITY_BEATS:
                bc = 650
            elif (body_node, body_aff) in AFFINITY_BEATS:
                bc = -250
            else:
                bc = 0
            if hand_node == "NORMAL" or hand_aff == "NORMAL":
                hc = 0
            elif hand_aff == hand_node:
                hc = 350
            elif (hand_aff, hand_node) in AFFINITY_BEATS:
                hc = 350
            elif (hand_node, hand_aff) in AFFINITY_BEATS:
                hc = -100
            else:
                hc = 0
            cand = 1000 + bc + hc
            if cand > best:
                best = cand
    return best


def _bounty_integral(
    *,
    power: int,
    violence: int,
    elapsed_sec: float,
    efficacy: int,
    bounty_boost: int = 0,
    fertility_boost_pct_x1000: int = 0,
    intensity_boost_pct_x1000: int = 0,
    intensity_flat_per_hr: float = 0.0,
    t_offset_sec: float = 0.0,
) -> float:
    """Forward-projected bounty over `elapsed_sec` continuing from
    `t_offset_sec` of cumulative-since-start (intensity grows linearly with
    minutesElapsed since harvest_start). Returns Musu (float).

    Mirrors executor/hp_projection.py:projected_bounty but supports a non-zero
    starting-offset so we can reset the integral after each on-chain touch
    (collect/feed) — those reset the active accumulator on chain.

    NOTE: per session 86 doctrine, intensity does NOT actually reset on
    collect/feed in the canonical formula; it's a function of total elapsed
    since harvest_start. Use t_offset_sec=time-since-start (NOT 0) when
    integrating a sub-segment.
    """
    if elapsed_sec <= 0:
        return 0.0
    P, V = power, violence
    T = float(elapsed_sec)
    tau = float(t_offset_sec)
    fert_per_sec_1e6 = P * 1500.0 * efficacy / 3600.0
    fert_total = fert_per_sec_1e6 * T
    int_const = 1e6 * 10.0 / (480.0 * 3600.0)
    # Int(t) = int_const * (V*5 + t/60); integral from tau to tau+T of dt:
    # = int_const * (V*5*T + ((tau+T)^2 - tau^2)/120)
    int_total = int_const * (
        V * 5.0 * T
        + ((tau + T) ** 2 - tau ** 2) / 120.0
    )
    fert_mult = 1.0 + fertility_boost_pct_x1000 / 1000.0
    int_mult = 1.0 + intensity_boost_pct_x1000 / 1000.0
    bounty_fert = (fert_total * fert_mult) / 1e6
    bounty_int = (int_total * int_mult) / 1e6
    bounty = (bounty_fert + bounty_int) * (1.0 + bounty_boost / 1000.0)
    bounty += intensity_flat_per_hr * (T / 3600.0)
    return bounty


def reconstruct_bounty_pool(
    kami_index: int,
    *,
    now_ts: int | None = None,
    strain_calibration: float = 1.5,
) -> dict:
    """Reconstruct the live `harvest.bounty.balance` from oracle action stream.

    Walks all kami_action events since the latest `harvest_start`. For each
    inter-event interval, integrates the canonical Fertility+Intensity bounty
    formula. At each `harvest_collect` / `feed`, the chain resets the active
    accumulator (collect drains pool; feed updates sync_hp without draining
    pool — but we treat feed as resetting harvest.time.last for chain
    consistency).

    NOTE: the back-fit certificate (session 84, N=200, M=199, 99.5%) used this
    same forward-simulation logic when in `empirical` mode. The
    `strain_calibration` knob mirrors the back-fit's ×1.5 calibrated mode.

    Returns:
      {kami_index, kami_id, harvest_start_ts, harvest_id, node_id,
       elapsed_sec, n_collects, sum_collected, pool_now, confidence,
       freshness_warnings}
    """
    if now_ts is None:
        now_ts = int(time.time())

    # Pull static fields
    s = _q1(
        "SELECT kami_id, account_id, account_name, body_affinity, hand_affinity, "
        "       total_power, total_violence, total_harmony, total_health, "
        "       strain_boost, harvest_fertility_boost, harvest_intensity_boost, "
        "       harvest_bounty_boost, build_refreshed_ts "
        f"FROM kami_static WHERE kami_index = {int(kami_index)}"
    )
    warnings: list[str] = []
    if s is None:
        return {"kami_index": int(kami_index), "error": "not_in_kami_static",
                "freshness_warnings": ["kami_static row missing"]}
    kami_id = s["kami_id"]

    # Pull all relevant actions for this kami; descending so we can find the
    # latest harvest_start cycle
    actions = _qn(
        f"SELECT action_type, block_timestamp, node_id, harvest_id, amount, item_index "
        f"FROM kami_action WHERE kami_id = '{kami_id}' "
        f"  AND action_type IN ('harvest_start','harvest_stop','harvest_collect',"
        f"                      'harvest_liquidate','feed') "
        f"ORDER BY block_timestamp DESC, id DESC LIMIT 200"
    )

    # Walk newest-first to find the latest harvest_start that has not been
    # closed by a subsequent harvest_stop / harvest_liquidate.
    cycle_start = None
    cycle_events_after_start: list[dict] = []
    for a in actions:
        if a["action_type"] in ("harvest_stop", "harvest_liquidate"):
            # Hit a close before finding a start — kami isn't currently harvesting
            break
        if a["action_type"] == "harvest_start":
            cycle_start = a
            break
        cycle_events_after_start.append(a)

    if cycle_start is None:
        return {
            "kami_index": int(kami_index),
            "kami_id": kami_id,
            "state_inferred": "RESTING_OR_DEAD",
            "harvest_start_ts": None,
            "pool_now": 0.0,
            "confidence": 0.95,
            "freshness_warnings": warnings + [
                "no open harvest_start in last 200 actions"
            ],
        }

    # Reverse so events are oldest-first within the cycle
    events = list(reversed(cycle_events_after_start))
    # Convert timestamps to unix
    def _ts(s_iso: str) -> int:
        # DuckDB returns ISO-like strings without 'Z'; treat as UTC
        if not s_iso:
            return 0
        # e.g. "2026-05-02T00:24:36"
        from datetime import datetime, timezone
        try:
            dt = datetime.fromisoformat(s_iso)
        except ValueError:
            return 0
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())

    start_ts = _ts(cycle_start["block_timestamp"])
    elapsed_total = max(0, now_ts - start_ts)

    # Resolve node info
    node_id = cycle_start.get("node_id")
    node_aff_str = None
    if node_id:
        nrow = _q1(f"SELECT affinity FROM nodes_catalog WHERE node_index = {int(node_id)}")
        if nrow:
            node_aff_str = nrow.get("affinity")
    node_affs = _split_node_affinities(node_aff_str)

    body_aff = (s.get("body_affinity") or "NORMAL").upper()
    hand_aff = (s.get("hand_affinity") or "NORMAL").upper()
    eff = _harvest_efficacy(body_aff, hand_aff, node_affs)

    power = _safe_int(s.get("total_power"))
    violence = _safe_int(s.get("total_violence"))
    harmony = _safe_int(s.get("total_harmony"))
    sb = _safe_int(s.get("strain_boost"))
    hfb = _safe_int(s.get("harvest_fertility_boost"))
    hib = _safe_int(s.get("harvest_intensity_boost"))  # Musu/hr flat
    hbb = _safe_int(s.get("harvest_bounty_boost"))

    # Walk events in chronological order. We track "active accumulator" since
    # the last accumulator reset. Per session 86 doctrine, harvest_collect
    # drains the pool to 0 (subtract collected amount as a sanity check); feed
    # updates sync but does NOT drain. BUT — for the LIVE pool reconstruction
    # we just need to compute "pool since last collect" since the chain stores
    # zero between collects.

    last_drain_ts = start_ts  # accumulator reset after harvest_start
    cumulative_offset_at_drain = 0  # seconds since start at last drain

    n_collects = 0
    sum_collected = 0
    n_feeds = 0
    feed_events: list[int] = []

    for e in events:
        ts = _ts(e["block_timestamp"])
        atype = e["action_type"]
        if atype == "harvest_collect":
            n_collects += 1
            sum_collected += _safe_int(e.get("amount"))
            last_drain_ts = ts
            cumulative_offset_at_drain = max(0, ts - start_ts)
        elif atype == "feed":
            n_feeds += 1
            feed_events.append(ts)
            # feed does NOT drain the active accumulator per harvesting.md;
            # but heal-event guard rule still applies (caller checks).

    # Bounty since last drain to now
    sub_elapsed = max(0, now_ts - last_drain_ts)
    pool_now = _bounty_integral(
        power=power, violence=violence,
        elapsed_sec=sub_elapsed, efficacy=eff,
        bounty_boost=hbb, fertility_boost_pct_x1000=hfb,
        intensity_boost_pct_x1000=0,
        intensity_flat_per_hr=hib,
        t_offset_sec=cumulative_offset_at_drain,
    )

    # Confidence: high if we observed at least one collect (per-collect
    # validation possible); medium if pure forward-projection.
    if n_collects > 0:
        confidence = 0.85
    else:
        confidence = 0.7
        warnings.append(
            "no harvest_collect events since start — pool is pure formula "
            "projection; apply strain_calibration ≥ 1.5 for back-fit-proven "
            "97% accuracy"
        )

    # Apply calibration (caller can override). Returns BOTH raw and calibrated.
    pool_calibrated = pool_now * strain_calibration

    return {
        "kami_index": int(kami_index),
        "kami_id": kami_id,
        "state_inferred": "HARVESTING",
        "harvest_start_ts": start_ts,
        "harvest_id": cycle_start.get("harvest_id"),
        "node_id": int(node_id) if node_id is not None else None,
        "node_affinity_str": node_aff_str,
        "node_affinities": node_affs,
        "efficacy": eff,
        "elapsed_total_sec": elapsed_total,
        "elapsed_since_last_drain_sec": sub_elapsed,
        "n_collects": n_collects,
        "sum_collected": sum_collected,
        "n_feeds": n_feeds,
        "feed_event_ts": feed_events,
        "pool_now_raw": pool_now,
        "pool_now": pool_calibrated,
        "strain_calibration": strain_calibration,
        "confidence": confidence,
        "freshness_warnings": warnings,
        "build_refreshed_ts": str(s.get("build_refreshed_ts") or ""),
        "stats": {
            "power": power, "violence": violence, "harmony": harmony,
            "max_hp": _safe_int(s.get("total_health")),
            "strain_boost": sb,
            "harvest_fertility_boost": hfb,
            "harvest_intensity_boost": hib,
            "harvest_bounty_boost": hbb,
        },
    }


# ---------------------------------------------------------------------------
# oracle_kami_state — composite primitive
# ---------------------------------------------------------------------------


@dataclass
class KamiState:
    kami_index: int
    kami_id: str
    handle: str
    account_id: str
    state: str  # "HARVESTING" | "RESTING_OR_DEAD"
    sync_hp_at_last_touch: float
    max_hp: int
    last_action_ts: int | None
    harvest_start_ts: int | None
    node_id: int | None
    node_affinities: list[str]
    body_affinity: str
    hand_affinity: str
    power: int
    violence: int
    harmony: int
    bounty_pool_now: float  # calibrated
    bounty_pool_now_raw: float
    n_collects: int
    sum_collected: int
    n_feeds_since_start: int
    feed_event_ts: list[int]
    bonuses: dict
    freshness_warnings: list[str]
    confidence: float
    build_refreshed_ts: str

    def to_dict(self) -> dict:
        return self.__dict__.copy()


def oracle_kami_state(
    kami_index: int,
    *,
    now_ts: int | None = None,
    strain_calibration: float = 1.5,
) -> KamiState:
    """One-stop oracle-only state read for a kami.

    Combines kami_static (build, traits, bonuses) with kami_action stream
    (current harvest cycle, pool reconstruction, feed events).

    Returns KamiState with all fields needed to feed compute_current_hp +
    kill_threshold without ANY kamibots call.
    """
    if now_ts is None:
        now_ts = int(time.time())

    s = _q1(
        "SELECT kami_id, account_id, account_name, body_affinity, hand_affinity, "
        "       total_power, total_violence, total_harmony, total_health, base_health, "
        "       strain_boost, harvest_fertility_boost, harvest_intensity_boost, "
        "       harvest_bounty_boost, rest_recovery_boost, "
        "       attack_threshold_shift, attack_threshold_ratio, attack_spoils_ratio, "
        "       defense_threshold_shift, defense_threshold_ratio, defense_salvage_ratio, "
        "       cooldown_shift, build_refreshed_ts "
        f"FROM kami_static WHERE kami_index = {int(kami_index)}"
    )
    if s is None:
        raise RuntimeError(f"kami_index {kami_index} not in oracle kami_static")
    kami_id = s["kami_id"]

    pool = reconstruct_bounty_pool(
        kami_index, now_ts=now_ts, strain_calibration=strain_calibration
    )

    # sync_hp_at_last_touch: read latest action that touches HP
    # harvest_start sets sync to current (capped at max_hp at the time);
    # harvest_collect/feed update sync. For simplicity, project from harvest
    # start ts if no collect/feed since (sync = max_hp at start).
    max_hp = _safe_int(s.get("total_health"))
    state = pool.get("state_inferred", "UNKNOWN")
    if state == "HARVESTING":
        # Default: sync_hp at harvest_start = max_hp (kami had to be RESTING with
        # full HP, modulo any partial recovery). For accuracy, look at the most
        # recent feed/collect event since start; if any, sync was reset there.
        sync_hp = float(max_hp)
        feed_ts = pool.get("feed_event_ts") or []
        if feed_ts:
            # A feed restores HP toward max (capped). Without per-feed item
            # heal amount in oracle, set sync conservatively to max_hp at last
            # feed (overestimates HP — caller should treat any feed-since-start
            # as an automatic reject per session 85 heal-event guard).
            sync_hp = float(max_hp)
        last_action_ts = max(
            pool.get("harvest_start_ts") or 0,
            *(pool.get("feed_event_ts") or [0]),
        )
    else:
        # RESTING/DEAD path — would need rest recovery projection. Out of scope
        # for predator targeting (we only target HARVESTING). Caller should
        # filter; we return a conservative passthrough.
        sync_hp = float(max_hp)
        last_action_ts = None

    bonuses = {
        "strain_boost": _safe_int(s.get("strain_boost")),
        "harvest_fertility_boost": _safe_int(s.get("harvest_fertility_boost")),
        "harvest_intensity_boost": _safe_int(s.get("harvest_intensity_boost")),
        "harvest_bounty_boost": _safe_int(s.get("harvest_bounty_boost")),
        "rest_recovery_boost": _safe_int(s.get("rest_recovery_boost")),
        "cooldown_shift": _safe_int(s.get("cooldown_shift")),
        "attack_threshold_shift": _safe_int(s.get("attack_threshold_shift")),
        "attack_threshold_ratio": _safe_int(s.get("attack_threshold_ratio")),
        "attack_spoils_ratio": _safe_int(s.get("attack_spoils_ratio")),
        "defense_threshold_shift": _safe_int(s.get("defense_threshold_shift")),
        "defense_threshold_ratio": _safe_int(s.get("defense_threshold_ratio")),
        "defense_salvage_ratio": _safe_int(s.get("defense_salvage_ratio")),
    }

    warnings = list(pool.get("freshness_warnings") or [])
    # Build staleness check
    brt = str(s.get("build_refreshed_ts") or "")
    if brt:
        from datetime import datetime, timezone
        try:
            brt_dt = datetime.fromisoformat(brt)
            if brt_dt.tzinfo is None:
                brt_dt = brt_dt.replace(tzinfo=timezone.utc)
            age_s = now_ts - int(brt_dt.timestamp())
            if age_s > 24 * 3600:
                warnings.append(
                    f"kami_static build_refreshed_ts is {age_s/3600:.1f}h old "
                    "— consider refresh_kami_build_onchain for fresh skills"
                )
        except Exception:
            pass

    return KamiState(
        kami_index=int(kami_index),
        kami_id=kami_id,
        handle=s.get("account_name") or "",
        account_id=s.get("account_id") or "",
        state=state,
        sync_hp_at_last_touch=sync_hp,
        max_hp=max_hp,
        last_action_ts=last_action_ts,
        harvest_start_ts=pool.get("harvest_start_ts"),
        node_id=pool.get("node_id"),
        node_affinities=pool.get("node_affinities") or ["NORMAL"],
        body_affinity=(s.get("body_affinity") or "NORMAL").upper(),
        hand_affinity=(s.get("hand_affinity") or "NORMAL").upper(),
        power=_safe_int(s.get("total_power")),
        violence=_safe_int(s.get("total_violence")),
        harmony=_safe_int(s.get("total_harmony")),
        bounty_pool_now=pool.get("pool_now") or 0.0,
        bounty_pool_now_raw=pool.get("pool_now_raw") or 0.0,
        n_collects=pool.get("n_collects") or 0,
        sum_collected=pool.get("sum_collected") or 0,
        n_feeds_since_start=pool.get("n_feeds") or 0,
        feed_event_ts=pool.get("feed_event_ts") or [],
        bonuses=bonuses,
        freshness_warnings=warnings,
        confidence=pool.get("confidence") or 0.5,
        build_refreshed_ts=brt,
    )


# ---------------------------------------------------------------------------
# Smoke test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: python oracle_state.py <kami_index>")
        sys.exit(1)
    idx = int(sys.argv[1])
    ks = oracle_kami_state(idx)
    print(json.dumps(ks.to_dict(), indent=2, default=str))
