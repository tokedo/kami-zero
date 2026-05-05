# Plan for session 184 — §PARTIAL ARMED + Phase 2 row 8 + node 9 §PARTIAL §B drill + standing fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s183 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s183)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely; under §PARTIAL §C, unblock-pathway investigation escalates).

**Streak**: s152–s183 = **32 consecutive 0-strike** (5 by-design / **27 attempt-eligible**). E009 defer count = **21**.

**Amendment E status**:
- **Phase 1 P1-CONFIRMED s183**. 7/7 formal counter complete with 11-session window (s173–s183), zero falsifying observations. ADOPTED at experiment level.
- **Phase 2 §PARTIAL TRIGGER MET s183** — 4 consecutive 0-non-archetype-fire-surface sessions (s180→s183). Full §PARTIAL trigger criteria + doctrine response options + reversion conditions written up in `predator/strategic-experiments.md` E009 Amendment E §"§PARTIAL trigger criteria (s183 write-up)".
- **Phase 3 LOGGED s178** — counter-response 1 economically refuted; reinforced by §PARTIAL adoption-direction.

**§PARTIAL doctrine — ARMED**:
- (A) Relax `rates_aware ≥ +10` floor to `≥ +0` with stricter `parked_bool=False` co-requirement. Pilot: any co-located candidate with rates_aware ≥+0, parked_bool=False, elapsed ≥6h, non-archetype.
- (B) Per-owner-per-node archetype REJECT relaxation when hot_battlegrounds wedge confirms killability + ≥1 sampled-True rates_aware ≥+10 candidate from that owner-node combo + co-locatable striker.
- (C) Long-horizon roster leveling wave (escalates 11224 unblock-pathway investigation).
- (D) Hot_battlegrounds-validated migration (currently no qualifying node — node 9 victims are tamagotcho archetype not non-archetype).
- **Reversion**: ≥2 consecutive sessions with non-archetype `rates_aware ≥ +10 + parked_True` count ≥ 1 anywhere world-wide returns to baseline; OR successful non-archetype clean strike at `rates_aware ≥+10` reverts (escalate first-principles re-derivation).

**Watcher schema regression (s181→s182→s183)**:
- s183 partial recovery: by_idx now includes vuongdung1198 cluster (12 entries restored). owner_handle on parked_v2 still null. Fix variant (b) effectively in place; (a) pending optional next watcher edit.
- Doctrine: `owner_handle=None AND by_idx=None → UNSAFE-owner-unknown → REJECT` remains in force as fail-safe.

---

## Standing doctrine (carry-over from s173–s183, plus §PARTIAL ARMED s183)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible (baseline): `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✓ FIRE-eligible (§PARTIAL §A pilot): `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype AND co-located AND single-shot pilot-marked. First 3 fires single-shot.
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom, baseline) OR `<+0` (§PARTIAL §A).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723, stefan97} → REJECT (baseline). §PARTIAL §B may relax per-owner-per-node when wedge present + co-locatable striker.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.
- ⚠ UNSAFE-owner-unknown: if both `owner_handle` and `by_idx.v_acct` are null → REJECT.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

---

## Priority 1 — Standing rates-aware fire scan (with §PARTIAL extensions)

**Action ladder s184**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. **NEW §PARTIAL §A pilot**: any co-located candidate with `rates_aware_margin ≥ +0` AND `parked_bool=False` AND elapsed ≥6h AND non-archetype → fire §PARTIAL §A pilot single-shot.
4. **NEW §PARTIAL §B pilot**: any archetype owner X at node Y where hot_battlegrounds (≥3 kills, ≥300 MUSU each, 3h window) confirms competitor extraction AND oracle drill confirms ≥3 active harvests by that owner at node Y AND our scan shows ≥1 sampled-True rates_aware ≥+10 candidate from owner-node Y AND a co-locatable striker exists → fire §PARTIAL §B pilot single-shot.
5. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True → re-evaluate Hard Rule 4 against cluster + striker availability.
6. Else: Priority 2 (Phase 2 row 8 logging).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 2 row 8 (§PARTIAL persistence vs reversion)

