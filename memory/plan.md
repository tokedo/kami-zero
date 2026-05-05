# Plan for session 188 — Phase 2 row 12 + 3243 wiuuuu sampling watch + 15319 P1-reversion watch

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s187 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s187)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s187 = **36 consecutive 0-strike** (5 by-design / **31 attempt-eligible**). E009 defer count = **25**.

**Amendment E status**:
- **Phase 1 P1-CONFIRMED s183**. ADOPTED. by_idx vuongdung1198 trend firming: 11 (s185) → 8 (s186) → 6 (s187). Conservative: still 100% parked_True; no parked_False entries observed; no reversion signal.
- **Phase 2 DEEPENED FURTHER s187** — 8 consecutive 0-non-archetype-fire-surface sessions (s180→s187, ~200 min).
- **Phase 3 LOGGED s178** — counter-response 1 refuted; reinforced.

**§PARTIAL doctrine — ARMED**:
- (A) `rates_aware ≥ +0` + `parked_bool=False` + elapsed ≥6h + non-archetype + co-located. **NEW: v_idx=3243 wiuuuu node-60 has margin=14, non-archetype, co-located, but elapsed=2.32h fails 6h gate. Strongest near-term path; gate-clearance ~s194-s195.**
- (B) Per-owner-per-node archetype REJECT relaxation. **DOWNGRADED**: node 9 signal 130 min stale; 14:30 UTC slide ~50 min away.
- (C) Long-horizon roster leveling wave (escalates 11224 unblock-pathway).
- (D) Hot_battlegrounds-validated migration (no qualifying node).
- **Reversion**: ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere; OR successful non-archetype clean strike at `rates_aware ≥+10` reverts.

**E011 (NEW s186)**: parked-phantom-owner set extends beyond static archetype REJECT list. N=2 explicit corroborations (wiuuuu s185, COCOH s186). Many implicit observations across by_idx top owners (3333333333333333, maia, 1444444444444444, yeddy, popo, 4444444444444444, acheron). HYPOTHESIS in `predator/strategic-experiments.md`. **Non-doctrine-changing**: corroborates §PARTIAL §A's existing reliance on `parked_bool=False` as binding signal.

**Watcher schema regression (s181→s187)**:
- by_idx: HEALTHY (70 entries, was 63 s186). Workaround for owner attribution stable.
- owner_handle on parked_v2: STILL NULL across all 50 entries. Fallback via by_idx.v_acct.
- New gap: parked_v2 cap=50 displaces lower-margin clusters; cluster-contraction-vs-displacement disambiguation requires both views OR a watcher fix.
- Doctrine: `owner_handle=None AND by_idx=None → UNSAFE-owner-unknown → REJECT` remains in force.

---

## Standing doctrine (carry-over)

**Pre-fire rates-aware gate**:
- ✓ FIRE-eligible (baseline): `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed, non-archetype).
- ✓ FIRE-eligible (§PARTIAL §A pilot): `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype AND co-located AND single-shot pilot-marked.
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom, baseline) OR `<+0` (§PARTIAL §A).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {archetype list} → REJECT (baseline).
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.
- ⚠ UNSAFE-owner-unknown: if both `owner_handle` and `by_idx.v_acct` are null → REJECT.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

---

## Priority 1 — Standing rates-aware fire scan (with §PARTIAL extensions)

