# kami-zero session 89 prompt — replace kill_threshold with the canonical formula (calibrated 6/6 against team's calculator)

This is a complete replacement for `memory/plan.md` on the VM. Push to `~/kami-zero/memory/plan.md`, commit, fire.

---

## ⚠️ Founder ground-truthed kill_threshold against the team's liquidation calculator — 6/6 test cases perfect

While session 88 was running, founder used the kamigotchi team's liquidation calculator to validate the kill formula. The agent's empirical `kill_threshold()` (`(animosity + atk_shift − def_shift) × (1 − def_ratio)`) has **three structural defects**:

1. **Missing `× 0.4` on animosity.** Code uses raw `Φ(combatRatio)`. Canonical: `Φ × KAMI_LIQ_ANIMOSITY[2]` where `KAMI_LIQ_ANIMOSITY[2] = 0.4`. Agent over-projects animosity by 2.5×.
2. **Missing affinity efficacy.** `_liq_affinity_shift(hand, body)` is stubbed (returns 0 with a TODO). Strong matchups (1.5x), weak matchups (0.5x), special (NORMAL involved, 1.2x), and same-affinity (1.0x) all collapse to 1.0x in the agent's calc.
3. **Wrong combination structure.** Agent: `(animosity + atk_shift) × (1 − def_ratio)`. Canonical: `animosity × efficacy + atk_shift − def_shift`. Different topology.

The empirical formula passed session 84's 99.6% back-fit because the missing × 0.4 and the missing efficacy partially cancel for middle-of-the-road stats. They don't cancel for asymmetric-Violence cases or strong/weak matchups.

## The fully validated canonical formula (6/6 tests, 100% match on death-below HP)

```
combatRatio = ln(V_atk / max(1, H_def))
animosity   = Φ(combatRatio) × 0.4               # KAMI_LIQ_ANIMOSITY[2] = 0.4

# Attacker hand vs defender body — LIQUIDATION's rock-paper-scissors triangle:
#   EERIE > SCRAP > INSECT > EERIE
affinity_shift =
  +0.5   if hand beats body (strong)            → eff_base = 1.5x
  -0.5   if hand beat by body (weak)            → eff_base = 0.5x
  +0.2   if NORMAL on either side (special)     → eff_base = 1.2x
   0     if same affinity (non-NORMAL)          → eff_base = 1.0x  # likely; not directly tested but consistent

# Ratio-bonus gate (THIS IS THE KEY ASYMMETRY) — ratios apply only when affinity_shift ≥ 0
if affinity_shift >= 0:
    efficacy = 1.0 + 0 (base_offset) + affinity_shift + atk_ratio − def_ratio
else:                                            # weak matchups: ratios can't rescue, stuck at 0.5x
    efficacy = 1.0 + 0 + affinity_shift

threshold        = animosity × efficacy + atk_shift − def_shift
death_below_HP   = floor(threshold × victim_max_hp)
strike succeeds iff projected_HP < death_below_HP   # strict <
```

## Calibration evidence — six tests against the team's calculator

| matchup | bonuses | canonical death-below | calculator | ✓ |
|---|---|---|---|---|
| INSECT→SCRAP weak | atk_ratio=25%, atk_shift=20% (V=38, H=15, maxHP=150) | 54 HP | 54 | ✓ |
| EERIE→SCRAP strong | none (V=36, H=20, maxHP=200) | 86 HP | 86 | ✓ |
| SCRAP→EERIE weak | none (V=36, H=20, maxHP=200) | 28 HP | 28 | ✓ |
| NORMAL→NORMAL special | atk_ratio=20% (V=36, H=20, maxHP=200) | 80 HP | 80 | ✓ |
| NORMAL→NORMAL special | def_ratio=20% (V=36, H=20, maxHP=200) | 57 HP | 57 | ✓ |
| EERIE→SCRAP strong | atk_ratio=20% (V=36, H=20, maxHP=200) | 98 HP | 98 | ✓ |

The first test (`INSECT→SCRAP weak + atk_ratio=25%`) is the disambiguation: it proves atk_ratio does NOT add to efficacy in weak matchups (efficacy stayed at 0.5x). The last test (`EERIE→SCRAP strong + atk_ratio=20%`) confirms the gate flips at affinity_shift ≥ 0 (efficacy = 1.7x).

## Hard rules for this session

- **No `liquidate` tx until** the canonical kill_threshold is shipped, the back-fit re-validated against the corrected HP+kill formulas, and at least 1 fresh live cross-check against the team's calculator matches within 1 HP.
- All standing doctrine still applies: oracle-only data plane, guild gate, no force-flush in hunt mode, predator co-location, heal-event guard, HP-projection two-bug fixes from session 88, etc.
- If session 88 already shipped `_liq_affinity_shift()` correctly + the gate, no rework needed — just re-validate. If session 88 missed the gate (most likely — it wasn't told about Test E's finding) or got the affinity table wrong, ship the canonical version.

