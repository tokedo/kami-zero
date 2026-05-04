#!/usr/bin/env python3
"""Parked-rates background refresher.

Reads the top-N candidates from `predator/world_targets.json`, calls the
Kamibots playwright slim endpoint for each, and writes a per-victim
snapshot of the on-chain harvest rates / sync HP to
`predator/parked_rates_state.json`. The watcher consumes that file to
filter `killable_v2` rows whose chain state shows the parked-rates pattern
(rates.intensity.average == 0 AND rates.fertility == 0 AND balance == 0
AND state == "ACTIVE" AND sync == total).

Designed to run on a 5-min cron without any LLM in the loop.

Hard-rule note: CLAUDE.md hard rule #8 forbids Kamibots state reads in any
predator-decision path. Oracle does not currently surface the on-chain
harvest.rates fields (ideas_to_founder.md § 6 ask). Until oracle exposes
them, this cron is the sanctioned workaround per ideas_to_founder § 6.3
("kami-zero will pre-strike slim-verify rates.intensity > 0"). Migrate to
oracle the moment the field lands.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
WORLD_TARGETS_PATH = REPO_ROOT / "predator" / "world_targets.json"
OUTPUT_PATH = REPO_ROOT / "predator" / "parked_rates_state.json"
ENV_PATH = Path.home() / ".blocklife-keys" / ".env"

KAMIBOTS_BASE = "https://api.kamibots.xyz"
TOP_N = 50           # candidates per cycle (matches killable_v2 size)
REQ_TIMEOUT = 15     # seconds per slim call
SLEEP_BETWEEN = 0.05 # 50ms politeness pause between calls
MAX_TOTAL_SEC = 240  # hard ceiling so the cron never overlaps a 5-min window


def load_api_key() -> str:
    """Read KAMIBOTS_API_KEY from ~/.blocklife-keys/.env (no python-dotenv)."""
    if not ENV_PATH.exists():
        raise RuntimeError(f"env file missing: {ENV_PATH}")
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            if k.strip() == "KAMIBOTS_API_KEY":
                return v.strip()
    raise RuntimeError("KAMIBOTS_API_KEY missing from .env")


def fetch_slim(kami_index: int, api_key: str) -> dict | None:
    """GET /api/playwright/kami/{idx}/slim. Returns parsed dict or None on error."""
    req = urllib.request.Request(
        f"{KAMIBOTS_BASE}/api/playwright/kami/{kami_index}/slim",
        headers={"X-Agent-Key": api_key},
    )
    try:
        with urllib.request.urlopen(req, timeout=REQ_TIMEOUT) as r:
            return json.loads(r.read())
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
        print(f"slim {kami_index} error: {type(e).__name__}: {e}", file=sys.stderr)
        return None


def extract_state(slim: dict) -> dict | None:
    """Pull the parked-rates 5-tuple + a couple of context fields from slim."""
    if not isinstance(slim, dict):
        return None
    harvest = slim.get("harvest") or {}
    stats = slim.get("stats") or {}
    health = stats.get("health") or {}
    rates = harvest.get("rates") or {}
    intensity = rates.get("intensity") or {}

    try:
        rates_intensity_avg = int(intensity.get("average") or 0)
        rates_fertility = int(rates.get("fertility") or 0)
        balance = int(harvest.get("balance") or 0)
        sync_hp = int(health.get("sync") or 0)
        total_hp = int(health.get("total") or 0)
    except (TypeError, ValueError):
        return None

    harvest_state = (harvest.get("state") or "").upper()
    kami_state = (slim.get("state") or "").upper()

    # Parked-rates signal: when both rate components are zero AND no balance is
    # accumulating AND the entity is still ACTIVE, no strain is being applied
    # going forward — the watcher's elapsed-based proj_hp is invalid for this
    # candidate. We do NOT require sync==total (s155 observed brief sync<total
    # windows on otherwise-parked 4444… rows; the rate-triplet is the canonical
    # disqualifier, sync==total was an incidental corollary in s152 doctrine).
    parked_bool = (
        rates_intensity_avg == 0
        and rates_fertility == 0
        and balance == 0
        and harvest_state == "ACTIVE"
        and sync_hp > 0
    )

    return {
        "rates_intensity_avg": rates_intensity_avg,
        "rates_fertility": rates_fertility,
        "balance": balance,
        "sync": sync_hp,
        "total": total_hp,
        "harvest_state": harvest_state,
        "kami_state": kami_state,
        "parked_bool": parked_bool,
        "last_checked_ts": int(time.time()),
    }


def load_candidates() -> list[dict]:
    """Read killable_v2 (margin-sorted) from the watcher snapshot."""
    if not WORLD_TARGETS_PATH.exists():
        print(f"world_targets.json missing — run watcher first", file=sys.stderr)
        return []
    try:
        with open(WORLD_TARGETS_PATH) as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"world_targets.json read error: {e}", file=sys.stderr)
        return []
    return data.get("killable_v2") or []


def main() -> int:
    t0 = time.time()
    api_key = load_api_key()
    candidates = load_candidates()
    if not candidates:
        # Still emit an empty snapshot so consumers can detect "scanner ran but
        # had no work" vs "scanner stale".
        snap = {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "scan_duration_sec": round(time.time() - t0, 2),
            "candidates_scanned": 0,
            "candidates_skipped_resting": 0,
            "candidates_failed": 0,
            "schema_version": 1,
            "by_idx": {},
        }
        OUTPUT_PATH.with_suffix(".json.tmp").write_text(json.dumps(snap, indent=2))
        OUTPUT_PATH.with_suffix(".json.tmp").rename(OUTPUT_PATH)
        print("parked_rates_state.json: 0 candidates (no killable_v2 in watcher)")
        return 0

    by_idx: dict[str, dict] = {}
    skipped_resting = 0
    failed = 0

    for c in candidates[:TOP_N]:
        if time.time() - t0 > MAX_TOTAL_SEC:
            print(f"hit MAX_TOTAL_SEC={MAX_TOTAL_SEC}; stopping early", file=sys.stderr)
            break
        v_idx = c.get("v_idx")
        if v_idx is None:
            continue
        slim = fetch_slim(int(v_idx), api_key)
        if slim is None:
            failed += 1
            continue
        st = extract_state(slim)
        if st is None:
            failed += 1
            continue
        # Skip non-HARVESTING — they cycled out between watcher scan and slim call.
        # Watcher will pick them up again next cycle if they restart.
        if st["kami_state"] != "HARVESTING":
            skipped_resting += 1
            continue
        st["v_acct"] = c.get("v_acct")
        st["node_id"] = c.get("node_id")
        by_idx[str(int(v_idx))] = st
        time.sleep(SLEEP_BETWEEN)

    snap = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "scan_duration_sec": round(time.time() - t0, 2),
        "candidates_scanned": len(by_idx),
        "candidates_skipped_resting": skipped_resting,
        "candidates_failed": failed,
        "schema_version": 1,
        "by_idx": by_idx,
    }
    tmp = OUTPUT_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(snap, indent=2))
    tmp.rename(OUTPUT_PATH)

    n_parked = sum(1 for v in by_idx.values() if v["parked_bool"])
    print(
        f"parked_rates_state.json refreshed: {len(by_idx)} HARVESTING / "
        f"{n_parked} parked / {skipped_resting} skipped-resting / {failed} failed "
        f"in {snap['scan_duration_sec']}s"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
