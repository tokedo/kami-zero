# kami-zero session 88 prompt — fix two specific formula bugs in hp_projection.py (founder cross-check)

This is a complete replacement for `memory/plan.md` on the VM. Push to `~/kami-zero/memory/plan.md`, commit, fire.

---

## ⚠️ Founder cross-checked the formula against in-game client truth — found two bugs

While session 87 was running, founder + assistant ran a 5-kami cross-check using in-game client snapshots from Geometric Cliffs (node 82). The session 87 work was good (oracle-only data plane, ×1.4 calibration approximates 16479's right answer), but **the calibration multiplier is a fudge factor masking two structural bugs in `executor/hp_projection.py`**. With both fixed, the formula matches client within 0–1 HP across all 5 kamis, mean error 0.11%. **Remove the calibration multiplier this session — replace with the rigorous fixes.**

The cross-check evidence (all on node 82, body=SCRAP, eff varies):

| kami | hand | eff (correct) | client pool | client HP | elapsed |
|------|------|---------------|-------------|-----------|---------|
| 16479 | EERIE | 1550 | 1674 | 29/220 | 18.81h |
| 12386 | INSECT | 1550 | 1289 | 89/260 | 15.16h |
| 12293 | NORMAL | 1650 | 881 | 166/280 | 12.41h |
| 12728 | EERIE | 1550 (+ib_total=45) | 482 | 184/240 | 5.66h |
| 15042 | NORMAL | 1650 | 1424 | 55/240 | 15.94h |

## Bug 1 — `harvest_efficacy()` uses LIQUIDATION's affinity rule (rock-paper-scissors triangle)

`executor/hp_projection.py::harvest_efficacy()` currently uses `_AFFINITY_BEATS` / `_is_strong` / `_is_weak` based on the rock-paper-scissors triangle (`EERIE > SCRAP > INSECT > EERIE`). That's the rule for **liquidation kill_threshold efficacy** (per `systems/liquidation.md`).

For **harvesting**, per `systems/harvesting.md` and `kamigotchi-gdd/mechanics/economy/harvesting.md`, the rule is much simpler:

| Trait | Node | Effect |
|---|---|---|
| Same affinity | — | **Strong** (+650 body / +350 hand) |
| Different non-NORMAL | Different non-NORMAL | **Weak** (−250 body / −100 hand) |
| NORMAL on either side | — | Neutral (0) |

There is no "strong against by triangle" in harvesting. Same = strong; different non-NORMAL = weak; NORMAL = neutral.

**Effect of bug**: kami 16479 has hand=EERIE, node=SCRAP. Triangle says EERIE > SCRAP → +350. Harvest rule says EERIE ≠ SCRAP both non-NORMAL → −100. The bug *over*-credits efficacy by +450 (1550 → 2000), causing ~30% pool over-projection.

**Fix**: rewrite `harvest_efficacy()` to drop the triangle. Body/hand component:

```python
def _component(trait_aff, node_aff, strong_bonus, weak_penalty):
    if trait_aff == "NORMAL" or node_aff == "NORMAL":
        return 0
    if trait_aff == node_aff:
        return strong_bonus       # +650 body / +350 hand
    return weak_penalty           # -250 body / -100 hand

def harvest_efficacy(body_aff, hand_aff, node_affs):
    if not node_affs:
        return 1000
    body_aff = (body_aff or "").upper()
    hand_aff = (hand_aff or "").upper()
    nodes = [(a or "").upper() for a in node_affs]
    if len(nodes) == 1:
        nodes = [nodes[0], nodes[0]]
    best = 1000
    for body_node in nodes:
        for hand_node in nodes:
            cand = 1000 + _component(body_aff, body_node, 650, -250) \
                       + _component(hand_aff, hand_node, 350, -100)
            if cand > best:
                best = cand
    return best
```

Drop the now-unused `_AFFINITY_BEATS`, `_is_strong`, `_is_weak` functions.

## Bug 2 — `projected_bounty()` uses time-integrated Intensity; contract uses END-RATE × Duration

`projected_bounty()` integrates Intensity over `[0, T]` (uses `(V*5 + T/120)` for the time-average). The contract uses **end-of-period rate × Duration** (snapshot semantics).

Verify against `systems/harvesting.md` worked example (P=10, V=10, neutral, 1h, 60min):
- Doc takes Intensity at **minute 60** (end-of-period): `1e6 × (10×5 + 60) × 10 / (480 × 3600) = 636` (intermediate)
- Bounty = (4167 + 636) × 3600 × 1000 / 1e9 ≈ 17 Musu ✓

Time-integration gives ~16.7 — close for short 1h windows, but diverges sharply for long windows because Intensity grows linearly with `minutesElapsed`. For 16479's 18.8h: time-integrated underestimates pool by ~33%.

**Fix** in the HARVESTING branch of `compute_current_hp` (and the projection-mode pool fallback):

```python
# End-of-period intensity rate × duration (snapshot semantics)
M = harvest_elapsed / 60.0
Fert_intermediate = power * 1500 * efficacy / 3600.0
ib_total = 10 + intensity_boost_pct  # config_boost(10) + bonus
Int_end_intermediate = 1e6 * (violence * 5 + M) * ib_total / (480.0 * 3600.0)
bnt_boost = 1000 + bounty_boost  # (×1000 prec; bonus_x1k additive)
pool = (Fert_intermediate + Int_end_intermediate) * harvest_elapsed * bnt_boost / 1e9
```

Apply the same correction to `projected_bounty()` if it's used elsewhere; otherwise inline in `compute_current_hp`.

## Hard rules for this session

- **No `liquidate` tx until** the two fixes are shipped, the back-fit re-validated, and at least one fresh live cross-check against an in-game-client-observable target matches within ≤2 HP.
- **Remove the ×1.4 (or whatever) calibration multiplier shipped in session 87.** Calibration multipliers paper over structural errors; the two fixes are the structural correction.
- All standing doctrine still applies (oracle-only data plane, guild gate, no force-flush in hunt mode, predator co-location, heal-event guard, etc.).

---

## Priority 0 — Re-read the relevant docs (fresh eyes)

End-to-end, with the bug findings in mind:

1. **`systems/harvesting.md`** — Affinity & Efficacy section. Note the "Same as node = Strong, Different non-NORMAL = Weak" rule (no triangle). Bounty formula worked example uses end-of-period Intensity.
2. **`systems/liquidation.md`** — Threshold Efficacy section. THIS uses the triangle (attacker hand vs victim body); confirm you keep the triangle in `kill_threshold()`, but NOT in `harvest_efficacy()`.
3. **`kamigotchi-gdd/mechanics/economy/harvesting.md`** — `LibAffinity.sol:82–90` source ref, table at line 195 confirms `Same/Different non-NORMAL/NORMAL` rule.

After reading, reconfirm in your own words why the two bugs are real before writing the fix.

---

## Priority 1 — Ship the two fixes

In `executor/hp_projection.py`:

1. Rewrite `harvest_efficacy()` per Bug 1 fix above. Add a code comment pointing to `systems/harvesting.md` § "Affinity & Efficacy" and explicitly noting *"NOT the liquidation triangle — that lives in kill_threshold()."*
2. In `compute_current_hp()` HARVESTING branch (and any helper that projects pool from elapsed time), replace time-integrated Intensity with end-of-period × Duration per Bug 2 fix above. Add a code comment with the systems/harvesting.md worked-example reference.
3. Drop `_AFFINITY_BEATS`, `_is_strong`, `_is_weak` from this module if they're no longer referenced. They belong in `kill_threshold()` if anywhere.
4. Search for any session-87 calibration multiplier (e.g., `×1.4`, `* 1.5`, `STRAIN_MULT`, `POOL_CALIBRATION`) introduced as a fudge. Remove. The fixes make the multiplier unnecessary.

Commit `harness:` prefix with a clear message.

---

## Priority 2 — Re-validate the back-fit cert

Run `executor/scripts/backfit_liquidations.py` (or the oracle-only equivalent shipped in session 87) on the corrected formula. Sample size N ≥ 200, ideally the same N=495 corpus session 87 used so you can compare apples-to-apples.

**Expected**: cert holds at ≥99.5%, possibly improves slightly. The bugs primarily affect *forward projection* on long-runner kamis; the empirical mode (collect-anchored, short windows) was already strong. Document the new cert (N, M, %) in `predator/mechanics.md`.

If accuracy *drops* below 99%, the fixes have a regression — investigate before continuing.

---

## Priority 3 — Cross-check on the 5 calibration kamis

For each of `[16479, 12386, 12293, 12728, 15042]`, run the corrected `compute_current_hp` and compare to the founder's client-truth table above. Expected: all 5 within 0–1 HP. Log the table to `predator/learnings.md` § "Session 88 cross-check".

If 16479 doesn't come out at 29 ± 1 HP, the fix is incomplete — re-investigate before targeting live.

---

## Priority 4 — Live-target cross-check

The 5 calibration kamis are guild-blocked (`caw-caw` and other founder accounts on the no-touch list — confirmed in session 87). Pick **one or two non-guild HARVESTING kamis from the broader oracle scan** and run the new projection. If you can observe their HP / pool through any reliable means (oracle's reconstructed values, on-chain reads), confirm match within ≤2 HP.

If oracle's reconstruction matches your formula prediction for non-calibration kamis, the fix generalizes.

---

## Priority 5 — Hunt with the corrected formula

Now run the full predator pipeline:

1. `oracle_kami_state` (the new primitive from session 87) for all currently HARVESTING non-guild kamis.
2. Apply corrected `compute_current_hp` to each.
3. Filter to: `projected_HP + 5 ≤ kill_zone(our_striker, target)` AND no `feed_kami` event since `harvest.time.last` AND counter-predator scan clear AND co-location feasible.
4. Pick the highest-margin candidate, fire one strike. Single attempt.

If the strike connects: log, scan immediately for next candidate on the same node, chain.

If revert: this is critical signal — the formula said killable and chain disagreed. Pull the target's full state and figure out what's still missing.

---

## Priority 6 — Self-schedule

- First kill landed → 15 min re-wake, chain.
- Migration done, no kill yet → 25–35 min re-wake.
- Cert validation incomplete → 30–60 min re-wake to continue.

---

## Stop conditions

- First kill + post-mortem of the corrected formula's accuracy at the kill point (predicted vs actual margin) → end session, log.
- 3 consecutive deep-reverts despite passing the corrected pre-flight → stop, log, post-mortem (the fix is incomplete).
- Total gas > 20M without a kill → end session, post-mortem.

---

## Out of scope

- Force-flush, quest progression, kamibots state reads (forbidden), 11224 SP allocation (still gated on first kill).
- Modifying kami-oracle code (route oracle gaps via `ideas_to_founder.md` per session 87).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Bug 1 fix shipped: Y/N (confirm `_AFFINITY_BEATS` removed from harvest path).
- Bug 2 fix shipped: Y/N (confirm end-rate × Duration replaces time-integration).
- Calibration multiplier removed: Y/N.
- Re-validated cert: N, M, %.
- 5-kami cross-check: pass/fail per kami (within 0–1 HP).
- First kill: Y/N. If Y, predicted margin vs actual outcome.
- `next-run-at` and rationale.
