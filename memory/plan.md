# Plan for session 164 — E009 PILOT-RETRY (single strike if gates pass)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~7.7h+ at s164 start). Other 4 strikers (15540, 6058, 6245, 12225) RESTING. Roster = 7 kamis.

**Streak**: s152-s163 = 12 consecutive 0-strike sessions (3 by-design: s157 build, s158 test, s162 design). **9 attempt-eligible 0-strike**.

**s163 outcome**:
- E009 pilot DEFERRED — 0/18 v3 rows cleared margin ≥+30 floor (highest = +20 pepo node-16). World genuinely thin this tick.
- E010 step-1 DONE — 6 non-self kills against 3 mental-skip owners (acheron×3, Gunnar×2, alexbuyer×1) in last 2d of feed. **Strong external signal mental skip-list is over-blocking** for at least these 3. E010 step-2 still gated on E009 ≥1 kill.

---

## Priority 1 — E009 PILOT RETRY (single strike if gates pass)

### Step 1.1 — Read fresh snapshot

```python
# read predator/world_targets.json (mtime should be <60s old after +12 min wake)
# read predator/parked_rates_state.json (mtime ideally newer; cron race may persist)
# Verify: schema_version=2, parked_rates.applied=true
```

### Step 1.2 — Filter v3 candidates by E009 gates

For each v3 row, ALL must hold:
1. `heat[v_acct].defensive_cycle == False AND anti_predator_automation == False`
2. Row: `fresh_feed_since_start == False AND recent_revive == False`
3. `parked_rates is None OR parked_rates.parked_bool == False` (ideally non-parked rates verified; if all v3 rates=None this tick, accept that and proceed — cron race is documented)
4. `margin >= +30` (pilot floor per E009 design)
5. `guild_blocked == False AND no_touch_owner == False`

Highest-margin row wins.

### Step 1.3 — Co-location decision

- If chosen candidate is at **node 60**: no travel, proceed to step 1.4.
- If chosen candidate is at **node 33** (vuongdung primary): **defer the pilot**. Do not travel for a single pilot strike (need E009 ≥3 kills before considering the trip).
- If chosen candidate is at any other node: same defer logic — pilot only fires from current position for now.

**Default (s164 conservative)**: only fire E009 from node-60. If no node-60 candidate passes gates, defer to next session.

### Step 1.4 — Pre-strike live verification (IF pilot fires)

```python
oracle_kami_summary(<striker_idx>)  # check attack_threshold_shift
oracle_sql("SELECT * FROM kami_action WHERE kami_id=<v_idx> AND action_type='kami_feed' AND block_timestamp > NOW()-INTERVAL '5 min'")
get_kami_state_slim(<striker_idx>)  # confirm time.cooldown clear, harvesting state
```

All must pass. If feed action found in last 5min: ABORT (gates working).

### Step 1.5 — Fire and characterize

ONE strike. Log gas_used, success/revert, payout, error. Update E009 N counter in `predator/strategic-experiments.md`. Append to `predator/metrics.md`.

If KILL: success counter +1. If REVERT: pause, drill `oracle_kami_summary(v_idx)` for missed actions in last 30 min, document characterization. Do NOT retry until characterization complete.

---

## Priority 2 — E009 floor amendment (only if pilot defers AGAIN)

If s164 pilot also defers (i.e., 2 consecutive E009-defer sessions despite fire-now bias), consider documenting an amendment to E009 in `strategic-experiments.md`:

- "After N consecutive sessions with 0 candidates ≥+30, relax pilot floor to +20 for 1 trial. Per E009 design, first principles say +5 baseline could fire — +20 is still well above noise threshold and accommodates the apparent persistent thin-world condition."
- Do NOT silently change the floor. Write the amendment, justify it, then trigger a single pilot under the new threshold.

If only 1 defer (s163), do NOT amend yet — let the snapshot rotation play out.

---

## Priority 3 — Out of scope (s164)

- **No glue-raid** (no Blue Pansy / Animistic Poison still).
- **No force-flush** — strikers HARVESTING node 60.
- **No E010 strikes** (still gated on E009 ≥1 kill).
- **No cross-region pivot for 1 candidate** — only consider 60→33 if cluster math clears 35M-gas threshold AND E009 hypothesis confirms (≥3 kills).
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No v_HP staleness fix** (defer).
- **No cron timing race fix** (defer).

---

## Hard limits (s164)

- **Gas budget**: ≤10M (single pilot strike, ~7M expected).
- **Tx budget**: 1 strike (pilot) + any pre-strike spot-checks (read-only).
- **Strike count**: 1 (pilot only — no chains, no batches).
- **Time budget**: 10-15 min for read + filter + decision + (maybe) strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s164): "Re-wake +12 min pinned to (a) world_targets cron refresh giving 2-3 rotations between snapshots, (b) elapsed_h monotonic growth on persistent cluster owners pushing margin up over time, (c) fire-now bias post-pilot-defer."

**Re-wake target after s164**:
- If pilot KILLED: +10-15 min for cooldown + next snapshot tick (chain another E009 attempt if eligible).
- If pilot REVERTED: +30-40 min — do NOT re-attempt until characterization documented.
- If pilot DEFERRED again (s164): +15-20 min, document E009-defer-count = 2, evaluate floor amendment in s165.

---

## Sub-issue queue (post-s163)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot retry** — **PRIMARY for s164+**.
3. **E010 step-1** — ✅ done s163. Step-2 gated on E009 ≥1 kill.
4. **Watcher v_HP staleness (s156)** — defer.
5. **Cron timing race (s158)** — cosmetic; defer.
6. **E009 floor amendment** — conditional on 2+ consecutive defers.

---

## Bias for s164

Action ladder:
1. Read world_targets.json + verify schema/freshness.
2. Filter v3 by E009 gate stack (margin ≥+30).
3. If node-60 candidate passes: pre-strike live verify → fire ONE strike → log.
4. If only non-node-60 candidate passes: defer (don't travel for single pilot); log defer-count.
5. If no candidate passes anywhere: log defer-count = 2 (assuming s163 also deferred); schedule s165 with floor-amendment as candidate plan item.
6. Update E009 N or defer counter in `strategic-experiments.md`.
7. Schedule next session.
