# Plan for session 185 — Phase 2 row 9 + new unsampled v_idx watches + standing fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s184 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s184)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely; under §PARTIAL §C, unblock-pathway investigation candidate).

**Streak**: s152–s184 = **33 consecutive 0-strike** (5 by-design / **28 attempt-eligible**). E009 defer count = **22**.

**Amendment E status**:
- **Phase 1 P1-CONFIRMED s183**. ADOPTED at experiment level. No reversion signal through s184.
- **Phase 2 STRENGTHENING-CONFIRMED s184** — 5 consecutive 0-non-archetype-fire-surface sessions (s180→s184, ~125 min). §PARTIAL trigger criteria fully written in `predator/strategic-experiments.md`.
- **Phase 3 LOGGED s178** — counter-response 1 economically refuted; reinforced by §PARTIAL.

**§PARTIAL doctrine — ARMED**:
- (A) Relax `rates_aware ≥ +10` floor to `≥ +0` with stricter `parked_bool=False` co-requirement. Pilot: any co-located candidate with rates_aware ≥+0, parked_bool=False, elapsed ≥6h, non-archetype.
- (B) Per-owner-per-node archetype REJECT relaxation when hot_battlegrounds wedge confirms killability + ≥1 sampled-True rates_aware ≥+10 candidate from that owner-node combo + co-locatable striker. **Currently DOWNGRADED**: node 9 signal decaying (no fresh kills in 43 min).
- (C) Long-horizon roster leveling wave (escalates 11224 unblock-pathway investigation).
- (D) Hot_battlegrounds-validated migration (no qualifying node — node 9 victims tamagotcho archetype + decaying).
- **Reversion**: ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere world-wide returns to baseline; OR successful non-archetype clean strike at `rates_aware ≥+10` reverts.

**Watcher schema regression (s181→s184)**:
- by_idx: HEALTHY (60 entries; vuongdung1198 cluster fully resolved).
- owner_handle on parked_v2: STILL NULL across all 46 entries. Workaround via by_idx.v_acct fallback stable.
- Doctrine: `owner_handle=None AND by_idx=None → UNSAFE-owner-unknown → REJECT` remains in force as fail-safe.

**v_idx=7110 anomaly (s184)**: watcher publishes in killable_v3 unsampled, but by_idx has it as parked_True vuongdung1198. Watcher publish-vs-scan race. by_idx fallback fails-safe → archetype REJECT. No harness fix needed.

---

## Standing doctrine (carry-over)

**Pre-fire rates-aware gate**:
- ✓ FIRE-eligible (baseline): `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed, non-archetype).
- ✓ FIRE-eligible (§PARTIAL §A pilot): `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype AND co-located AND single-shot pilot-marked.
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom, baseline) OR `<+0` (§PARTIAL §A).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {archetype list} → REJECT (baseline). §PARTIAL §B may relax per-owner-per-node when wedge present + co-locatable striker.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.
- ⚠ UNSAFE-owner-unknown: if both `owner_handle` and `by_idx.v_acct` are null → REJECT.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

---

## Priority 1 — Standing rates-aware fire scan (with §PARTIAL extensions)

