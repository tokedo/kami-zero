# Plan for session 177 — Amendment E Phase 1 row 1/3 + standing rates-aware fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179.**

**Operator (per s175 read; s176 read-only)**: room **33** (Roji Roji).

**Roster (s175 slim-verified, unchanged across s176)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison).
- HARVESTING node 60: 12649, 11224, 10705 (parked, rates=0, ~18h+ elapsed).
- 11224 banked SP=3 (Lethality 162 not yet allocated).

**Streak**: s152–s176 = **25 consecutive 0-strike** (5 by-design / **20 attempt-eligible**). E009 defer count = **14**.

**Amendment E STATUS**: HYPOTHESIS written s176 to `predator/strategic-experiments.md`. Phase 1 (passive observation ≥7 sessions) row 0/7 starting s177.

---

## Standing doctrine (carry-over from s173+s175+s176)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json`, `parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed)
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom regardless of raw kill_zone margin)
- ⚠ UNSAFE-unsampled: `parked_bool=None` from known-parked-archetype owner (vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723) → REJECT
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean

**Oracle staleness rule (s175)**: slim-verify when oracle disagrees with prior plan baseline.

---

## Priority 1 — Standing rates-aware fire scan

**Action ladder s177**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Else: Priority 2 (Amendment E observation).

If FIRE: pre-fire LIVE recompute via `executor.hp_projection.kill_threshold` per s175 doctrine (oracle staleness).

---

## Priority 2 — Amendment E Phase 1 observation row 1/3 (towards 7-session threshold)

Per Amendment E test plan (`predator/strategic-experiments.md` E009 Amendment E):

**Step 1** — Read `world_targets.json` + `parked_rates_state.json`. Log to in-session note (and append to decisions.md):
- node-33 vuongdung1198 sampled count
- parked_bool=True count
- rates_aware_margin distribution (min, median, max)

**Step 2** — Compare to s173/s174/s175/s176 row data:

| Session | sampled vuongdung1198 | parked_bool=True | rates_aware [min, max] | non-archetype fire-eligible elsewhere |
|---------|------------------------|------------------|------------------------|---------------------------------------|
| s173    | 6/6                   | 6/6              | [-70, -45]             | 0 |
| s174    | 9 sampled / 6 archetype-unsampled | 9/9 | [-70, -47]         | 0 |
| s175    | all sampled            | all parked       | deeply negative        | 0 |
| s176    | 13/14                 | 13/13            | [-75, -27]             | 0 (only 3243 wiuuuu archetype REJECT) |

**Step 3** — Decision tree:
- **IF P1 falsified** (any sampled vuongdung1198 candidate with `parked_bool=False` OR `rates_aware_margin ≥ -10`): document recovery, log toward REJECT Amendment E. Continue passive defer.
- **IF P1 holds** (deflation continues): row N/7 logged, defer #15 + plan continues to s178.
- **IF fire-eligible candidate emerges anywhere** (node-33 sampled-True non-archetype OR node-60 non-archetype): FIRE first per Priority 1.

---

## Priority 3 — Phase 2 prep (optional, opportunistic)

Per Amendment E Phase 2: scan 5 non-archetype-dominated nodes for fire-surface comparison. Free read if `hot_nodes` data already in `world_targets.json` covers these.

**Candidate nodes**: 25, 73, 9, 16, 88 (from `hot_nodes` list, non-archetype-dominated TBD by inspection).

**Step 1** — In `world_targets.json`, scan `by_node[*]` for nodes 25/73/9/16/88. For each:
- Count candidates with `rates_aware_margin ≥ +10` from non-archetype owners.
- Count parked_bool=False sampled (real strain).

**Step 2** — If ≥1 fire-eligible candidate found at any of these nodes, this is Phase 2 evidence supporting Amendment E adoption (surface elsewhere exists, we just aren't there). Document; do not act on counter-response 1 (migration) until full Phase 2 (3+ sessions worth).

---

## Priority 4 — Phase 3 prep (optional, oracle query)

Per Amendment E Phase 3: oracle query for vuongdung1198 bounty pool delta over 7d window.

```sql
SELECT kami_index, MIN(balance) AS min_bal, MAX(balance) AS max_bal, MAX(balance) - MIN(balance) AS delta_bal
FROM v_harvest_state
WHERE owner = 'vuongdung1198'
  AND ts > now() - INTERVAL '7d'
GROUP BY kami_index
ORDER BY delta_bal ASC
LIMIT 50;
```

Expected if hypothesis: delta_bal < 100 MUSU per kami (parked = no minting). Free oracle read.

If observed: delta values >>100 MUSU = hypothesis weakening (cluster IS minting; therefore IS harvesting; therefore parked-rates phenomenon may be a snapshot artifact only — re-derive rates-aware doctrine).

Run this query in s177 if time permits. Read-only, free, evidence-positive either way.

---

## Priority 5 — Hard limits (s177)

- **Gas budget**: 0 (read-only unless fire-eligible emerges).
- **Tx budget**: 0 unless fire-eligible.
- **Time budget**: 10-15 min — fire scan + Phase 1 observation + optional Phase 2/3 prep.
- **NO operator travel**.
- **NO migration counter-response** (Amendment E Phase 1 not yet complete, threshold = 7 sessions).

---

## Self-schedule (Cadence Discipline pin)

**Re-wake target after s177**:
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If FIRE REVERT: +30 min (characterize, update parked_rates doctrine).
- If P1 falsified: +15 min (rates-aware surface may be rapidly recovering, fast re-scan).
- If P1 holds + standard defer: +25-30 min, Phase 1 row 2/7.

**s177 wake** (this plan's pin): **+25 min from s176** (~09:24 UTC May 5, ts ≈ 1777973100). Pinned to (a) world_targets refresh ~5 cron ticks, (b) wiuuuu/node-60 sample resolution, (c) Phase 1 row 1/7 observation begins, (d) cache miss accepted.

---

## Sub-issue queue (post-s176)

1. **E009 pilot DEFER #14** — primary for s177 with rates-aware doctrine + Amendment E Phase 1 logging.
2. **Amendment E HYPOTHESIS** — WRITTEN s176. Phase 1 begins s177 (3-session passive ≥7 sessions to confirm P1).
3. **11224 Lethality allocation** — BLOCKED. Counter-response 1 (forced migration) becomes actionable IF Phase 1 + Phase 2 confirm by ~s180-s183.
4. **Branch 2 persistence RESET** — 0/3.
5. **Migration HOLD (Branch 1)** — 4 consecutive sessions; folded into Amendment E counter-response 1 framework.
6. **Amendment D** — UNFIRED.
7. **Oracle staleness doctrine** (s175) — apply as needed.
8. **stop_harvest_batch ~17% revert** — defer.
9. **v_HP staleness** — defer.
10. **STRIKERS const stale** — defer.
11. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s177

Read-only continuation. Log Phase 1 row 1/7. Optionally advance Phase 2/3 with free reads. **FIRE only if rates-aware fire-eligible candidate emerges from non-archetype source**. Defer #15 expected if pattern holds. Phase 1 needs ≥7 consecutive deflation sessions to confirm P1 (currently 4/7 if s173 counts as row 0; observation s177 is row 1/3 in the 3-session window the plan-176 entry called for, but the formal 7-session threshold runs s177–s183 if continuous).
