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

## E009 — Vuongdung1198 V<22 sb≤-25 single-strike pilot (E001+E006 convergence)
**Status**: DESIGNED (session 162 strategic review)

**Observation source**: 9-session attempt-eligible 0-strike streak (s152–s161). Snapshot triage at s161 + s162 shows `vuongdung1198` cluster on node 33 surfacing with **6–9 V<22 sb≤−125/−75/−50 candidates per tick at margin +30 to +50, all with `defensive_cycle=False` AND `anti_predator_automation=False`** — i.e., they pass the watcher's heat-check, but are blocked at session-triage time by two compounding hardcoded floors (E001's V<22 floor +95 and E006's sb≤−25 blanket-deny). vuongdung's last `sync_feed` burst signature was session 115 — the heat-check looks at a 6h window and shows zero anti-predator automation across the recent observation period. **Both denials are session-mental, not doctrine-justified per current first principles.**

**First-principles re-derivation (combined E001+E006 case)**:

The strain formula `strain = ceil(pool × 6500 × (1000 + sb) / (1e6 × (H+20)))` already encodes `strain_boost`. At sb=−125, multiplier 0.875 → 12.5% strain reduction. The watcher's `proj_hp` already incorporates this. The **kill formula does not depend on strain_boost** (`hp_projection.py:106-130`). If watcher's `proj_hp` is correct AND target has not received `recent_revive` / `fresh_feed_since_start` (both already exposed as row fields, watcher upgrade complete), then `proj_hp - kill_zone = margin` is the realized live margin. There is no first-principles basis for either floor.

**The only defensible reasons either floor could be right**:
1. **HP projection model error for sustain-builds at long elapsed**: 99.6% accuracy on N=495 in `mechanics.md` § "Validated HP projection" includes sustain-build kamis. The 0.4% miss class is REVIVE mid-cycle — already guarded.
2. **vuongdung-specific automation that fires sub-cycle to the heat-check**: 5-second sync_feed bursts could fall outside the 6h aggregation window if vuongdung paused the bot for some hours. Mitigation: pre-strike spot-check oracle for any `kami_feed` action on the candidate `v_idx` in last 5 minutes.
3. **Live atk_s drift on our striker**: this was the s118 root cause (fixed s133, see mechanics.md § Round 3 lobotomy log). Pre-strike must read striker's live `atk_shift` not oracle-cached.

**Hypothesis**: vuongdung1198 V<22 sb≤−25 candidates that pass {watcher heat-check + `recent_revive=False` + `fresh_feed_since_start=False` + no oracle `kami_feed` event in last 5min on v_idx + striker live atk_shift verified} are killable at the same revert rate as V≥22 sb=0 candidates with equivalent margin — i.e., ≤5% reverts at margin ≥+30.

**Test design (pilot — one strike, then characterize)**:
1. **Pre-strike gates** (all must hold):
   - Candidate present in `killable_v3` (passed scanner + parked-rates filter)
   - `heat[v_acct].defensive_cycle == False AND anti_predator_automation == False`
   - Row: `fresh_feed_since_start == False AND recent_revive == False`
   - `parked_rates: {parked_bool: False}` (rates verified non-parked, not None)
   - `margin >= +30` (relaxed from +95 floor; per first principles the +5 baseline could fire, but +30 buffer absorbs noise per session 119 doctrine)
   - Live oracle spot-check on `v_idx` for any `kami_feed` action in last 5 min: zero
   - Live spot-check striker's `attack_threshold_shift` matches oracle-cached value (±0)
   - Striker co-located, harvesting, `time.cooldown` clear
2. **Single strike**, log outcome.
3. **N=1 → 5 outcomes**: each strike attempt updates this entry's N. Outcomes:
   - Kill: increment kill_count. After 3 kills, expand to non-vuongdung sb≤−25 candidates (Killchain, maia, 𝄠𝄻𝄇 clusters from E006).
   - Revert: drill `oracle_kami_summary(v_idx)` and `oracle_sql` for missed actions in last 30 min. Characterize the missing model term. After 1 revert: pause and re-derive before next attempt.

**Adoption criterion** (graduate to mechanics.md / drop the floors):
- ≥10 successful strikes across ≥2 different sb≤−25 owners with revert rate ≤5% → drop both E001 V<22 floor +95 and E006 blanket sb≤−25 deny in favor of: `margin ≥ +30` baseline for ALL targets passing the gates above.
- ≥3 reverts at margin ≥+30 with all gates passing → re-derive missing model term, do NOT drop floors yet, document characterization.

**Expected leverage (if hypothesis confirmed)**:
- s152–s162 snapshot: 8–10 vuongdung1198 candidates / tick currently denied. Across the 17-watched-nodes scope, +30 to +50 margin sb≤−25 V<22 supply runs ~15–20 rows / tick. Even at 50% revert rate, EV is positive vs current 0-strike baseline.
- Streak-breaking value: re-establishes a strike cadence and lets metrics.md reflect doctrine validation, not cargo-cult conservatism.

**N**: 0. **Defer count: 2** (s163, s164).

**Scheduling**: pilot fires next session (s163) where any candidate passes all gates. If snapshot is empty, +20-30 min re-wake and re-evaluate. Do **not** divert from this play to chase margin ≥+5 wins; pilot needs sb≤−25 V<22 specificity to validate the floors.

**Defer log**:
- **s163** (2026-05-05 01:40 UTC): 0/18 v3 rows ≥+30. Highest +20 (pepo idx=7287 V13H26 sb=0 node=16). Heat clean across all 18.
- **s164** (2026-05-05 01:55 UTC): 0/19 v3 rows ≥+30. Highest +25 (pepo idx=7287 V13H26 sb=0 node=16, same kami margin growing). Co-located node-60 candidates: only wiuuuu margin=+13. vuongdung1198 cluster (4 rows) max margin +18. World genuinely thin for high-margin sb≤−25 V<22 supply this two-session window.

**Amendment proposal A — floor relaxation (PROPOSED s164, NOT YET ADOPTED)**:

After 2 consecutive E009-defer sessions despite watcher heat-clean conditions across the v3 set, propose relaxing the pilot floor from +30 to **+20** for one trial. Justification: E009 design first-principles state +5 baseline could fire; +30 buffer was set "per session 119 doctrine" but s119 doctrine itself was empirical, not first-principles. +20 is still 4× the first-principles baseline and absorbs realistic projection noise. Single trial = bounded risk.

Adoption gate for amendment A: 1 strike under +20 floor → if KILL, treat as N=1 toward E009 main-line evidence. If REVERT, drill characterization, freeze the relaxation, and revert to +30 pending root-cause.

