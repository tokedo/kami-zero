"""
Back-fit validation for compute_current_hp.

Loads a JSON dump of historical liquidations (one row per kill, enriched with
victim + attacker static fields and node affinity), runs hp_projection over
each row, and reports accuracy:

  "Correctly explained" iff projected_HP < kill_zone (strict <).

Usage:
    python -m executor.scripts.backfit_liquidations <input.json>

Input JSON shape: either:
  (a) {"columns": [...], "rows": [[...], ...]}  -- raw oracle_sql response
  (b) [{"col": val, ...}, ...]                  -- already-rowified records

Output: stdout report, plus a per-row CSV at /tmp/backfit_rows.csv for
deeper inspection.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Allow `python -m executor.scripts.backfit_liquidations` from repo root or
# `python executor/scripts/backfit_liquidations.py` ad-hoc.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import math

from executor.hp_projection import (
    compute_current_hp,
    kill_threshold,
    harvest_efficacy,
    strain_from_bounty,
)


def _normalize(payload) -> list[dict]:
    """Accept either oracle_sql columns/rows shape or a list of dicts."""
    if isinstance(payload, dict) and "columns" in payload and "rows" in payload:
        cols = payload["columns"]
        return [dict(zip(cols, r)) for r in payload["rows"]]
    if isinstance(payload, list):
        return payload
    raise ValueError("unrecognized input shape")


def _safe_int(x, default=0) -> int:
    try:
        return int(x) if x is not None else default
    except (TypeError, ValueError):
        return default


def _safe_str(x, default="NORMAL") -> str:
    if x is None:
        return default
    return str(x).upper()


def _split_node_affinities(node_affinity_str: str | None) -> list[str]:
    if not node_affinity_str:
        return ["NORMAL"]
    parts = [p.strip().upper() for p in node_affinity_str.split(",") if p.strip()]
    return parts or ["NORMAL"]


def empirical_strain(
    *,
    sum_collected: int,
    n_collects: int,
    liq_musu: int,
    harmony: int,
    strain_boost: int = 0,
    spoils_ratio_assumed: float = 0.5,
) -> float:
    """
    Empirical strain using actual oracle collect data.

    Per-collect strain applies ceil rounding *separately on each collect
    amount*, so total strain > strain(total_bounty) when many small collects
    happen. Plus the final uncollected pool at liq adds more strain.

    sum_collected : sum of actual collected MUSU during this harvest
    n_collects    : number of harvest_collect events
    liq_musu      : MUSU stolen by attacker (= spoils, fraction of final pool)
    spoils_ratio_assumed : approximate spoils fraction (default 0.5 ⇒ pool ≈ 2× liq_musu)

    Returns total strain HP loss.
    """
    avg_per_collect = (sum_collected / n_collects) if n_collects > 0 else 0.0
    per_collect_strain = strain_from_bounty(
        avg_per_collect, harmony=harmony, strain_boost=strain_boost,
    )
    # Final pool at liq (includes uncollected since last collect)
    final_pool_est = (liq_musu / spoils_ratio_assumed) if spoils_ratio_assumed > 0 else liq_musu
    final_strain = strain_from_bounty(
        final_pool_est, harmony=harmony, strain_boost=strain_boost,
    )
    return n_collects * per_collect_strain + final_strain


def backfit_one(row: dict, *, mode: str = "formula", strain_mult: float = 1.0) -> dict:
    """
    Run projection + threshold for one liquidation row.
    mode:
      "formula"   — use canonical formula (projected_bounty)
      "empirical" — use actual collect data from oracle
    strain_mult — multiplier on strain (calibration knob; 1.0 = canonical)
    """
    elapsed = _safe_int(row.get("elapsed_sec"))

    # Victim build
    v_total_hp = _safe_int(row.get("v_total_hp"))
    v_base_hp = _safe_int(row.get("v_base_hp"))
    v_power = _safe_int(row.get("v_power"))
    v_violence = _safe_int(row.get("v_violence"))
    v_harmony = _safe_int(row.get("v_harmony"))
    v_body = _safe_str(row.get("v_body_aff"))
    v_hand = _safe_str(row.get("v_hand_aff"))
    v_sb = _safe_int(row.get("v_sb"))
    v_hib = _safe_int(row.get("v_hib"))
    v_hfb = _safe_int(row.get("v_hfb"))
    v_hbb = _safe_int(row.get("v_hbb"))
    v_dts = _safe_int(row.get("v_dts"))
    v_dtr = _safe_int(row.get("v_dtr"))

    a_violence = _safe_int(row.get("a_violence"))
    a_ats = _safe_int(row.get("a_ats"))
    a_atr = _safe_int(row.get("a_atr"))

    node_affs = _split_node_affinities(row.get("node_affinity"))

    if mode == "empirical" and "sum_collected" in row:
        # Use ACTUAL collected musu from oracle for strain
        strain = empirical_strain(
            sum_collected=_safe_int(row.get("sum_collected")),
            n_collects=_safe_int(row.get("n_collects")),
            liq_musu=_safe_int(row.get("liq_musu")),
            harmony=v_harmony, strain_boost=v_sb,
        )
        strain *= strain_mult
        projected_hp = max(0.0, v_total_hp - strain)
        formula_branch = "empirical_strain"
        notes_str = f"sum_collected={row.get('sum_collected')}, n_collects={row.get('n_collects')}, strain={strain:.1f}"
    else:
        proj = compute_current_hp(
            state="HARVESTING",
            sync_hp=v_total_hp,
            base_hp=v_base_hp,
            shift_hp=v_total_hp - v_base_hp,
            boost_hp=0,
            last_action_ts=0, now_ts=elapsed,
            harvest_start_ts=0,
            power=v_power, violence=v_violence, harmony=v_harmony,
            body_affinity=v_body, hand_affinity=v_hand,
            node_affinities=node_affs,
            strain_boost=v_sb,
            strain_ratio=0,
            bounty_boost=v_hbb,
            fertility_boost=v_hfb,
            intensity_boost_pct=0,
            intensity_boost_flat=v_hib,
        )
        # Apply strain multiplier
        strain = (v_total_hp - proj.projected_hp) * strain_mult
        projected_hp = max(0.0, v_total_hp - strain)
        formula_branch = proj.formula_branch
        notes_str = "; ".join(proj.notes)

    kt = kill_threshold(
        attacker_violence=a_violence,
        victim_harmony=v_harmony,
        victim_max_hp=v_total_hp,
        atk_threshold_shift=a_ats,
        atk_threshold_ratio=a_atr,
        def_threshold_shift=v_dts,
        def_threshold_ratio=v_dtr,
    )

    explained = projected_hp < kt["kill_zone"]
    margin = kt["kill_zone"] - projected_hp

    return {
        **row,
        "projected_hp": round(projected_hp, 2),
        "kill_zone": round(kt["kill_zone"], 2),
        "animosity": round(kt["animosity"], 4),
        "threshold_ratio": round(kt["threshold_ratio"], 4),
        "explained": explained,
        "margin": round(margin, 2),
        "formula_branch": formula_branch,
        "notes": notes_str,
    }


def report(rows: list[dict], *, mode: str = "formula", strain_mult: float = 1.0) -> None:
    enriched = [backfit_one(r, mode=mode, strain_mult=strain_mult) for r in rows]
    print(f"\n=== Mode: {mode!r}, strain_mult={strain_mult} ===")

    n = len(enriched)
    m = sum(1 for e in enriched if e["explained"])
    pct = 100.0 * m / n if n else 0.0

    print(f"\n=== Back-fit summary ===")
    print(f"N kills sampled : {n}")
    print(f"M explained     : {m}  ({pct:.1f}%)")
    print(f"Target          : ≥ 90%\n")

    # Miss-mode breakdown
    misses = [e for e in enriched if not e["explained"]]
    if misses:
        # Bucket by margin sign / size
        proj_too_high = [e for e in misses if e["projected_hp"] >= e["kill_zone"]]
        print(f"Miss-modes ({len(misses)} total):")
        print(f"  projected_HP ≥ kill_zone (underestimating strain): {len(proj_too_high)}")
        # Distribution of margin (how far off)
        if proj_too_high:
            avg_excess = sum(e["projected_hp"] - e["kill_zone"] for e in proj_too_high) / len(proj_too_high)
            print(f"    avg gap (proj_HP − kill_zone): {avg_excess:.1f} HP")
            # Top 5 worst misses
            print("\n  Top 5 worst misses (largest proj_HP − kill_zone):")
            worst = sorted(proj_too_high, key=lambda e: e["projected_hp"] - e["kill_zone"], reverse=True)[:5]
            for e in worst:
                print(
                    f"    v_idx={e.get('v_idx'):<5} elapsed={e.get('elapsed_sec'):>6}s  "
                    f"v_HP={e.get('v_total_hp'):>4} sb={e.get('v_sb'):>4}  "
                    f"H={e.get('v_harmony'):>3} P={e.get('v_power'):>3}  "
                    f"node_aff={e.get('node_affinity')!s:<14}  "
                    f"proj={e['projected_hp']:>6.1f}  kz={e['kill_zone']:>6.1f}  "
                    f"gap={e['projected_hp'] - e['kill_zone']:>6.1f}"
                )

    # CSV dump for inspection
    if enriched:
        import csv
        out = Path("/tmp/backfit_rows.csv")
        with out.open("w", newline="") as fh:
            keys = list(enriched[0].keys())
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            for e in enriched:
                w.writerow(e)
        print(f"\nPer-row CSV: {out}")

    # Summary by elapsed bucket — long harvests vs short
    by_bucket = {"<1h": [], "1-6h": [], "6-24h": [], "1-3d": [], ">3d": []}
    for e in enriched:
        s = e.get("elapsed_sec") or 0
        if s < 3600:
            by_bucket["<1h"].append(e)
        elif s < 21600:
            by_bucket["1-6h"].append(e)
        elif s < 86400:
            by_bucket["6-24h"].append(e)
        elif s < 259200:
            by_bucket["1-3d"].append(e)
        else:
            by_bucket[">3d"].append(e)
    print("\nAccuracy by elapsed bucket:")
    for k, lst in by_bucket.items():
        if not lst:
            continue
        ok = sum(1 for e in lst if e["explained"])
        print(f"  {k:>5}: {ok}/{len(lst)}  ({100*ok/len(lst):.1f}%)")


def main():
    if len(sys.argv) < 2:
        print("usage: backfit_liquidations.py <input.json> [mode] [strain_mult]")
        sys.exit(1)
    src = Path(sys.argv[1])
    mode = sys.argv[2] if len(sys.argv) > 2 else "formula"
    strain_mult = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    raw = src.read_text()

    payload = json.loads(raw)
    if (
        isinstance(payload, list)
        and len(payload) == 1
        and isinstance(payload[0], dict)
        and "text" in payload[0]
    ):
        payload = json.loads(payload[0]["text"])

    rows = _normalize(payload)
    report(rows, mode=mode, strain_mult=strain_mult)


if __name__ == "__main__":
    main()
