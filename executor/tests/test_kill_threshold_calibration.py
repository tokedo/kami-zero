"""Calibration: kill_threshold() must match the team's official liquidation
calculator on the 6 founder cross-check cases (2026-05-02). This is the
regression bar for any future kill-formula change.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hp_projection import kill_threshold


CASES = [
    # (label, kwargs, expected_death_below_hp)
    (
        "INSECT->SCRAP weak + atk_ratio=25%, atk_shift=20%",
        dict(
            attacker_violence=38,
            victim_harmony=15,
            victim_max_hp=150,
            atk_threshold_shift=200,   # +0.20
            atk_threshold_ratio=250,   # +0.25 (gated out by weak matchup)
            attacker_hand="INSECT",
            victim_body="SCRAP",
        ),
        54,
    ),
    (
        "EERIE->SCRAP strong, no bonuses",
        dict(
            attacker_violence=36,
            victim_harmony=20,
            victim_max_hp=200,
            attacker_hand="EERIE",
            victim_body="SCRAP",
        ),
        86,
    ),
    (
        "SCRAP->EERIE weak, no bonuses",
        dict(
            attacker_violence=36,
            victim_harmony=20,
            victim_max_hp=200,
            attacker_hand="SCRAP",
            victim_body="EERIE",
        ),
        28,
    ),
    (
        "NORMAL->NORMAL special + atk_ratio=20%",
        dict(
            attacker_violence=36,
            victim_harmony=20,
            victim_max_hp=200,
            atk_threshold_ratio=200,
            attacker_hand="NORMAL",
            victim_body="NORMAL",
        ),
        80,
    ),
    (
        "NORMAL->NORMAL special + def_ratio=20%",
        dict(
            attacker_violence=36,
            victim_harmony=20,
            victim_max_hp=200,
            def_threshold_ratio=200,
            attacker_hand="NORMAL",
            victim_body="NORMAL",
        ),
        57,
    ),
    (
        "EERIE->SCRAP strong + atk_ratio=20%",
        dict(
            attacker_violence=36,
            victim_harmony=20,
            victim_max_hp=200,
            atk_threshold_ratio=200,
            attacker_hand="EERIE",
            victim_body="SCRAP",
        ),
        98,
    ),
]


def main() -> int:
    fails = 0
    for label, kwargs, expected in CASES:
        result = kill_threshold(**kwargs)
        actual = int(result["kill_zone"])
        ok = actual == expected
        marker = "OK" if ok else "FAIL"
        print(f"[{marker}] {label}: expected={expected} actual={actual} "
              f"(animosity={result['animosity']:.4f}, eff={result['efficacy']:.4f})")
        if not ok:
            fails += 1
    print()
    print(f"{len(CASES) - fails}/{len(CASES)} tests pass")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
