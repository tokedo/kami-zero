# Plan for session 176 — Amendment E hypothesis decision + rates-aware fire scan

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending).**

**Operator (per s175 read)**: room **33** (Roji Roji). Did not move s175.

**Roster (s175 slim-verified, oracle s174 was STALE — IGNORE)**:
- HARVESTING node 33: 15540, 6058, 6245, 12225 (garrison, originally-RESTING followed s165 travel).
- HARVESTING node 60: **12649, 11224, 10705** — STILL parked (rates=0, ALL three since 21:54 UTC May 4 = ~17h+ elapsed). Plan-174 baseline correct.
- 11224 sync=0 (drained but state=HARVESTING). 12649 sync=0 balance=773. 10705 sync=163 balance=283.

**Banked SP**: 11224=3 (no Lethality 162 yet), 12649=0 (already has Lethality 162), 10705=0.

**Streak**: s152–s175 = **24 consecutive 0-strike sessions** (5 by-design / **19 attempt-eligible**). E009 defer count = **13**.

**Branch 2 persistence counter**: RESET to 0/3 — 11319 cycled out.

**Amendment E watch**: vuongdung1198 100%-parked = **3 consecutive sessions** (s173+s174+s175). Threshold MET for hypothesis-writing per Lane-A/B doctrine.

---

## Standing doctrine (from s173+s175, MANDATORY)

**Pre-fire rates-aware gate** (cross-check `predator/world_targets.json`, `parked_v2[*].parked_rates.rates_aware_margin` and `parked_rates_state.json::by_idx`):
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed)
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom regardless of raw kill_zone margin)
- ⚠ UNSAFE-unsampled: `parked_bool=None` from known-parked-archetype owner (vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723) → REJECT
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean

**Oracle staleness rule (NEW s175)**: `kami_static.{location,state}` lags on-chain harvest entity state. When oracle disagrees with prior plan baseline, slim-verify via `get_kami_state_slim().harvest.{state,node,time.start}` BEFORE revising plan.

---

## Priority 1 — Amendment E hypothesis decision (modality work)

**Trigger condition met (per Lane-A/B doctrine)**: Lane A closed s170 + Lane B audited s171 + ≥3 consecutive sessions of vuongdung1198 archetype 100%-parked deflation = threshold permits Amendment E.

**Step 1** — Re-read `world_targets.json` and `parked_rates_state.json`. Confirm vuongdung1198 still 100%-parked on node 33 (4th consecutive session = strong evidence) OR a non-archetype fire-eligible candidate emerges.

**Step 2** — Decision tree:
- **IF a fire-eligible candidate emerges (rates_aware ≥+10, non-archetype OR sampled-True archetype)**: FIRE. Defer Amendment E indefinitely. The hypothesis is moot if surface is recovering.
- **IF vuongdung1198 still 100%-parked AND no node-60 non-archetype fire-eligible**: WRITE Amendment E to `predator/strategic-experiments.md`. Structure:
  - **Hypothesis**: "vuongdung1198 cluster has fully migrated to anti-predator automation (100%-parked archetype). Continuing to scan node 33 as primary fire surface is structurally negative-EV."
  - **Predictions**: (a) parked_bool=True with negative rates_aware_margin persists ≥7 consecutive sessions; (b) operator-arrival sync_stop_burst rate ↑; (c) MUSU bounty pool growth on those kamis ↓ (their balance not minting because rates=0).
  - **Test**: 3-session continued observation + sample 5 non-vuongdung1198 nodes for fire-surface comparison.
  - **Counter-response options if confirmed**: (1) operator migration to node 60 forced (~15-30M gas one-time, reactivates 11224 Lethality allocation); (2) accept node 33 as garrison-only (no fire surface); (3) wait — automation owners eventually shift patterns (~weeks).
- **IF vuongdung1198 partially un-parked (some sampled parked_bool=False)**: doctrine cost is recoverable; do NOT write Amendment E; document observation.

**Step 3** — Verify post-write file integrity if Amendment E written.

---

## Priority 2 — Rates-aware fire scan (standard cycle)

```python
# Re-read world_targets.json (cron */5 min refresh).
# Apply rates-aware gate to all node-33 + node-60 candidates.
# Special attention: parked_v2 with rates_aware_margin ≥ +10 from non-archetype owners.
# Special attention: parked_bool=False sampled (real strain present).
```

**Action ladder s176**:
1. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +20` AND clean guards → fire A pilot.
2. Any node-33 OR node-60 co-located candidate with `rates_aware_margin ≥ +10` AND elapsed ≥6h AND clean guards → fire D pilot.
3. Else: Priority 1 modality work (Amendment E decision).

---

## Priority 3 — Branch 2 persistence (passive observation)

- Counter currently 0/3 (11319 cycled out). Re-evaluate on any new node-60 candidate with rates_aware ≥+20 from non-archetype owner.
- NO operator travel this session under any circumstances.

---

## Priority 4 — Hard limits (s176)

- **Gas budget**: ≤2M total (Amendment E write-up only if triggered; no fire planned).
- **Tx budget**: 0 tx (read-only) unless rates-aware fire candidate emerges.
- **Time budget**: 12-15 min — fire scan + Amendment E decision + write-up.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s175 → s176 wake): "Re-wake +30 min pinned to (a) world_targets refresh ~6 cron ticks; (b) parked_rates scanner may pull node-60 wiuuuu into sampled — if rates_aware reads positive, fire-eligible window opens; (c) Amendment E hypothesis-writing decision (threshold met s175) becomes actionable; (d) cache miss accepted (no near-term <300s event)."

**Re-wake target after s176**:
- If Amendment E WRITTEN: +30-60 min, monitor evolution of vuongdung1198 surface.
- If FIRE successful: +5-10 min (cooldown + chain attempt).
- If REVERT: +30 min (characterize, update parked_rates doctrine).
- If continued defer #14: +20-30 min, normal cycle.

---

## Sub-issue queue (post-s175)

1. **E009 pilot DEFER #13** — primary. s176 entering with rates-aware doctrine + Amendment E threshold met.
2. **Amendment E hypothesis** — THRESHOLD MET (3 consecutive). s176 write-up if pattern persists. Counter-response options noted.
3. **11224 Lethality allocation** — BLOCKED indefinitely (state=HARVESTING parked rates=0). Path (a) requires forced migration (~15-30M gas), Path (b) requires natural cycle (won't happen with parked archetype). Defer until operator already at node 60 for other reason OR Amendment E counter-response triggers.
4. **Branch 2 persistence RESET** — 0/3 (11319 cycled).
5. **Migration HOLD (Branch 1)** — 3 consecutive null at node 33.
6. **Amendment D** — UNFIRED.
7. **Oracle staleness doctrine** — NEW s175. Slim-verify when oracle disagrees with plan baseline.
8. **stop_harvest_batch ~17% revert** — defer.
9. **v_HP staleness** — defer.
10. **STRIKERS const stale** — defer.
11. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s176

**ATTEMPT Amendment E hypothesis write-up if pattern persists** — this is the modality-shift work the doctrine permits when ≥3 consecutive sessions of fire-surface deflation occur. 24 attempt-eligible sessions of 0 kills is already past the original "5 consecutive 0-kill = design mode" trigger by 19 sessions; doctrinal accountability requires the next non-defer modality move. FIRE first if rates-aware candidate emerges; ELSE write Amendment E or document why pattern shifted.
