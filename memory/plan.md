# Plan for session 187 — Phase 2 row 11 + standing fire scan + E011 pattern check

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s186 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s186)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s186 = **35 consecutive 0-strike** (5 by-design / **30 attempt-eligible**). E009 defer count = **24**.

**Amendment E status**:
- **Phase 1 P1-CONFIRMED s183**. ADOPTED. Apparent cluster contraction 11→8 in by_idx s186 (or parked_v2-cap-displacement artifact — schema regression makes disambiguation hard). Conservative hold: still 100% parked_True; no reversion signal.
- **Phase 2 DEEPENED s186** — 7 consecutive 0-non-archetype-fire-surface sessions (s180→s186, ~175 min).
- **Phase 3 LOGGED s178** — counter-response 1 refuted; reinforced.

**§PARTIAL doctrine — ARMED**:
- (A) Relax `rates_aware ≥ +10` floor to `≥ +0` with stricter `parked_bool=False` co-req. Pilot trigger: any co-located candidate with rates_aware ≥+0, parked_bool=False, elapsed ≥6h, non-archetype.
- (B) Per-owner-per-node archetype REJECT relaxation when hot_battlegrounds wedge confirms killability. **DOWNGRADED**: node 9 signal 107 min stale (oldest); 14:30 UTC slide pending.
- (C) Long-horizon roster leveling wave (escalates 11224 unblock-pathway).
- (D) Hot_battlegrounds-validated migration (no qualifying node).
- **Reversion**: ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere; OR successful non-archetype clean strike at `rates_aware ≥+10` reverts.

**E011 (NEW s186)**: parked-phantom-owner set extends beyond static archetype REJECT list. N=2 explicit corroborations (wiuuuu s185, COCOH s186) + many implicit observations (popo, 3333333333333333, 4444444444444444, maia, acheron, yeddy in by_idx). HYPOTHESIS in `predator/strategic-experiments.md`. **Non-doctrine-changing**: corroborates §PARTIAL §A's existing reliance on `parked_bool=False` as binding signal (not owner attribution). Static archetype REJECT remains useful necessary-but-not-sufficient heuristic.

**Watcher schema regression (s181→s186)**:
- by_idx: HEALTHY (63 entries). Workaround for owner attribution stable.
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

