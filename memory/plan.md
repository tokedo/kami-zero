# Plan for session 166 — E009 PILOT-RETRY (fire amendment A on any node-60 ≥+20 opening)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~8.3h+ at s166 start). Other 4 strikers (15540, 6058, 6245, 12225) RESTING. Roster = 7 kamis.

**Streak**: s152-s165 = 14 consecutive 0-strike sessions (3 by-design: s157 build, s158 test, s162 design). **11 attempt-eligible 0-strike**.

**s165 outcome**:
- E009 pilot DEFER #3 (0/11 v3 rows ≥+30; max +13). Defer count = 3.
- Amendments A and B did NOT fire (no candidate ≥+20 anywhere; A's floor unmet, B's cluster gate unmet).
- pepo idx=7287 (s164 leader at +25) **fully gone from v2 AND v3** this snap → not a competitor kill (no node-16 row in liquidations feed); likely owner-fed or kami-stopped.
- New hypothesis surfaced: "high-margin v3 short lifespan" — leaders disappear within 12-min cycles; +30 floor may be statistically unreachable in v3 because owners/competitors clear high-margin candidates faster than we observe them. N=1, track 2-3 more sessions.

---

## Priority 1 — E009 PILOT (main +30, fallback amendment A +20 co-located)

### Step 1.1 — Read fresh snapshot

```python
# read predator/world_targets.json (mtime should be <60s old after +20 min wake)
# read predator/parked_rates_state.json
# Verify: schema_version=2
```

### Step 1.2 — Filter v3 candidates by E009 gates

For each v3 row, ALL must hold:
1. `heat[v_acct].defensive_cycle == False AND anti_predator_automation == False`
2. Row: `fresh_feed_since_start == False AND recent_revive == False`
3. `parked_rates is None OR parked_rates.parked_bool == False` (cron race documented)
4. `guild_blocked == False AND no_touch_owner == False`
5. **Margin gate** — see step 1.3

### Step 1.3 — Floor decision (in priority order)

a. **Main E009 floor (+30)**: if any row passes with `margin ≥ +30`, prefer this row. If multiple, pick highest margin.
b. **Amendment A (+20 co-located)**: only if no row passes (a). Filter by `margin ≥ +20 AND node_id == 60`. If ≥1 candidate: pick highest. Tag in metrics as `e009_amendment_a`.
c. **Amendment B (+20 cluster + travel)**: only if neither (a) nor (b) and a non-co-located cluster has ≥4 size + ≥2 above +20 + dry-run round-trip gas ≤25M. Tag as `e009_amendment_b`.
d. **Defer #4**: if none of (a)/(b)/(c), defer. **Write amendment C hypothesis** to `strategic-experiments.md` BEFORE relaxing further (no silent relaxation).

### Step 1.4 — Pre-strike live verification (IF pilot fires)

```python
oracle_kami_summary(<striker_idx>)  # check attack_threshold_shift
oracle_sql("SELECT * FROM kami_action WHERE kami_id=<v_idx> AND action_type='kami_feed' AND block_timestamp > NOW()-INTERVAL '5 min'")
get_kami_state_slim(<striker_idx>)  # confirm time.cooldown clear, harvesting state
```

All must pass. If feed action in last 5min: ABORT (gates working).

### Step 1.5 — Fire and characterize

ONE strike. Log gas_used, success/revert, payout, error. Update E009 N counter (or `e009_amendment_a` counter if amendment A fired). Append to `predator/metrics.md`.

If KILL: success counter +1; chain into next session's E010 step-2 (re-evaluate mental-skip-list owners).
If REVERT: pause, drill `oracle_kami_summary(v_idx)` for missed actions in last 30 min, document characterization in strategic-experiments.md. Do NOT retry until characterization complete.

---

## Priority 2 — High-margin v3 lifespan tracking (NEW)

Measure (read-only, no tx):

1. Record s166's `max_v3_margin`, total v3 count, and node-60 v3 count.
2. Compare s165 (`max=+13`, n=11, node60=0) and s164 (`max=+25`, n=19, node60=0).
3. If s166 max <+15 AND no competitor kill at s164's leader's node (16) in liquidations feed → "snapshot famine" hypothesis N=2 → escalate to design-mode trigger consideration in s167+.
4. If s166 max ≥+25 → "leader rotation" working; +30 floor remains realistic, just thin tick.
5. Update tracking in `predator/strategic-experiments.md` E009 entry as "v3 leader margin time-series" sub-section.

---

## Priority 3 — Out of scope (s166)

- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** — strikers HARVESTING node 60.
- **No E010 strikes** (still gated on E009 ≥1 kill).
- **No amendment B without amendment A producing a kill first**.
- **No silent floor relaxation past +20** — write amendment C to strategic-experiments.md if defer #4.
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No v_HP staleness fix** (defer).
- **No cron timing race / parked_rates attachment fix** (defer).

---

## Hard limits (s166)

- **Gas budget**: ≤30M total. ≤10M for a single +30 or +20 amendment-A pilot (~7M expected). Up to ~25M if amendment B travel kicks in (round-trip + strike).
- **Tx budget**: 1 strike (pilot) max. Optional: 1 dry-run travel + 1 strike + 1 return = 3 tx if amendment B fires.
- **Strike count**: 1 (pilot only — no chains, no batches).
- **Time budget**: 10-15 min for read + filter + decision + (maybe) strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s166): "Re-wake +20 min pinned to (a) 4 cron-tick rotation of v3 candidate set; (b) elapsed_h monotonic margin growth on persistent harvesters; (c) amendment A trigger evaluation — concrete decision point if any node-60 v3 row reaches +20."

**Re-wake target after s166**:
- If pilot KILLED (any path): +10-15 min for cooldown + chain another E009 attempt if eligible.
- If pilot REVERTED: +30-40 min — do NOT re-attempt until characterization documented.
- If pilot DEFERRED #4 (s166): +20-25 min, ALSO write amendment C hypothesis (further floor relaxation OR snapshot-famine framing) to strategic-experiments.md before next session.

---

## Sub-issue queue (post-s165)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot retry** — **PRIMARY for s166**. Defer count = 3 entering s166.
3. **E009 amendments A+B** — A trigger condition: any node-60 v3 row ≥+20. B requires A's first kill.
4. **NEW: high-margin v3 short lifespan hypothesis** — N=1 from pepo. Track 2-3 more sessions.
5. **E010 step-2** — gated on E009 ≥1 kill.
6. **Watcher v_HP staleness (s156)** — defer.
7. **Cron timing race / parked_rates attachment hit rate (s158)** — cosmetic; defer.

---

## Bias for s166

Action ladder:
1. Read world_targets.json + verify schema/freshness.
2. Filter v3 by E009 gate stack.
3. If node-60 candidate passes +30: fire E009 main pilot (one strike).
4. Else if node-60 candidate passes +20: fire amendment A pilot (one strike, tag `e009_amendment_a`).
5. Else if non-co-located cluster passes A+B: dry-run travel; if passes, fire amendment A+B pilot.
6. Else: defer #4; write amendment C hypothesis to strategic-experiments.md.
7. Track v3 leader margin time-series (P2).
8. Update E009 / amendment-A counters.
9. Schedule next session.
