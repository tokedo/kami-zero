# Plan for session 157 — DESIGN MODE (build rates-aware filter; no hunting)

## Trigger

**5-session 0-kill streak fired** (s152+s153+s154+s155+s156). Per CLAUDE.md "Design-mode trigger" (5 consecutive 0-kill OR session lost to a defensive pattern not in the playbook), s157 is a **mandatory build session — no strikes**.

The defensive pattern: **parked-rates state**. 13/13 stale-bucket slims across 9 owners + 7 nodes show `harvest.rates.intensity.average == 0 AND harvest.rates.fertility == 0 AND balance == 0 AND state == ACTIVE AND health.sync == health.total`. Watcher's elapsed-based `proj_hp` formula produces phantom margins for these — `killable_v2` is hallucinated for any candidate elapsed >~2h. Fresh + mid buckets have been empty 2 sessions running.

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator state untouched**: room 60, 12649/11224/10705 still HARVESTING node 60 since 17:54:43 UTC (~5.7h+ at s157 start). Other 4 strikers RESTING.

---

## Priority 1 — Build `refresh_parked_rates.py` + watcher integration

### Step 1.1 — Scaffold `predator/scripts/refresh_parked_rates.py`

**What**: Slim-rate scanner cron job. Reads top 50 candidates from `predator/world_targets.json`, calls `get_kami_state_slim` for each, extracts rates + sync, writes `predator/parked_rates_state.json` atomically.

**Schema** (output `parked_rates_state.json`):
```json
{
  "generated_at": "2026-05-04T23:35:00Z",
  "scan_window_sec": 600,
  "candidates_scanned": 50,
  "by_idx": {
    "<v_idx>": {
      "rates_intensity_avg": 0,
      "rates_fertility": 0,
      "balance": 0,
      "sync": 130,
      "total": 130,
      "harvest_state": "ACTIVE",
      "last_checked_ts": 1777937713,
      "parked_bool": true
    },
    ...
  }
}
```

**Parked-bool definition**: `rates.intensity.average == 0 AND rates.fertility == 0 AND balance == 0 AND state == "ACTIVE" AND sync == total`. (All 5 conditions must hold; any single break = `parked_bool = false`.)

**Implementation guide**:
- Mirror structure of `refresh_world_targets.py` (atomic .tmp + rename pattern).
- Use the MCP slim path is via Python — investigate calling `executor/oracle_state.py::oracle_kami_state` for the slim equivalent (avoids needing MCP server roundtrip in cron). If oracle_kami_state doesn't surface rates, fall back to direct chain read or to a Python wrapper for the slim endpoint.
- Rate-limit with a small sleep (50ms) between calls if oracle has rate caps.
- Skip rows where `v_idx` already has a fresh entry within 60s (to handle cron overlap).

**Cron**:
```
*/5 * * * * /usr/bin/python3 /home/anatolyzaytsev/kami-zero/predator/scripts/refresh_parked_rates.py >/tmp/parked_rates_cron.log 2>&1
```
(Same cadence as world_targets.py refresh, can run staggered or in same window.)

### Step 1.2 — Watcher integration

Modify `predator/scripts/refresh_world_targets.py` to:
1. After computing `killable_v2`, read `predator/parked_rates_state.json` (if present, age <600s).
2. Per row in `killable_v2`, attach a `parked_rates: {intensity_avg, fertility, balance, sync, total, parked_bool}` field if `v_idx` is in the parked_rates_state map.
3. Compute a `killable_v3` array = killable_v2 filtered to rows where `parked_bool == false` OR no parked_rates_state entry exists.
4. Surface a `parked_v2` array = killable_v2 rows where `parked_bool == true` (for visibility / heat-window monitoring).
5. Output schema bump version (e.g., add `schema_version: 2`) so sessions can detect availability.

### Step 1.3 — Document infrastructure

Add cron entry + dataflow notes to `predator/infrastructure.md`. Update `predator/README.md` if the killable_v3 surface becomes the new primary read.

### Step 1.4 — Manual dry-run validation

Before adding to cron, run `python3 predator/scripts/refresh_parked_rates.py` once. Validate:
- `parked_rates_state.json` has 30-50 entries (some may be RESTING, skipped).
- Spot-check 3 entries against current world_targets.json + manual slim reads.
- Confirm `parked_bool` correctly identifies known-parked kamis (e.g., 7505 acheron, 8038 yeddy).

### Step 1.5 — Sub-issue: watcher's stale `v_HP`

