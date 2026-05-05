# Plan for session 183 — Amendment E Phase 1 row 7/7 (formal threshold crossing) + Phase 2 §PARTIAL write-up trigger + 4845 watch + node 9 drill

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176–s182 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176–s182)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~25h+ extrapolated).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s182 = **31 consecutive 0-strike** (5 by-design / **26 attempt-eligible**). E009 defer count = **20**.

**Amendment E status**:
- **Phase 1 row 6/7 LOGGED s182**. P1 HOLDS (10 consecutive watcher-sessions s173-s182; formal counter 6/7 toward Phase 1). **s183 is row 7/7 — formal threshold crossing if P1 holds.**
- **Phase 2 row 6 LOGGED s182** — world-wide deflation **persisting at 0 for 3 consecutive sessions** (s180, s181, s182). §PARTIAL adoption criterion at threshold-1; **4th consecutive 0-session at s183 triggers explicit §PARTIAL trigger criteria write-up**.
- Phase 3 LOGGED s178 — on-chain zero-collect for vuongdung1198 cluster. Counter-response 1 economically refuted.

**Watcher schema regression (s181→s182, deepened)**:
- s181: `owner_handle` null on parked_v2; by_idx fallback worked.
- s182: `owner_handle` null on all parked_v2 entries; **by_idx now also missing the entire vuongdung1198 cluster on node 33** (only 53 entries, focused on killable_v3 superset). Both attribution chains broken for node-33 cluster.
- Workaround: historical v_idx persistence (s173→s182) confirms cluster identity.
- Doctrine: `owner_handle=None AND by_idx=None → UNSAFE-owner-unknown → REJECT` (fail-safe for fire decisions).
- Escalated to `ideas_to_founder.md § 7` (s182).

---

## Standing doctrine (carry-over from s173–s182)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723, stefan97} → REJECT.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean AND elapsed ≥6h AND kill margin meets D-pilot.
- ⚠ UNSAFE-owner-unknown: if both `owner_handle` and `by_idx.v_acct` are null → REJECT.

**SIUUUU edge case (s177)**: archetype owner IS strikeable when sampled-True with rates_aware ≥+10. Block by Hard Rule 4 (cross-region single target), not doctrine.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

**Phase 3 doctrine update (s178)**: when watcher shows sustained `parked_bool=True` with `rates_aware_margin ≪ -10` for a cluster + on-chain `harvest_collect` count = 0 over 7 days, that cluster is a zero-bounty target and counter-response 1 (forced migration) is economically refuted.

**Meta-shift watch (s179, strengthening s180→s181→s182)**: when EVERY margin-≥+10 + elapsed-≥6h non-archetype candidate world-wide is a sampled-True phantom OR the world-wide non-archetype fire surface contracts to 0, the doctrine response shifts from counter-response 1 to §PARTIAL (relax `rates_aware ≥+10` floor to +0 with stricter parked_bool=False co-requirement, OR adopt longer-horizon strategy like roster leveling wave). s182 confirmed sustained 0 across s180→s181→s182 (3 consecutive).

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s183**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True → re-evaluate Hard Rule 4 against cluster + striker availability.
4. Else: Priority 2 (Amendment E observation).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 1 row 7/7 + Phase 2 row 7 (§PARTIAL trigger candidate)

Per `predator/strategic-experiments.md` E009 Amendment E.

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to decisions.md:
- node-33 vuongdung1198 historical-attribution count (use v_idx persistence if owner_handle + by_idx still null)
- parked_bool=True count
- rates_aware_margin distribution (min, median, max)
- world-wide non-archetype margin≥+10 + parked_True count

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
| s182    | 10/10 (historical)    | 10/10            | [-57, -27]             | 0 (sustained 3 consecutive; cluster 9→10) |

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E.
- **IF P1 holds (row 7/7 LOGGED)**: **formal threshold crossing**. P1 confirmed at watcher level. Update strategic-experiments.md to mark Amendment E Phase 1 as P1-CONFIRMED.
- **IF Phase 2 deflation persists at 0 (4th consecutive)**: **§PARTIAL trigger criteria write-up REQUIRED** in `predator/strategic-experiments.md`. Specify: (a) trigger conditions (e.g., 4+ consecutive 0-non-archetype-fire-surface sessions), (b) doctrine change (relax `rates_aware ≥+10` floor to +0 with stricter parked_bool=False co-requirement, OR adopt long-horizon roster leveling wave), (c) reversion conditions (e.g., 2 consecutive non-zero non-archetype fire-surface sessions reverts to baseline doctrine).
- **IF fire-eligible candidate emerges co-located**: FIRE first per Priority 1.