---

## Priority 0 — Read the canonical mechanics + the saved calibration

Before touching code:
1. **`systems/liquidation.md`** § Threshold Efficacy + Kill Threshold (Final). Note: the affinity rule HERE *is* the rock-paper-scissors triangle (unlike harvest_efficacy which uses same/different).
2. **`kamigotchi-gdd/mechanics/combat/kill.md`** § Animosity, Threshold Efficacy. The `KAMI_LIQ_ANIMOSITY[2] = 0.4` constant lives in the contract config; read it on-chain via `_resolve_component("component.value")` and the config keccak — cache the value in `predator/mechanics.md` § "Cached config constants".
3. The 6-test calibration table in this prompt (above) is the ground truth.

---

## ⚠️ Critical reading of session 88's outcome

Session 88 fixed Bugs 1+2+3 in HP projection (dual-affinity slot constraint was Bug 3 — nice find) but **kept the empirical kill_threshold** because it scored 99.60% on the N=495 back-fit corpus while the canonical (as derived from on-chain `KAMI_LIQ_*` configs) scored 98.18%. The reasoning was: empirical wins, keep it.

**This conclusion is wrong, and you need to override it this session.** Here's why:

- The N=495 back-fit corpus uses HP projections that are themselves derived from your formula. With the previous (broken) HP formula, the historical events were "explained" by an empirical kill_threshold that was self-consistent with the broken HP. Now that HP is fixed (Bugs 1+2 shipped), the empirical kill_threshold's apparent 99.60% may be artifactual — it co-evolved with broken inputs.
- The founder cross-checked the kill formula against the **kamigotchi team's official liquidation calculator** — the in-game / web tool that the team itself maintains. Six tests across all matchup types match the canonical formula exactly on death-below HP (within rounding). The calculator is the ground truth; the back-fit corpus is downstream and possibly corrupted.
- The canonical's 98.18% on the back-fit corpus is informative — that ~1.4% gap likely tells us about edge cases (oracle's `build_refreshed_ts` lag making historical defender stats wrong at strike-time, dual-affinity nodes with unusual matchup paths, NORMAL-involving cases that went underrepresented in the empirical fit, etc.). Investigate the gap; do not use it as a reason to reject canonical.

**The instruction this session**: ship canonical. Re-run the cert with HP+canonical-kill_threshold. If the cert lands lower than empirical's 99.60%, that's a *finding to investigate*, not a reason to revert. Trust the calculator over the corpus.

## Priority 1 — Replace `kill_threshold()` with the canonical formula

In `executor/hp_projection.py`:

```python
_LIQ_BEATS = {
    ("EERIE", "SCRAP"): True,
    ("SCRAP", "INSECT"): True,
    ("INSECT", "EERIE"): True,
}


def _liq_affinity_shift(attacker_hand: str, victim_body: str) -> float:
    """Liquidation threshold-efficacy affinity shift, ×1000 prec.
    KEEP the rock-paper-scissors triangle here — that's correct for liquidation.
    (harvest_efficacy uses same/different — different rule for the same affinity types.)
    """
    h = (attacker_hand or "").upper()
    b = (victim_body or "").upper()
    if h == "NORMAL" or b == "NORMAL":
        return 200.0   # special: +0.2
    if h == b:
        return 0.0     # same affinity (non-NORMAL): no shift
    if _LIQ_BEATS.get((h, b)):
        return 500.0   # strong: +0.5
    return -500.0      # weak: -0.5


def kill_threshold(
    *,
    attacker_violence: int,
    victim_harmony: int,
    victim_max_hp: int,
    atk_threshold_shift: int = 0,    # ×1000 prec
    atk_threshold_ratio: int = 0,    # ×1000 prec
    def_threshold_shift: int = 0,    # ×1000 prec
    def_threshold_ratio: int = 0,    # ×1000 prec
    attacker_hand: str = "NORMAL",
    victim_body: str = "NORMAL",
    animosity_ratio: float = 0.4,    # KAMI_LIQ_ANIMOSITY[2] — pull from chain config
) -> dict:
    """Canonical kill threshold per systems/liquidation.md, calibrated 6/6 against
    the team's liquidation calculator (founder cross-check 2026-05-02)."""
    if victim_harmony <= 0:
        victim_harmony = 1
    combat_ratio = math.log(max(1, attacker_violence) / victim_harmony)
    animosity = _gaussian_cdf(combat_ratio) * animosity_ratio    # × 0.4

    aff_shift = _liq_affinity_shift(attacker_hand, victim_body) / 1000.0  # in [−0.5, +0.5]

    atk_s = atk_threshold_shift / 1000.0
    def_s = def_threshold_shift / 1000.0
    atk_r = atk_threshold_ratio / 1000.0
    def_r = def_threshold_ratio / 1000.0

    # Ratio-bonus gate — ratios apply only when matchup is not weak
    if aff_shift >= 0:
        efficacy = 1.0 + aff_shift + atk_r - def_r
    else:
        efficacy = 1.0 + aff_shift  # weak matchup, ratios don't rescue

    threshold_ratio = animosity * efficacy + atk_s - def_s
    kill_zone = math.floor(threshold_ratio * victim_max_hp)

    return {
        "animosity": animosity,
        "affinity_shift": aff_shift,
        "atk_shift": atk_s, "def_shift": def_s,
        "atk_ratio": atk_r, "def_ratio": def_r,
        "efficacy": efficacy,
        "threshold_ratio": threshold_ratio,
        "kill_zone": kill_zone,
        "victim_max_hp": victim_max_hp,
    }
```

