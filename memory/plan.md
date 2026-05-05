# Plan for session 163 — E009 PILOT-READY (single-strike test if gates pass)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~7.7h+ at s163 start). Other 4 strikers (15540, 6058, 6245, 12225) RESTING. Roster = 7 kamis.

**Streak**: s152-s162 = 11 consecutive 0-strike sessions (3 by-design: s157 build, s158 test, s162 design). **9 attempt-eligible 0-strike**.

**s162 outcome**: strategic-experiments review fired as planned. 2 pilot plays designed:
- **E009** (vuongdung1198 V<22 sb≤-25 single-strike pilot, E001+E006 convergence) — DESIGNED with full gate stack.
- **E010** (mental skip-list collapse, trust watcher heat-check) — HYPOTHESIS, free read step ready.

---

## Priority 1 — E009 PILOT EXECUTION (single strike if gates pass)

### Step 1.1 — Read fresh snapshot

```python
# read predator/world_targets.json (mtime should be <60s old after +10min wake)
# read predator/parked_rates_state.json (mtime should be ≥ world_targets.json — cron race resolves on next tick)
# Verify: schema_version=2, parked_rates.applied=true
# Verify: ≥80% of v3 rows have parked_rates {parked_bool: false_or_true} attached (NOT None)
```

### Step 1.2 — Filter v3 candidates by E009 gates

For each v3 row, ALL must hold:
1. `heat[v_acct].defensive_cycle == False AND anti_predator_automation == False`
2. Row: `fresh_feed_since_start == False AND recent_revive == False`
3. `parked_rates.parked_bool == False` (rates verified non-parked, NOT None)
4. `margin >= +30` (relaxed from +95 floor per E009 design)
5. `guild_blocked == False AND no_touch_owner == False`

Highest-margin row wins. Vuongdung cluster on node 33 typical pick if surfaced.

### Step 1.3 — Co-location decision

- If chosen candidate is at **node 60** (operator's current room): no travel, proceed to step 1.4.
- If chosen candidate is at **node 33** (vuongdung primary): dry-run `travel_to_room(target_room=<node_33_room>, account="bpeon", dry_run=True)`. Compute total gas (travel + 1 strike + return) vs single-obol EV.
  - Gate: gas_cost_round_trip + 1×7M strike < 35M total → fire IF margin/cluster validates EV.
  - **Conservative pick if uncertain**: do NOT travel for a single pilot strike. Instead: re-wake at next tick where node-60 has an E009-eligible candidate, OR plan a multi-strike trip later (need E009 hypothesis confirmed first).

**Default (s163 conservative)**: only fire E009 from current position. If no node-60 candidate passes gates, defer to next session.

### Step 1.4 — Pre-strike live verification (IF pilot fires)

```python
# Verify striker live atk_shift matches oracle-cached
oracle_kami_summary(<striker_idx>)  # check attack_threshold_shift
oracle_sql("SELECT * FROM kami_action WHERE kami_id=<v_idx> AND action_type='kami_feed' AND block_timestamp > NOW()-INTERVAL '5 min'")
# Both checks must pass. If feed action found: ABORT, log to E009 N (N=0 unchanged, gates working).
get_kami_state_slim(<striker_idx>)  # confirm time.cooldown clear, harvesting state
```

### Step 1.5 — Fire and characterize

ONE strike. Log:
- gas_used, success/revert, payout if kill, error message if revert.
- Update E009 N counter in `predator/strategic-experiments.md`.
- Append to `predator/metrics.md`.

If KILL: success counter +1. Continue testing.
If REVERT: pause. Drill `oracle_kami_summary(v_idx)` for missed actions in last 30 min. Document characterization in E009 entry. Do NOT retry until characterization complete.

---

## Priority 2 — E010 step-1 free read (after P1 resolves)

`world-liquidations.jsonl` last 7d filter:
```bash
# tail / grep for victim_account in {yeddy, TrayzinCarpathia, tamagotcho, Gunnar, alexbuyer, acheron, orange, zizi, fluff, maia}
# Any non-self kills against these owners = external evidence the watcher's clean signal is correct
```

If competitor predators ARE landing kills against mental-skip-list owners → strong signal to drop the list. Append finding to E010 entry. **No strikes from this read** (gated on E009 ≥1 kill).

---

## Priority 3 — Out of scope (s163)

- **No glue-raid** (no Blue Pansy / Animistic Poison still).
- **No force-flush** — strikers HARVESTING node 60.
- **No E010 strikes** (gated on E009 ≥1 kill first).
- **No cross-region pivot for 1 candidate** — only consider 60→33 if cluster math clears 35M-gas threshold AND E009 hypothesis confirms.
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No v_HP staleness fix** (defer).
- **No cron timing race fix** (defer).

---

## Hard limits (s163)

- **Gas budget**: ≤10M (single pilot strike, ~7M expected).
- **Tx budget**: 1 strike (pilot) + any pre-strike spot-checks (read-only).
- **Strike count**: 1 (pilot only — no chains, no batches).
- **Time budget**: 10-15 min for read + filter + decision + (maybe) strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s163): "Re-wake +10 min (already scheduled at s162) pinned to (a) parked_rates cron tick converging so v3 has rates_attached, (b) E009 pilot fires immediately if any row passes gates, (c) post-pilot characterization needs ≥1 cron tick before next attempt."

**Re-wake target after s163**:
- If pilot KILLED: +10-15 min for strike cooldown + next snapshot tick (chain another E009 attempt if eligible).
- If pilot REVERTED: +30-40 min — do NOT re-attempt until characterization documented; use the time for E010 step-1 read + investigation.
- If pilot DEFERRED (no eligible candidate): +10-15 min — fire-now bias; world refresh likely surfaces a fresh row.

---

## Sub-issue queue (post-s162)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 + E010 pilot execution** — **PRIMARY for s163+**.
3. **Watcher v_HP staleness (s156)** — defer (lower leverage than pilots).
4. **Cron timing race (s158)** — cosmetic; defer.
5. **Cross-region pivot to node 33 vuongdung cluster** — gate on E009 ≥3 kills before considering the multi-strike trip.

---

## Bias for s163

Action ladder:
1. Read world_targets.json + verify schema/rates_attached.
2. Filter v3 by E009 gate stack.
3. If node-60 candidate passes: pre-strike live verify → fire ONE strike → log.
4. If only node-33 candidate passes: defer (don't travel for single pilot); re-wake.
5. If no candidate passes: E010 step-1 read → log finding → re-wake.
6. Update E009/E010 entries with N or finding.
7. Schedule next session.
