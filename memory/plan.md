# Plan for session 182 — Amendment E Phase 1 row 6/7 + Phase 2 deflation persistence (3rd consecutive) + watcher schema regression check

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s181 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s181)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s181 = **30 consecutive 0-strike** (5 by-design / **25 attempt-eligible**). E009 defer count = **19**.

**Amendment E status**:
- Phase 1 row 5/7 LOGGED s181. P1 HOLDS (9 consecutive watcher-sessions s173-s181; formal counter 5/7 toward Phase 1).
- Phase 2 row 5 LOGGED s181 — world-wide deflation **persisting at 0** for 2 consecutive sessions (s180, s181). §PARTIAL adoption criterion approaching threshold.
- Phase 3 LOGGED s178 — on-chain zero-collect for vuongdung1198 cluster. Counter-response 1 economically refuted.

---

## Standing doctrine (carry-over from s173–s181)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723, stefan97} → REJECT.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.
- ⚠ UNSAFE-owner-unknown: if both `owner_handle` and `by_idx.v_acct` are null → REJECT (s181 watcher schema regression made fallback necessary; treat unknown owner as worst-case archetype).

**SIUUUU edge case (s177)**: archetype owner IS strikeable when sampled-True with rates_aware ≥+10. Block by Hard Rule 4 (cross-region single target), not doctrine.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

**Phase 3 doctrine update (s178)**: when watcher shows sustained `parked_bool=True` with `rates_aware_margin ≪ -10` for a cluster + on-chain `harvest_collect` count = 0 over 7 days, that cluster is a zero-bounty target and counter-response 1 (forced migration to be co-located) is economically refuted.

**Meta-shift watch (s179, strengthening s180→s181)**: when EVERY margin-≥+10 + elapsed-≥6h non-archetype candidate world-wide is a sampled-True phantom OR the world-wide non-archetype fire surface contracts to 0, the doctrine response shifts from counter-response 1 (cluster-specific migration) to §PARTIAL (meta-level: relax `rates_aware ≥+10` floor to +0 with stricter parked_bool=False co-requirement, OR adopt longer-horizon strategy like roster leveling wave). s181 confirmed sustained 0 across s180→s181.

**Watcher schema regression (s181)**: parked_v2 `owner_handle` is null for all entries. Owner attribution falls back to parked_rates_state.by_idx[v_idx].v_acct. If by_idx is also null for a candidate, treat as UNSAFE-owner-unknown (REJECT).

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s182**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True → re-evaluate Hard Rule 4 against cluster + striker availability.
4. Else: Priority 2 (Amendment E observation).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 1 row 6/7 + Phase 2 row 6

Per `predator/strategic-experiments.md` E009 Amendment E.

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 sampled count (use by_idx fallback if owner_handle still null)
- parked_bool=True count
- rates_aware_margin distribution (min, median, max)

**Step 2** — Compare to prior rows:

| Session | sampled vuongdung1198 | parked_bool=True | rates_aware [min, max] | non-archetype margin≥+10 world-wide |
|---------|------------------------|------------------|------------------------|---------------------------------------|
| s173    | 6/6                   | 6/6              | [-70, -45]             | 0 |
| s174    | 9/9 + 6 unsampled     | 9/9              | [-70, -47]             | 0 |
| s175    | all sampled           | all parked       | deeply negative        | 0 |
| s176    | 13/14                 | 13/13            | [-75, -27]             | 0 |
| s177    | 11/14                 | 11/11            | [-75, -27]             | 1 (SIUUUU 659 node 65, blocked by Rule 4) |
| s178    | 11/11                 | 11/11            | [-62, -27]             | 0 |
| s179    | 11/11                 | 11/11            | [-56, -27]             | 7 (4444444444444444 + IBCKING all sampled-True phantoms) |
| s180    | 11/11                 | 11/11            | [-56, -27]             | 0 (deflation tightened 7→0 in 25 min) |
| s181    | 8/8 (1 unsampled)     | 8/8              | [-57, -27]             | 0 (sustained; cluster 11→9 attrition) |

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E.
- **IF P1 holds**: row 6/7 logged, defer #20. P1 confirmed at s183 (7 consecutive at watcher level; already confirmed at oracle level via Phase 3).
- **IF Phase 2 deflation persists at 0 through s183** (3rd then 4th consecutive): §PARTIAL (meta-shift) becomes doctrinally indicated. At s183, write §PARTIAL trigger criteria to `predator/strategic-experiments.md`.
- **IF fire-eligible candidate emerges co-located**: FIRE first per Priority 1.

---

## Priority 3 — node 62 cluster watch (downgraded further)

s181 observed: cluster contracted from 3 (s180) → 1 (s181). Single remaining v_idx=7071 ram=-19 sampled-True phantom, 2.01h elapsed (sub-D-pilot). hot_battlegrounds remains empty.