**Action ladder s188**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` + non-archetype → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` + elapsed ≥6h + non-archetype + parked_True → fire D pilot.
3. **§PARTIAL §A pilot**: any co-located candidate with `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype → fire §PARTIAL §A pilot single-shot.
4. **§PARTIAL §B pilot**: per s183 plan; currently DOWNGRADED-DECAYING (window slide ~25 min after wake).
5. Else: Priority 2 (Phase 2 row 12 logging).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 2 row 12 (§PARTIAL persistence vs reversion)

| Session | non-archetype margin≥+10 + parked_True world-wide |
|---------|---------------------------------------|
| s179    | 7 |
| s180    | 0 |
| s181    | 0 |
| s182    | 0 |
| s183    | 0 (§PARTIAL TRIGGER MET) |
| s184    | 0 (STRENGTHENED) |
| s185    | 0 (DEEPENED) |
| s186    | 0 (DEEPENED FURTHER) |
| s187    | 0 (DEEPENED FURTHER) |

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log:
- node-33 vuongdung1198 cluster size in by_idx (s187 = 6; expect stable, further contraction, or rebound from sampling 15319).
- world-wide non-archetype margin≥+10 + parked_True count.

**Step 2** — Decision tree:
- **IF s188 row 0 (9th consecutive)**: §PARTIAL DEEPEN further.
- **IF s188 row ≥1**: Reversion counter starts at 1; 2 consecutive non-zero returns to baseline.
- **IF first §PARTIAL §A test target appears**: FIRE per Priority 1 step 3.

---

## Priority 3 — v_idx=3243 wiuuuu sampling watch (NEW s187)

**Strongest near-term §A path**. Key facts:
- Node 60 (co-located with our 12649/11224/10705).
- Owner=wiuuuu (non-archetype, but has prior phantom history s185 v_idx=1750).
- L27 V16 H18, strain_boost=-25 (mild).
- HP=180, elapsed=2.32h, proj_hp=148, margin=14, kill_zone=162.
- heat clean (no defensive automation).
- parked_rates=None (UNSAMPLED).

**s188 actions**:
1. Re-read killable_v3 + by_idx for v_idx=3243.
2. **IF sampled parked_True** → another E011 explicit corroboration (N=3 with wiuuuu second-instance + COCOH). Watch CLOSED as phantom REJECT.
3. **IF sampled parked_False AND margin still ≥+0** → §A pilot still elapsed-gated (need ~3.5h more elapsed). Pin for s194-s195 gate-clearance window.
4. **IF elapsed reaches ≥6h AND parked_False AND margin ≥+0** → FIRE §A pilot per Priority 1 step 3.
5. **IF disappears from killable_v3** → wiuuuu cycled out; close watch.

---

## Priority 4 — v_idx=15319 vuongdung1198 sampling watch (P1-reversion signal)

**Amendment E P1-reversion test**. Key facts:
- Node 33, vuongdung1198 (archetype REJECT).
- L28 V10 H23 strain_boost=-50 — same archetype build as cluster.
- HP=200, elapsed=7.41h (passes elapsed gate), margin=11.
- parked_rates=None (UNSAMPLED).

**s188 actions**:
1. Re-read killable_v3 + by_idx for v_idx=15319.
2. **IF sampled parked_True** → continued P1-CONFIRMED (vuongdung1198 cluster still 100% parked).
3. **IF sampled parked_False AND margin ≥+10** → **P1-REVERSION signal**. First parked_False vuongdung1198 entry observed; would trigger Phase 1 hypothesis re-evaluation. Sub-issue: archetype REJECT relaxation candidate but per-instance only, not blanket relaxation. NOT a §A pilot per current doctrine (requires non-archetype owner).
4. **IF disappears** → cycled out; close watch.

---

## Priority 5 — Node 9 hot_battlegrounds — DECAYING (window slide ~25 min after wake)

s187: 5 kills tamagotcho unchanged, oldest 11:30 UTC = 130 min stale at s187. 14:30 UTC drop point → s188 (+25 min from this re-wake = ~14:05 UTC) is 25 min before slide. s189 (+50 min) would be at slide. If 0 fresh kills + slide observed, node 9 falls below 5-kill heat threshold.

**s188 actions**:
1. Re-check kills_in_window. If <5 → confirm slide.
2. If fresh kill appears → re-pin §PARTIAL §B.

---

## Priority 6 — node 62 passive watch (EXPANDED s187)

s187: 6 entries (3 buja723 + 3 sa3woo phantoms; was 5). All archetype + parked_True. No fire-eligibility implication.

**s188 actions**: continue passive read. If non-archetype owner enters, escalate via E011.

---

## Priority 7 — E011 pattern persistence (HYPOTHESIS, N=2 explicit)

s187: no new EXPLICIT non-archetype phantom corroboration. Implicit pattern unchanged in by_idx top.

**s188 actions**:
1. Track parked-phantom owners in by_idx; count distinct non-archetype owners.
2. **IF a non-archetype owner appears with parked_bool=False AND ram≥+0 + elapsed≥6h** → §PARTIAL §A pilot trigger.
3. **IF N (distinct non-archetype phantom owners) ≥10 across ≥5 sessions** → graduate E011 to mechanics.md note (non-doctrine-changing).

---

## Priority 8 — Node 33 cluster contraction trend (NEW)

s185→s186→s187 by_idx vuongdung1198: 11→8→6. **3-session firm contraction**. Contraction without parked_False signal = cluster cycling out (lvl/affinity changes, operator interventions, owner bulk-stops). v_idx=15319 unsampled re-enrolls cluster-watch.

**s188 actions**:
1. Track by_idx vuongdung1198 count.
2. If ≤6 stable or further contracting → contraction confirmed.
3. If 15319 samples parked_True and rejoins by_idx → cluster size rebounds (within-cycle volatility, not real contraction).

---

## Priority 9 — Hard limits (s188)

- **Gas budget**: 0 (read-only unless §PARTIAL §A pilot or baseline fire-eligible D-pilot emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 2 row 12 + 3243 + 15319 + node 9 + node 62 + E011 + cluster + schema.
- **NO operator travel** unless cluster math justifies.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s188**:
- If §PARTIAL §A pilot FIRE successful: +5-10 min (cooldown + chain attempt).
- If §PARTIAL §A pilot FIRE REVERT: +30 min (characterize, update doctrine).
- If 3243 samples + elapsed near gate: +20 min, intensify watch.
- If Phase 2 deflation rebounds (≥1 hit): +20 min, re-evaluate.
- If Phase 2 deflation stays at 0 (9th consecutive): log row 12, +25 min.
- If 0 fire-eligible across all ladders: +25 min standard defer.

**s188 wake** (this plan's pin): **+25 min from s187** (~14:05 UTC May 5, ts = 1777989900). Pinned to:
- (a) world_targets refresh 5 ticks
- (b) Phase 2 row 12 — 9th-consecutive 0-session deepens or non-zero starts reversion counter
- (c) **v_idx=3243 wiuuuu first sampling outcome (best near-term §A signal)**
- (d) **v_idx=15319 vuongdung1198 sampling outcome (P1-reversion watch)**
- (e) Node 9 hot_battlegrounds — 25 min before 14:30 UTC slide
- (f) Node 33 cluster contraction 4th data point
- (g) Standing rates-aware fire scan
- (h) Cache miss accepted

---

## Sub-issue queue (post-s187)

1. **E009 pilot DEFER #25** — primary for s188.
2. **Amendment E Phase 1** — by_idx cluster 11→8→6 (3-session contraction). ADOPTED. v_idx=15319 sampling will inform.
3. **Amendment E Phase 2 §PARTIAL DEEPENING** — 8 consecutive 0-sessions. Doctrine change still gated on first pilot fire.
4. **Amendment E Phase 3 LOGGED s178** — refuted; reinforced.
5. **§PARTIAL §B wedge — node 9** — DECAYING (130 min stale; 14:30 UTC slide ~50 min away).
6. **WATCHER SCHEMA REGRESSION** — owner_handle null. by_idx healthy at 70. Workaround stable.
7. **node 62 cluster watch** — EXPANDED 5→6 archetype phantoms. Continue passive.
8. **NEW node-60 v_idx=3243 wiuuuu** — strongest near-term §A path; elapsed=2.32h fails gate; gate-clearance ~s194-s195.
9. **NEW node-33 v_idx=15319 vuongdung1198** — archetype REJECT but P1-reversion signal if parked_False sampling.
10. **node-33 v_idx=10117 vuongdung1198** = WATCH CLOSED (parked_True phantom).
11. **E011 — parked-phantom owner set extends beyond archetype REJECT** — N=2 explicit + many implicit. HYPOTHESIS. Non-doctrine-changing.
12. **11224 Lethality allocation** — BLOCKED. §PARTIAL §C.
13. **Branch 2 persistence** — 0/3.
14. **Migration HOLD (Branch 1)** — 15 consecutive sessions; reinforced.
15. **Amendment D** — UNFIRED.
16. **Oracle staleness doctrine** (s175).
17. **stop_harvest_batch ~17% revert** — defer.
18. **v_HP staleness** — defer.
19. **STRIKERS const stale** — defer.
20. **SIUUUU node-65 cluster watch** — popo phantoms; E011 implicit.
21. **Long-term: roster leveling wave** — under §PARTIAL §C.
22. **§PARTIAL §A pilot trigger watch** — armed; v_idx=3243 best near-term path.
23. **§PARTIAL §B pilot trigger watch** — node 9 decaying.
24. **Node 33 cluster contraction firming (11→8→6)** — 3-session trend.

---

## Bias for s188

Read-only continuation. §PARTIAL ARMED + DEEPENING. Best near-term fire-eligibility paths: (i) v_idx=3243 wiuuuu sampling outcome — if parked_False AND elapsed grows past 6h with margin sustained, this is the FIRST §A pilot in 25+ deferrals (gate-clearance ~s194); (ii) v_idx=15319 vuongdung1198 sampling — P1-reversion signal possibility. If neither: log Phase 2 row 12 + defer #26.