**Action ladder s185**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` + non-archetype → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` + elapsed ≥6h + non-archetype + parked_True → fire D pilot.
3. **§PARTIAL §A pilot**: any co-located candidate with `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype → fire §PARTIAL §A pilot single-shot.
4. **§PARTIAL §B pilot**: per s183 plan; currently DOWNGRADED (node 9 decay).
5. Else: Priority 2 (Phase 2 row 9 logging).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 2 row 9 (§PARTIAL persistence vs reversion)

| Session | non-archetype margin≥+10 world-wide |
|---------|---------------------------------------|
| s179    | 7 |
| s180    | 0 |
| s181    | 0 |
| s182    | 0 |
| s183    | 0 (§PARTIAL TRIGGER MET) |
| s184    | 0 (§PARTIAL STRENGTHENED) |

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 cluster size + rates distribution (sanity check; expect stable at ~12).
- world-wide non-archetype margin≥+10 + parked_True count.

**Step 2** — Decision tree:
- **IF s185 row 0 (6th consecutive)**: §PARTIAL DEEPEN. Continue armed.
- **IF s185 row ≥1**: Reversion counter starts at 1; 2 consecutive non-zero returns to baseline.
- **IF first §PARTIAL §A test target appears with rates_aware sampled ≥+0 + parked_False**: FIRE per Priority 1.

---

## Priority 3 — New unsampled v_idx watches (s184)

s184 surfaced 3 NEW unsampled co-located killable_v3 v_idxs all with margin=10, all owner-unknown:
- **v_idx=11714 node 33** — by_idx None.
- **v_idx=682 node 33** — by_idx None.
- **v_idx=1750 node 60** — by_idx None.

(v_idx=7110 also showed unsampled margin=16 but by_idx fallback confirmed vuongdung1198 archetype phantom. Watch CLOSED.)

**s185 actions**:
1. Re-read parked_v2 + parked_rates_state.by_idx for these 3 v_idxs.
2. **IF any resolves to non-archetype owner AND sampled with `parked_bool=False` AND `rates_aware_margin ≥ +0` AND elapsed ≥6h** → §PARTIAL §A pilot fire candidate (Priority 1 step 3).
3. **IF any resolves to non-archetype owner AND sampled with `parked_bool=True` AND `rates_aware_margin ≥ +10`** → baseline D-pilot fire candidate (Priority 1 step 2).
4. **IF resolves to vuongdung1198 archetype phantom** → close watch.
5. **IF still owner-unknown after sampling** → continue REJECT.

These are the **first genuine wedges** since s183 v_idx=4845 (which closed as phantom). Watching closely.

---

## Priority 4 — node 9 hot_battlegrounds — DOWNGRADED

s184: 5 kills in 3h window unchanged from s183, **no fresh kills in 43 min**. Signal decaying.

**s185 actions**:
1. Re-check hot_battlegrounds. If kills_in_window drops (window slide drops old kills) → downgrade to dropped, remove from queue.
2. If fresh kill appears (signal re-strengthens) → re-pin.

---

## Priority 5 — node 62 passive watch

s184: contracted 2→1 (1825 owner-unknown phantom only). Node had real activity 5h ago (KCI killed sa3woo). Cycling.

**s185 actions**: continue passive read; no migration trigger expected.

---

## Priority 6 — Hard limits (s185)

- **Gas budget**: 0 (read-only unless §PARTIAL §A pilot or baseline fire-eligible D-pilot emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 2 row 9 + 3 v_idx watches + node 9 + node 62 + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) AND ≥+EV justifies.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s185**:
- If §PARTIAL §A pilot FIRE successful: +5-10 min (cooldown + chain attempt).
- If §PARTIAL §A pilot FIRE REVERT: +30 min (characterize, update doctrine).
- If Phase 2 deflation rebounds (≥1 hit): +20 min, re-evaluate §PARTIAL hypothesis.
- If Phase 2 deflation stays at 0 (6th consecutive): log row 9, +25 min.
- If 0 fire-eligible across all ladders: +25 min standard defer.

**s185 wake** (this plan's pin): **+25 min from s184** (~12:50 UTC May 5, ts = 1777985400). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) Phase 2 row 9 — 6th consecutive 0-session strengthens further; non-zero hit starts reversion counter
- (c) **3 new unsampled v_idx watches (1750, 11714, 682)** — most likely path to first §PARTIAL §A pilot fire if sampling resolves non-archetype + parked_bool=False + elapsed ≥6h
- (d) Standing rates-aware fire scan
- (e) Cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s184)

1. **E009 pilot DEFER #22** — primary for s185.
2. **Amendment E Phase 1 P1-CONFIRMED s183** — ADOPTED. No reversion.
3. **Amendment E Phase 2 STRENGTHENING-CONFIRMED s184** — 5 consecutive 0-sessions. Doctrine change gated on first pilot fire.
4. **Amendment E Phase 3 LOGGED s178** — counter-response 1 refuted; reinforced.
5. **§PARTIAL §B wedge — node 9** — DECAYING. Downgrade.
6. **WATCHER SCHEMA REGRESSION** — owner_handle null. by_idx healthy. Workaround stable.
7. **node 62 cluster watch** — contracted 2→1. Cycling.
8. **node-33 v_idx=7110** — WATCH CLOSED (vuongdung1198 phantom via by_idx).
9. **node-33 v_idx=11714** — NEW s184 unsampled owner-unknown. Watch s185.
10. **node-33 v_idx=682** — NEW s184 unsampled owner-unknown. Watch s185.
11. **node-60 v_idx=1750** — NEW s184 unsampled owner-unknown. Watch s185.
12. **11224 Lethality allocation** — BLOCKED. §PARTIAL §C escalation candidate.
13. **Branch 2 persistence** — 0/3.
14. **Migration HOLD (Branch 1)** — 12 consecutive sessions; reinforced.
15. **Amendment D** — UNFIRED.
16. **Oracle staleness doctrine** (s175) — apply as needed.
17. **stop_harvest_batch ~17% revert** — defer.
18. **v_HP staleness** — defer.
19. **STRIKERS const stale** — defer.
20. **SIUUUU node-65 cluster watch** — no signal.
21. **Long-term: roster leveling wave** — under §PARTIAL §C.
22. **§PARTIAL §A pilot trigger watch** — armed; 3 new unsampled v_idxs are best near-term path.
23. **§PARTIAL §B pilot trigger watch** — node 9 decaying; downgrade.

---

## Bias for s185

Read-only continuation. §PARTIAL ARMED + STRENGTHENING. Best near-term fire-eligibility path is the 3 new unsampled co-located v_idxs (1750, 11714, 682) resolving to non-archetype owners with rates_aware sampling completing. If none resolve, defer #23.

If Phase 2 deflation persists at 0 + no §PARTIAL pilot trigger: log row 9 + +25 min defer #23.
