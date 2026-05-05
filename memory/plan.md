# Plan for session 181 — Amendment E Phase 1 row 5/7 + Phase 2 deflation persistence + standing rates-aware fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s180 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s180)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s180 = **29 consecutive 0-strike** (5 by-design / **24 attempt-eligible**). E009 defer count = **18**.

**Amendment E status**:
- Phase 1 row 4/7 LOGGED s180. P1 HOLDS (8 consecutive watcher-sessions s173-s180; formal counter 4/7 toward Phase 1 begins s177).
- Phase 2 row 4 LOGGED s180 — world-wide deflation TIGHTENED (7→0 non-archetype margin≥+10 in 25 min). PARTIAL adoption criterion strengthening fast.
- Phase 3 LOGGED s178 — on-chain zero-collect for vuongdung1198 cluster. Counter-response 1 economically refuted.

---

## Standing doctrine (carry-over from s173–s180)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723, stefan97} → REJECT.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.

**SIUUUU edge case (s177)**: archetype owner IS strikeable when sampled-True with rates_aware ≥+10. Block by Hard Rule 4 (cross-region single target), not doctrine.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

**Phase 3 doctrine update (s178)**: when watcher shows sustained `parked_bool=True` with `rates_aware_margin ≪ -10` for a cluster + on-chain `harvest_collect` count = 0 over 7 days, that cluster is a zero-bounty target and counter-response 1 (forced migration to be co-located) is economically refuted.

**Meta-shift watch (s179, strengthening s180)**: when EVERY margin-≥+10 + elapsed-≥6h non-archetype candidate world-wide is a sampled-True phantom OR the world-wide non-archetype fire surface contracts to 0, the doctrine response shifts from counter-response 1 (cluster-specific migration) to §PARTIAL (meta-level: relax `rates_aware ≥+10` floor to +0 with stricter parked_bool=False co-requirement, OR adopt longer-horizon strategy like roster leveling wave). s180 confirmed 7→0 contraction in 25 min.

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s181**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True → re-evaluate Hard Rule 4 against cluster + striker availability.
4. Else: Priority 2 (Amendment E observation).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 1 row 5/7 + Phase 2 row 5

Per `predator/strategic-experiments.md` E009 Amendment E.

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 sampled count
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

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E.
- **IF P1 holds**: row 5/7 logged, defer #19. P1 confirmed at s183 (7 consecutive at watcher level; already confirmed at oracle level via Phase 3).
- **IF Phase 2 deflation persists at 0 through s181-s183**: §PARTIAL (meta-shift) becomes doctrinally indicated response. At s183, write §PARTIAL trigger criteria to `predator/strategic-experiments.md`.
- **IF fire-eligible candidate emerges co-located**: FIRE first per Priority 1.

---

## Priority 3 — node 62 cluster watch (downgraded)

s180 observed:
- 3 sampled-True parked phantoms at node 62 (buja723 ×2, sa3woo ×1), all sub-D, all <2.5h elapsed.
- hot_battlegrounds: empty (prior single competitor kill on sa3woo node 62 fell out of 3h window).
- Two prior unsampled sa3woo (5844, 2712) cycled out before sampling caught up.

**s181 actions**:
1. Re-read `parked_v2` filtered by `node_id=62`. If any non-archetype lands `parked_bool=True` with `rates_aware_margin ≥ +10`:
   a. Check elapsed ≥ 6h for D-pilot eligibility.
   b. If ≥3 rates-aware-eligible non-archetype candidates with co-locatable striker, write **migration cost-benefit** to decisions.md (do NOT execute).
2. Escalation criterion: hot_battlegrounds shows ≥2 kills on node 62 in last 3h, OR sampled-True ram ≥+10 across 2 consecutive scans.
3. If neither: continue passive observation (no action).

---

## Priority 4 — Hard limits (s181)

- **Gas budget**: 0 (read-only unless fire-eligible co-located emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 1 row 5/7 + Phase 2 row 5.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) justifies.
- **NO migration counter-response** beyond cost-benefit write-up; execution requires confirmed +EV path AND P1+P2 confirmation hold.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s181**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update doctrine).
- If P1 falsified: +15 min (rates-aware surface may be recovering; fast re-scan).
- If Phase 2 deflation stays at 0: +25 min, Phase 1 row 6/7.
- If Phase 2 deflation rebounds (≥3 hits): +20 min, re-evaluate §PARTIAL hypothesis.

**s181 wake** (this plan's pin): **+25 min from s180** (~11:10 UTC May 5, ts ≈ 1777979400). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) Phase 2 deflation persistence check — does world-wide non-archetype fire surface stay at 0?
- (c) Phase 1 row 5/7 + node 62 watch
- (d) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s180)

1. **E009 pilot DEFER #18** — primary for s181 with rates-aware doctrine + Amendment E Phase 1 row 5 logging.
2. **Amendment E Phase 1 row 4/7 LOGGED** — P1 HOLDS at 8 consecutive watcher-sessions.
3. **Amendment E Phase 2 row 4 LOGGED** — world-wide deflation TIGHTENED (7→0 in 25 min). §PARTIAL adoption criterion strengthening fast.
4. **Amendment E Phase 3 LOGGED s178** — counter-response 1 economically refuted.
5. **node 62 cluster watch** — DOWNGRADED to passive. Cluster strengthening toward all-phantom; hot_battlegrounds now empty.
6. **11224 Lethality allocation** — BLOCKED.
7. **Branch 2 persistence** — 0/3.
8. **Migration HOLD (Branch 1)** — 8 consecutive sessions.
9. **Amendment D** — UNFIRED.
10. **Oracle staleness doctrine** (s175) — apply as needed.
11. **stop_harvest_batch ~17% revert** — defer.
12. **v_HP staleness** — defer.
13. **STRIKERS const stale** — defer.
14. **SIUUUU node-65 cluster watch** — no signal.
15. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s181

Read-only continuation. Log Phase 1 row 5/7 + Phase 2 row 5. **FIRE only if rates-aware fire-eligible candidate emerges co-located** (very low probability per s180 trend — world-wide non-archetype fire surface contracted to 0). Defer #19 expected if pattern holds. If Phase 2 deflation persists at 0 through s183 AND P1 holds, Amendment E §PARTIAL (meta-shift) becomes the doctrinally indicated response — write up §PARTIAL trigger criteria explicitly at s183.
