# Plan for session 158 — LIVE TEST: rates-aware filter armed

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC (~6h+ at s158 start). Other 4 strikers RESTING.

**s157 shipped**:
- `predator/scripts/refresh_parked_rates.py` (cron 5-min) — slim-rate scanner.
- `predator/scripts/refresh_world_targets.py` integration — adds `killable_v3` (rates-filtered), `parked_v2` (visibility), `parked_rates` per-row field, `schema_version=2`.
- Cron entry registered.
- Documented in `predator/infrastructure.md`; visibility note in `ideas_to_founder.md § 6a`.

---

## Priority 1 — Live test: read killable_v3 first

### Step 1.1 — Read `world_targets.json`

```python
import json
with open("predator/world_targets.json") as f: snap = json.load(f)
assert snap.get("schema_version", 1) >= 2, "watcher schema too old; cron may be down"
assert snap["parked_rates"]["applied"] is True, "rates filter unloaded — fall back to legacy slim-verify"
```

If `parked_rates.applied=false` or `snapshot_age_sec > 600`: fall back to legacy doctrine — slim-verify rates per candidate before strike.

### Step 1.2 — Triage `killable_v3` top 10 by margin

```python
for c in snap["killable_v3"][:10]:
    pr = c.get("parked_rates")
    # Apply doctrine: V≥22 OR sb≥-25 (E006 floor for sb<-25 is +95)
    # Not skip-list owners (yeddy, TrayzinCarpathia, Gunnar, alexbuyer,
    #   acheron, tamagotcho, orange/zizi, fluff, maia)
    # Not deny-set (Aenne, 3333…/4444…/1444…, foden, dias, stefan97,
    #   rtvvvvv, vuongdung1198 V<22, POWELL, PuppyPriestess)
    # Not guild_blocked, no_touch_owner, fresh_feed_since_start
    ...
```

### Step 1.3 — Strike-go criteria (in order)

A row strikes if ALL hold:
1. `margin >= 30` (watcher's elapsed-projected margin, sanity floor)
2. `parked_rates` is non-null AND `parked_bool == false` AND `rates_intensity_avg > 0` — **canonical rates-go signal**
3. `parked_rates.rates_aware_margin >= 30` if available (sync-based real margin) — belt-and-suspenders
4. Doctrine-permissible (above filters)
5. **Belt-and-suspenders slim-verify** — cron snapshot can be ≤300s old; one fresh slim re-confirms before strike. Cost: ~free.

If a row satisfies all 5: `liquidate(target=v_idx, target_handle=v_acct)` from striker `striker_idx`.

### Step 1.4 — Empty case

If `killable_v3` empty OR no row passes the strike-go criteria:
- That's NOT a failure of the filter; it's the filter doing its job (correctly suppressing phantom margins).
- Write streak-continuation entry (s158 = 6th 0-kill, now post-design-mode).
- Schedule **short re-wake** (15 min) — fresh harvest_starts can flip rates into the strike window briefly.

### Step 1.5 — Validate the integration end-to-end

While we're here, also verify:
- `parked_v2` non-empty (confirms cron is sampling and the filter is suppressing phantoms).
- `parked_rates_state.json` modified within last 10 min (cron healthy).
- Spot-check 1 row in `parked_v2` against a fresh manual slim — fields match.

---

## Priority 2 — Adoption tracking (s158-s162)

Per plan-156 P2 adoption criterion:
- ≥1 strike landed by s162 (5 sessions from now) with margin ≥+30 verified by rates check, no revert.
- Or: zero strikes but at least one confirmed-non-parked candidate that passed doctrine and was striked → measure landed/reverted.

If by s162 still 0 strikes AND killable_v3 always empty: parked-rates is universal across the entire surfaced population, not just our sample. Time to investigate **counter-mechanisms**:
- Animistic Poison test (gated on Blue Pansy supply, ideas_to_founder § 5a) — does STRAIN+50% un-park a kami?
- Cross-region pivot to nodes we haven't been scanning.
- Operator presence as deterrent (defensive cycle triggers).

---

## Priority 3 — Out of scope (s158)

- **No design-mode iteration this session** — design-mode shipped in s157, s158 tests it.
- **No glue-raid** — no Blue Pansy in inventory, no Animistic Poison crafted.
- **No force-flush** — strikers HARVESTING node 60 with no HP loss; intensity continues.
- **No cross-region pivot** without ≥3-row rates-verified cluster.
- **Quest progression paused** (CLAUDE.md PREDATOR mode).

---

## Hard limits (s158)

- **Gas budget**: ~5M (single strike if criteria pass).
- **Tx budget**: 1 strike + 1 close-feed if landed.
- **Time budget**: 5–10 min unless a strike lands and triggers cleanup.
- **Cooldown**: 200s post-strike before close-feed (predator/mechanics doctrine).

---

## Sub-issue queue (post-rates-filter)

1. **Watcher v_HP staleness** — when `parked_rates_state.json` has fresh `total` for a v_idx, prefer it over watcher's build-cache `total_health`. Issue surfaced s156 (3203 maia 190 vs 130, ~38 HP overstated). Patch ~10 LOC; 5–10 min build. Schedule for s159 if s158 lands a strike (positive momentum to follow).
2. **Killable_v3 should also flag `no_entry(unscanned)`** — currently rendered as nullable. Document so sessions know to slim-verify these rows manually until the next cron tick covers them. Already covered by belt-and-suspenders rule above.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~00:03 UTC May 5, ts **1777939404**). Pinned to (a) parked_rates cron convergence (1 full tick + watcher tick + next tick), (b) live-test of rates-aware filter, (c) potential fresh-harvest opportunism. Cache miss (>300s) accepted."

**Re-wake**: **1777939404** (~00:03 UTC May 5).

---

## Bias fire-now (s158)

Action ladder:
1. Read world_targets.json + verify schema_version=2 + parked_rates.applied=true.
2. Triage killable_v3 top 5 by doctrine-permissible criteria.
3. For top doctrine-permissible row: slim-verify (belt-and-suspenders), strike if rates>0 AND actual_margin ≥+30.
4. If empty: write streak-continuation note, log infrastructure validation results, schedule +15-min re-wake to s159.
5. Track adoption metric in `predator/metrics.md` after the session.
