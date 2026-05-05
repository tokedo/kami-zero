# Plan for session 178 — Amendment E Phase 1 row 2/7 + standing rates-aware fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (s175 read; s176/s177 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176+s177)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~21h+ elapsed).
- 11224 banked SP=3 (Lethality 162 BLOCKED indefinitely).

**Streak**: s152–s177 = **26 consecutive 0-strike** (5 by-design / **21 attempt-eligible**). E009 defer count = **15**.

**Amendment E status**: Phase 1 row 1/7 LOGGED s177. P1 HOLDS (5 consecutive deflation sessions: s173+s174+s175+s176+s177). Phase 2 row 1 partial LOGGED — 4/5 surveyed nodes archetype-dominated, 0 fire-eligible elsewhere.

---

## Standing doctrine (carry-over from s173+s175+s176+s177)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json::parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed).
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom).
- ⚠ UNSAFE-unsampled-archetype: `parked_bool=None` from {vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723} → REJECT.
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean.

**SIUUUU edge case (s177)**: archetype owner IS strikeable when sampled-True with rates_aware ≥+10 (real strain confirmed, not snapshot artifact). Block by Hard Rule 4 (cross-region single target), not doctrine.

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s178**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Any **co-located** OR same-room candidate with `rates_aware_margin ≥ +10` + parked_bool=True (the SIUUUU 659 case repeats) → re-evaluate Hard Rule 4 against cluster + striker availability.
4. Else: Priority 2 (Amendment E observation).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine.

---

## Priority 2 — Amendment E Phase 1 row 2/7 + Phase 2 row 2

Per `predator/strategic-experiments.md` E009 Amendment E.

### Phase 1 (passive observation, target 7 sessions to confirm P1)

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

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E. Continue passive defer.
- **IF P1 holds** (deflation continues): row 2/7 logged, defer #16. P1 confirmed at s181 (7 consecutive).
- **IF fire-eligible candidate emerges co-located**: FIRE first per Priority 1.

### Phase 2 (5-node breadth survey)

Re-scan nodes 25/73/9/16/88 + add 62 (sa3woo cluster has good elapsed). Count:
- candidates / archetype share / sampled-True share / fire-eligible.
- node 65 watch — does SIUUUU 659 persist or cycle? Does a 2nd non-Killchain candidate emerge?

If by s181, Phase 2 shows persistent deflation across all surveyed nodes (≤2 fire-eligible cumulative across 4 sessions), counter-response 1 EV degrades.

If Phase 2 shows ≥3 fire-eligible candidates at a SINGLE alternative node by s180, counter-response 1 (forced migration to that node) becomes actionable.

---

## Priority 3 — Phase 3 oracle query (still optional, free read)

Per `predator/strategic-experiments.md` Amendment E Phase 3:

```sql
SELECT kami_index, MIN(balance) AS min_bal, MAX(balance) AS max_bal, MAX(balance) - MIN(balance) AS delta_bal
FROM v_harvest_state
WHERE owner = 'vuongdung1198'
  AND ts > now() - INTERVAL '7d'
GROUP BY kami_index
ORDER BY delta_bal ASC
LIMIT 50;
```

Expected if P1 holds: `delta_bal < 100 MUSU/kami` (parked = no minting). If observed `>>100`: hypothesis weakening (cluster IS minting → IS harvesting → parked-rates is snapshot artifact).

Run in s178 if attention budget permits — adds high-confidence Phase 3 evidence in 1 free oracle call.

---

## Priority 4 — Hard limits (s178)

- **Gas budget**: 0 (read-only unless fire-eligible co-located emerges).
- **Tx budget**: 0 unless Priority 1 fires.
- **Time budget**: 10-15 min — fire scan + Phase 1 row 2/7 + Phase 2 row 2 + optional Phase 3.
- **NO operator travel** unless cluster math (≥3 candidates with co-located striker capability) justifies.
- **NO migration counter-response** (Amendment E threshold not yet met).

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s178**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update doctrine).
- If P1 falsified: +15 min (rates-aware surface may be rapidly recovering; fast re-scan).
- If P1 holds + standard defer: +25-30 min, Phase 1 row 3/7.

**s178 wake** (this plan's pin): **+25 min from s177** (~09:50 UTC May 5, ts ≈ 1777974612). Pinned to:
- (a) world_targets.json refresh (5 watcher cron ticks)
- (b) node 65 SIUUUU monitoring — does 659 cycle/persist?
- (c) Phase 1 row 2/7 + Phase 2 row 2
- (d) cache miss accepted (no near-term <300s event)

---

## Sub-issue queue (post-s177)

1. **E009 pilot DEFER #15** — primary for s178 with rates-aware doctrine + Amendment E Phase 1 row 2 logging.
2. **Amendment E Phase 1 row 1/7 LOGGED** — P1 HOLDS at 5 consecutive sessions.
3. **Amendment E Phase 2 row 1 partial LOGGED** — regional deflation likely.
4. **11224 Lethality allocation** — BLOCKED indefinitely. Counter-response 1 EV weakened by Phase 2 finding.
5. **Branch 2 persistence** — 0/3 (no candidates).
6. **Migration HOLD (Branch 1)** — 5 consecutive sessions.
7. **Amendment D** — UNFIRED.
8. **Oracle staleness doctrine** (s175) — apply as needed.
9. **stop_harvest_batch ~17% revert** — defer.
10. **v_HP staleness** — defer.
11. **STRIKERS const stale** — defer.
12. **NEW (s177)** SIUUUU node-65 cluster watch — passive observe for 2nd candidate or 659 cycle.
13. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s178

Read-only continuation. Log Phase 1 row 2/7. Phase 2 row 2. Optionally run Phase 3 oracle query. **FIRE only if rates-aware fire-eligible candidate emerges co-located OR cluster math justifies travel**. Defer #16 expected if pattern holds.
