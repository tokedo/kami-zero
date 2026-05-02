"""
HP projection — forward-simulate a kami's current HP from last on-chain action.

HP is never stored on-chain directly. Sync HP reflects only the value at the
last action that touched the kami; between actions, HP must be COMPUTED from:
  - HARVESTING: strain accumulated from bounty earned over elapsed time
  - RESTING: metabolism recovery over elapsed time
  - DEAD: 0 (no progression)

Canonical formulas live in:
  systems/harvesting.md  (Fertility, Intensity, Bounty, Strain)
  systems/health.md       (maxHP, metabolism, recovery)
  systems/state-reading.md (projection patterns)

This module is self-contained — no chain reads, no MCP. Inputs are plain
Python dicts; outputs are plain dicts. Suitable for unit testing and
historical back-fitting against oracle liquidation events.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Affinity table — efficacy multiplier on Fertility (raw integer, /1000 -> x)
# Source: systems/harvesting.md table.
# ---------------------------------------------------------------------------

_AFFINITY_BEATS = {
    ("EERIE", "SCRAP"): True,
    ("SCRAP", "INSECT"): True,
    ("INSECT", "EERIE"): True,
}


def _is_strong(a: str, b: str) -> bool:
    return _AFFINITY_BEATS.get((a, b), False)


def _is_weak(a: str, b: str) -> bool:
    return _AFFINITY_BEATS.get((b, a), False)


def harvest_efficacy(body_aff: str, hand_aff: str, node_affinities: list[str]) -> int:
    """
    Efficacy multiplier (raw integer, divide by 1000 for the x-multiplier).
    Returns 1000 (neutral) if any affinity is NORMAL or unrecognized.

    Per harvesting.md, dual-affinity nodes ("EERIE, SCRAP") let the system
    pick the best matchup order. We try every (body_aff vs node_aff_i,
    hand_aff vs node_aff_j) combination and take the max — the canonical
    behavior is "best match wins".
    """
    if not node_affinities:
        return 1000

    body_aff = (body_aff or "").upper()
    hand_aff = (hand_aff or "").upper()

    best = 1000
    # Try each pair (body_node, hand_node) where the two node slots are distinct
    # if there are 2 affinities, else duplicate.
    nodes = [(a or "").upper() for a in node_affinities]
    if len(nodes) == 1:
        nodes = [nodes[0], nodes[0]]

    for body_node in nodes:
        for hand_node in nodes:
            base = 1000  # base
            # Body component: ±650 (or ±250 weak)
            if body_node == "NORMAL" or body_aff == "NORMAL":
                body_comp = 0
            elif body_aff == body_node:
                body_comp = 650
            elif _is_strong(body_aff, body_node):
                body_comp = 650
            elif _is_weak(body_aff, body_node):
                body_comp = -250
            else:
                body_comp = 0

            # Hand component: ±350 (or ±100 weak)
            if hand_node == "NORMAL" or hand_aff == "NORMAL":
                hand_comp = 0
            elif hand_aff == hand_node:
                hand_comp = 350
            elif _is_strong(hand_aff, hand_node):
                hand_comp = 350
            elif _is_weak(hand_aff, hand_node):
                hand_comp = -100
            else:
                hand_comp = 0

            cand = base + body_comp + hand_comp
            if cand > best:
                best = cand
    return best


# ---------------------------------------------------------------------------
# Bounty / strain
# ---------------------------------------------------------------------------


def projected_bounty(
    *,
    power: int,
    violence: int,
    elapsed_sec: float,
    efficacy: int,
    bounty_boost: int = 0,
    intensity_boost_per_hr: float = 0.0,
    fertility_boost_pct_x1000: int = 0,
    intensity_boost_pct_x1000: int = 0,
) -> float:
    """
    Forward-project bounty earned over `elapsed_sec` seconds of harvesting.
    Returns Musu (float — caller can floor for chain-equivalent).

    Inputs:
      power: total_power (post-shift, post-boost)
      violence: total_violence (post-shift, post-boost)
      elapsed_sec: seconds since harvest_start
      efficacy: from harvest_efficacy()
      bounty_boost: harvest_bounty_boost (×1000 prec, e.g. 100 = +10%)
      intensity_boost_per_hr: harvest_intensity_boost (Musu/hr; flat add)
      fertility_boost_pct_x1000: harvest_fertility_boost (×1000 prec)
      intensity_boost_pct_x1000: multiplicative boost on Intensity portion

    Formula (canonical, time-integrated):
      Fert  = Power * 1500 * Efficacy / 3600       # 1e6-prec Musu/sec
      Int(t) = 1e6 * (Violence*5 + t/60) * 10 / (480*3600)   # 1e6-prec Musu/sec
      Bounty = ∫(Fert+Int(t)) dt * (1+bounty_boost/1000) * (1+fertility/1000) / 1e6

    Plus flat intensity_boost_per_hr added in Musu directly.
    """
    P = power
    V = violence
    T = float(elapsed_sec)
    if T <= 0:
        return 0.0

    # Fertility component (1e6-prec Musu/sec)
    fert = P * 1500.0 * efficacy / 3600.0

    # Time-integrated intensity (in 1e6-prec Musu*sec)
    # Int(t) = 1e6*10/(480*3600) * (V*5 + t/60)
    # ∫Int(t) dt from 0..T = 1e6*10/(480*3600) * (V*5*T + T*T/120)
    int_const = 1e6 * 10.0 / (480.0 * 3600.0)
    int_integral = int_const * (V * 5.0 * T + T * T / 120.0)

    # Total raw bounty (still in 1e6-prec Musu*sec equivalent)
    raw = fert * T + int_integral

    # Apply fertility-boost (multiplies Fert portion only; conservative — use on raw)
    # Per oracle docs HFB is "% boost to base income rate"; treating as overall pct.
    fert_mult = 1.0 + fertility_boost_pct_x1000 / 1000.0
    int_mult = 1.0 + intensity_boost_pct_x1000 / 1000.0

    # Decompose: fertility part vs intensity part get different multipliers
    bounty_fert = (fert * T) * fert_mult / 1e6
    bounty_int = int_integral * int_mult / 1e6

    # Bounty boost is applied to the sum
    bounty_boost_mult = 1.0 + bounty_boost / 1000.0
    bounty = (bounty_fert + bounty_int) * bounty_boost_mult

    # Flat intensity_boost_per_hr (Musu/hr) → add over T seconds
    bounty += intensity_boost_per_hr * (T / 3600.0)

    return bounty


def strain_from_bounty(
    bounty: float,
    *,
    harmony: int,
    strain_boost: int = 0,
    strain_ratio: int = 0,
) -> float:
    """
    Strain (HP loss) from total bounty earned.

    Formula (harvesting.md):
      strain = ceil(bounty * 6500 * (1000 + strain_boost) / (1e6 * (Harmony + 20)))

    strain_boost is ×1000 prec (negative reduces strain). strain_ratio is the
    multiplier (×1000 prec) on the resulting strain — observed in slim's
    bonuses.harvest.strain.ratio. We treat both: ratio multiplies after.
    """
    if bounty <= 0:
        return 0.0
    s = bounty * 6500.0 * (1000.0 + strain_boost) / (1e6 * (harmony + 20.0))
    s *= 1.0 + strain_ratio / 1000.0
    # Game rounds via ceil — match it
    return math.ceil(max(0.0, s))


# ---------------------------------------------------------------------------
# Resting recovery
# ---------------------------------------------------------------------------


def projected_recovery(
    *,
    harmony: int,
    elapsed_sec: float,
    rest_metabolism_boost: int = 0,
) -> float:
    """
    HP recovered while RESTING.

    metabolism = 1000 * (Harmony + 20) * 600 * (1000 + rest_boost) / 3600
    recovery   = floor(elapsedSeconds * metabolism / 1e9)
    """
    if elapsed_sec <= 0:
        return 0.0
    metabolism = 1000.0 * (harmony + 20.0) * 600.0 * (1000.0 + rest_metabolism_boost) / 3600.0
    recovery = math.floor(elapsed_sec * metabolism / 1e9)
    return recovery


# ---------------------------------------------------------------------------
# maxHP
# ---------------------------------------------------------------------------


def max_hp(base: int, shift: int, boost: int) -> int:
    """maxHP = max(0, floor((1000 + boost) * (base + shift) / 1000))"""
    return max(0, math.floor((1000 + boost) * (base + shift) / 1000.0))


# ---------------------------------------------------------------------------
# compute_current_hp — main entry
# ---------------------------------------------------------------------------


@dataclass
class HPProjection:
    projected_hp: float
    sync_hp: float
    max_hp: int
    state: str
    elapsed_sec: float
    formula_branch: str
    confidence: float
    notes: list[str]

    def to_dict(self) -> dict:
        return {
            "projected_hp": self.projected_hp,
            "sync_hp": self.sync_hp,
            "max_hp": self.max_hp,
            "state": self.state,
            "elapsed_sec": self.elapsed_sec,
            "formula_branch": self.formula_branch,
            "confidence": self.confidence,
            "notes": list(self.notes),
        }


def compute_current_hp(
    *,
    state: str,
    sync_hp: float,
    base_hp: int,
    shift_hp: int,
    boost_hp: int,
    last_action_ts: int,
    now_ts: int,
    # Harvesting-only:
    harvest_start_ts: int | None = None,
    power: int = 0,
    violence: int = 0,
    harmony: int = 0,
    body_affinity: str = "NORMAL",
    hand_affinity: str = "NORMAL",
    node_affinities: list[str] | None = None,
    strain_boost: int = 0,           # ×1000 prec, negative = less strain
    strain_ratio: int = 0,           # ×1000 prec, post-multiplier
    bounty_boost: int = 0,           # ×1000 prec, harvest_bounty_boost
    fertility_boost: int = 0,        # ×1000 prec, harvest_fertility_boost
    intensity_boost_pct: int = 0,    # ×1000 prec, harvest_intensity_boost (% form)
    intensity_boost_flat: float = 0, # Musu/hr flat add
    bounty_pool_now: float | None = None,  # live harvest.bounty.balance from chain
    # Resting-only:
    rest_metabolism_boost: int = 0,  # ×1000 prec
) -> HPProjection:
    """
    Forward-simulate a kami's HP from last_action_ts to now_ts.

    For HARVESTING: requires harvest_start_ts (or last_action_ts as fallback).
    Returns projected current HP using the canonical strain formula.

    Confidence:
      1.0 — formula directly applied with all inputs known
      0.7 — formula applied with one or more boost inputs defaulted to 0
      0.5 — best-effort projection (state has no formula here, e.g. EXTERNAL)
    """
    notes: list[str] = []
    state_u = (state or "").upper()
    mhp = max_hp(base_hp, shift_hp, boost_hp)
    elapsed = max(0.0, float(now_ts) - float(last_action_ts))

    if state_u == "DEAD":
        return HPProjection(
            projected_hp=0.0, sync_hp=sync_hp, max_hp=mhp, state="DEAD",
            elapsed_sec=elapsed, formula_branch="dead", confidence=1.0, notes=notes,
        )

    if state_u == "RESTING":
        recovery = projected_recovery(
            harmony=harmony, elapsed_sec=elapsed,
            rest_metabolism_boost=rest_metabolism_boost,
        )
        proj = min(mhp, sync_hp + recovery)
        if rest_metabolism_boost == 0 and harmony > 0:
            confidence = 0.95
        else:
            confidence = 1.0
        return HPProjection(
            projected_hp=proj, sync_hp=sync_hp, max_hp=mhp, state="RESTING",
            elapsed_sec=elapsed, formula_branch="resting_metabolism",
            confidence=confidence, notes=notes,
        )

    if state_u == "HARVESTING":
        # VALIDATED MODEL (back-fit 99.5% on 200 historical kills, 7d window):
        #
        # Strain only applies to the CURRENT uncollected bounty pool. Each
        # harvest_collect tx drains the pool and applies strain at that moment,
        # updating sync_hp on chain. Between actions, the pool grows but no
        # HP loss is recorded until the next sync.
        #
        # Therefore:
        #   projected_hp = sync_hp − strain(current_pool)
        #
        # where current_pool is read live from the harvest entity's bounty.balance
        # (passed in as `bounty_pool_now`), or projected from the time since the
        # last sync (harvest_start OR latest harvest_collect — pick the more recent).
        #
        # Per-collect ceil rounding accumulates only across past collects (already
        # baked into sync_hp); for the current live projection it doesn't matter.
        start_ts = harvest_start_ts if harvest_start_ts is not None else last_action_ts
        harvest_elapsed = max(0.0, float(now_ts) - float(start_ts))
        if node_affinities is None:
            node_affinities = ["NORMAL"]
            notes.append("node_affinities defaulted to NORMAL")

        eff = harvest_efficacy(body_affinity, hand_affinity, node_affinities)

        if bounty_pool_now is not None:
            # Live mode: caller passed the on-chain current pool. Best path.
            pool = float(bounty_pool_now)
            confidence = 0.95
            notes.append(f"bounty_pool_now={pool:.1f} (live)")
        else:
            # Projection mode: estimate pool from elapsed since last sync.
            # NOTE: empirical back-fit shows the canonical Fertility+Intensity
            # formula UNDER-projects bounty by ~1.5× for many builds (likely
            # because Boost factor / equipment effects aren't fully modeled).
            # When using projected pool for striking decisions, prefer reading
            # bounty.balance live; fall back to this with strain_mult ≥ 1.5.
            pool = projected_bounty(
                power=power, violence=violence, elapsed_sec=harvest_elapsed,
                efficacy=eff, bounty_boost=bounty_boost,
                intensity_boost_per_hr=intensity_boost_flat,
                fertility_boost_pct_x1000=fertility_boost,
                intensity_boost_pct_x1000=intensity_boost_pct,
            )
            confidence = 0.7
            notes.append(f"bounty projected from elapsed={harvest_elapsed:.0f}s (no live pool)")

        strain = strain_from_bounty(
            pool, harmony=harmony,
            strain_boost=strain_boost, strain_ratio=strain_ratio,
        )
        proj = max(0.0, sync_hp - strain)

        return HPProjection(
            projected_hp=proj, sync_hp=sync_hp, max_hp=mhp, state="HARVESTING",
            elapsed_sec=harvest_elapsed, formula_branch="harvesting_pool_strain",
            confidence=confidence, notes=[
                *notes, f"efficacy={eff}", f"pool={pool:.1f}", f"strain={strain:.1f}",
            ],
        )

    notes.append(f"unknown state '{state}' — returning sync_hp")
    return HPProjection(
        projected_hp=sync_hp, sync_hp=sync_hp, max_hp=mhp, state=state_u,
        elapsed_sec=elapsed, formula_branch="passthrough", confidence=0.3,
        notes=notes,
    )


# ---------------------------------------------------------------------------
# Kill threshold (reproduced from systems/liquidation.md for back-fit)
# ---------------------------------------------------------------------------


def _gaussian_cdf(x: float) -> float:
    """Standard-normal CDF (no external deps)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def kill_threshold(
    *,
    attacker_violence: int,
    victim_harmony: int,
    victim_max_hp: int,
    atk_threshold_shift: int = 0,    # ×1000 prec
    atk_threshold_ratio: int = 0,    # ×1000 prec (slim returns 500 = 0.5)
    def_threshold_shift: int = 0,    # ×1000 prec
    def_threshold_ratio: int = 0,    # ×1000 prec
    affinity_efficacy: float = 1.0,  # placeholder — exact contribution still empirical
) -> dict:
    """
    Returns dict with animosity, threshold_ratio, kill_zone, formula_used.

    Empirical formula (sessions 76-79):
      threshold_ratio = (animosity + atk_shift − def_shift) × (1 − def_ratio)
      kill_zone       = threshold_ratio × victim_max_hp
      strike clears iff projected_HP < kill_zone (strict <)

    The contribution of `atk_threshold_ratio` and the `affinity_efficacy`
    multiplier are NOT included here — they didn't reproduce empirically
    in sessions 77-78 reverts. Back-fit will reveal whether they belong.
    """
    if victim_harmony <= 0:
        victim_harmony = 1
    combat_ratio = math.log(max(1, attacker_violence) / victim_harmony)
    animosity = _gaussian_cdf(combat_ratio)

    atk_s = atk_threshold_shift / 1000.0
    def_s = def_threshold_shift / 1000.0
    def_r = def_threshold_ratio / 1000.0

    threshold_ratio = (animosity + atk_s - def_s) * (1.0 - def_r)
    kill_zone = threshold_ratio * victim_max_hp

    return {
        "animosity": animosity,
        "atk_shift": atk_s,
        "def_shift": def_s,
        "def_ratio": def_r,
        "threshold_ratio": threshold_ratio,
        "kill_zone": kill_zone,
        "victim_max_hp": victim_max_hp,
    }