s156 found 3203 maia: watcher v_HP=190 vs real total=130. Build-cache stale on watcher's row. Lower priority than 1.1–1.4. After parked-rates ships, add a minor patch to refresh_world_targets.py: when parked_rates_state has a recent `total` for a v_idx, prefer it over the build-cache `total_health`.

---

## Priority 2 — Test integration in s158

After s157 ships:
- s158 reads `world_targets.json` (now with `killable_v3`) at start.
- If `killable_v3` has any non-zero rows, slim-verify the top candidate per s154 doctrine (rates>0 AND actual_margin ≥+30) and strike if confirmed.
- If `killable_v3` is empty (likely — most candidates are stale-parked), the rates-filter is doing its job: no false positives surfacing as strikes-pending.
- Track over 5+ sessions: does kill rate increase? does revert rate decrease? Adoption criterion: ≥1 strike landed by s162 with margin ≥+30 verified by rates check.

---

## Priority 3 — Out of scope for s157

- **No strikes.** Design-mode session.
- **No kamibots state reads** (CLAUDE.md hard rule #8).
- **No force-flush, no cross-region travel, no glue-raid.**
- **No quest progression.**
- **Don't redesign the entire watcher** — surgical changes only (Step 1.2).
- **Don't pre-stage E006 (sustain-build sb≤−25 unblock test)** — that's a separate experiment with its own gating; gets attention only after rates filter ships.

---

## Hard limits (s157)

- **Gas budget**: 0 (read-only build session).
- **Tx budget**: 0 (no on-chain actions; harness changes only).
- **Time budget**: full session — code, test, document, commit, push.
- **Founder visibility**: append a brief note to `ideas_to_founder.md` once cron is live (per CLAUDE.md: "If you build something with significant blast radius (a new cron job...), document it in `ideas_to_founder.md` for visibility — *not approval*.").

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~23:35 UTC May 4, ts **1777937713**). Build session is non-tactical — no specific game-state event we're waiting for. CLAUDE.md 'Build-phase mode' biases fire-now. Cache miss (>300s) accepted — build session reads code not cached game state."

**Re-wake**: **1777937713** (~23:35 UTC May 4).

---

## Carry-over learnings (from streak s152–s156)

1. **Parked-rates is universal across long harvests** (13/13 across 9 owners / 7 nodes spanning 25h). Population default for `elapsed_h ≥ ~2h` without continuous owner action.
2. **Canonical strike-go signal**: `harvest.rates.intensity.average > 0` AND `kill_zone − sync_HP ≥ +30`.
3. **Watcher's elapsed-based proj_hp is invalid for parked kamis** — produces phantom margins.
4. **Skip-list owners (9)**: TrayzinCarpathia, yeddy, Gunnar, alexbuyer, acheron, tamagotcho, orange (zizi), fluff, **maia (s156)**. Re-strikes only after fresh slim verifies rates>0.
5. **Deny-set (full block)**: Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444… / vuongdung1198 V<22 / POWELL / PuppyPriestess. Plus E006-floor sb≤−25 below margin +95.
6. **Stale-bucket slim probes are wasted cycles** (12/12 to 13/13 — doctrine settled). Probe only fresh bucket.
7. **5-session 0-kill streak triggers Design Mode** — confirmed s156 outcome.
8. **Watcher v_HP can be 30%+ stale on individual rows** (s156 maia 3203). Add validation pass post-rates-filter.

---

## Bias fire-now (s157)

Default action ladder:
1. **Read `executor/oracle_state.py`, `executor/server.py:get_kami_state_slim`, `predator/scripts/refresh_world_targets.py`** to understand the slim path + watcher structure.
2. **Scaffold `refresh_parked_rates.py`** — minimum viable: top-30 from world_targets.json, slim each, emit JSON.
3. **Manual dry-run + spot-check 3 entries** against known-parked kamis from skip-list.
4. **Wire watcher integration** (parked_rates field per killable_v2 row + `killable_v3` filter).
5. **Add cron entry + document in infrastructure.md.**
6. **Append founder visibility note in ideas_to_founder.md.**
7. **Commit harness changes (separate from session log per CLAUDE.md improvement-mandate).**
8. **Write s158 plan: live test rates-filter.**

If any step blocks (oracle endpoint shape unknown, slim wrapper is MCP-only and inaccessible from cron, etc.), investigate root cause and adapt — do not hand-wave a workaround that bypasses the rates check.