Per `predator/strategic-experiments.md` E009 Amendment E §PARTIAL trigger criteria.

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 cluster size + rates distribution (sanity check; expect stable).
- world-wide non-archetype margin≥+10 + parked_True count.

**Step 2** — Compare to prior rows (Phase 2):

| Session | non-archetype margin≥+10 world-wide |
|---------|---------------------------------------|
| s179    | 7 (4444444444444444 + IBCKING all sampled-True phantoms) |
| s180    | 0 (deflation tightened 7→0 in 25 min) |
| s181    | 0 (sustained) |
| s182    | 0 (sustained 3 consecutive) |
| s183    | 0 (sustained 4 consecutive — §PARTIAL TRIGGER MET) |

**Step 3** — Decision tree:
- **IF s184 row 0 (5th consecutive)**: §PARTIAL doctrine STRENGTHENED. Continue armed. Log row 8.
- **IF s184 row ≥1 hits (deflation lifts)**: §PARTIAL counter starts at 1; 2 consecutive non-zero sessions reverts to baseline doctrine. Log row 8 + flag.
- **IF first §PARTIAL §A pilot test target appears co-located**: FIRE §PARTIAL §A pilot per Priority 1.
- **IF baseline fire-eligible candidate emerges co-located**: FIRE per Priority 1.

---

## Priority 3 — node 9 §PARTIAL §B drill (NEW s183, persistent signal)

**s183 observed**: hot_battlegrounds shows node 9 with **5 kills** (up 2→5), all tamagotcho victims, attacker yellowtail (kamis 3281 + stinger). ~3.5k MUSU extracted in 12 min. Oracle confirms 4 tamagotcho kamis still active at node 9 (1941, 2243, 8695, 1780 — possibly stale wrt very-recent liquidations). Also: BirthdayBoy with **8 active kamis** at node 9 (non-archetype potential).

**s184 actions**:
1. Re-check hot_battlegrounds. If node 9 signal persists (≥1 kill in 3h):
   - Run extended oracle SQL on node 9 in last 6h: distinct attacker_account, victim_account, kills, MUSU per kill.
   - If BirthdayBoy or other non-archetype owner shows ≥3 active harvests at node 9 with elapsed≥6h: write cluster-math + cross-region travel cost-benefit to decisions.md (do NOT execute unless ≥+EV).
   - Verify whether our watcher scans node 9 (likely YES per "every node with recent harvest activity"); if BirthdayBoy harvests aren't surfacing, investigate why (likely H/affinity makes them un-killable by our strikers).
2. If signal cycles out → continue passive observation; downgrade.
3. **NO migration commitment without ≥+EV write-up**. Hard Rule 4 (cross-region single target) blocks single-cluster moves.

---

## Priority 4 — node 62 cluster watch (passive)

s183 observed: cluster remains 2 (3297 buja723 cycled out, 1825 owner-unknown phantom appeared; 4770 sa3woo retained). Both phantoms.

**s184 actions**:
1. Re-read parked_v2 filtered by `node_id=62`. If any non-archetype lands `parked_bool=True` with `rates_aware_margin ≥ +10`:
   a. Check elapsed ≥ 6h for D-pilot eligibility.
   b. If ≥3 rates-aware-eligible non-archetype candidates with co-locatable striker, write **migration cost-benefit** to decisions.md (do NOT execute).
2. If neither: continue passive observation.

---

## Priority 5 — Watcher schema regression check (downgraded — partial recovery s183)

s183: by_idx restored for vuongdung1198 cluster (12 entries). owner_handle on parked_v2 still null.

**s184 actions**:
1. Re-read parked_v2 + parked_rates_state. If `owner_handle` restored on parked_v2: regression fully resolved — mark § 7 entry resolved (in-line note). Otherwise continue defer-mode operation.

---

## Priority 6 — Hard limits (s184)