---

## Priority 3 — node-33 v_idx=4845 watch (NEW s182)

**s182 observed**: NEW v_idx in killable_v3, co-located node 33, margin=10, elapsed=6.42h, parked_bool=None (unsampled), owner_handle=None, by_idx attribution missing. First co-located candidate in 31+ sessions to pass BOTH the elapsed≥6h AND margin≥+10 gates.

**s183 actions**:
1. Re-check killable_v3 + parked_v2 for v_idx=4845. Possible outcomes:
   - **Owner attribution restored** + non-archetype + sampled-True with ram≥+10 → **D-pilot candidate**: pre-fire LIVE recompute, fire if margin holds.
   - Owner attribution restored + archetype → REJECT.
   - Owner attribution restored + non-archetype + sampled-True with ram<+10 → REJECT (parked phantom).
   - Owner attribution still missing → continue REJECT (UNSAFE-owner-unknown).
   - Cycled out → log attrition; no further action.
2. If FIRE: standard pre-strike protocol (slim-verify striker, kill_threshold recompute, single-shot pilot).

---

## Priority 4 — node 9 hot_battlegrounds drill (NEW s182)

**s182 observed**: hot_battlegrounds shows node 9 with 2 kills in 3h window, sample victim tamagotcho (archetype). Another predator is finding fire-eligible targets there. Implication: either competitor predators are violating our REJECT-archetype rule (irrational), OR they have direct evidence (rates-sampled fresh data, on-chain confirmation) of harvestable archetype/non-archetype targets we're not seeing in our scan.

**s183 actions**:
1. Re-check hot_battlegrounds. If node 9 signal persists (≥1 kill in 3h):
   - Run oracle SQL on node 9 victims+attackers last 6h to identify the non-archetype population pattern.
   - Cross-reference with our parked_v2/killable_v3 to see why our watcher isn't surfacing fire-eligible candidates there.
   - If a non-archetype harvest population exists at node 9 that our scan is missing → patch the watcher (or note ideas_to_founder.md ask).
2. If signal cycles out → no action.

---

## Priority 5 — node 62 cluster watch (passive)

s182 observed: cluster expanded 1→2 (3297 buja723 archetype phantom ram=-48, 4770 sa3woo phantom ram=-22). Both sampled-True phantoms. hot_battlegrounds remains empty for node 62.

**s183 actions**:
1. Re-read parked_v2 filtered by `node_id=62`. If any non-archetype lands `parked_bool=True` with `rates_aware_margin ≥ +10`:
   a. Check elapsed ≥ 6h for D-pilot eligibility.
   b. If ≥3 rates-aware-eligible non-archetype candidates with co-locatable striker, write **migration cost-benefit** to decisions.md (do NOT execute).
2. Escalation criterion: hot_battlegrounds shows ≥2 kills on node 62 in last 3h, OR sampled-True ram ≥+10 across 2 consecutive scans.
3. If neither: continue passive observation.

---

## Priority 6 — Watcher schema regression check (continuing)

s181→s182: confirmed across 2 sessions; deepened in s182 (by_idx loss for node-33 cluster). Escalated to `ideas_to_founder.md § 7`.

**s183 actions**:
1. Re-read parked_v2 + parked_rates_state. If `owner_handle` restored on parked_v2 OR by_idx now includes the vuongdung1198 cluster: the regression was transient — mark § 7 entry resolved (in-line note).
2. If still broken: continue defer-mode operation; § 7 entry remains pending founder review.

---

## Priority 7 — Hard limits (s183)

