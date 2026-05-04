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

## E006 — Sustain-build (sb≤−25) blanket-deny re-evaluation
**Status**: DESIGNED (session 145 design-mode)

**Observation source**: 8 consecutive zero-strike sessions (137-144). World snapshot every cycle shows 20-30 V<22 sb≤−25 candidates at margins +60 to +160 (maia 80 cluster, Killchain 65 cluster, KCI 62 cluster, vuongdung1198 84 cluster, 𝄠𝄻𝄇 cluster). All denied by current rule: *"v_strain_boost ≤ −25 = sustain off-limits"*. We've never tested a strike against one. The rule's lineage is unclear — may be cargo-cult from V<22 floor +95 paranoia era.

**First-principles re-derivation**:

The strain formula (`hp_projection.py:215`):
```
strain = ceil(bounty * 6500 * (1000 + strain_boost) / (1e6 * (Harmony + 20)))
```
`strain_boost` is added to the constant 1000 in the multiplier, raw-units (not ×1000 prec). At sb = −125 (maia / 𝄠𝄻𝄇 / vuongdung1198 cluster), the multiplier is `(1000 − 125)/1000 = 0.875` — only **12.5% strain reduction**. At sb = −25 (current denial threshold), it's `975/1000 = 0.975` — **2.5% strain reduction**. The watcher's `proj_hp` already incorporates this multiplier when computing `strain` from elapsed bounty.

Concretely, for **maia kami 59** (V11/H23/sb=−125, NORMAL body, EERIE hand) sitting in `killable_v2[0]` of the 15:55 UTC snapshot at `proj_hp=16`, `kill_zone=135`, `margin=+119` after 14.56h elapsed: the projection has already reduced strain by 12.5% relative to a baseline V11/H23/sb=0 kami. With 14.56h of accumulated bounty against H=23 and the sustain reduction baked in, the kami's HP is *still* projected at 16. The kill formula does NOT use strain_boost (verified hp_projection.py:106-130 `_liq_affinity_shift`); kill_zone depends only on attacker V, victim H, attacker hand vs victim body, atk_shift, def_shift. **There is no first-principles basis for sb=-125 being unkillable**.

Possible defensive primitives sustain-builds *could* hide that the watcher misses:
1. **REVIVE mid-cycle**: 2/495 (0.4%) of session 87 back-fit corpus had revive-mid-cycle invalidating proj_hp. Detection: `harvest.start_ts` versus most recent REVIVE event for the kami in 6h action stream. Watcher does not currently expose this — adding it is a watcher upgrade, not a doctrinal blanket-deny.
2. **Out-of-band feed**: feed action lands inside oracle ingest lag (typically <60s). Mitigation: pre-strike spot-check oracle_kami_summary for last 300s.
3. **Owner with anti-predator automation**: orthogonal to strain_boost. Already filtered by `defensive_cycle` flag. Sustain-build owners with defensive_cycle=False (e.g. maia, Killchain) would not trigger it.

**Hypothesis**: sustain-build (sb ≤ −25) candidates with all of {V<22, margin ≥+50, defensive_cycle=False, fresh_feed_since_start=False, no-REVIVE-in-last-1h} are killable at the same rate as sb=0 candidates with equivalent margin. The blanket denial is leaving 20-30 high-margin clean targets per snapshot on the table.

**Test design**:
1. **Watcher upgrade prerequisite**: extend `owner_heat_check` (or scan_node) with a `recent_revive` check on each candidate — query oracle for any `kami_revive` action on `v_idx` in last 3600s. Surface as `recent_revive: bool` row field. ~30min implementation.
2. **Opportunistic single-strike test**: pick highest-margin sb=-125 V<22 candidate at ≥1-hop reach with all guards (defensive_cycle=False, fresh_feed=False, recent_revive=False). Strike with the watcher-assigned striker. Log outcome.
3. **N≥10 trials** across ≥3 different sb=-125 owners (maia, Killchain, 𝄠𝄻𝄇, vuongdung1198 V<22, KCI). If revert rate ≤ 5%, REJECT the blanket denial. If revert rate >> 5%, characterize the missing model term and document in mechanics.md as a refined denial criterion (e.g., "deny if sb≤−25 AND <X hour elapsed" or "deny if sb≤−25 AND H>30").
4. **Adoption criterion for revised rule**: ≥10 successful strikes (or ≥10 reverts justifying the denial) before changing plan-floor for sb=-25 candidates.

**Expected leverage (if hypothesis confirmed)**:
- Current snapshot has 30+ V<22 sb≤−25 candidates at margin ≥+50; ~15 at margin ≥+95 (V<22 floor) with non-defensive owners. At ~0.110 obol/Mgas baseline and ~7M gas/strike, that's ~30+ obols of currently-denied EV per cycle.
- Maia 80 cluster alone has 5 candidates (59 +119, 3117 +88, 7689 +67, 8559 +64, 9850 +57, 7160 +56) — would be a single-deploy multi-strike opportunity once stamina constraint resolved (E007).

**N**: 0.

## E007 — Stamina constraint revision (Rock Candyfloss audit)
**Status**: ADOPTED IMMEDIATELY (session 145 inventory recheck)

**Observation source**: 8 consecutive sessions cited "stamina-locked at ~30 SP, need 80 SP for cross-region round-trip" as the reason for not pursuing yeddy 53 / popo 26 / maia 80 clusters. That citation was wrong: inventory has been carrying **461 Rock Candyfloss (item 21205, SP+80 each)** the whole time. That's **36,880 SP available on demand** if we burn them.