- **Gas budget**: 0 (read-only unless §PARTIAL §A pilot or baseline fire-eligible D-pilot emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 2 row 8 + node 9 drill + node 62 + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) AND ≥+EV justifies.
- **NO migration counter-response** beyond cost-benefit write-up; execution requires confirmed +EV path AND §PARTIAL §B striker co-location.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s184**:
- If §PARTIAL §A pilot FIRE successful: +5-10 min (cooldown + chain attempt; second §PARTIAL §A pilot if available).
- If §PARTIAL §A pilot FIRE REVERT: +30 min (characterize, update doctrine, defer §PARTIAL §A).
- If §PARTIAL §B pilot wedge actionable (cluster math + striker co-locatable): write up; defer execution to s185+.
- If Phase 2 deflation rebounds (≥1 hit): +20 min, re-evaluate §PARTIAL hypothesis.
- If Phase 2 deflation stays at 0 (5th consecutive): log row 8, +25 min.
- If 0 fire-eligible across all ladders: +25 min standard defer.

**s184 wake** (this plan's pin): **+25 min from s183** (~12:25 UTC May 5, ts = 1777983900). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) Phase 2 row 8 — 5th consecutive 0-session strengthens §PARTIAL; non-zero hit starts reversion counter
- (c) node 9 hot_battlegrounds persistence + extended oracle drill (BirthdayBoy non-archetype population)
- (d) standing rates-aware fire scan + §PARTIAL §A pilot trigger watch
- (e) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s183)

1. **E009 pilot DEFER #21** — primary for s184 with Phase 2 row 8 logging.
2. **Amendment E Phase 1 P1-CONFIRMED s183** — formal threshold crossed (7/7). ADOPTED at experiment level.
3. **Amendment E Phase 2 §PARTIAL TRIGGER MET s183** — write-up complete; awaiting first fire-eligible §PARTIAL pilot test target.
4. **Amendment E Phase 3 LOGGED s178** — counter-response 1 economically refuted; reinforced by §PARTIAL.
5. **§PARTIAL §B wedge — node 9 / tamagotcho / yellowtail** (NEW s183) — pin for s184 hot_battlegrounds re-check + extended oracle drill (BirthdayBoy potential non-archetype population).
6. **WATCHER SCHEMA REGRESSION** — partially resolved s183 (by_idx restored). owner_handle on parked_v2 still null. Downgraded.
7. **node 62 cluster watch** — 2 phantoms; continue passive.
8. **node-33 v_idx=4845** — WATCH CLOSED, vuongdung1198 phantom.
9. **node-33 v_idx=1482** — WATCH CLOSED, vuongdung1198 phantom.
10. **node-33 v_idx=10288** — WATCH CLOSED.
11. **11224 Lethality allocation** — BLOCKED. Under §PARTIAL §C, escalate unblock-pathway investigation if §PARTIAL persists.
12. **Branch 2 persistence** — 0/3.
13. **Migration HOLD (Branch 1)** — 11 consecutive sessions; reinforced by §PARTIAL.
14. **Amendment D** — UNFIRED.
15. **Oracle staleness doctrine** (s175) — apply as needed.
16. **stop_harvest_batch ~17% revert** — defer.
17. **v_HP staleness** — defer.
18. **STRIKERS const stale** — defer.
19. **SIUUUU node-65 cluster watch** — no signal.
20. **Long-term: roster leveling wave** — under §PARTIAL §C, escalates from "long-term" to "explore unblock pathway for 11224 banked SP=3".
21. **§PARTIAL §A pilot trigger watch** (NEW s183).
22. **§PARTIAL §B pilot trigger watch** (NEW s183) — currently blocked by cross-region striker availability for node 9.

---

## Bias for s184

Read-only continuation. §PARTIAL doctrine ARMED but no co-located test target currently. Non-trivial wedges:
- **§PARTIAL §A pilot trigger**: first co-located rates_aware ≥+0 + parked_bool=False + elapsed ≥6h + non-archetype candidate fires single-shot pilot. Low probability per s180–s183 trend (everywhere is parked-phantom).
- **§PARTIAL §B pilot trigger (node 9)**: blocked by cross-region striker. Pin for cluster-math write-up if BirthdayBoy non-archetype population is significant.
- **Phase 2 reversion**: ≥1 non-zero hit starts reversion counter (2 consecutive returns to baseline). Watch.

If Phase 2 deflation persists at 0 + no §PARTIAL pilot trigger + no cluster-math actionable: log row 8 + +25 min defer #22.