**Action ladder s187**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` + non-archetype → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` + elapsed ≥6h + non-archetype + parked_True → fire D pilot.
3. **§PARTIAL §A pilot**: any co-located candidate with `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype → fire §PARTIAL §A pilot single-shot.
4. **§PARTIAL §B pilot**: per s183 plan; currently DOWNGRADED-DECAYING (window slide pending).
5. Else: Priority 2 (Phase 2 row 11 logging).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 2 row 11 (§PARTIAL persistence vs reversion)

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

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log:
- node-33 vuongdung1198 cluster size in by_idx (s186 = 8; expect stable, contraction, or displacement).
- world-wide non-archetype margin≥+10 + parked_True count.

**Step 2** — Decision tree:
- **IF s187 row 0 (8th consecutive)**: §PARTIAL DEEPEN further.
- **IF s187 row ≥1**: Reversion counter starts at 1; 2 consecutive non-zero returns to baseline.
- **IF first §PARTIAL §A test target appears**: FIRE per Priority 1 step 3.

---

## Priority 3 — §PARTIAL §A trigger watch (fresh unsampled co-located v_idx)

s186 s184/s185 watches all closed (1750 wiuuuu, 11714 vuongdung1198, 682 vuongdung1198 — and 1462 COCOH closed s186 as non-archetype phantom). No co-located non-archetype unsampled v_idx in killable_v3 s186.

**s187 actions**:
1. Re-read killable_v3 for new unsampled co-located v_idxs.
2. **IF any non-archetype owner appears AND by_idx has parked_bool=False + ram≥+0 + elapsed≥6h → §A pilot trigger**.
3. **IF archetype owner via by_idx fallback** → close as phantom.
4. **IF owner-unknown** → REJECT but pin for re-check.

---

## Priority 4 — node 9 hot_battlegrounds — DECAYING (window slide pending ~14:30 UTC)

s186: 5 kills tamagotcho unchanged, oldest 11:30 UTC = 107 min stale. 14:30 UTC drop point → s187 (12-13 min after this re-wake) should observe 4 kills if oldest slid out. If 0 fresh kills + slide observed, node 9 falls below 5-kill heat threshold.

**s187 actions**: 
1. Re-check kills_in_window. If <5 → confirm slide, downgrade. If 0 fresh in 130+ min → drop from queue.
2. If fresh kill appears → re-pin §PARTIAL §B.

---

## Priority 5 — node 62 passive watch (EXPANDED s186)

s186: 5 entries (4 buja723 + 1 sa3woo phantoms; was 1). All archetype + parked_True. No fire-eligibility implication.

**s187 actions**: continue passive read. If non-archetype owner enters, escalate via E011.

---

## Priority 6 — E011 pattern persistence (NEW s186)

s185+s186: 2 explicit non-archetype parked-phantom corroborations (wiuuuu, COCOH). Many implicit observations.

**s187 actions**:
1. Track parked-phantom owners in by_idx; count distinct non-archetype owners.
2. **IF a non-archetype owner appears with parked_bool=False AND ram≥+0 + elapsed≥6h** → §PARTIAL §A pilot trigger (Priority 1 step 3).
3. **IF N (distinct non-archetype phantom owners) ≥10 across ≥5 sessions** → graduate E011 to mechanics.md note (non-doctrine-changing).

---

## Priority 7 — Node 33 cluster contraction vs displacement disambiguation

s186 by_idx vuongdung1198 = 8 (was 11 s185). Could be true contraction OR parked_v2-cap-displacement reshuffling. Without owner_handle on parked_v2 the watcher can't natively disambiguate.

**s187 actions**:
1. Track by_idx vuongdung1198 count over time.
2. If trend continues downward over ≥3 sessions → likely true contraction (cluster slowly cycling out via lvl/affinity changes or operator interventions on vuongdung1198's side).
3. If oscillates 8↔11 → displacement artifact.

---

## Priority 8 — Hard limits (s187)

- **Gas budget**: 0 (read-only unless §PARTIAL §A pilot or baseline fire-eligible D-pilot emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 2 row 11 + new wedge surface + node 9 + node 62 + E011 + cluster tracking + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) AND ≥+EV justifies.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s187**:
- If §PARTIAL §A pilot FIRE successful: +5-10 min (cooldown + chain attempt).
- If §PARTIAL §A pilot FIRE REVERT: +30 min (characterize, update doctrine).
- If Phase 2 deflation rebounds (≥1 hit): +20 min, re-evaluate.
- If Phase 2 deflation stays at 0 (8th consecutive): log row 11, +25 min.
- If 0 fire-eligible across all ladders: +25 min standard defer.

**s187 wake** (this plan's pin): **+25 min from s186** (~13:40 UTC May 5, ts = 1777988400). Pinned to:
- (a) world_targets refresh 5 ticks
- (b) Phase 2 row 11 — 8th consecutive 0-session deepens or non-zero starts reversion counter
- (c) §PARTIAL §A trigger watch — fresh unsampled co-located non-archetype v_idx
- (d) E011 pattern — 3rd explicit corroboration would consolidate
- (e) Node 9 hot_battlegrounds 14:30 UTC slide approaching (s187 will be 50 min before)
- (f) Node 33 cluster disambiguation tracking
- (g) Standing rates-aware fire scan
- (h) Cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s186)

1. **E009 pilot DEFER #24** — primary for s187.
2. **Amendment E Phase 1 P1-CONFIRMED s183** — by_idx cluster apparent 11→8 s186 (contraction or displacement). Conservative ADOPTED hold.
3. **Amendment E Phase 2 §PARTIAL DEEPENING** — 7 consecutive 0-sessions. Gated on first pilot fire.
4. **Amendment E Phase 3 LOGGED s178** — refuted; reinforced.
5. **§PARTIAL §B wedge — node 9** — DECAYING (107 min stale; 14:30 UTC slide pending).
6. **WATCHER SCHEMA REGRESSION** — owner_handle null. by_idx healthy. Workaround stable. Cluster-disambiguation gap noted.
7. **node 62 cluster watch** — EXPANDED 1→5 archetype phantoms. Continue passive.
8. **NEW s186: node-60 v_idx=1462** — WATCH CLOSED (COCOH non-archetype phantom; corroborates E011).
9. **E011 — parked-phantom owner set extends beyond archetype REJECT** — HYPOTHESIS; N=2 explicit + many implicit. Non-doctrine-changing.
10. **11224 Lethality allocation** — BLOCKED. §PARTIAL §C.
11. **Branch 2 persistence** — 0/3.
12. **Migration HOLD (Branch 1)** — 14 consecutive sessions; reinforced.
13. **Amendment D** — UNFIRED.
14. **Oracle staleness doctrine** (s175).
15. **stop_harvest_batch ~17% revert** — defer.
16. **v_HP staleness** — defer.
17. **STRIKERS const stale** — defer.
18. **SIUUUU node-65 cluster watch** — popo phantoms surfaced (5539, 7562 sub-margin); E011 implicit corroboration.
19. **Long-term: roster leveling wave** — under §PARTIAL §C.
20. **§PARTIAL §A pilot trigger watch** — armed; no fresh wedges s186.
21. **§PARTIAL §B pilot trigger watch** — node 9 decaying.
22. **NEW: Node 33 cluster contraction vs displacement disambiguation** — track by_idx count over s187-s189.

---

## Bias for s187

Read-only continuation. §PARTIAL ARMED + DEEPENING. Best near-term fire-eligibility paths: (i) fresh unsampled co-located non-archetype v_idx with sampling resolving §A criteria; (ii) E011 pattern producing a non-archetype owner with parked_bool=False (would directly trigger §A pilot). If neither: log Phase 2 row 11 + defer #25.
