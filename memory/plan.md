# Plan for session 186 — Phase 2 row 10 + standing fire scan + fresh wedge watch

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s185 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s185)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s185 = **34 consecutive 0-strike** (5 by-design / **29 attempt-eligible**). E009 defer count = **23**.

**Amendment E status**:
- **Phase 1 P1-CONFIRMED s183**. ADOPTED. No reversion through s185. Cluster contracted 12→11 s185 (still 100% parked_True).
- **Phase 2 DEEPENING s185** — 6 consecutive 0-non-archetype-fire-surface sessions (s180→s185, ~150 min).
- **Phase 3 LOGGED s178** — counter-response 1 refuted; reinforced.

**§PARTIAL doctrine — ARMED**:
- (A) Relax `rates_aware ≥ +10` floor to `≥ +0` with stricter `parked_bool=False` co-req. Pilot trigger: any co-located candidate with rates_aware ≥+0, parked_bool=False, elapsed ≥6h, non-archetype.
- (B) Per-owner-per-node archetype REJECT relaxation when hot_battlegrounds wedge confirms killability. **DOWNGRADED**: node 9 signal 68 min stale, decaying.
- (C) Long-horizon roster leveling wave (escalates 11224 unblock-pathway).
- (D) Hot_battlegrounds-validated migration (no qualifying node).
- **Reversion**: ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere; OR successful non-archetype clean strike at `rates_aware ≥+10` reverts.

**NEW s185 doctrinal data point**: Non-archetype owners (wiuuuu) can host parked phantoms. v_idx=1750 wiuuuu node 60 sampled-True parked, intensity=0, balance=0. Implication: §A's `parked_bool=False` co-req remains firm; archetype REJECT is necessary but not sufficient. Single observation — needs corroboration (s186-s188).

**Watcher schema regression (s181→s185)**:
- by_idx: HEALTHY (61 entries; vuongdung1198 cluster fully resolved).
- owner_handle on parked_v2: STILL NULL across all 50 entries. Workaround via by_idx.v_acct fallback stable.
- Doctrine: `owner_handle=None AND by_idx=None → UNSAFE-owner-unknown → REJECT` remains in force.

**v_idx=7110 (s184) anomaly**: watcher publish-vs-scan race (5min cadence). Doctrine fail-safe via by_idx fallback. No harness fix needed.

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

