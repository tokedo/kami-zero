# kami-zero session 83 prompt — STOP STRIKING. Build & validate the HP-projection utility (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. Push to `~/kami-zero/memory/plan.md`, commit, fire.

---

## ⚠️ Foundational pivot — the missing piece

Founder reviewed sessions 76–82 (8 sessions, 70M+ gas, 0 kills) and identified the root cause:

> "The current HP is never stored on-chain. What is stored is the last transaction and time when it happens. From there kami-zero has to calculate what is Kami current HP. […] Until kami-zero can fully explain it — can explain why each liquidation happens — there is no point of keep trying to liquidate."

**You have been guessing at strain rates.** Session 80's "≤ 0.072 HP/min on H≥25 skill-boosted" was a *cap*, not a *formula*. The actual formulas are deterministic, fully documented, and live in your own working directory. With a real formula, projected HP carries no multi-HP error and you stop missing kills by single-digit margins.

**Operating rule going forward (and for every future session):** HP is **computed** from last action + time delta + base/skill stats using the canonical formulas. Until you can back-fit historical liquidations with your projection function (≥90% of past kills explainable), **no strike attempts**. Kill drought is not the failure mode — guessing-at-HP is. The discipline of session 81/82 (walking away) was correct; this session converts that discipline into a calibrated weapon.

---

## Hard rule for this session and forward

**No `liquidate` tx until back-fit validation produces ≥90% accuracy on historical kills AND a fresh candidate clears the validated kill threshold by margin ≥ 5 HP.** All other gas spending stays at your discretion (reads, harness builds, marketplace if needed).

This isn't a temporary stop — it's the new default. From this session forward, any strike must be preceded by: validated projection function + verified candidate. If a future session sees the projection drift (e.g., new skill mechanic discovered), validation must be re-run.

---

## Priority 0 — Read the canonical strain & HP formulas (no skim)

End-to-end:

1. **`~/kami-zero/systems/harvesting.md`** — strain mechanics. Look for: strain rate formula (likely a function of Power, Harmony, affinity-on-node, harvest tier, skills like 222 / 232 / 312 / 322 / metabolism), how strain converts to HP loss per unit time, any non-linear thresholds.
2. **`~/kami-zero/systems/health.md`** — max HP formula, RESTING regen rate, item heal effects, DEAD state.
3. **`~/kami-zero/systems/state-reading.md`** — the canonical "project HP from last action" pattern. This file likely already describes the exact algorithm you need.
4. **`~/kami-zero/systems/leveling.md`** — refresh on which Predator/Guardian/Metabolism skills affect strain, regen, max HP.
5. **`~/kami-zero/catalogs/items.csv`** — heal/revive items and their effect strings.

If any formula references a config constant (`KAMI_HARVEST_*`, `KAMI_REGEN_*`, etc.), read those constants on-chain via `component.value` once, cache them, and never read again. Document the cached values in `predator/mechanics.md` § "Cached config constants".

---

## Priority 1 — Build `compute_current_hp(...)` utility

Sketch (you decide implementation details — Python in `executor/`):

```python
def compute_current_hp(
    kami_full_state: dict,    # base HP, stats, skills, traits, current sync HP
    last_action: dict,        # {state: HARVESTING|RESTING|DEAD, ts: int, node_id?, harvest_id?}
    now_ts: int = None,
) -> dict:
    """
    Forward-simulate the kami's HP from last_action.ts to now_ts.
    Returns: {projected_hp: float, time_delta_s: int, formula_branch: str,
              confidence: float, notes: list}
    """
    ...
```

Branches to handle:
- `HARVESTING` → strain decay using harvest formulas (node's affinity tier, kami's stats/skills, accumulated harvest output).
- `RESTING` → regen using metabolism / harmony / state-reading.md formulas.
- `DEAD` → HP = 0, no progression.
- Other states (HEALING / item-effect midstream) — handle if encountered, else flag as out-of-model in `notes`.

Implement once, test against your own kamis first (you know their state and HP exactly via `get_kami_state`). If `compute_current_hp(11224, last_action, now)` matches the live read within ±1 HP, you're calibrated for self-state. That's the smoke test.

Build `find_kill_candidates_v3(our_kami_id)` on top — same as v2 but using the new HP function. Don't merge until validation passes.

---

## Priority 2 — Validate via historical back-fitting

This is the rigor step. Pull oracle's `harvest_liquidate` events from a recent window (start with 7d, expand if data is sparse — there were 1,676 in 28d per session 73). For each:

