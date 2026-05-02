"""
HP projection — forward-simulate a kami's current HP from last on-chain action.

HP is never stored on-chain directly. Sync HP reflects only the value at the
last action that touched the kami; between actions, HP must be COMPUTED from:
  - HARVESTING: strain accumulated from bounty earned over elapsed time
  - RESTING: metabolism recovery over elapsed time
  - DEAD: 0 (no progression)

Canonical formulas live in:
  systems/harvesting.md       (Fertility, Intensity, Bounty, Strain)
  systems/health.md           (maxHP, metabolism, recovery)
  systems/state-reading.md    (projection patterns)
  systems/liquidation.md      (kill threshold + affinity triangle)

This module is self-contained — no chain reads, no MCP. Inputs are plain
Python dicts; outputs are plain dicts. Suitable for unit testing and
historical back-fitting against oracle liquidation events.

Founder cross-check (2026-05-02) corrected two structural bugs:
  Bug 1 — harvest_efficacy was using the LIQUIDATION rock-paper-scissors
          triangle (EERIE > SCRAP > INSECT > EERIE). Harvest's rule is
          simpler: same affinity = strong, different non-NORMAL = weak,
          NORMAL = neutral. The triangle now lives only in kill_threshold().
  Bug 2 — projected_bounty integrated Intensity over [0,T]. The contract
          uses end-of-period rate × Duration ("snapshot" semantics). This
          mostly hurt long-runners (~33% under-projection at 18h elapsed).

These fixes match founder client-truth for 5 cross-check kamis at 0.11%
mean error — see predator/mechanics.md § "Validated formula corrections
(founder cross-check 2026-05-02)".
"""

from __future__ import annotations

import math
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Affinity — HARVEST rule (per systems/harvesting.md § "Affinity Match")
# Same non-NORMAL → strong (+650 body / +350 hand)
# Different non-NORMAL → weak (-250 body / -100 hand)
# NORMAL on either side → neutral (0)
# NOT the liquidation triangle — that lives in kill_threshold().
# ---------------------------------------------------------------------------


def _harvest_component(trait_aff: str, node_aff: str, strong_bonus: int, weak_penalty: int) -> int:
    if trait_aff == "NORMAL" or node_aff == "NORMAL":
        return 0
    if trait_aff == node_aff:
        return strong_bonus
    return weak_penalty


def harvest_efficacy(body_aff: str, hand_aff: str, node_affinities: list[str]) -> int:
    """Efficacy multiplier for HARVEST (raw integer, /1000 for the x-multiplier).

    Per systems/harvesting.md § "Affinity Match" — same affinity is strong,
    different non-NORMAL is weak, NORMAL on either side is neutral. There is
    no rock-paper-scissors triangle in harvesting. The triangle is for
    LIQUIDATION efficacy only — see kill_threshold().

    Dual-affinity nodes (e.g., "EERIE, SCRAP"): both body AND hand check
    against the SAME single node affinity slot — they cannot independently
    pick different slots. The system picks the slot that maximizes overall
    efficacy. Founder cross-check confirmed kami 16479 (body=SCRAP,
    hand=EERIE) on node 82 EERIE+SCRAP yields 1550 (both checked against
    SCRAP: body match +650, hand mismatch −100), NOT 2000.
    """
    if not node_affinities:
        return 1000

    body_aff = (body_aff or "").upper()
    hand_aff = (hand_aff or "").upper()
    nodes = list(dict.fromkeys((a or "").upper() for a in node_affinities))
    if not nodes:
        return 1000

    best = 1000
    for slot in nodes:
        cand = (
            1000
            + _harvest_component(body_aff, slot, 650, -250)
            + _harvest_component(hand_aff, slot, 350, -100)
        )
        if cand > best:
            best = cand
    return best


# ---------------------------------------------------------------------------
# LIQUIDATION affinity — rock-paper-scissors triangle (attacker hand vs victim body)
# Used only in kill_threshold(). EERIE > SCRAP > INSECT > EERIE; NORMAL is neutral.
# ---------------------------------------------------------------------------


_LIQ_TRIANGLE = {
    ("EERIE", "SCRAP"),   # attacker EERIE strong vs victim SCRAP body
    ("SCRAP", "INSECT"),
    ("INSECT", "EERIE"),
}


def _liq_affinity_shift(attacker_hand: str, victim_body: str) -> int:
    """Threshold-efficacy affinity shift (×1000 prec).

    Per systems/liquidation.md and the team's liquidation calculator
    (founder cross-check 2026-05-02, 6/6 tests):
      NORMAL on either side  → +200  (special, +0.2)
      same affinity (non-NORMAL) → 0
      attacker hand strong vs victim body → +500  (+0.5)
      attacker hand weak vs victim body   → −500  (−0.5)
    """
    a = (attacker_hand or "").upper()
    v = (victim_body or "").upper()
    if a == "NORMAL" or v == "NORMAL":
        return 200
    if a == v:
        return 0
    if (a, v) in _LIQ_TRIANGLE:
        return 500
    if (v, a) in _LIQ_TRIANGLE:
        return -500
    return 0


