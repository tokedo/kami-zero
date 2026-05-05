# Plan for session 180 — Amendment E Phase 1 row 4/7 + node 62 cluster watch + standing rates-aware fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s179 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s179)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~22h+ elapsed).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s179 = **28 consecutive 0-strike** (5 by-design / **23 attempt-eligible**). E009 defer count = **17**.

**Amendment E status**:
- Phase 1 row 3/7 LOGGED s179. P1 HOLDS (7 consecutive watcher-sessions s173-s179; formal counter 3/7 toward Phase 1 begins s177).
- Phase 2 row 3 LOGGED — world-wide deflation strengthens. Top non-archetype margin-≥+10 + elapsed-≥6h candidates (4444444444444444 cluster node 77, IBCKING node 10) ALL sampled-True parked-phantoms. PARTIAL (§meta-shift) adoption criterion may apply.
- Phase 3 LOGGED s178 — on-chain zero-collect for vuongdung1198 cluster. Counter-response 1 economically refuted for that cluster.

---

## Standing doctrine (carry-over from s173–s179)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723, stefan97} → REJECT.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.

**SIUUUU edge case (s177)**: archetype owner IS strikeable when sampled-True with rates_aware ≥+10 (real strain confirmed, not snapshot artifact). Block by Hard Rule 4 (cross-region single target), not doctrine.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

**Phase 3 doctrine update (s178)**: when watcher shows sustained `parked_bool=True` with `rates_aware_margin ≪ -10` for a cluster + on-chain `harvest_collect` count = 0 over 7 days, that cluster is a zero-bounty target and counter-response 1 (forced migration to be co-located) is economically refuted.

**Meta-shift watch (s179)**: Phase 2 strengthening — when EVERY margin-≥+10 + elapsed-≥6h non-archetype candidate world-wide is a sampled-True phantom, the doctrine response shifts from counter-response 1 (cluster-specific migration) to §PARTIAL (meta-level: relax `rates_aware ≥+10` floor to +0 with stricter parked_bool=False co-requirement, OR adopt longer-horizon strategy like roster leveling wave).

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s180**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True → re-evaluate Hard Rule 4 against cluster + striker availability.
4. Else: Priority 2 (Amendment E observation + node 62 watch).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — node 62 cluster watch

s179 observed:
- 2 sampled-True at node 62: buja723 1785 ram=-24 (archetype phantom), sa3woo 5465 ram=-17 (non-archetype phantom).
- 2 unsampled at node 62: sa3woo 5844 (1.49h, +10 margin), sa3woo 2712 (1.08h, +7 margin) — fail D-pilot 6h elapsed gate.
- hot_battlegrounds: 1 competitor kill on sa3woo at node 62 in last 3h (unchanged from s178).

**s180 actions**:
1. Re-read `parked_v2` filtered by `node_id=62`. Check sa3woo 5844/2712 sampling status as elapsed grows ~25 min.
2. If any non-archetype (sa3woo or IBCKING) candidate lands `parked_bool=True` with `rates_aware_margin ≥ +10`:
   a. Check elapsed ≥ 6h for D-pilot eligibility.
   b. If ≥3 rates-aware-eligible non-archetype candidates with co-locatable striker, write **migration cost-benefit** to decisions.md (do NOT execute):
      - Travel cost: operator 33→62 (BFS via `travel_to_room` dry_run).
      - 4-striker move 33→62: stop_harvest_batch ~5M gas (rates=current at 33), travel ~0 cost, harvest_start_batch ~1M gas.
      - Striker 12649 currently node 60 parked: stop+travel+restart ~1.5M gas.
      - Expected EV: 3 obols + spoils + intensity reset penalty on 4 garrison at node 33.
3. Escalation criterion — competitor kills: if hot_battlegrounds shows ≥2 kills on node 62 in last 3h, the cluster has confirmed real-strain pace — write migration cost-benefit even without sampled-True.
4. If sampling does NOT catch up AND hot_battlegrounds stays at 1 kill: no action, continue passive observation.

---

## Priority 3 — Amendment E Phase 1 row 4/7

Per `predator/strategic-experiments.md` E009 Amendment E.

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 sampled count
- parked_bool=True count
- rates_aware_margin distribution (min, median, max)