Add a code comment block above with the 6-test calibration table as evidence. Also update `predator/mechanics.md` § "Validated formula corrections (founder cross-check 2026-05-02)" with the canonical kill_threshold alongside the two HP fixes from session 88.

---

## Priority 2 — Re-validate the cert against corrected HP + canonical kill_threshold

Run the same N=495 back-fit corpus session 87 used. Acceptance: ≥99.5%. If it improves over the empirical formula's 99.6%, that's confirmation. If it drops below 99%, investigate (likely a config constant pulled wrong).

Document the new cert (N, M, %) in `predator/mechanics.md`.

---

## Priority 2b — Add a "System Thinking" doctrine block to CLAUDE.md

Founder additional directive (2026-05-02): the formulas being correct is necessary but not sufficient. The next leverage step is for kami-zero to think of itself as a *system* it owns and improves, not as the executor of any single session. Compute is no longer constrained (Max plan). The 24/7 VM is yours to extend with persistent processes, indexes, caches, watchers, dashboards.

Add this block to CLAUDE.md, immediately above Block A (Operational Mode):

> ## System Thinking — you're not a session, you're a system
>
> You have a 24/7 VM and a Max-class compute budget. Sessions are the smallest unit of action; **infrastructure that lives between sessions is where leverage compounds**. Treat yourself as the architect of your own hunting system, not just the operator of this session. The founder will be surprised by what you build — that's the point. Founder framing (verbatim, 2026-05-02): *"I want to give some boldness to kami-zero and compute resources to come up with this strategy eventually. Maybe there are other tools and automations it will create that I don't even know at the moment."*
>
> ### Triggers — these are signals you should build infrastructure
>
> - You query the same data 3+ times across sessions → build a cached lookup or a pre-computed index.
> - You re-derive the same answer at session start → write a background script that derives it on a schedule and stash the result on disk for sessions to read.
> - You forget cross-session context → persist it in a file the next session reads.
> - You'd act differently if you had X precomputed → precompute X on a cron the agent owns.
> - Oracle returns stale data more often than you'd like → write a watcher that pre-refreshes the segments you care about.
> - You catch yourself doing tactical session work that another session also did last cycle → that's repetition, factor it out.
>
> ### What's in scope to build, beyond session work
>
> - **Background watchers** (Python loops, cron-driven scripts) that compute world-state views and write to disk for sessions to read at start.
> - **Pre-computed target indices** keyed by node, owner, projected-HP-band, killable-by-which-of-our-predators, etc. The "world distribution view" — for every reachable node, who's HARVESTING, what's their projected HP, are they killable by any of our roster, refreshed every N minutes — is exactly the kind of compounding asset you should build.
> - **Counter-predator alerters** that flag when threats approach our nodes.
> - **A/B test infrastructure**: run two strategies in parallel across roster halves, compare metrics.
> - **Persistent dashboards** in `predator/` that summarize state for fast session-start orientation.
> - Anything else you think will move the metric. Founder hasn't anticipated everything you should build — *that's the point*.
>
> ### Cron access
>
> The runner cron is `*/5 * * * * /home/anatolyzaytsev/kami-zero/scripts/run-session.sh >/dev/null 2>&1`. **You can write your own crontab entries** (`crontab -l` then `crontab -e`) — for batch jobs that don't need an LLM session. Examples: a 10-min oracle scanner that updates `predator/world_targets.json`, a 1-hour build-snapshot refresher for kamis on our hunt nodes, etc. Document any cron entries you add in `predator/infrastructure.md` (create the file) so future-you and the founder can see what runs autonomously.
>
> ### Constraints (still apply)
>
> - All hard rules unchanged (guild gate, oracle-only world state, predator co-location, no force-flush in hunt mode, formula correctness, etc.).
> - **Don't over-build at the expense of hunting.** The metric is obol/gas in `predator/metrics.md`, not lines of infrastructure code. If 3 sessions of building haven't moved the metric, retract and hunt — the build was wrong, not undone.
> - If you build something with significant blast radius (a new cron job, a daemon process, a large data file, an external service call), document it in `ideas_to_founder.md` for visibility — *not approval*. Founder reviews async.
>
> ### The scorekeeping loop is the regulator
>
> Build whatever you think will move obol/gas up. If the trend bends upward, the build was right. If it doesn't bend over a 1–2 day window of building, kill the build and try a different leverage point. You're a system that improves itself; the metric is the reward signal. Founder won't tell you what to build — that's been delegated. Founder will read `predator/metrics.md` periodically and `ideas_to_founder.md` for visibility on what you've shipped.