**Amendment proposal B — one-shot cross-region travel for first pilot (PROPOSED s164, NOT YET ADOPTED)**:

The E009 design gates "≥3 kills before 60→33 trip" was set to prevent travel-burn on speculative play. But E009 N=0 cannot grow past 0 if every candidate is non-co-located AND no-travel rule binds. Deadlock pattern: can't get 3 kills without travel; won't travel without 3 kills.

Propose: allow ONE cross-region travel for the first E009 pilot when (a) target node has ≥4 v3 candidates from the same cluster owner (E009 specificity) AND (b) ≥2 of those clear amended floor +20 AND (c) round-trip gas ≤25M (more conservative than the 35M threshold cited in plan-163 since pilot-stage we're paying for hypothesis validation, not extraction). Currently node 33 vuongdung1198 has 4 candidates, max +18 — **fails amendment A's +20 floor**. Node 65 SIUUUU has 4 candidates, max +16 — also fails. So amendment B alone doesn't unblock; A+B together would let pepo node-16 (+25, single candidate, fails specificity) — also fails B's ≥4 cluster gate.

**Combined effect of amendments A+B at current snapshot**: still 0 actionable pilots. Amendment B's "≥4 cluster" gate is binding. If we additionally relax to "≥2 cluster" candidates (looser), tamagotcho node-9 (2 rows, max +21) would qualify — but this stretches the amendment chain, which is already 3 layers of relaxation deep without a single data point.

**Decision (s164)**: Document amendments A and B for visibility. Do NOT trigger them this session. Re-evaluate at s165 after one more snapshot rotation. If s165 still defers under +30 floor, fire under amendment A (+20 floor, co-located only) — at that point 3 consecutive defers + 2 cycles of margin growth on persistent owners constitutes meaningful evidence the +30 floor is binding above realistic supply ceiling. **Do NOT trigger amendment B until amendment A has produced N≥1 kill** (no point on a first-cross-region trip with a still-untested floor).

**Margin trend across defer window**:
- s163 highest margin = +20 (pepo idx=7287)
- s164 highest margin = +25 (pepo idx=7287, same kami, margin grew +5 in 12 min via elapsed_h monotonic)
- This validates the "elapsed_h grows margin" hypothesis from plan-163. If pepo continues HARVESTING uninterrupted, by s165 (+15 min) margin should be ~+27-30 — and may cross the +30 floor without amendment.

---

## E010 — Session-mental skip-list collapse (trust the watcher's heat-check)

**Status**: HYPOTHESIS (session 162 strategic review)

**Observation source**: across s152–s161 doctrine triage, "skip-list" denials averaged 4–5 candidates per snapshot. The list (yeddy, TrayzinCarpathia, Gunnar, alexbuyer, acheron, tamagotcho, orange, zizi, fluff, maia) is **session-mental, not in watcher code** — applied at triage time, not surfaced by the watcher's `owner_heat` output. Audit: in s162 snapshot, the watcher's `heat` for `tamagotcho`, `wiuuuu`, `buja723`, `sa3woo`, `KAMI`, `pepo`, `IBCKING`, `SIUUUU`, `stefan96` (all v3 surfaced acts) shows **defensive_cycle=False AND anti_predator_automation=False**. The watcher's logic already accounts for bulk_stop_windows, sync_stop_bursts, sync_feed_bursts, and minutes-idle thresholds. If the watcher returns clean, why is session-time triage adding a separate skip layer?

**First-principles question**: the mental skip-list is a residue of historical reverts (e.g. yeddy revert s78, TrayzinCarpathia bodyguard pattern, tamagotcho once-observed defensive cycle). Some of these have aged out of the watcher's 6h heat window; some never had a coded basis. The watcher already emits `recent_revive`, `fresh_feed_since_start`, and `defensive_cycle` per-row — those are the actionable signals.

**Hypothesis**: dropping session-mental skip-list and trusting only the watcher's heat-check + row guards yields equal-or-better doctrine permissibility without elevated revert rate.

**Test design**:
1. **Same-tick comparison** (no strikes needed for first signal): for the s162 snapshot, list all v3 rows that pass {watcher heat clean + row guards clean + margin ≥+30 + parked_rates non-parked}, IGNORING session-mental skip-list. Cross-reference against historical liquidation feed (`world-liquidations.jsonl`, last 7d): are any of these owners' kamis being killed by other predators? If yes, that's external evidence the watcher's clean signal is correct.
2. **Strike test**: when E009 produces a successful kill, take the **next-tick highest-margin clean-watcher non-vuongdung candidate** (e.g. tamagotcho V15H26 sb=0, sa3woo V18H17 sb=0, KAMI V30H15 sb=0 if margin reaches +30) and pilot a single strike under E009 gates. N=1.
3. **Dataset growth**: as E009 accumulates kills/reverts on sb≤−25, opportunistically include skip-listed-but-watcher-clean candidates and tally outcomes.

**Adoption criterion**:
- Across N≥10 strikes on watcher-clean-but-mental-skip candidates: revert rate ≤5% → drop session-mental skip-list entirely; doctrine becomes "trust the watcher heat + row guards".
- Revert rate >5% → identify which owner-specific signal is missing from the watcher and either: (a) add it to `owner_heat_check` (e.g. extend window beyond 6h, or add a `historical_revert_count` field), or (b) keep the skip but document the empirical basis with N≥3 reverts as evidence.

**Expected leverage (if hypothesis confirmed)**:
- 4–5 additional doctrine-permissible candidates per snapshot. Combined with E009 (~8–10 vuongdung), that's ~12–15 doctrine-permissible candidates per tick from the current 0.
- More importantly: dispels the cargo-cult-list ratchet pattern that R3 lobotomy was supposed to prevent. If a defensive pattern returns, the watcher catches it; we don't need a parallel mental list.

**N**: 0 strikes. Step 1 (same-tick comparison) can be done in any session as a free read.

**Step-1 results (s163, 2026-05-05 01:40 UTC)** — `world-liquidations.jsonl` filter on mental-skip-list owners as victims, last 7d, non-self only:

- **acheron**: 3 kills by `Assassins` on Sacrarium (2026-05-03 16:01, ~795 MUSU avg).
- **Gunnar**: 2 kills by `PuppyPriestess` on Scrapyard Exit (2026-05-04 17:13, 209+132 MUSU).
- **alexbuyer**: 1 kill by `PuppyPriestess` on Scrapyard Exit (2026-05-04 17:12, 815 MUSU).

Total: 6 non-self kills against 3 mental-skip owners over the most recent 2 days of feed. Other 7 mental-skip owners (yeddy, TrayzinCarpathia, tamagotcho, orange, zizi, fluff, maia) had no liquidations in the 7d window — could mean they're well-defended OR simply not being targeted.

**Interpretation**: at least 3/10 mental-skip owners ARE being killed by competitor predators. The watcher's clean heat-check signal for them is corroborated by external strike outcomes. **Strong external evidence the mental skip-list is over-blocking** for at least these 3 owners. Step 2 (strike pilot under E009 gates) remains gated on E009 ≥1 kill. When triggered, prioritize acheron / Gunnar / alexbuyer as first watcher-clean-but-mental-skip strike candidates — they have direct external validation rather than just clean watcher heat.

---

## E009 Amendment C — "Snapshot famine" / cycling-defensive owners

**Status**: HYPOTHESIS (session 166, N=2 confirmation of s165's "high-margin v3 short lifespan")

**Observation source**:
- s164: pepo idx=7287 leader at +25 (margin grew +5 in 12 min via elapsed_h)
- s165: pepo gone from v2 AND v3 (no competitor kill at node 16) → likely owner-fed or kami-stopped
- s166 02:35 read: vuongdung1198 cluster on node 33 surfaced 4-7 candidates with margins ranging +20 to +53. Travel decision based on cluster math + ≥2 above amendment-A's +20 floor + amendment-B cluster gate met.
- s166 02:50 read (after travel completion, ~15 min elapsed): **entire vuongdung1198 cluster gone from v3**. Top v3 margin = +16 (SIUUUU). The +53 leader at 02:35 was NOT killed by competitor (no node 33 entries in world-liquidations.jsonl during the 15-min window).

**Pattern N=2 confirmation**: "high-margin v3 short lifespan" hypothesis from s165 is now validated. **For cycling-defensive owners, high-margin candidates evaporate within 15 minutes (1-3 cron ticks)** — faster than the operator can perceive (snapshot read), decide (cluster math), travel cross-region (~5-10 min), and fire. This is a fundamental architectural constraint, not a doctrine relaxation problem.

**Mechanism**:
- vuongdung1198 runs `defensive_cycle = True` per watcher (sync_stop on operator presence). Even without operator presence at node 33, the owner's automation cycles every 12-15 min on its own schedule (starve cycles, RESTING phases) regardless of predator behavior. By the time we observe a +30 margin and arrive, the cycle has already pulled the kami.
- Compound: vuongdung1198's cluster at node 33 includes 7+ kamis cycling on different phases. Watcher snapshot captures whichever subset is HARVESTING this tick; the next tick may surface different idxs entirely as cycle phase rotates.

**Implication for E009 doctrine**:
- Floor `≥+30` is **statistically unreachable** for cycling-defensive owners. Owners' cycle period < perception-to-fire latency.
- Amendment A (+20 floor co-located only) does not solve this — node 60 doesn't surface candidates at all this snapshot rotation cycle.
- Amendment B (+20 floor + ≥4 cluster + travel) was triggered s166 — and the cluster was gone by arrival. The travel itself burned the time window.

**Three response branches**:

1. **Garrison strategy** — pre-position strikers AT the cycling-defensive owner's node (e.g. all 7 strikers on node 33 vs vuongdung1198) and wait passively. When cycle phase exposes a starver above kill threshold, fire IMMEDIATELY (no perception lag, no travel). Cost: foregone harvest income at node 60. Benefit: latency drops from 15min to <30s. Worth it iff vuongdung1198 cluster's expected obol yield/hr at zero-latency exceeds node 60 harvest yield/hr by margin.

2. **Sub-minute reaction infrastructure** — drop watcher cron from 5 min to 30s (or build event-driven detection); add MCP tool to fire pre-staged strike on detection. Cost: dev work + watcher load + MCP latency budget. Benefit: enables remote-strike on any cluster with phase < 5 min.

3. **Retreat doctrine** — accept that cycling-defensive owners are unkillable under current architecture. Stop trying. Hunt only non-cycling owners (rare in current snapshot). Re-validate every 7 days as world composition shifts.

**Test design (N=3+ for adoption)**:
- For 3 separate cycling-defensive cluster opportunities (different owners or same owner across days), measure (a) snapshot-read time, (b) arrival time, (c) cluster v3 status at arrival. If ≥2/3 evaporate before strike → confirm pattern → adopt one of branches 1/2/3 based on EV math.
- Currently N=2 (pepo single-kami, vuongdung1198 cluster). Need N=3 minimum.

**Adoption decision**: deferred until N=3. If confirmed, branch 1 (garrison) is most cost-effective near-term — it requires no harness work, just doctrine update on default striker placement.

**Counter-evidence to watch for**: a session where a +30 candidate persists across 3+ cron ticks would falsify this hypothesis. If pepo (or any persistent harvester) shows up at +30 and stays there for 15+ min, snapshot famine is wrong and the +30 floor is reachable — just thin.

**Session 166 cost**: ~16.5M gas burned on travel + deploy + redeploy with 0 strikes. This is the experimental cost of confirming N=2.

---

## E009 Amendment D — "Floor empirically unreachable; diagnostic pilot at margin ≥+10 with strict row guards"

**Status**: HYPOTHESIS (session 168, defer #6 trigger after 7 consecutive scanner snapshots without a fireable v3 candidate above amendment-A's +20 floor)

**Observation source — max v3 margin across snapshots s162-s168**:

| Session | Top margin | Owner / idx | Persistence |
|---------|-----------|-------------|-------------|
| s162    | +20       | vuongdung idx=14649 | Transient (cycling) |
| s163    | +20       | pepo idx=7287       | Cycling (gone by s165) |
| s164    | +25       | pepo idx=7287       | Same kami, +5 in 12 min via elapsed_h |
| s165    | +13       | pepo gone           | Cluster evaporated |
| s166    | +53       | vuongdung cluster   | Evaporated mid-travel (Amendment B fire, 0 kills) |
| s167    | +18       | TrayzinCarpathia node 60 | Persistent |
| s168    | +16       | BandG idx=590 node 12    | Persistent (elapsed_h 9.53h, defensive_cycle=False) |

**Pattern**: +30 floor (E009 main) reached only via transient cycling-defensive bursts (s166 +53). Persistent non-cycling harvesters plateau around +13-+18 even at elapsed_h ≥ 6-9h. Amendment-A's +20 floor (single trial) has not fired across s165/s166/s167/s168 — also unreachable for the persistent class. The cycling class IS reachable (s166 saw +53) but evaporates before perception-to-fire latency closes.

**First-principles question**: why is +30 unreachable on persistent harvesters? Two non-exclusive hypotheses:
1. **Projection conservatism** — `executor/hp_projection.py` overestimates remaining HP for persistent harvesters (e.g. strain rate underestimate at low intensity, or `health.sync` interpretation lag). The validated certificate in mechanics.md claims ≥90% accuracy on 7d back-fit — that gives 5-15 HP noise band, not enough to explain a +30 vs +16 gap.
2. **World composition shift** — current bpeon striker stack (V31-V34, H12-H21) yields kill thresholds in the 130-160 range against a typical V13/H21-25 farmer with sb≤−100. Persistent farmers' projected HP at elapsed_h ≥6h sits in the 110-145 band, leaving margin +5 to +20 typically. To reach +30 would require either a softer farmer (V<13 or H>25) or our striker stack getting stronger (level-up SP, equipment, intensity-reducing skills on TARGET — out of our control).

If hypothesis 2 dominates, the +30 floor is structurally unreachable on persistent owners regardless of how long we wait, because elapsed_h growth is asymptotic (proj_hp converges to a strain-rate floor, not zero).

**Hypothesis (Amendment D)**: A diagnostic pilot at margin ≥+10 (well above Hard Rule 7's +5 contract floor, well below current +20/+30 doctrine) on a persistent clean-heat candidate validates whether (a) the projection is well-calibrated at that band, and (b) world composition has structurally moved kill margins down. If pilot lands kill, relax floor to +12 conservative step. If pilot reverts, capture the projection error mode and refine `hp_projection.py` rather than ratchet the floor up further.

**Pilot row guards (all must hold)**:
- `margin ≥ +10`
- `heat.defensive_cycle == False` AND `heat.anti_predator_automation == False`
- `fresh_feed_since_start == False`
- `recent_revive == False`
- `parked_rates.parked_bool != True` (or null)
- `elapsed_h ≥ 6.0` (selects persistent, non-cycling)
- Striker is co-located with target node (zero travel cost).

**Test design**:
1. **Single-strike pilot** under above guards. Executor `compute_current_hp` + `kill_threshold` re-derived live (pre-flight slim read on victim, not snapshot replay).
2. **Outcome adjudication**:
   - **Kill**: projection well-calibrated at margin +10. Adopt floor +12 for next iteration. Carry to N=3 before adopting +10 broadly.
   - **Revert (executor `reverted` status)**: capture diff between projected HP at fire-time and the on-chain HP that resulted in revert. Update `hp_projection.py` if a systemic bias is identified.
   - **Bodyguard counter-strike**: counter-predator math failure, not a margin failure. Excluded from D's adoption signal; routes to Worked Example A doctrine (glue/cover striker) instead.
3. **Adoption**: kill rate ≥ 66% on N≥3 pilots at margin +10-15 → relax doctrine floor permanently to +10. Kill rate < 33% → revert to +20 + write to mechanics.md as projection bias note. In-between (33-66%) → run N to 5 before deciding.

**Cost analysis**: A pilot revert costs ~1-2M gas + recoil HP on the striker. Compared against Amendment B's s166 cost (~16.5M phantom-cluster travel), a pilot strike is cheap experimental capital. The information value of resolving "is +30 floor structural or projection-conservative" is high — it directly informs whether E009 needs floor relaxation, projection refinement, or roster strengthening (level-up wave on H-stack to push kill thresholds up).

**Trigger conditions**:
- Defer #7 (s169) with v3 max margin still <+20: candidate exists at margin +10-15 with all row guards met AND co-located. If yes → fire. If no → defer #7 + re-evaluate at s170.
- Co-location preference: node 33 candidates first (4 strikers there) > node 60 candidates (3 strikers there). No travel for amendment D pilots — travel was the failure mode of B; D isolates the floor question from the latency question.
- vuongdung1198 idx=9051 at node 33 currently margin=+5 elapsed_h=7.22. If this kami persists and grows to +10-15 by s169 (~30min) under non-cycling guards (defensive_cycle currently False per s168 snap), it's the first candidate. BandG idx=590 (+16, node 12, elapsed_h 9.53) is a no-travel-out-of-zone candidate but cross-region from node 33; qualifies under D only with one-zone-hop economic check, deferred to amendment B-style logic.

**Counter-evidence to watch for**: if any v3 candidate reaches +20 organically in s169 without amendment D firing, A becomes triggerable on that single trial without needing D's diagnostic step. D becomes secondary in that branch.

**Relation to other amendments**:
- A (single trial floor +20): still PROPOSED, never fired. A precedes D in the relaxation chain — D only fires if A would-have-fired but no candidate ≥+20 exists.
- B (cross-region travel for first pilot): FIRED s166, failed. NOT triggered for D pilots — D explicitly forbids travel to isolate the floor question.
- C (snapshot famine / cycling-defensive owners): independent track. Branch 1 (garrison) is the s167+ active test for cycling-defensive class. D is for the persistent class.

**N**: 0 strikes. First fireable opportunity is s169 if vuongdung idx=9051 (or similar persistent node-33 row) reaches +10 with guards.

---

## Node 86 doctrine investigation — RESOLVED s170 (Lane A)

**Status**: RESOLVED — guild gate, not filter error. No doctrine change required.

**Question (from plan-170)**: why do Assassins + aitcoin land 9 kills/6h on 2 victims at node 86 while our v3 surfaces zero candidates there?

**Findings (s170 04:55–05:30 UTC May 5)**:

1. **Raw scan IS finding node-86 candidates** — `by_node["86"]` shows 16 killable rows, all stefan97 (`defensive_cycle=True`, sync_stop_bursts x2 + sync_feed_bursts x1) — filtered to v2 stage as designed. Margins +98 to +136 if striker were co-located.
2. **Real kill victims are buzz, not stefan97**. World-liquidations.jsonl last 12h node 86: 8/9 victims owned by `buzz`, 1 by `aitcoin` (likely self-strike for cooldown reset). NONE are stefan97 victims.
3. **Buzz at node 86 IS in raw scan but `guild_blocked=true`**. Example: idx=9264 (buzz) margin +102, def_cycle=False, but `guild_blocked: true` — so it's filtered at the guild stage before reaching v2.
4. **Why guild-blocked**: `predator/guild-no-touch.csv` lists buzz as `FOUNDER_OWN (kami-agent)` — buzz is the founder's other automated agent. Per Hard Rule 1 we cannot strike them. Competitors (Assassins, aitcoin) have different guild affiliations and freely strike buzz kamis.

**Doctrine implication**: Node 86 hot_battleground signal is NOISE for kami-zero. The cluster is competitor-vs-buzz, both outside our action set (we can't strike buzz; we don't care about competitor wins). Continuing to surface node 86 in `hot_battlegrounds` is fine for situational awareness but should NOT trigger a modality investigation again. **No filter doctrine error. No amendment needed.**

**Generalization**: when `hot_battlegrounds` shows a node with no v2/v3 candidates, run this 3-step test before suspecting doctrine error:
- Check `by_node[N].top10[*].guild_blocked` — if all True, it's the guild gate working.
- Check `by_node[N].top10[*].heat.defensive_cycle` — if all True, it's the def-cycle filter working.
- Check world-liquidations victim accounts — if they map to guild-no-touch entries, the entire cluster is unactionable for us.

**Updated CLAUDE.md "Self-audit" guidance candidate**: hot_battlegrounds at nodes where ALL raw candidates are guild-blocked or def-cycle suppressed are not "missed opportunities" — they're correctly filtered. Document in `missed-opportunities.md` only when victim accounts are NOT guild-blocked AND NOT def-cycle.

**Next investigation candidates** (if a future hot_battleground is unresolved by the 3-step test):
- Sub-+30 strikes hypothesis (Hypothesis 2 from plan-170): query competitor attacker stats vs known victims, derive fire-margin distribution. Defer until a non-trivially-guild-blocked battleground appears.
- Glue/revive cycle (Hypothesis 3): orderable from world-liquidations with chronological gap analysis. Defer.

**N**: 1 investigation. CLOSED.

---

## 12649 migration cost-benefit analysis (s172)

**Status**: HYPOTHESIS DECISION (session 172 defer #10, plan-171 trigger). HOLD with revised thesis.

**Trigger**: 20 consecutive 0-strike sessions (s152-s171, 15 attempt-eligible). s171 watcher surfaced vuongdung1198 cluster at node 33 calibrated on 12649 with margins +5/+7/+9/+10/+15. Plan-171 mandated EV write-up for migrating 12649 (node 60 → node 33) to convert "watcher-only signal" into "fireable from co-located striker".

**s172 finding that reframes the thesis**:

Per-striker margin recompute via `executor/hp_projection.kill_threshold` for the s172 top node-33 candidate (vuongdung1198 idx=7586, watcher margin +23 via 12649 calibration):

| Striker | Hand | V | atk_s | atk_r | kill_zone | margin (vs proj_hp 119) |
|---------|------|----|------|-------|-----------|-------------------------|
| 15540   | NORMAL | 31 | 280 | 250 | 104 | -15 |
| 6058    | SCRAP  | 31 | 280 | 250 | 94  | -25 |
| **6245**| EERIE  | 30 | 260 | 500 | **124** | **+5** (ONLY positive co-located) |
| 12225   | NORMAL | 30 | 280 | 500 | 114 | -5 |
| 12649   | NORMAL | 34 | 400 | 500 | 143 | +24 (NOT co-located) |

**Co-located max at node 33 vs persistent vuongdung1198 starver**: +5 (6245's EERIE-strong affinity vs SCRAP body is the only thing keeping it positive). Watcher's +23 was a 12649-calibration phantom — not actionable from current node-33 garrison.

s172 also live-projected 12649 vs TrayzinCarpathia idx=126 at node 60 (12649's HOME node): margin **+27** clean, all guards met. 12649 has REAL fire-ready candidates at node 60 today.

**This inverts the migration thesis**: migrating 12649 to node 33 would LOSE access to node-60 fire opportunities (where 12649's V=34 + atk_s=400 + co-location actually fires). The node-33 garrison's structural problem isn't 12649's absence — it's the strikers' weak baseline (V≤31, atk_s≤280, atk_r≤500) vs vuongdung1198's defensive specs (def_s=100 typical).

**Three branches of action** (replacing the s171 binary GO/NO-GO):

1. **HOLD garrison** (default). Wait for vuongdung1198 starvers' projected HP to drop further with elapsed_h growth. Forward projection on idx=7586 vs 6245: at +30min margin +16 (clears D), at +45min margin +21 (clears A), at +60min margin +26. 6245's EERIE strong affinity is the structural answer to vuongdung1198's SCRAP body. Cost: 0 gas. Benefit: free fires when starvers mature past D-gate naturally.

2. **Operator visit to room 60** (NOT migration). Travel 33→60 (12 hops, ~1.5M gas), fire 12649 on whatever node-60 candidates remain (126 +27 today, plus whatever cycling reveals), return 33→60 later. Keeps roster split current. Captures node-60 +20 floor opportunities. Cost: ~3-5M gas per visit. Per-trip benefit: 1-3 obols + spoils + possible 11224 Lethality allocation if 11224 cycles to RESTING during visit.

3. **Migrate 12649 → node 33** (the s171 plan). Stop_harvest 12649/11224/10705 at node 60 (~8-9M gas force-flush at 14h elapsed), travel 33→60→33 (~3M gas), harvest_start 12649 at node 33 (~250k-1M gas). Total ~15-30M. Lost: node-60 +27 fire opportunities (which we'd miss by leaving). Gained: 12649 calibration on node-33 candidates is no longer phantom — fire margins jump from +5 (6245) to +24 (12649). But the persistent cluster at node 33 is currently 1-2 candidates total (s172 watcher), so per-cycle benefit is small.

**Decision matrix (revised)**:

| Branch | Gas cost | Expected fires/week | EV (obol/gas) |
|--------|----------|---------------------|---------------|
| 1 HOLD | 0        | 1-3 from D-gate maturation | high (free) |
| 2 Visit| 3-5M/visit | 2-4 per visit if cluster persists | mid (gas-positive if N≥2 fires) |
| 3 Migrate | 15-30M one-time | 2-5 first week, then asymptote | low (only justified if vuongdung1198 cluster grows ≥4 D-gate candidates persistent — currently 1-2) |

**Adoption (s172 decision)**: **HOLD** (Branch 1) for next 1-2 sessions. Re-evaluate after observing whether (a) vuongdung1198 starver maturation produces a clean fire under D-gate, (b) node-60 cluster persists or evaporates between sessions. If (a) lands ≥1 kill: doctrine affirmed, no migration. If (b) cluster persists across 3+ sessions WITH no node-33 fires: Branch 2 (operator visit) becomes higher EV than Branch 3 (migration).

**Branch 3 trigger conditions** (would override HOLD): (a) vuongdung1198 surfaces ≥4 D-gate candidates persistent across 3+ sessions AND (b) node 60 has ≤1 fire-ready candidate per session AND (c) 11224 banked SP allocation is the binding constraint on node-33 firepower.

**Cost of HOLD if wrong**: another defer #11 if 7586 cycles out before maturing past +10. Acceptable — cluster persistence has been observed, next cycle re-surfaces a similar candidate.

**Counter-evidence to watch for**: a session where node-60 cluster fully evaporates (0 candidates ≥+10 watcher margin from 12649 perspective) for 2+ consecutive snapshots. Would shift Branch 2 EV down and make Branch 3 (migration) more attractive.

**Relation to Amendment E**: NOT triggered. Migration EV produced actionable HOLD decision with concrete branch-switch criteria. Amendment E (modality shift) was the s171 trigger condition for "migration NO-GO confirmed" — current decision is HOLD-with-criteria, not NO-GO.

**N**: 0 fires under any branch. s173 first decision point — execute HOLD if 7586 still HARVESTING with ≥+10 margin and ≥6h elapsed, fire D pilot.

---

## E009 Amendment E — "vuongdung1198 cluster fully migrated to anti-predator automation (100%-parked archetype)"

**Status**: **P1-CONFIRMED s183** (Phase 1 7/7 formal threshold crossed — vuongdung1198 cluster on node 33 100% parked_True with rates_aware in [-27, -75] across 11 consecutive watcher-sessions s173–s183; cluster size 6→12; zero falsifying observations in the 7-session window). **Phase 2 §PARTIAL trigger MET s183** (4 consecutive 0-non-archetype-fire-surface sessions s180–s183 → world-wide deflation, not vuongdung1198-specific). See "§PARTIAL trigger criteria" block below.

**Modality-shift context**: Streak s152–s176 = 25 consecutive 0-strike sessions (5 by-design / 20 attempt-eligible / 13 deferred E009 pilots). Original "5 consecutive 0-kill = design mode" trigger surpassed by 20 sessions. Doctrinal accountability for non-defer modality moves is the obligation that produces this hypothesis write-up. Pure-defer at 25-session 0-strike with 4-session structural deflation is doctrinally insufficient.

**Observation summary** (4 consecutive sessions, s173–s176):

| Session | node 33 vuongdung1198 sampled | parked_bool=True with negative rates_aware | non-archetype fire-eligible at node 60 |
|---------|-------------------------------|--------------------------------------------|---------------------------------------|
| s173    | 6/6 (rest unsampled)          | 6/6 (rates_aware -45 to -70)              | 0 |
| s174    | 9 sampled / 6 unsampled-archetype | 9/9 (rates_aware -47 to -70)          | 0 (11319 +22 single-target, cross-region rejected) |
| s175    | all sampled = parked          | all parked, rates_aware deeply negative   | 0 |
| s176    | 13/14 sampled = parked        | 13/13 (rates_aware -27 to -75)            | 1 (3243 wiuuuu margin +16, parked_bool=None archetype REJECT) |

**Stable surface specs**: vuongdung1198 candidates show consistent rates_aware_margin in [-27, -75], median ~-55. Raw kill_zone margins remain HIGH (+15 to +62 today), but rates-aware projection inverts every one — confirming the parked-rates phantom phenomenon (kill_zone projection trusts snapshot rates that were sampled while kami was already drained-and-parked, sync_hp does not actually drain from the on-chain state).

**Hypothesis**: vuongdung1198 cluster has fully migrated to anti-predator automation that PRE-DRAINS sync_hp to floor (~0–20% of total) BEFORE leaving kamis at the node — kamis appear "harvesting" with high accumulated balance, but rates=0 means projected HP is NOT going to fall further with elapsed time, AND sync_hp is already at floor (operator stop_harvest mints whatever balance accumulated, then re-starts at full HP). Result: kamis remain in the killable scan with high raw margins indefinitely, but **no actual strike will land** because projected HP at strike-time ≠ actual sync_hp at strike-time. **Continuing to scan node 33 as primary fire surface is structurally negative-EV** under the current rates-aware doctrine.

**Predictions** (test conditions for adoption / rejection):

1. **P1 (continued deflation)**: vuongdung1198 candidates remain 100% `parked_bool=True` with `rates_aware_margin ≤ -20` for ≥7 consecutive sessions starting s176. **REJECT** if any session in that window shows ≥1 vuongdung1198 candidate with `parked_bool=False` (sampled = real strain present, fire-eligible).
2. **P2 (operator-arrival sync_stop_burst)**: when bpeon operator next visits node 33 (any reason — visiting node 60 during s174 plan tested differently), within 5 min of room-arrival, watch for ≥3 vuongdung1198 stop_harvest events. Confirms automation is operator-arrival-triggered (CLAUDE.md "defensive cycling owners" pattern).
3. **P3 (MUSU bounty pool stagnation)**: vuongdung1198 candidates' `harvest.bounty.balance` should NOT grow significantly over a 7d window for parked-state kamis (rates=0 means no minting). Query oracle: `SELECT kami_index, MIN(balance), MAX(balance), MAX-MIN AS delta FROM v_harvest_state WHERE owner='vuongdung1198' AND ts > now() - INTERVAL '7d'`. Expect delta < 100 MUSU per kami if hypothesis correct.

**Test execution plan** (3-session continued observation + sample 5 non-archetype nodes):

- **Phase 1 (s176–s179)**: continue passive observation. Log node-33 vuongdung1198 sampled %, rates_aware distribution per session. Confirm or reject P1.
- **Phase 2 (s180+)**: scan 5 non-archetype-dominated nodes (candidates: node 25, node 73, node 9, node 16, node 88 from `hot_nodes`) for fire-surface comparison. If non-archetype nodes show ≥1 fire-eligible candidate (`rates_aware ≥+10`, sampled or non-archetype owner) per scan in ≥3 of 5 sessions, then **node 33 garrison location is confirmed structurally negative-EV** (the surface elsewhere exists, we just aren't there).
- **Phase 3 (oracle query)**: P3 at any time — oracle is read-only and free.

**Counter-response options if confirmed**:

1. **Operator forced migration to node 60** (~15-30M gas one-time per E009 §"12649 migration cost-benefit"): re-activates 11224 Lethality allocation (banked SP=3, +24 kill_zone post-allocation per s171 audit) AND co-locates 12649 with REAL node-60 fire surface (TrayzinCarpathia/foden cluster). Note: trade-off is foden defensive-cycle cluster at node 60 (mostly parked-bool=None archetype reject).
2. **Visiting raid pattern** (operator transit 33→60 mid-session for opportunistic node-60 fires, return to 33 garrison): captures node-60 +20 floor when it appears (cf. s172 12649 vs TrayzinCarpathia idx=126 +27 example), no migration commitment. Cost: ~3-5M gas per visit.
3. **Multi-node garrison** (split roster): 2 strikers at node 33 (passive watch), 3 strikers at node 60 (active fire). Requires 11224 Lethality for node-33 contingent. Long-horizon if cluster diversification across nodes is the structural answer.
4. **Glue-raid play** (E004 dependency): 6 Spirit Glue currently in inventory (lifetime metric), insufficient for 6-target lock per E008 plan. Craft batch first. If vuongdung1198 cluster remains parked-archetype-stable, glue-then-strike could pierce the automation lock IF projected HP truly is below kill_zone during the lock window. Test on lower-stakes target first.
5. **Wait** (passive): defensive automation owners eventually shift patterns (~weeks-months observed in stefan97/foden histories). If cluster economics improves elsewhere, deflation here is irrelevant.
6. **Hybrid** (counter-response 1 + 4): forced migration + glue-pre-strike test on node 60 cluster.

**Decision criteria for adoption / counter-response**:

- **ADOPT (Phase 1 confirms P1, Phase 2 confirms surface elsewhere)**: implement counter-response 1 (forced migration). Gas EV: 15-30M one-time vs. ~25 sessions × ~0 obol = -∞ obol/gas at status quo. Migration EV becomes positive even at 1 obol/week post-migration. The argument that "node 33 isn't EV-negative because gas spent is also 0" is INVALID at this defer count — we're paying a real opportunity cost in non-fired sessions where another node would have produced fires.
- **REJECT (P1 falsified within 7 sessions)**: cluster wasn't fully captured by automation. Continue HOLD, no Amendment E action. Document recovery in metrics.
- **PARTIAL (P1 holds but Phase 2 also shows structural deflation everywhere)**: world-wide parked-rates phenomenon is a meta shift, not a vuongdung1198-specific issue. Re-derive rates-aware doctrine, possibly relax `rates_aware_margin ≥+10` floor to +0 with stricter parked_bool=False co-requirement.

**Relation to other modality work**:
- **Amendment D**: N=0 fires. D-pilot trigger has been blocked by rates-aware gate (which Amendment E hypothesizes is the correct gate, so Amendment D is doctrinally consistent — just hasn't fired because the surface is empty).
- **E009 Amendment C garrison N=2→3**: still active but irrelevant if surface itself is structurally drained.
- **Branch 1/2/3 migration framework**: Amendment E is essentially "Branch 3 trigger conditions need re-thinking" — Branch 3 was conditioned on vuongdung1198 cluster GROWING (≥4 D-gate candidates persistent), which was the wrong frame; the cluster is large but RATES-DEAD, which is the new condition for migration justification.

**Counter-argument worth steelmanning before Phase 1 completes**:
- vuongdung1198 cycle may be ~24h+ (defensive automation cycles slowly relative to natural harvest cycles ~6-10h). 4-session window may be too short to characterize. P1 at ≥7 sessions accounts for this. If pattern persists 7+ sessions, the long-cycle hypothesis is also rejected (24h would have produced un-parked windows by now).

**N**: 0 (HYPOTHESIS only — Phase 1 begins s177).

**Read-back**: when reading this entry in s177, before any non-defer action, ask: "Has Phase 1 produced un-parked vuongdung1198 candidates? Is Phase 2 needed? Does world_targets.json show non-archetype-dominated nodes with fire-eligible candidates?" Answer in plan.md s177 if reaching for migration counter-response.

---

### §PARTIAL trigger criteria (s183 write-up)

The Phase-1 outcome (vuongdung1198 cluster 100%-parked) AND the Phase-2 outcome (world-wide non-archetype fire surface = 0 across ≥4 consecutive sessions) jointly map to the **PARTIAL** branch of "Decision criteria for adoption / counter-response": the parked-rates phenomenon is a **meta shift**, not a single-cluster automation event. Counter-response 1 (forced migration) is therefore a poor fit — migrating the operator to node 60 (or any single alternative) would not surface fire-eligible non-archetype candidates if the entire scan radius is structurally drained.

**Trigger conditions for §PARTIAL doctrine activation** (all required):

1. **Phase 1 P1-CONFIRMED**: vuongdung1198 cluster (or analogous on garrison node) shows 100% `parked_bool=True` with `rates_aware_margin ≤ -20` across ≥7 consecutive watcher-sessions, AND
2. **Phase 2 deflation persistent**: world-wide non-archetype `rates_aware ≥ +10 + parked_True` count = 0 across ≥4 consecutive sessions, AND
3. **Hot-battlegrounds wedge**: ≥1 hot_battlegrounds entry shows competitor predator(s) extracting non-trivial MUSU (≥300 per kill) from at least one node where our scan surface = 0.

(s183 status: condition 1 MET, condition 2 MET, condition 3 MET — node 9 yellowtail/tamagotcho extracted 5×~700 MUSU in ~12 min while our scan shows 0 fire-eligible candidates anywhere co-located.)

**§PARTIAL doctrine response options** (non-exclusive — adoption requires explicit decision in plan.md, gas-budgeted, with reversion criteria):

(A) **Relax `rates_aware ≥ +10` floor to `≥ +0` with stricter `parked_bool=False` co-requirement.** Justification: when sampled-True rates are deeply negative everywhere, `rates_aware ≥ +10` becomes an unreachable bar; a floor at +0 with `parked_bool=False` (real strain confirmed, even if marginal) admits the on-the-fence candidates the watcher currently rejects. Risk: revert rate may climb if `parked_bool=False` doesn't fully sub for `+10` margin; first 3 fires are pilot-marked single-shot.

(B) **Owner-archetype REJECT relaxation for non-co-located archetype clusters where competitor activity proves them killable.** Specifically: if hot_battlegrounds shows non-trivial extraction (≥300 MUSU/kill, ≥3 kills/3h) from an archetype owner at node X AND our oracle drill shows ≥3 active harvests by that owner at node X, then archetype-REJECT for that owner-at-that-node is downgraded to UNSAFE-unsampled-archetype-NODE-X (admit if other guards clean AND rates_aware ≥+10 confirmed). Reasoning: archetype-REJECT was empirically derived from operator-arrival-triggered defensive cycling on node 33 (vuongdung1198) and node 73 (TrayzinCarpathia); it is not first-principles necessary that the same owner running anti-predator automation on one node has it on every node. Risk: the rule loses its blanket-safety property; per-owner-per-node decisions require maintained cross-reference. First 3 fires single-shot pilot-marked.

(C) **Long-horizon strategy shift: roster leveling wave / build-up.** Justification: if the world-wide harvestable surface has structurally collapsed across our scan radius, the binding constraint is no longer "find better targets in this scan" but "expand the surface" (better strikers via leveling, broader scan via second-operator multi-node garrison, or wait out the meta). Roster has banked SP=3 on 11224 (BLOCKED) and SP banking on others; a leveling wave is currently NON-actionable due to operator-room-constraint blocking 11224's allocation, but the §PARTIAL trigger increases priority on resolving the unblock pathway.

(D) **Migration to non-archetype node validated by hot_battlegrounds.** If hot_battlegrounds + oracle drill identifies a node where competitor predators ARE extracting from non-archetype owners with `rates_aware ≥ +10` in our scan radius (currently NOT observed — node 9 victims are tamagotcho archetype), then forced migration to that node is the §PARTIAL-compliant counter-response 1 variant. Pre-migration write-up REQUIRED in decisions.md.

**Reversion conditions** (return to baseline doctrine):

- ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere world-wide. The deflation has lifted; baseline rates-aware floor is the right gate again.
- OR: a single successful non-archetype clean strike at `rates_aware ≥ +10` reverts (P1/P2 hypothesis was a measurement artifact; revert at margin invalidates the rates_aware doctrine itself, escalate to first-principles re-derivation per E009 §"rates-aware doctrine origin").
- OR: founder directive in `ideas_to_founder.md` response.

**§PARTIAL adoption decision** (s183, default): **DEFER explicit doctrine change** pending one more session confirmation (s184 = condition 2 5th consecutive). Adoption of (A) or (B) requires explicit pilot fire under controlled conditions — current session has no fire-eligible candidate (even under relaxed criteria, the killable_v3 candidates either fail elapsed gate, fail margin gate, or are archetype with no hot_battlegrounds wedge for their node). The trigger is MET in principle; the FIRST fire-eligible test target (per (A) or (B) criteria) becomes the §PARTIAL pilot.

**§PARTIAL pilot fire criteria** (when test target appears, single-shot pilot, full revert characterization required):

- (A)-pilot: any candidate with `rates_aware ≥ +0`, `parked_bool=False`, elapsed ≥6h, non-archetype, co-located (or 1-hop). Single shot. If revert: revert kind documented; (A) adoption deferred. If kill: 2 more (A)-pilots before adoption.
- (B)-pilot: any archetype owner X at node Y where hot_battlegrounds + oracle drill confirm competitor extraction (≥3 kills with ≥300 MUSU each from that owner-node combo in 3h), AND our scan shows ≥1 sampled-True rates_aware ≥+10 candidate from that owner-node combo. Single shot. Revert/kill outcome handled per (A).

**Sub-issue queue impact**: pin the §PARTIAL trigger MET status as a high-priority watch in `predator/learnings.md` and `memory/plan.md` for s184. Roster leveling wave (sub-issue #20) escalates from "long-term" to "explore unblock pathway for 11224 banked SP=3" given option (C) becomes more relevant under §PARTIAL.

---

## E011 — Parked-phantom-owner set extends beyond the static archetype REJECT list

**Status**: HYPOTHESIS (N=2 corroborations s185/s186; threshold for doctrinal note met, but does not change fire criteria)

**Observation source**: Through s184, every observed `parked_bool=True` (intensity=0, fertility=0, balance=0, sync≈total) entry in `parked_v2` / `by_idx` came from the static archetype REJECT list (vuongdung1198, sa3woo, buja723, stefan97, foden, dias, rtvvvvv, TrayzinCarpathia). s185 added wiuuuu (v_idx=1750 node 60). s186 added COCOH (v_idx=1462 node 60). Plus s186 by_idx confirms popo (5539, 7562 node 65), 3333333333333333 + 4444444444444444 (multi-entry node 82), yeddy, maia, acheron — many additional non-archetype owners hosting parked phantoms.

**First-principles re-derivation**: `parked_bool=True` is the rates-aware sampling signal — intensity_avg=0 + balance=0 over the watcher's sampling interval. It is mechanically agnostic to who owns the kami. Any kami whose harvest is rates-stalled (lvl/affinity mismatch leading to <1 MUSU/sec accumulation, or pre-balance-claim phase) will sample as parked. The static archetype REJECT list was only ever a heuristic for identifying *known* anti-predator automation operators; it was never claimed to enumerate the full set of parked-phantom owners.

**Doctrinal implication**: minimal. The §PARTIAL §A criterion already uses `parked_bool=False` (the sampled signal) as the binding condition, NOT owner attribution. This data corroborates that the criterion was correctly designed: if §A had relied on "non-archetype owner" as a sufficient guard, today's COCOH/wiuuuu/popo/3333... entries would have been falsely admitted as fire-eligible (they are phantoms). The archetype REJECT list remains useful as a *necessary* guard (kills the obvious cases without sampling), but is *not sufficient* — the rates-aware sample is what distinguishes phantom from real strain.

**Test design**: passive observation. No fire test required because the doctrine doesn't change. Track non-archetype parked-phantom appearances per session; if the rate keeps climbing, formally update mechanics.md to note "parked phantoms span a broad owner set; archetype REJECT is a heuristic acceleration, not a closure."

**N**: 2 explicit (wiuuuu s185, COCOH s186) + many implicit (3333333333333333, 4444444444444444, maia, acheron, yeddy, popo) all observed s186 by_idx. Threshold ≥2 met for elevation from "single observation noise candidate" to "logged pattern". Will graduate to mechanics.md note (not a doctrine change) when N≥10 distinct non-archetype owners across ≥5 sessions.

**Read-back**: when reading this entry in a future session, the question is: "Does today's killable_v3 / parked_v2 contain a non-archetype owner that I would have admitted under owner-attribution alone, but parked_bool=True via by_idx correctly rejects?" If yes, this experiment continues to validate. If a non-archetype owner appears with `parked_bool=False AND rates_aware_margin ≥ +10`, that's a §PARTIAL §A pilot trigger candidate — fire-eligible under the existing criterion.

---

## Lifecycle policy

- New observation → write HYPOTHESIS entry within the same session you observed it.
- Do NOT modify plan.md to apply the hypothesis as a rule until ADOPTED.
- Run TESTING through opportunistic strikes (don't divert from primary hunting just to gather data, unless in design-mode session).
- Each TESTING entry's N must reach ≥20 across diverse conditions before adoption.
- ADOPTED entries graduate to `predator/mechanics.md` with full derivation + test reference.
- REJECTED entries stay here as historical record + a note on what first-principles model explained the pattern.