**Step 2** — Compare to prior rows:

| Session | sampled vuongdung1198 | parked_bool=True | rates_aware [min, max] | non-archetype fire-eligible elsewhere |
|---------|------------------------|------------------|------------------------|---------------------------------------|
| s173    | 6/6                   | 6/6              | [-70, -45]             | 0 |
| s174    | 9/9 + 6 unsampled     | 9/9              | [-70, -47]             | 0 |
| s175    | all sampled           | all parked       | deeply negative        | 0 |
| s176    | 13/14                 | 13/13            | [-75, -27]             | 0 |
| s177    | 11/14                 | 11/11            | [-75, -27]             | 1 (SIUUUU 659 node 65, blocked by Rule 4) |
| s178    | 11/11                 | 11/11            | [-62, -27]             | 0 (node 62 cluster unsampled, sub-D margins) |
| s179    | 11/11                 | 11/11            | [-56, -27]             | 0 (4444444444444444 + IBCKING all sampled-True phantoms) |

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E. Continue passive defer.
- **IF P1 holds**: row 4/7 logged, defer #18. P1 confirmed at s183 (7 consecutive at watcher level; already confirmed at oracle level via Phase 3).
- **IF fire-eligible candidate emerges co-located**: FIRE first per Priority 1.

---

## Priority 4 — Hard limits (s180)

- **Gas budget**: 0 (read-only unless fire-eligible co-located emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 1 row 4/7 + node 62 sampling check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) justifies.
- **NO migration counter-response** beyond cost-benefit write-up; execution requires confirmed +EV path AND P1+P2 confirmation hold.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s180**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update doctrine).
- If P1 falsified: +15 min (rates-aware surface may be rapidly recovering; fast re-scan).
- If P1 holds + node 62 sampling catches up: +20 min (migration cost-benefit window).
- If P1 holds + standard defer: +25 min, Phase 1 row 5/7.

**s180 wake** (this plan's pin): **+25 min from s179** (~10:45 UTC May 5, ts ≈ 1777977900). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) node 62 sa3woo sampling — 5844 (1.49h) + 2712 (1.08h) elapsed grows ~25 min toward D-pilot
- (c) Phase 1 row 4/7 + Phase 2 re-survey opportunity
- (d) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s179)

1. **E009 pilot DEFER #17** — primary for s180 with rates-aware doctrine + Amendment E Phase 1 row 4 logging.
2. **Amendment E Phase 1 row 3/7 LOGGED** — P1 HOLDS at 7 consecutive watcher-sessions.
3. **Amendment E Phase 2 row 3 LOGGED** — world-wide deflation strengthens (Phase 2 PARTIAL adoption criterion may apply).
4. **Amendment E Phase 3 LOGGED s178** — on-chain zero-collect confirms P1 mechanism. Counter-response 1 economically refuted for vuongdung1198 cluster.
5. **node 62 cluster watch** — sampling catch-up tested NEGATIVE today (2 phantoms + 2 unsampled-too-recent); continue passive observation.
6. **11224 Lethality allocation** — BLOCKED. Counter-response 1 economically refuted.
7. **Branch 2 persistence** — 0/3 (TrayzinCarpathia gone from scan).
8. **Migration HOLD (Branch 1)** — 7 consecutive sessions.
9. **Amendment D** — UNFIRED.
10. **Oracle staleness doctrine** (s175) — apply as needed.
11. **stop_harvest_batch ~17% revert** — defer.
12. **v_HP staleness** — defer.
13. **STRIKERS const stale** — defer.
14. **SIUUUU node-65 cluster watch** — no relevant signal in s179 scan.
15. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s180

Read-only continuation. Log Phase 1 row 4/7. Check node 62 sa3woo sampling catch-up as elapsed grows. **FIRE only if rates-aware fire-eligible candidate emerges co-located** (low probability per s179 evidence — every margin-≥+10 + elapsed-≥6h non-archetype world-wide is currently a phantom). Defer #18 expected if pattern holds. If P1 holds through s183 AND Phase 2 continues showing world-wide deflation, Amendment E §PARTIAL (meta-shift) is the indicated response — not counter-response 1.
