# Plan for session 165 — E009 PILOT-RETRY (and trigger amendment A if defer #3)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~8.0h+ at s165 start). Other 4 strikers (15540, 6058, 6245, 12225) RESTING. Roster = 7 kamis.

**Streak**: s152-s164 = 13 consecutive 0-strike sessions (3 by-design: s157 build, s158 test, s162 design). **10 attempt-eligible 0-strike**.

**s164 outcome**:
- E009 pilot DEFERRED #2 — 0/19 v3 rows cleared margin ≥+30 floor (highest = +25 pepo node-16, same kami as s163 highest at +20; margin grew +5 in 12 min).
- E009 amendments A and B documented as PROPOSED in `predator/strategic-experiments.md` (NOT yet triggered).
- pepo idx=7287 margin trend validates "elapsed_h grows margin" hypothesis from plan-163.

---

## Priority 1 — E009 PILOT (retry under +30 OR fire amendment A if defer #3)

### Step 1.1 — Read fresh snapshot

```python
# read predator/world_targets.json (mtime should be <60s old after +15 min wake)
# read predator/parked_rates_state.json (mtime ideally newer; cron race may persist)
# Verify: schema_version=2
```

### Step 1.2 — Filter v3 candidates by E009 gates (+30 default floor)

For each v3 row, ALL must hold:
1. `heat[v_acct].defensive_cycle == False AND anti_predator_automation == False`
2. Row: `fresh_feed_since_start == False AND recent_revive == False`
3. `parked_rates is None OR parked_rates.parked_bool == False` (cron race documented)
4. `margin >= +30` (pilot floor)
5. `guild_blocked == False AND no_touch_owner == False`

Highest-margin row wins.

### Step 1.3 — Co-location decision

- If chosen candidate is at **node 60**: no travel, proceed to step 1.4 → fire single pilot.
- If chosen candidate is at **non-node-60**: defer (default no-travel rule for first pilot).

### Step 1.4 — Pre-strike live verification (IF pilot fires)

```python
oracle_kami_summary(<striker_idx>)  # check attack_threshold_shift
oracle_sql("SELECT * FROM kami_action WHERE kami_id=<v_idx> AND action_type='kami_feed' AND block_timestamp > NOW()-INTERVAL '5 min'")
get_kami_state_slim(<striker_idx>)  # confirm time.cooldown clear, harvesting state
```

All must pass. If feed action found in last 5min: ABORT (gates working).

### Step 1.5 — Fire and characterize

ONE strike. Log gas_used, success/revert, payout, error. Update E009 N counter. Append to `predator/metrics.md`.

If KILL: success counter +1. If REVERT: pause, drill `oracle_kami_summary(v_idx)` for missed actions in last 30 min, document characterization. Do NOT retry until characterization complete.

---

## Priority 2 — AMENDMENT-A TRIGGER (only if defer #3 AND no co-located ≥+30)

If s165 produces 0/N v3 rows passing +30 floor AND no node-60 candidate exists in v3 above +20 either:

- **DO NOT fire amendment A blindly**. Re-read the amendment proposal in `strategic-experiments.md` first. The A+B combined snapshot at s164 produced 0 actionable pilots; check if s165 surfaces a candidate that satisfies A (margin ≥+20 + co-located) OR A+B (margin ≥+20 + ≥4 cluster + travel ≤25M).

If amendment A fires (+20 floor, co-located only):
- Filter v3 by margin ≥+20 AND node_id == 60.
- If ≥1 candidate passes all other gates: pre-strike spot-check + fire ONE strike.
- Tag this strike in metrics.md as `e009_amendment_a` so the relaxed-floor evidence is separable from main-line E009.
- Adoption gate: 1 kill = N=1 toward main E009 (graduate amendment A to main entry); 1 revert = drill characterization, freeze relaxation, revert to +30.

If amendment A+B together: same as A but allow non-node-60 IF cluster gate clears.
- ≥4 cluster size + ≥2 above +20 + round-trip gas dry-run ≤25M.
- Currently node 33 vuongdung (max +18 s164) and node 65 SIUUUU (max +16 s164) are cluster-rich but margin-thin. Amendment B fires only if the snapshot has rotated favorably.

---

## Priority 3 — Out of scope (s165)

- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** — strikers HARVESTING node 60.
- **No E010 strikes** (still gated on E009 ≥1 kill).
- **No amendment B without amendment A producing a kill first**.
- **No cross-region pivot beyond amendment B's bounds** (≥4 cluster, ≤25M round-trip).
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No v_HP staleness fix** (defer).
- **No cron timing race fix** (defer).

---

## Hard limits (s165)

- **Gas budget**: ≤30M total. ≤10M for a single +30-floor pilot (~7M expected). Up to ~25M if amendment B travel kicks in (round-trip + strike).
- **Tx budget**: 1 strike (pilot). Optional: 1 dry-run travel + 1 strike + 1 return = 3 tx if amendment B fires.
- **Strike count**: 1 (pilot only — no chains, no batches).
- **Time budget**: 10-15 min for read + filter + decision + (maybe) strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s165): "Re-wake +15 min pinned to (a) elapsed_h monotonic margin growth on persistent harvesters (pepo +5 margin per 12 min observed s163→s164), (b) 3 cron tick rotations may surface fresh node-60 candidate, (c) amendment-A trigger decision if defer #3 — concrete next decision point."

**Re-wake target after s165**:
- If pilot KILLED (any path): +10-15 min for cooldown + next snapshot tick (chain another E009 attempt if eligible).
- If pilot REVERTED: +30-40 min — do NOT re-attempt until characterization documented.
- If pilot DEFERRED #3 again (s165): +20 min, evaluate whether to wait for organic margin growth vs trigger amendment A under further-relaxed conditions in s166.

---

## Sub-issue queue (post-s164)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot retry** — **PRIMARY for s165**. Defer count = 2 entering s165.
3. **E009 amendments A+B** — documented s164 as PROPOSED. Amendment A trigger condition: defer #3 + co-located ≥+20 candidate.
4. **E010 step-1** — ✅ done s163. Step-2 gated on E009 ≥1 kill.
5. **Watcher v_HP staleness (s156)** — defer.
6. **Cron timing race (s158)** — cosmetic; defer.

---

## Bias for s165

Action ladder:
1. Read world_targets.json + verify schema/freshness.
2. Filter v3 by E009 +30 gate stack.
3. If node-60 candidate passes +30: fire ONE strike (no amendment).
4. If no node-60 ≥+30 BUT node-60 ≥+20 exists: fire amendment A pilot (+20 floor, co-located only).
5. If no node-60 ≥+20 BUT non-co-located cluster passes A+B (≥4 cluster, ≥2 ≥+20, gas ≤25M): dry-run travel; if passes, fire amendment A+B pilot.
6. If neither: defer #3; consider whether snapshot supply is the binding constraint (wait) vs floor itself (relax further) — write to strategic-experiments.md if amendment C is needed.
7. Update E009 counters (defer or N).
8. Schedule next session.