- **Gas budget**: 0 (read-only unless 4845 resolves to fire-eligible D-pilot).
- **Tx budget**: 0 unless Priority 1/3 fires.
- **Time budget**: 10-15 min — fire scan + Phase 1 row 7/7 + Phase 2 row 7 (§PARTIAL write-up if 4th consecutive) + 4845 watch + node 9 drill + schema check.
- **NO operator travel** unless cluster math (≥3 rates-aware-eligible non-archetype candidates with co-located striker capability) justifies.
- **NO migration counter-response** beyond cost-benefit write-up; execution requires confirmed +EV path AND P1+P2 confirmation hold.

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s183**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update doctrine).
- If P1 falsified at row 7/7: +15 min (fast re-scan).
- If Phase 2 deflation rebounds (≥3 hits): +20 min, re-evaluate §PARTIAL hypothesis.
- If Phase 2 deflation stays at 0 (4th consecutive): write up §PARTIAL trigger criteria, +25 min.
- If 4845 fires successfully: +5 min for cooldown chain.

**s183 wake** (this plan's pin): **+25 min from s182** (~12:00 UTC May 5, ts = 1777982400). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) **Phase 1 row 7/7 = formal threshold crossing** if P1 holds
- (c) **Phase 2 row 7 = §PARTIAL trigger criteria write-up** if 4th consecutive 0-session
- (d) **node-33 v_idx=4845 watch** (first genuine on-the-fence co-located candidate in 31+ sessions)
- (e) **node 9 hot_battlegrounds drill** if signal persists
- (f) owner_handle regression check
- (g) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s182)

1. **E009 pilot DEFER #20** — primary for s183 with Amendment E Phase 1 row 7/7 logging.
2. **Amendment E Phase 1 row 6/7 LOGGED** — P1 HOLDS at 10 consecutive watcher-sessions. **s183 = formal threshold crossing**.
3. **Amendment E Phase 2 row 6 LOGGED** — world-wide deflation persisting at 0 (3 consecutive). §PARTIAL adoption criterion at threshold-1; **s183 4th-consecutive triggers explicit §PARTIAL write-up**.
4. **Amendment E Phase 3 LOGGED s178** — counter-response 1 economically refuted.
5. **WATCHER SCHEMA REGRESSION** (s181→s182, deepened) — escalated to `ideas_to_founder.md § 7`. Workaround in use.
6. **node-33 v_idx=4845 (NEW s182)** — first genuine co-located on-the-fence candidate in 31+ sessions; watch s183.
7. **node-33 v_idx=10288** — WATCH CLOSED; confirmed parked_v2 phantom.
8. **node-33 v_idx=1482** — re-appeared in killable_v3 unsampled (margin=15, elapsed=6.99h); historical archetype → continued REJECT.
9. **NEW: node 9 hot_battlegrounds signal** — 2 competitor kills, sample victim tamagotcho. Pin for s183 oracle drill if persistent.
10. **node 62 cluster watch** — expanded 1→2, both phantoms; continue passive.
11. **11224 Lethality allocation** — BLOCKED.
12. **Branch 2 persistence** — 0/3.
13. **Migration HOLD (Branch 1)** — 10 consecutive sessions.
14. **Amendment D** — UNFIRED.
15. **Oracle staleness doctrine** (s175) — apply as needed.
16. **stop_harvest_batch ~17% revert** — defer.
17. **v_HP staleness** — defer.
18. **STRIKERS const stale** — defer.
19. **SIUUUU node-65 cluster watch** — no signal.
20. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s183

Read-only continuation, BUT with two non-trivial wedges:
- **v_idx=4845** is the first genuine co-located candidate to pass both elapsed AND margin gates in 31 sessions; if owner attribution restores AND it's non-archetype AND sampled with ram≥+10 → **fire D-pilot**. Low probability but non-zero.
- **Phase 2 deflation 4th-consecutive** would be the formal §PARTIAL trigger; expect to write up §PARTIAL trigger criteria in `predator/strategic-experiments.md` if it holds.

If Phase 2 deflation rebounds OR P1 falsifies: write doctrine update, fast re-scan.
