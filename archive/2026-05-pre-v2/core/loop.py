"""Executor tick orchestrator. Run once per cron firing.

    perceive → filter → pick → maybe strike → log

If you can read this file and understand what kami-zero does, the
architecture is working. Anything not here is either config (yaml) or
adapter glue (perception/, predator/strike.py).
"""

import argparse
import asyncio
import json
import os
import time
from pathlib import Path

from core import anomaly, config as cfg_module
from core.perception import self_state, world
from core.predator import filter as pfilter
from core.predator import hunt as hunt_module
from core.predator import strike, targeting

ROOT = Path(__file__).resolve().parent.parent  # repo root (kami-zero/)


def _load_config() -> dict:
    """Validate config against schema, then return as dict (downstream
    modules accept dicts so the optimizer can edit shape without
    fighting attribute access)."""
    return cfg_module.load(ROOT / "core" / "config.yaml").model_dump()


def _abs(rel: str) -> Path:
    return ROOT / rel


def _log_run(path: Path, record: dict) -> None:
    record = {"ts": int(time.time()), **record}
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _recent_defer_streak(runs_path: Path) -> int:
    """Count trailing 'defer' outcomes in runs.jsonl. Used for anomaly emission."""
    if not runs_path.exists():
        return 0
    streak = 0
    with runs_path.open() as f:
        for line in reversed(f.readlines()):
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            if rec.get("outcome") == "defer":
                streak += 1
            else:
                break
    return streak


async def tick() -> dict:
    cfg = _load_config()
    runs_path = _abs(cfg["paths"]["runs_log"])
    anomalies_path = _abs(cfg["paths"]["anomalies_log"])
    account = cfg["account"]["primary"]

    # 1. Perceive world
    try:
        world_blob = world.load_world(_abs(cfg["paths"]["world_targets"]))
    except FileNotFoundError:
        anomaly.emit(anomalies_path, "world_targets_missing")
        rec = {"outcome": "abort", "reason": "world_targets_missing"}
        _log_run(runs_path, rec)
        return rec

    cands = world.candidates(world_blob)
    by_idx = world.parked_rates_by_idx(_abs(cfg["paths"]["parked_rates_state"]))

    if not cands:
        rec = {"outcome": "defer", "reason": "no_candidates", "reject_counts": {}}
        _log_run(runs_path, rec)
        return rec

    # Data-quality anomaly: owner_handle null share
    null_handle = sum(1 for c in cands if not (c.get("v_acct") or "").strip())
    null_pct = 100.0 * null_handle / max(1, len(cands))
    if null_pct >= cfg["anomalies"]["owner_handle_null_pct_alert"]:
        anomaly.emit(
            anomalies_path,
            "data_quality_owner_handle_null",
            null_pct=round(null_pct, 1),
            sample=len(cands),
        )

    # 2. Read self state
    try:
        ss = await self_state.read_self_state(account=account)
    except Exception as e:  # noqa: BLE001
        anomaly.emit(anomalies_path, "self_state_read_failed", error=str(e))
        rec = {"outcome": "abort", "reason": "self_state_read_failed", "error": str(e)}
        _log_run(runs_path, rec)
        return rec

    # 3. Filter
    survivors, reject_counts = pfilter.apply(cands, by_idx, ss, cfg)

    if not survivors:
        rec = {
            "outcome": "defer",
            "reason": "all_rejected",
            "reject_counts": reject_counts,
            "candidates_seen": len(cands),
            "operator_node": ss["operator_node"],
        }
        _log_run(runs_path, rec)

        # Defer-streak anomaly (the dead-loop signal)
        streak = _recent_defer_streak(runs_path)
        if streak == cfg["anomalies"]["defer_streak_alert_threshold"]:
            anomaly.emit(
                anomalies_path,
                "defer_streak_threshold",
                streak=streak,
                last_reject_counts=reject_counts,
            )

        # Migration-candidate hint: high-margin candidate where no
        # striker is co-located. The optimizer can use this to plan
        # roster repositioning.
        striker_nodes = {
            v["node"] for v in ss["kamis"].values()
            if v.get("state") == "HARVESTING" and v.get("node") is not None
        }
        for c in cands[:5]:
            m = c.get("margin", 0) or 0
            if m >= cfg["predator"]["margin_floor"] + 10 and c.get("node_id") not in striker_nodes:
                anomaly.emit(
                    anomalies_path,
                    "migration_candidate",
                    target_node=c.get("node_id"),
                    striker_nodes=sorted(striker_nodes),
                    margin=m,
                    handle=c.get("v_acct"),
                )
                break
        return rec

    # 4. Pick
    ranked = targeting.rank(survivors)
    pick = ranked[0]

    # 5. Strike or hunt depending on mode
    if cfg["predator"]["hunting_mode"]:
        outcome = await hunt_module.hunt(pick, account=account)
        rec = {
            "outcome": "hunt",
            "candidates_seen": len(cands),
            "survivors": len(survivors),
            "reject_counts": reject_counts,
            **outcome,
        }
        _log_run(runs_path, rec)
        if not outcome.get("success"):
            anomaly.emit(
                anomalies_path,
                "hunt_failed",
                target=outcome.get("target"),
                aborted_at=outcome.get("aborted_at"),
                abort_reason=outcome.get("abort_reason"),
                total_gas=outcome.get("total_gas"),
            )
        return rec

    outcome = await strike.fire(pick, account=account)
    rec = {
        "outcome": "strike",
        "candidates_seen": len(cands),
        "survivors": len(survivors),
        "reject_counts": reject_counts,
        **outcome,
    }
    _log_run(runs_path, rec)

    if outcome["blocked"] or outcome.get("revert_reason"):
        anomaly.emit(
            anomalies_path,
            "strike_failed",
            target=outcome["target"],
            block_reason=outcome.get("block_reason"),
            revert_reason=outcome.get("revert_reason"),
        )
    return rec


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run perceive+filter+pick but do not call strike.fire().",
    )
    args = parser.parse_args()
    if args.dry_run:
        os.environ["KAMI_ZERO_DRY_RUN"] = "1"
    result = asyncio.run(tick())
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
