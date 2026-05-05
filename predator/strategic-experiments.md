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

## Lifecycle policy

- New observation → write HYPOTHESIS entry within the same session you observed it.
- Do NOT modify plan.md to apply the hypothesis as a rule until ADOPTED.
- Run TESTING through opportunistic strikes (don't divert from primary hunting just to gather data, unless in design-mode session).
- Each TESTING entry's N must reach ≥20 across diverse conditions before adoption.
- ADOPTED entries graduate to `predator/mechanics.md` with full derivation + test reference.
- REJECTED entries stay here as historical record + a note on what first-principles model explained the pattern.