# ---------------------------------------------------------------------------
# Bounty / strain — END-OF-PERIOD × DURATION semantics (Bug 2 fix)
#
# Per systems/harvesting.md "Yield & Timing":
#   bounty = (rate × duration × boost) / precision
#   rate = fertility + intensity     (1e6-prec MUSU/sec, snapshotted at sync)
#   intensity = 1e6 * (V*5 + minutes_elapsed) * boost / (480 * 3600)
#   duration = seconds since last sync
#
# This is "rate at end-of-period × duration" — NOT a time-integral. The
# previous time-integration form ∫Int(t)dt = const*(V*5*T + T²/120) gave half
# the linear-time intensity contribution and produced ~33% under-projection
# on 16479-class long-runners (18h elapsed). Founder cross-check on 5 kamis
# confirms the snapshot form matches client truth at 0.11% mean error.
# ---------------------------------------------------------------------------


def projected_bounty(
    *,
    power: int,
    violence: int,
    elapsed_sec: float,
    efficacy: int,
    bounty_boost: int = 0,
    intensity_boost_pct: int = 0,        # ×1000 prec — additive on the BASE intensity boost (10)
    fertility_boost_pct_x1000: int = 0,
) -> float:
    """End-of-period × Duration bounty projection (canonical snapshot form).

    Inputs:
      power, violence: total stats (post-shift, post-boost)
      elapsed_sec: seconds since harvest_start (or last sync if a sub-segment)
      efficacy: from harvest_efficacy()
      bounty_boost: HARV_BOUNTY_BOOST (×1000 prec, additive on 1000 base)
      intensity_boost_pct: HARV_INTENSITY_BOOST (additive on the 10 base
                          intensity-boost factor in the formula)
      fertility_boost_pct_x1000: HARV_FERTILITY_BOOST (×1000 prec mult on Fert rate)

    Returns Musu (float; caller can floor for chain-equivalent).

    Worked example (P=10, V=10, neutral, 1h, no bonuses):
      Fert    = 10 * 1500 * 1000 / 3600 = 4166.67    (1e6-prec MUSU/sec)
      Int@60m = 1e6 * (50 + 60) * 10 / (480*3600) = 636.57
      Bounty  = (4166.67 + 636.57) * 3600 * 1000 / 1e9 ≈ 17.29 Musu  ✓
    """
    if elapsed_sec <= 0:
        return 0.0

    P = power
    V = violence
    T = float(elapsed_sec)
    M = T / 60.0  # minutes elapsed since intensity reset (linear, not floored)

    # Fertility — steady rate, fertility-boost is a percentage on this rate
    fert_rate = P * 1500.0 * efficacy / 3600.0  # 1e6-prec MUSU/sec
    fert_rate *= 1.0 + fertility_boost_pct_x1000 / 1000.0

    # Intensity — END-OF-PERIOD rate (snapshot at t=T)
    # Base config boost is 10; HARV_INTENSITY_BOOST adds to that additively.
    ib_total = 10.0 + float(intensity_boost_pct)
    int_rate_end = 1e6 * (V * 5.0 + M) * ib_total / (480.0 * 3600.0)

    bnt_boost = 1000.0 + float(bounty_boost)  # 1000 base + additive bonus
    pool = (fert_rate + int_rate_end) * T * bnt_boost / 1e9
    return pool