1. Identify the **victim**: resolve `harvest_id` → `kami_id` (use the harvest→kami traversal you've already documented).
2. Find the victim's **last action before liquidation** (almost always a `harvest_start`).
3. Pull the victim's full state at that time (stats, skills, traits — `kami_static` indexed snapshot, plus on-chain reads if needed for skills not in `kami_static`).
4. Compute **time delta** from victim's `harvest_start` to the `liquidate` event timestamp.
5. Apply `compute_current_hp(...)` to project the victim's HP at the kill moment.
6. Compute the **kill threshold** for that liquidation given attacker's stats, hand affinity, victim's body affinity, and the formula in `systems/liquidation.md`.
7. **Verify**: projected_HP < threshold. If yes, your formula correctly explains this kill. If no, your formula is missing something.

Aggregate:
- Total kills sampled: N
- Kills correctly explained (projected_HP < threshold): M
- Accuracy: M / N

**Target: ≥90%.** Below that, the formula has gaps. Iterate:
- Misses where projected_HP > threshold (should have been below): you're underestimating strain. Look for missed skill bonuses, missed config constants, missed strain multipliers.
- Misses where projected_HP < 0 (impossibly low): you're overestimating strain. Cap or revisit linearity.
- Categorize miss-modes in `predator/mechanics.md` § "Back-fit miss-modes" to track formula evolution.

If after one full session of work back-fit is still <90%, that's a finding worth its own session — schedule a second validation session (no strikes) and continue. Don't claim accuracy you don't have.

---

## Priority 3 — Document the validated formula

In `predator/mechanics.md` § "Validated HP projection (backed by N=… historical liquidations, M=…/N correctly explained)":
- The formula (link to `systems/*.md` for derivation).
- Cached config constants and their values.
- Edge cases that fail back-fit and why (e.g., REVIVE midstream, item heal, oracle-action-row gap).
- The N and M numbers as the calibration certificate. Update on every re-validation.

This is the document that future-you reads to trust the projection — not a fresh empirical estimate.

---

## Priority 4 — IF and ONLY IF back-fit ≥90%: identify a real candidate

Run `find_kill_candidates_v3` against current oracle state, filter (guild, owner-blacklist `rtvvvvv`, healthy-counter-predator), pick the candidate with the highest validated margin (projected_HP below threshold by ≥ 5 HP), pre-flight (live state re-check, cooldown clear), fire **one strike**.

If kill lands: log everything (predicted vs actual margin, gas, recoil, obol). If revert: this is a critical signal — your formula said killable, the chain disagreed. Re-investigate that target's state in detail and return to validation.

If back-fit < 90%: do NOT strike. Schedule re-wake to continue validation.

---

## Priority 5 — Self-schedule

- Back-fit ≥90% achieved this session and a kill landed: re-wake 15–30 min, chain on the cluster.
- Back-fit ≥90% but no candidate live: re-wake 30–60 min, re-scan.
- Back-fit < 90% (still validating): re-wake 30–60 min, continue.

Compute is not the constraint. Quality of validation is.

---

## Stop conditions

- Back-fit accuracy ≥90% achieved AND first valid kill lands → end session, log, schedule short re-wake.
- Back-fit < 90% after a full session of work → end session, schedule re-wake, continue next session.
- Total gas > 30M without a kill → end session, post-mortem (this is mostly read + tool-build gas, so 30M is generous; if you're burning more than that, something's off).
- ≥3 consecutive on-chain reverts despite back-fit passing → critical signal, stop, post-mortem in `predator/mechanics.md`.

---

## Out of scope this session

- Cluster moves (still gated by validated projection).
- 11224 SP allocation (still gated by first kill).
- Force-flush.
- New travel anywhere unless cluster math justifies it AND projected HP function says targets there are killable.

---

## CLAUDE.md addition

Append to the Predator Doctrine in CLAUDE.md:

> **HP is computed, not read.** Kami current HP is never on-chain — it must be projected from last action + time delta + base/skill stats using formulas in `systems/harvesting.md`, `systems/health.md`, `systems/state-reading.md`. Before any strike, the projection function MUST have been back-fit-validated against historical liquidations from oracle (≥90% of past kills correctly explained). The validation certificate (N, M, accuracy %) lives in `predator/mechanics.md` § "Validated HP projection". No strike without a valid certificate. If skill mechanics or game balance change, re-validate.

---

## Communication back to founder

End-of-session in `decisions.md`:
- `compute_current_hp` shipped? Y/N (path, line count).
- Self-state smoke test passed? Y/N (predicted vs actual for 11224 / 12649 / etc.).
- Back-fit: N kills sampled, M correctly explained, accuracy %.
- Top miss-modes (if any).
- First-kill strike fired? If yes: target, predicted margin, actual outcome.
- `next-run-at` and rationale.

Founder watches the trend in `predator/metrics.md` async. The KPI for the next few sessions is **back-fit accuracy**, not kills. Once accuracy ≥90%, kills follow.
