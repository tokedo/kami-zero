# Strategic Experiments

> The home for empirical observations awaiting first-principles validation.
> Per CLAUDE.md "First principles before heuristics": one or two observations
> are NOT enough to crystallize a rule. Log them here as hypotheses, design
> a controlled test, gather ≥20 observations across diverse conditions, then
> graduate to mechanics doctrine OR reject.

## Status legend
- **HYPOTHESIS** — pattern observed, not yet designed test for
- **DESIGNED** — test conditions specified, awaiting opportunity to run
- **TESTING** — observations being gathered (track N here)
- **ADOPTED** — graduated to mechanics.md / doctrine
- **REJECTED** — first-principles model explained the pattern; heuristic unnecessary

---

## E001 — V<22 floor +95 (re-validate post-atk_s fix)
**Status**: TESTING
**Observation source**: session 118 revert at margin +30 on V13 victim. Promoted to V<22 floor +95 in session 120.
**First-principles re-derivation**: session 133 fixed STRIKERS atk_s drift (12649 oracle 300 vs live 400). With corrected formula, the session-118 revert is fully explained without needing a victim-V regime. The +95 floor may be cargo-cult.
**Test design**: strike V<22 sb=0 candidates at margins +30 to +94 using the corrected formula. Track outcomes. If revert rate ≤ 5% across N≥20, REJECT the +95 floor. If revert rate >> 5%, characterize what model term is missing (equipment effects? dual-affinity? something else).
**N**: 0 strikes since lobotomy.

## E002 — rtvvvvv re-test at low HP
**Status**: HYPOTHESIS
**Observation source**: 3 reverts s76/78/80 at high HP (>0.95 of kill threshold).
**First-principles question**: rtvvvvv farms are SCRAP-sustain builds with intensity_boost ≥ 20. Strain accumulates faster than the 0.075 HP/min default. Mechanics.md L569 already notes this. So at high HP they revert because strain hasn't bitten enough. **At low HP they should be killable like any other target.** Owner-blacklist was a symptom-side rule.
**Test design**: opportunistically strike rtvvvvv candidates at margin ≥+30 with `current_HP < 30%` of total. N≥10 to characterize.
**N**: 0.

## E003 — Cooldown computation accuracy
**Status**: DESIGNED
**Observation source**: lobotomy of 180s/95s fixed-interval rules.
**Test design**: for each pre-strike sequence, log (a) `time.cooldown` chain read at decision time, (b) computed cooldown from skills + items, (c) actual successful strike timing. Cross-check formula vs ground truth. If ≥95% agreement on N≥30, the formula is reliable; otherwise document the gap.
**N**: 0.

## E004 — Glue-raid play (CLAUDE.md worked example B)
**Status**: HYPOTHESIS
**Observation source**: founder doctrine + items-arsenal.md "Glue-then-walk-away" play.
**Test design**: craft 12+ Spirit Glues. Pick a defensive_cycle farmer with ≥10 active starvers (stefan97/foden/dias/Aenne/TrayzinCarpathia). Pre-throw 6 glues on highest-pool kamis BEFORE any harvest_start tx. Deploy full team. Strike the glued kamis during 180s lock. Log: kills, obols, spoils, ungliued-kamis-bulk-stopped (`interrupted_kamis`), MUSU disruption estimate, gas. Compare obols/Mgas vs clean-strike baseline (~0.110).
**N**: 0.
**Adoption criterion**: ≥3 successful runs across ≥2 different defensive farmers, with combined EV ≥ 0.15 obols/Mgas (50% premium over clean-strike baseline) AND positive MUSU disruption.

## E005 — Counter-counter strike on bodyguard
**Status**: HYPOTHESIS
**Observation source**: 2 missed counter-counter opportunities at Deeper Into Scrap (s107 — bodyguards 16841 + 14342 paid out 533+600 MUSU after killing our 11224+12649; would have been juicy counter-counter targets).
**Test design**: when scanning a contested node (any node where `harvest_liquidate` events show our account as victim in past 24h, or a bodyguard archetype is detected — full-HP non-harvesting kami camped on a node with starvers), deploy 2 strikers + 2 coverers. Bait with strike #1; if counter-fired, immediately fire cover striker on the bodyguard's reduced HP. Log: cover-strike success rate, total payout (kill + counter-counter MUSU).
**N**: 0.

---

## Lifecycle policy

- New observation → write HYPOTHESIS entry within the same session you observed it.
- Do NOT modify plan.md to apply the hypothesis as a rule until ADOPTED.
- Run TESTING through opportunistic strikes (don't divert from primary hunting just to gather data, unless in design-mode session).
- Each TESTING entry's N must reach ≥20 across diverse conditions before adoption.
- ADOPTED entries graduate to `predator/mechanics.md` with full derivation + test reference.
- REJECTED entries stay here as historical record + a note on what first-principles model explained the pattern.