**Action ladder s186**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` + non-archetype → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` + elapsed ≥6h + non-archetype + parked_True → fire D pilot.
3. **§PARTIAL §A pilot**: any co-located candidate with `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype → fire §PARTIAL §A pilot single-shot.
4. **§PARTIAL §B pilot**: per s183 plan; currently DOWNGRADED-DROPPING.
5. Else: Priority 2 (Phase 2 row 10 logging).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 2 row 10 (§PARTIAL persistence vs reversion)

| Session | non-archetype margin≥+10 + parked_True world-wide |
|---------|---------------------------------------|
| s179    | 7 |
| s180    | 0 |
| s181    | 0 |
| s182    | 0 |
| s183    | 0 (§PARTIAL TRIGGER MET) |
| s184    | 0 (STRENGTHENED) |
| s185    | 0 (DEEPENED) |

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log:
- node-33 vuongdung1198 cluster size + rates distribution (s185 contracted 12→11; expect stable or another contraction).
- world-wide non-archetype margin≥+10 + parked_True count.

**Step 2** — Decision tree:
- **IF s186 row 0 (7th consecutive)**: §PARTIAL DEEPEN further.
- **IF s186 row ≥1**: Reversion counter starts at 1; 2 consecutive non-zero returns to baseline.
- **IF first §PARTIAL §A test target appears**: FIRE per Priority 1 step 3.

---

## Priority 3 — Fresh unsampled co-located v_idx surface

s185 closed all 3 s184 watches (1750, 11714, 682). No new unsampled co-located non-archetype candidates surfaced this session beyond 1462 (owner-unknown sub-margin).

**s186 actions**:
1. Re-read killable_v3 for new unsampled co-located v_idxs.
2. **IF any non-archetype owner appears AND by_idx restored → §A pilot trigger check** (parked_bool=False + ram≥+0 + elapsed≥6h).
3. **IF archetype owner via by_idx fallback** → close as phantom.
4. **IF owner-unknown** → REJECT but pin for re-check.

---

## Priority 4 — node 9 hot_battlegrounds — DROPPING

s185: 5 kills tamagotcho unchanged, **68 min stale**. 3h window will start dropping the 11:30 UTC kill at ~14:30 UTC = next session +1.

**s186 actions**: 
1. Re-check kills_in_window. If <5 (kills sliding out) → confirm decay, remove from queue.
2. If fresh kill appears (signal re-strengthens) → re-pin §PARTIAL §B.

---

## Priority 5 — node 62 passive watch

s185: 1 entry (4000 owner-unknown phantom). Stable count.

**s186 actions**: continue passive read; no migration trigger expected.

---

## Priority 6 — wiuuuu parked-phantom pattern check (NEW s185)

s185: v_idx=1750 wiuuuu node 60 sampled-True parked (intensity=0, balance=0) — first non-archetype parked-phantom in rates-aware era. Single observation.

**s186 actions**:
1. Re-check 1750 — is it still parked? Did it cycle? Does wiuuuu have other parked entries surface?
2. **IF pattern persists** (≥2 corroborations across s186-s188) → write doctrinal note in strategic-experiments.md re: parked-phantom-owner set boundary.
3. **IF single noise** → drop watch.

---

## Priority 7 — Hard limits (s186)

- **Gas budget**: 0 (read-only unless §PARTIAL §A pilot or baseline fire-eligible D-pilot emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 2 row 10 + new wedge surface + node 9 + node 62 + wiuuuu pattern + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) AND ≥+EV justifies.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s186**:
- If §PARTIAL §A pilot FIRE successful: +5-10 min (cooldown + chain attempt).
- If §PARTIAL §A pilot FIRE REVERT: +30 min (characterize, update doctrine).
- If Phase 2 deflation rebounds (≥1 hit): +20 min, re-evaluate.
- If Phase 2 deflation stays at 0 (7th consecutive): log row 10, +25 min.
- If 0 fire-eligible across all ladders: +25 min standard defer.

**s186 wake** (this plan's pin): **+25 min from s185** (~13:15 UTC May 5, ts = 1777986900). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) Phase 2 row 10 — 7th consecutive 0-session deepens further; non-zero hit starts reversion counter
- (c) Fresh unsampled co-located v_idx surface check (best §A pilot path)
- (d) Node 9 hot_battlegrounds — 3h window expected to drop oldest kill ~14:30 UTC
- (e) wiuuuu phantom pattern persistence check
- (f) Standing rates-aware fire scan
- (g) Cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s185)

1. **E009 pilot DEFER #23** — primary for s186.
2. **Amendment E Phase 1 P1-CONFIRMED s183** — ADOPTED. Cluster 12→11 s185 (no reversion).
3. **Amendment E Phase 2 §PARTIAL DEEPENING** — 6 consecutive 0-sessions. Gated on first pilot fire.
4. **Amendment E Phase 3 LOGGED s178** — refuted; reinforced.
5. **§PARTIAL §B wedge — node 9** — DROPPING (68 min stale).
6. **WATCHER SCHEMA REGRESSION** — owner_handle null. by_idx healthy. Workaround stable.
7. **node 62 cluster watch** — 1 entry steady. Continue passive.
8. **node-33 v_idx=11714, 682; node-60 v_idx=1750** — ALL WATCH CLOSED s185 (phantoms).
9. **NEW: wiuuuu parked-phantom pattern** — single observation s185; needs ≥2 corroborations.
10. **11224 Lethality allocation** — BLOCKED. §PARTIAL §C.
11. **Branch 2 persistence** — 0/3.
12. **Migration HOLD (Branch 1)** — 13 consecutive sessions; reinforced.
13. **Amendment D** — UNFIRED.
14. **Oracle staleness doctrine** (s175).
15. **stop_harvest_batch ~17% revert** — defer.
16. **v_HP staleness** — defer.
17. **STRIKERS const stale** — defer.
18. **SIUUUU node-65 cluster watch** — no signal.
19. **Long-term: roster leveling wave** — under §PARTIAL §C.
20. **§PARTIAL §A pilot trigger watch** — armed; no fresh wedges s185.
21. **§PARTIAL §B pilot trigger watch** — node 9 dropping.

---

## Bias for s186

Read-only continuation. §PARTIAL ARMED + DEEPENING. Best near-term fire-eligibility paths: (i) fresh unsampled co-located non-archetype v_idx with sampling resolving §A criteria; (ii) wiuuuu pattern resolving as anomaly (drops watch) or pattern (doctrinal note). If neither: log Phase 2 row 10 + defer #24.