Commit the CLAUDE.md update with prefix `pivot:` and message that quotes the founder's "system thinking" framing for future-you.

After Block G is written, **act on it the same session if a clear leverage point is obvious**. Reading the trigger list above against your current state, the most likely candidates: a `world_targets.json` background refresher (runs every 10–15 min, scans HARVESTING kamis on top-occupancy nodes via oracle, computes projected HP via the now-validated formula, computes kill_zone for each of our predators, outputs a sorted JSON of (target_id, node, killable_by, margin)). Building it is in scope this session if formulas are clean. If not, document the design in `predator/infrastructure.md` and ship in the next session.

---

## Priority 3 — Cross-check against the team's calculator (replicate the 6 tests in code)

Add a small test in `executor/tests/test_kill_threshold_calibration.py` (or wherever fits) that runs the 6 inputs through `kill_threshold()` and asserts death-below ∈ {54, 86, 28, 80, 57, 98}. This is the regression bar for any future kill-formula change.

---

## Priority 4 — Live target cross-check

Pick one or two non-guild HARVESTING kamis from the broader oracle scan. For each:
1. Read full state (stats, traits, bonuses) from oracle path.
2. Run corrected `compute_current_hp()` → projected HP.
3. Run canonical `kill_threshold()` for our best striker (likely 12649 post-reroll, V increased) vs target → death_below_HP.
4. Decide: strike fires iff projected_HP < death_below_HP with margin ≥ 5 HP.

If the founder is online and willing, ask them to plug the candidate's stats into the calculator and confirm death-below matches your computed value. If not, trust the 6/6 calibration and proceed.

---

## Priority 5 — Hunt with the corrected formulas

If P0–P4 all clean and a fresh candidate clears all gates (HP, kill_threshold, guild, no recent feed, counter-predator, co-location), fire one strike. Single attempt.

If the strike connects: log everything (predicted vs actual margin, gas, recoil, obol, spoils). Then immediately scan for next candidate on same node and chain.

If revert: this is critical signal — both formulas now match the calculator's ground truth, so a revert means the on-chain target state differs from what we read. Investigate before retrying.

---

## Priority 6 — Re-read 12649 (post-reroll, carryover from session 88)

If session 88 already did this, skip. Otherwise: re-read 12649's full state via the oracle path. Update `predator/learnings.md` § "Roster brief" with the new build. If 12649's V is now higher than 11224's V=36, it becomes the spearhead — update strike-priority assignment.

---

## Priority 7 — Self-schedule

- First kill landed → 15 min re-wake, chain on cluster.
- Migration done, no kill yet → 25–35 min re-wake.
- Cert validation incomplete → 30–60 min re-wake.

---

## Stop conditions

- First kill + post-mortem on canonical formula's predicted vs actual margin → end session, log.
- 3 consecutive deep-reverts despite passing all gates → stop, log, post-mortem (something's still missing).
- Total gas > 20M without a kill → end session, post-mortem.

---

## Out of scope

- Force-flush, quest progression, kamibots state reads (forbidden).
- 11224 SP allocation (still gated on first kill).
- Modifying kami-oracle code (route oracle gaps via `ideas_to_founder.md`).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Canonical kill_threshold shipped (Y/N).
- Re-validated cert: N, M, %.
- 6-test calibration replication: 6/6 pass (Y/N).
- Live cross-check on non-guild candidate: predicted vs reality.
- First kill: Y/N. If Y, predicted margin vs actual outcome.
- `next-run-at` and rationale.