def strain_from_bounty(
    bounty: float,
    *,
    harmony: int,
    strain_boost: int = 0,
    strain_ratio: int = 0,
) -> float:
    """Strain (HP loss) from total bounty earned.

    Per systems/harvesting.md § "Strain":
      strain = ceil(bounty * 6500 * (1000 + strain_boost) / (1e6 * (Harmony + 20)))

    strain_boost is ×1000 prec (negative reduces strain).
    strain_ratio is the (rare) multiplier on the resulting strain — observed
    in slim's bonuses.harvest.strain.ratio. We treat both: ratio multiplies
    after.
    """
    if bounty <= 0:
        return 0.0
    s = bounty * 6500.0 * (1000.0 + strain_boost) / (1e6 * (harmony + 20.0))
    s *= 1.0 + strain_ratio / 1000.0
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
    """HP recovered while RESTING.

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
    intensity_boost_pct: int = 0,    # additive on the base 10 intensity boost
    bounty_pool_now: float | None = None,  # live harvest.bounty.balance from chain
    # Resting-only:
    rest_metabolism_boost: int = 0,  # ×1000 prec
) -> HPProjection:
    """Forward-simulate a kami's HP from last_action_ts to now_ts.

    For HARVESTING: requires harvest_start_ts (or last_action_ts as fallback).
    Returns projected current HP using the canonical strain formula.

    Confidence:
      0.95 — live `bounty_pool_now` passed in
      0.90 — formula-mode projection (post Bug 1+2 fixes; cert at ≥99.5%)
      0.5  — best-effort passthrough for unknown state
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
        confidence = 0.95 if (rest_metabolism_boost == 0 and harmony > 0) else 1.0
        return HPProjection(
            projected_hp=proj, sync_hp=sync_hp, max_hp=mhp, state="RESTING",
            elapsed_sec=elapsed, formula_branch="resting_metabolism",
            confidence=confidence, notes=notes,
        )

    if state_u == "HARVESTING":
        # Strain only applies to the CURRENT uncollected bounty pool. Each
        # harvest_collect drains the pool and applies strain at that moment,
        # updating sync_hp on chain. Between actions, the pool grows; HP loss
        # is realized only at the next sync.
        #
        #   projected_hp = sync_hp − strain(current_pool)
        #
        # current_pool comes either from live chain read (bounty_pool_now) or
        # from the corrected end-rate × Duration formula.
        start_ts = harvest_start_ts if harvest_start_ts is not None else last_action_ts
        harvest_elapsed = max(0.0, float(now_ts) - float(start_ts))
        if node_affinities is None:
            node_affinities = ["NORMAL"]
            notes.append("node_affinities defaulted to NORMAL")

        eff = harvest_efficacy(body_affinity, hand_affinity, node_affinities)

        if bounty_pool_now is not None:
            pool = float(bounty_pool_now)
            confidence = 0.95
            notes.append(f"bounty_pool_now={pool:.1f} (live)")
        else:
            # Formula mode: end-of-period × Duration (snapshot semantics).
            # See systems/harvesting.md "Yield & Timing" worked example.
            pool = projected_bounty(
                power=power, violence=violence, elapsed_sec=harvest_elapsed,
                efficacy=eff, bounty_boost=bounty_boost,
                fertility_boost_pct_x1000=fertility_boost,
                intensity_boost_pct=intensity_boost_pct,
            )
            confidence = 0.90
            notes.append(f"bounty projected end-rate × duration, elapsed={harvest_elapsed:.0f}s")

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
    attacker_hand: str = "NORMAL",
    victim_body: str = "NORMAL",
    animosity_ratio: float = 0.4,    # KAMI_LIQ_ANIMOSITY[2] (cached on-chain config)
) -> dict:
    """Canonical kill-threshold predicate. Strike fires iff projected_HP < kill_zone.

    Per systems/liquidation.md, calibrated 6/6 against the team's official
    liquidation calculator (founder cross-check 2026-05-02). See plan in
    memory/plan.md (session 89) for the calibration table.

      combat_ratio = ln(V_atk / max(1, H_def))
      animosity    = Φ(combat_ratio) × KAMI_LIQ_ANIMOSITY[2]   (= 0.4)

      affinity_shift (attacker hand vs victim body):
        NORMAL on either side       → +0.2  (special)
        same affinity (non-NORMAL)  → 0
        hand strong vs body         → +0.5
        hand weak vs body           → −0.5

      # Ratio bonuses (atk_ratio, def_ratio) only apply when matchup
      # is not weak. In a weak matchup, efficacy stays at base + shift.
      if affinity_shift >= 0:
          efficacy = 1.0 + affinity_shift + atk_ratio − def_ratio
      else:
          efficacy = 1.0 + affinity_shift   # weak matchup, ratios don't rescue

      threshold_ratio = animosity × efficacy + atk_shift − def_shift
      kill_zone       = floor(threshold_ratio × victim_max_hp)

    Calibration table (death-below HP from team's calculator):
      INSECT→SCRAP weak,  V=38, H=15, mhp=150, atk_r=0.25, atk_s=0.20  → 54  ✓
      EERIE→SCRAP strong, V=36, H=20, mhp=200                           → 86  ✓
      SCRAP→EERIE weak,   V=36, H=20, mhp=200                           → 28  ✓
      NORMAL→NORMAL,      V=36, H=20, mhp=200, atk_r=0.20               → 80  ✓
      NORMAL→NORMAL,      V=36, H=20, mhp=200, def_r=0.20               → 57  ✓
      EERIE→SCRAP strong, V=36, H=20, mhp=200, atk_r=0.20               → 98  ✓
    """
    if victim_harmony <= 0:
        victim_harmony = 1
    combat_ratio = math.log(max(1, attacker_violence) / victim_harmony)
    animosity = _gaussian_cdf(combat_ratio) * animosity_ratio

    aff_shift = _liq_affinity_shift(attacker_hand, victim_body) / 1000.0

    atk_s = atk_threshold_shift / 1000.0
    def_s = def_threshold_shift / 1000.0
    atk_r = atk_threshold_ratio / 1000.0
    def_r = def_threshold_ratio / 1000.0

    if aff_shift >= 0:
        efficacy = 1.0 + aff_shift + atk_r - def_r
    else:
        efficacy = 1.0 + aff_shift  # weak matchup gates ratio bonuses

    threshold_ratio = animosity * efficacy + atk_s - def_s
    kill_zone = math.floor(threshold_ratio * victim_max_hp)

    return {
        "animosity": animosity,
        "affinity_shift": aff_shift,
        "atk_shift": atk_s,
        "def_shift": def_s,
        "atk_ratio": atk_r,
        "def_ratio": def_r,
        "efficacy": efficacy,
        "threshold_ratio": threshold_ratio,
        "kill_zone": kill_zone,
        "victim_max_hp": victim_max_hp,
    }
