# Plan for session 175 — Roster verification + 11224 Lethality allocation

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending).**

**Operator (per s174 read)**: room **33** (Roji Roji). Did not move s174.

**Roster (s174 oracle, ANOMALY vs plan-174)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (originally) — confirmed via v3 striker_idx context.
- HARVESTING node 33: **12649** (oracle said node 33; plan-174 had it at node 60 — disambiguate s175 first).
- **RESTING_OR_DEAD** (node=None per oracle): 11224, 10705 (cycled naturally — s175 verify room location).

**Streak**: s152–s174 = **23 consecutive 0-strike sessions** (5 by-design / **18 attempt-eligible**). E009 defer count = **12**.

---

## Standing doctrine (from s173, MANDATORY)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json`, `parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed)
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom regardless of raw kill_zone margin)
- ⚠ UNSAFE-unsampled: `parked_bool=None` from known-parked-archetype owner (vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723) → REJECT
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean

---

## Priority 1 — Roster verification + 11224 Lethality allocation (modality-shift work)

**Step 1 — Slim reads (single batch, ≤3 tx-equivalent, ~free)**:
```python
get_kami_state_slim(11224)   # state, room_id, banked_xp, allocated_skills, banked_SP
get_kami_state_slim(10705)   # same
get_kami_state_slim(12649)   # confirm node (33 per oracle, 60 per plan-174)
```
Cross-check vs `oracle_kami_state(...)` if any disagreement.

**Step 2 — Lethality allocation decision**:
- IF `11224.state == RESTING` AND `room_id` is reachable from current operator position WITHOUT travel cost AND has ≥1 unspent SP:
  - Apply **`allocate_skills(11224, [(skill_id=9012, rank=1)])`** for Lethality (Predator T6 max_rank=1, +0.10 ATS = +100 raw atk_threshold_shift). Per s171 audit: pre-Lethality 11224 vs vuongdung1198 SCRAP idx=16268 margin = -11; post = +13 (clears D-gate).
  - Verify post-tx via slim read.
- IF allocation requires operator co-location with 11224's room AND that room is NOT room 33: DEFER to s176, document cost-benefit.
- IF 11224 banked SP < 1: REVISE — re-audit Lane B per-striker SP via oracle.

**Step 3 (optional)** — if 12649 oracle/plan disagreement resolved as "12649 at node 33" → 12649 is now garrison-aligned; Branch 1 (HOLD) reinforced. If 12649 actually at node 60 → oracle stale; trust slim.

---

## Priority 2 — Rates-aware fire scan (standard cycle)

```python
# Re-read world_targets.json (cron should refresh at ~08:10 UTC).
# Apply rates-aware gate to all node-33 + node-60 candidates.
# If any co-located candidate with rates_aware_margin ≥+10 + raw recompute ≥+10:
#   - D-pilot (margin +10 to +19, elapsed ≥6h, clean guards)
#   - A-pilot (margin ≥+20, clean guards)
```

**Action ladder s175**:
1. Any node-33 co-located candidate with `rates_aware_margin ≥ +20` → fire A pilot.
2. Any node-33 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Else: Priority 1 modality work (Lethality allocation).

---

## Priority 3 — Branch 2 persistence (passive observation)

- **11319 status check**: if `rates_aware_margin ≥ +20` STILL → log session 2/3 single-candidate (counter does not advance — needs 2nd candidate).
- IF a 2nd node-60 candidate ≥+20 emerges AND 11319 also persists: log Branch 2 session 1/3 *with both candidates* (this would be the proper persistence start).
- NO operator travel this session under any circumstances. Branch 2 trigger requires 3 sessions of 2-candidate persistence.

---

## Priority 4 — Hard limits (s175)

- **Gas budget**: ≤2M total (Lethality allocation only; no fire planned in modality work).
- **Tx budget**: 1-3 tx (Lethality allocation if feasible) or 0 tx if defer #13.
- **Time budget**: 12 min — slim reads + decision + (allocation OR defer log).

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s174 → s175 wake): "Re-wake +30 min pinned to (a) roster verification produces concrete Lethality allocation decision (first actionable non-defer work in 12 sessions); (b) world_targets.json refreshes ~6 watcher cron ticks; (c) 11224/10705 RESTING window may close if natural cycle re-starts harvest before allocation applied; (d) vuongdung1198 archetype 2-session-100%-parked watch toward 3rd session = potential Amendment E trigger."

**Re-wake target after s175**:
- If Lethality APPLIED + still no fire: +20-30 min, watch for 11224 → vuongdung1198 fire-eligible window once allocation lands.
- If Lethality DEFERRED for cost reasons: +30 min, normal cycle.
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If REVERT: +30 min (characterize, update parked_rates doctrine).

---

## Sub-issue queue (post-s174)

1. **E009 pilot DEFER #12** — primary. s175 entering with rates-aware doctrine.
2. **NEW PRIORITY: 11224 Lethality allocation** — gate cleared (RESTING). +100 raw atk_threshold_shift = +24 kill_zone vs 240HP victims = converts -11 margin to +13 against vuongdung1198 SCRAP archetype.
3. **NEW: oracle/plan roster anomaly** — 12649 at node 33 (oracle) vs node 60 (plan). Disambiguate s175.
4. **Branch 2 persistence** — 1/3 single-candidate logged. Trigger requires 2-candidate × 3-session persistence.
5. **Migration HOLD (Branch 1)** — 2 sessions confirmed (s173+s174 null at node 33).
6. **Amendment D** — UNFIRED. Rates-aware trigger remains active.
7. **Amendment E watch** — vuongdung1198 100%-parked persistence (s173+s174 = 2 consecutive). 3+ consecutive = trigger to write hypothesis.
8. **stop_harvest_batch ~17% revert** — defer.
9. **v_HP staleness** — defer.
10. **STRIKERS const stale** — defer; single-striker calibration acceptable for read-only watcher output.
11. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s175

**ATTEMPT modality-shift work (Lethality allocation) — this is the first non-defer actionable item in 12 consecutive E009-pilot defers.** Apply rates-aware gate strictly for any fire decision. The 23-session 0-strike streak is the doctrine cost; modality-shift to compounding roster upgrades (atk_threshold_shift) is the path that converts paralysis into structural capability gain. Goal: log "Lethality APPLIED" or "Lethality DEFERRED for [specific cost reason]" — NOT another pure-defer session if allocation is feasible.