**First-principles re-derivation**:
- Per `catalogs/items.csv:21205`: SP+80 per Rock Candyfloss, no cooldown noted. Item type FOOD; `use_account_item(21205, account="bpeon")` per CLAUDE.md "travel_to_room ... auto-uses SP+ items".
- 60 → 53 yeddy round-trip via portals: roughly 32 SP one-way, 64 SP round-trip baseline.
- Operator stamina cap is typically 80-100 SP; Rock Candyfloss can top us off pre-trip.
- One Rock Candyfloss covers roughly 1 round-trip from the buffer side; 461 of them is enough for hundreds of round trips. **Stamina is NOT the binding constraint on cross-region pivots — gas/EV is.**

**Adoption**: cross-region pivot decisions immediately revised to ignore stamina cost as a hard gate. The relevant constraint is:

```
gas_cost(travel_to_node + per-strike) + revert-risk-amortized-cost
  vs
expected_obols × 1 obol/strike + spoils_yield + MUSU_disruption
```

Per session 144 worked example (yeddy 53 with 3 V<22 sb=0 ≥+53):
- Travel 60 → 53: ~16 hops × ~250k gas/hop ≈ 4M gas one-way (8M round-trip).
- 3 strikes: 3 × ~7M = 21M gas.
- 1 Rock Candyfloss to refresh SP: 0 gas, 1 of 461.
- Total gas ~29M. Expected 3 obols × 0.110 obol/Mgas baseline = 0.319 obol/Mgas → above 0.110 baseline IF we land all 3 (revert rate would need to be ≤ ~33% to break even).

**EV trigger** (revised cross-region rule):
- ≥3 V<22 sb=0 candidates at same destination node, all margin ≥+50 with non-defensive owners, OR
- ≥4 V<22 sb≤-25 candidates at same destination node at margin ≥+95 with non-defensive owners (E006 dependency — pending validation),
- AND no closer cluster with comparable EV within 1-hop reach.

**Action items**:
1. Update plan.md / decisions.md / metrics.md mental model: cross-region travel is **no longer stamina-locked**. Re-evaluate every snapshot for E006 / cross-region E007 fire-now conditions.
2. Carry-out: future plan.md "Out of scope: cross-region (stamina)" lines should now say "Out of scope: cross-region (insufficient cluster EV)" — different gate.

**N**: doctrine adoption (single-observation correction of stale belief — no statistical adoption needed because it's an inventory fact, not a kill-rate hypothesis).

## E008 — Glue-raid prep throughput plan (E004 dependency)
**Status**: DESIGNED (session 145 design-mode)

**Inventory check (session 145)**:
- Item 19001 Spirit Glue: **0**
- Recipe 23 ingredients: Plastic Bottle (1003) **9013** / Microplastics (1103) **300,000** / Berry Chalk (1114) **1,000,000**.
- Tool: Portable Burner (23101) — have 2.
- Per-craft cost: 1 plastic + 200 microplastics + 200 berry chalk + 75 MUSU + 20 SP. Yield: 1 Spirit Glue.
- Bottleneck: Plastic at 9013 batches max → effectively unbounded for our scale. **Throughput limit is operator stamina + gas per craft tx, not ingredients.**
- Operator stamina: ~30 SP current + 36,880 SP from Rock Candyfloss (E007). Net: ~37,000 SP available.
- At 20 SP/craft, that's a theoretical max of **1,840 crafts** before SP+items run out. We will never need that many.

**Glue-raid target sizing** (CLAUDE.md worked example B):
- Carpet a defensive farmer's node with 6 glues. Consumes 6 SP*20 = 120 SP and ~6 craft tx + 6 throw tx + ~10 strike tx. Total gas ~50M.
- Realistic raid frequency: 1-2 raids/week against rotating defensive farmers (TrayzinCarpathia, foden, dias, stefan97, Aenne).

**Steady-state plan**:
1. **Session-145+1 craft batch**: craft 6 glues in a single session. Cost: 6 craft tx (~600k gas total assumption), 120 SP (burn 2 Rock Candyfloss). MUSU cost: 450. Net inventory: +6 glues.
2. **Subsequent craft maintenance**: craft 2 glues per session in any session that ends with a HOLD (no strikes). Maintain 6-12 glue inventory.
3. **First glue-raid candidate**: TrayzinCarpathia at node 60 — already co-located, no travel. Once heat-window clears (~17:43 UTC May 4) AND inventory ≥6 glues. Test the play in worked example B.

**Action item**: gate the next STRIKES-quiet session into glue-craft mode. Trigger: HOLD session at node 60 + glue inventory < 6 + Rock Candyfloss balance > 6.

---

## Lifecycle policy

- New observation → write HYPOTHESIS entry within the same session you observed it.
- Do NOT modify plan.md to apply the hypothesis as a rule until ADOPTED.
- Run TESTING through opportunistic strikes (don't divert from primary hunting just to gather data, unless in design-mode session).
- Each TESTING entry's N must reach ≥20 across diverse conditions before adoption.
- ADOPTED entries graduate to `predator/mechanics.md` with full derivation + test reference.
- REJECTED entries stay here as historical record + a note on what first-principles model explained the pattern.
