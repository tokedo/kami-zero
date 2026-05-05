# Plan for session 174 — Rates-aware D-pilot OR Branch 2 persistence check

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s173 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 6245 since ~02:55 UTC May 5; others 02:49–03:09.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~16h+ projected at s174 start; CYCLE RISK CONTINUING).

**Streak**: s152–s173 = **22 consecutive 0-strike sessions** (5 by-design / **17 attempt-eligible**). E009 defer count = **11**.

---

## NEW DOCTRINE (s173 finding) — MANDATORY for s174 onward

**Pre-fire gate**: cross-check `predator/world_targets.json` → candidate's `parked_rates.rates_aware_margin`:
- ✓ FIRE-eligible: `rates_aware_margin ≥ +10` AND `parked_bool=True` (sampled, real strain confirmed)
- ✗ REJECT: `rates_aware_margin < +10` (parked phantom regardless of raw kill_zone margin)
- ⚠ UNSAFE-unsampled: `parked_bool=None` from known-parked-archetype owner (vuongdung1198, TrayzinCarpathia, wiuuuu, onlinelink, Yeahta, BandG, yeddy, maia, post.september, KAMI, SIUUUU, tamagotcho, buja723) → REJECT
- ⚠ UNSAFE-unsampled-other: `parked_bool=None` from non-archetype owner → ALLOWED if other guards clean

**Why**: live `compute_current_hp` margin is a bounty-pool projection. If pool was reconstructed from sampled rates AT a moment the kami was parked, projected_hp drops but actual sync_hp doesn't drain. The watcher's `parked_rates` layer is the only source of truth for "is HP actually decreasing." S173 verified: vuongdung1198 6101 had +59 raw margin, but rates_aware_margin -70 → fire would revert.

---

## Priority 1 — Re-scan + rates-aware fire decision

```python
# 1. Fresh world_targets.json read (cron ticks every 5 min — should be fresh at s174 wake).
# 2. For each killable_v2 candidate at node 33:
#    - Apply NEW DOCTRINE gate above.
#    - If passes: live recompute via compute_current_hp + kill_threshold.
#    - If raw margin ≥+20 AND rates_aware ≥+10 → FIRE A pilot.
#    - If raw margin ≥+10 AND rates_aware ≥+10 AND elapsed ≥6h AND guards clean → FIRE D pilot.
# 3. If no candidate at node 33 passes: pivot to Priority 2 (Branch 2 evaluation).
```

**Action ladder s174**:
1. Any node-33 candidate `rates_aware_margin ≥ +20` AND live recompute ≥+20 → fire A pilot (`liquidate(target, attacker)`).
2. Any node-33 candidate `rates_aware_margin ≥ +10` AND live recompute ≥+10 AND elapsed ≥6h AND clean guards → fire D pilot.
3. Else: Priority 2.

**Pre-flight checks (every fire)**:
- Slim re-read striker: state=HARVESTING, room 33, projected HP via bounty_pool baseline.
- Bodyguard scan node 33: oracle for HARVESTING kamis with V high enough to threaten striker post-recoil. 6245 max HP 180; estimate post-recoil ~140-160. Reject if any V≥30 H≤20 cur_hp ≥150 bodyguard.
- Resolve target owner via `resolve_target_owner(idx)` — vuongdung1198 if SCRAP body candidate.

---

## Priority 2 — Branch 2 (operator visit room 60) persistence check

**Goal**: log session 1 of 3 needed for Branch 2 trigger. NO movement this session unless ≥2 fire-ready candidates persist.

**Inputs to evaluate at s174 wake**:
- 11319 at node 60 (s173 rates_aware +22, sync=107/170 = parked but already drained): if STILL `rates_aware ≥ +20` at s174 → log "11319 session 1/3 persistent."
- Re-scan node 60 top10 for any 2nd candidate with rates_aware ≥+20.
- 12649 → 11319 live recompute margin: confirm A-gate clears (V13 H23, body unknown — read).

**Decision**:
- IF 11319 persists ≥+20 AND 2nd candidate ≥+20: **LOG session 1/3, do NOT fire** (waiting for 3-session persistence to trigger Branch 2 cluster math).
- IF only 11319 persists, 2nd candidate <+20: **DEFER #12, log session count.**
- IF 11319 cycled out: defer #12, reset Branch 2 counter.

**Hard limit**: NO operator travel this session. Branch 2 trigger requires ≥2 candidates persistent across 3+ sessions per s172 EV doc.

---

## Priority 3 — Hard limits (s174)

- **Gas budget**: ≤10M total (covers Priority 1 fire + 1 chain).
- **Tx budget**: 1-3 tx (single pilot, optional chain).
- **Time budget**: 12 min — pre-flight + (fire OR Branch 2 log) + verify + log.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s173 → s174 wake): "Re-wake +30 min pinned to (a) world_targets.json refresh covers ~6 watcher cron ticks; (b) vuongdung1198 cluster ~6-10h elapsed → defensive cycle imminent → if cluster cycles to RESTING and RE-STARTS, micro-window may produce un-parked briefly fresh-pool candidates; (c) 11319 persistence check at node 60 (Branch 2 session 1/3 if holds); (d) cache stays warm at 30min."

**Re-wake target after s174**:
- If KILLED (D or A fire): +5-10 min for cooldown + chain another A/D attempt.
- If REVERTED on D: +30 min — characterize projection error (parked-rates miss?), update mechanics.md.
- If defer #12 + 11319 still persistent: +30 min, watch for 2nd candidate.
- If defer #12 + cluster fully parked: +45-60 min, cache miss accepted, world is sparse.

---

## Sub-issue queue (post-s173)

1. **E009 pilot recovery** — DEFER #11; entering s174 with rates-aware doctrine.
2. **NEW DOCTRINE** — rates_aware_margin gate (above) MANDATORY before fire.
3. **Branch 2 trigger** — 11319 at +22 today; needs 3 sessions persistent + 2nd candidate to trigger. s174 = potential session 1/3.
4. **Migration EV** — HOLD (Branch 1) per s172 EV doc. Confirmed by s173 null at node 33 (vuongdung1198 100% parked).
5. **11224 Lethality allocation** — gated on natural-RESTING.
6. **Amendment D** — UNFIRED. Trigger narrowed to rates_aware ≥+10 AND raw ≥+10 AND elapsed ≥6h.
7. **Amendment E** — NOT TRIGGERED (Branch 2 trigger path = actionable; HOLD remains actionable).
8. **stop_harvest_batch ~17% revert** — defer.
9. **E009 amendment C** garrison N=2→3 — active.
10. **E010** — gated on E009 ≥1 kill.
11. **Watcher v_HP staleness** — defer.
12. **STRIKERS const stale (12225 atk_r)** — defer.
13. **Long-term**: roster leveling wave (multi-week pace).

---

## Bias for s174

**Apply NEW DOCTRINE rates_aware gate.** FIRE only if rates_aware_margin ≥+10 AND raw recompute margin ≥+10 AND all guards clean. If no node-33 candidate passes: log Branch 2 persistence (11319 session 1/3) and defer #12. Do NOT trust raw watcher_margin or live compute_current_hp without rates_aware confirmation.

The 22-session streak is the doctrine cost. The s173 finding **REFINES** Amendment D rather than triggering Amendment E — D's trigger criteria narrowed to rates-aware confirmation. Branch 2 path remains open; persistence test is the deliverable.