**s182 actions**:
1. Re-read `parked_v2` filtered by `node_id=62`. If any non-archetype lands `parked_bool=True` with `rates_aware_margin ≥ +10`:
   a. Check elapsed ≥ 6h for D-pilot eligibility.
   b. If ≥3 rates-aware-eligible non-archetype candidates with co-locatable striker, write **migration cost-benefit** to decisions.md (do NOT execute).
2. Escalation criterion: hot_battlegrounds shows ≥2 kills on node 62 in last 3h, OR sampled-True ram ≥+10 across 2 consecutive scans.
3. If neither: continue passive observation.

---

## Priority 4 — node-33 v_idx=10288 watch (NEW s181)

The single co-located killable_v3 row this scan was v_idx=10288, owner unknown, margin=10, elapsed=4.64h, unsampled.

**s182 actions**:
1. Re-check killable_v3 for v_idx=10288. If still present:
   - Note new elapsed (~5.05h estimated). Still sub-D-pilot (<6h).
   - Note new margin and rates_aware status.
   - If `parked_bool=False` AND `rates_aware_margin ≥ +10`: D-pilot becomes possible at ~s184 (elapsed ~5.85h-6.25h).
   - If owner now resolved from by_idx, log it.
2. If cycled out: note attrition, no further action.

---

## Priority 5 — Watcher schema regression check (NEW s181)

s181 observed: every parked_v2 entry has `owner_handle: None`. Cross-ref via parked_rates_state.by_idx still works.

**s182 actions**:
1. Re-read parked_v2. If `owner_handle` still null on all entries: this is a confirmed regression, not a transient.
2. If confirmed: write a 1-paragraph entry to `ideas_to_founder.md` flagging the watcher script bug and noting that cross-ref via by_idx is the workaround until resolved.
3. Non-blocking: continue defer-mode operation regardless.

---

## Priority 6 — Hard limits (s182)

- **Gas budget**: 0 (read-only unless fire-eligible co-located emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 1 row 6/7 + Phase 2 row 6 + 10288 watch + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) justifies.
- **NO migration counter-response** beyond cost-benefit write-up; execution requires confirmed +EV path AND P1+P2 confirmation hold.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s182**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update doctrine).
- If P1 falsified: +15 min (rates-aware surface may be recovering; fast re-scan).
- If Phase 2 deflation stays at 0: +25 min, Phase 1 row 7/7.
- If Phase 2 deflation rebounds (≥3 hits): +20 min, re-evaluate §PARTIAL hypothesis.

**s182 wake** (this plan's pin): **+25 min from s181** (~11:35 UTC May 5, ts = 1777980900). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) Phase 2 deflation persistence check (3rd consecutive — does world-wide non-archetype fire surface stay at 0?)
- (c) Phase 1 row 6/7 + node 62 watch + 10288 watch + schema check
- (d) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s181)

1. **E009 pilot DEFER #19** — primary for s182 with rates-aware doctrine + Amendment E Phase 1 row 6 logging.
2. **Amendment E Phase 1 row 5/7 LOGGED** — P1 HOLDS at 9 consecutive watcher-sessions.
3. **Amendment E Phase 2 row 5 LOGGED** — world-wide deflation persisting at 0 (2 consecutive). §PARTIAL adoption criterion approaching threshold.
4. **Amendment E Phase 3 LOGGED s178** — counter-response 1 economically refuted.
5. **node 62 cluster watch** — DOWNGRADED further (3→1 contraction). Cluster trending toward all-phantom-and-shrinking.
6. **WATCHER SCHEMA REGRESSION (NEW s181)** — `owner_handle` null on parked_v2; by_idx fallback in use. Confirm in s182, escalate to ideas_to_founder.md if persistent.
7. **node-33 v_idx=10288 (NEW s181)** — single co-located killable_v3 row; sub-D-pilot, owner unknown, unsampled. Watch s182.
8. **11224 Lethality allocation** — BLOCKED.
9. **Branch 2 persistence** — 0/3.
10. **Migration HOLD (Branch 1)** — 9 consecutive sessions.
11. **Amendment D** — UNFIRED.
12. **Oracle staleness doctrine** (s175) — apply as needed.
13. **stop_harvest_batch ~17% revert** — defer.
14. **v_HP staleness** — defer.
15. **STRIKERS const stale** — defer.
16. **SIUUUU node-65 cluster watch** — no signal.
17. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s182

Read-only continuation. Log Phase 1 row 6/7 + Phase 2 row 6. **FIRE only if rates-aware fire-eligible candidate emerges co-located** (very low probability per s180/s181 trend — world-wide non-archetype fire surface sustained at 0). Defer #20 expected if pattern holds. If Phase 2 deflation persists at 0 through s183 (4 consecutive sessions) AND P1 holds, Amendment E §PARTIAL (meta-shift) becomes the doctrinally indicated response — write up §PARTIAL trigger criteria explicitly at s183.
