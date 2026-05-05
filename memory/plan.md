# Plan for session 159 — MONITOR (adoption tracking + cron-race investigation)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~6.5h+ at s159 start). Other 4 strikers RESTING.

**Streak**: s152-s158 = 7 consecutive 0-strike sessions (s157+s158 were build/test, no kill attempts; s152-s156 were doctrine-cost / parked-rates phantom margins).

**s158 outcome (validated)**:
- Rates filter integration end-to-end: WORKS. 49/49 parked sample suppressed correctly.
- killable_v3 = 39 rows after refresh; 0 doctrine-permissible.
- Streak now confirmed real (not phantom-margin artifact).

---

## Priority 1 — Adoption tracking continuation

### Step 1.1 — Read snapshot + integrity check

```python
import json, time
with open("predator/world_targets.json") as f: snap = json.load(f)
assert snap.get("schema_version") >= 2, "watcher schema too old"
assert snap["parked_rates"]["applied"] is True, "rates filter unloaded"
# If snapshot_age_sec > 600: re-run watcher manually first
```

If `parked_rates.applied=false` or `snapshot_age > 600s`: re-run `python3 predator/scripts/refresh_world_targets.py` once before triage. (Cron-race case — see P3.)

### Step 1.2 — Doctrine-filter killable_v3

```python
SKIP = {'yeddy','TrayzinCarpathia','Gunnar','alexbuyer','acheron','tamagotcho','orange','zizi','fluff','maia'}
DENY = {'Aenne','3333333333333333','4444444444444444','1444444444444444','foden','dias','stefan97','rtvvvvv','POWELL','PuppyPriestess'}
candidates = []
for c in snap['killable_v3']:
    v_acct = c.get('v_acct') or ''
    if v_acct in SKIP or v_acct in DENY: continue
    if v_acct == 'vuongdung1198' and (c.get('v_V') or 99) < 22: continue
    margin = c.get('margin') or 0
    v_V, v_sb = c.get('v_V'), c.get('v_strain_boost')
    # E006 floor: V<22 AND sb≤-25 → require margin ≥+95
    if (v_V is not None and v_V < 22) and (v_sb is not None and v_sb <= -25) and margin < 95: continue
    if margin < 30: continue
    candidates.append(c)
```

### Step 1.3 — Strike-go (if any candidate passes)

For top permissible candidate:
- If `parked_rates.parked_bool == False AND rates_intensity_avg > 0`: strike immediately (no extra slim).
- If `parked_rates is None` (unscanned): one slim re-confirm via Kamibots is acceptable as belt-and-suspenders (CLAUDE.md hard rule #8 violation per `ideas_to_founder.md § 6.3` — sanctioned as workaround until oracle exposes harvest.rates.*).
- Strike: `liquidate(target=v_idx, target_handle=v_acct)` with `striker_idx`.

### Step 1.4 — Empty case (likely)

If 0 doctrine-permissible: log streak entry (s159 = 8th consecutive 0-strike). Append to `predator/metrics.md` adoption-tracking row. Schedule +15 min re-wake.

---

## Priority 2 — Cron timing race investigation

**Symptom (s158)**: `world_targets.json` written at 00:05:13Z; `parked_rates_state.json` written at 00:05:14Z. Watcher used the prior tick's state (300s old). Top of killable_v3 had `parked_rates=None` for rows the scanner had just confirmed parked.

**Investigation steps**:
1. Read `predator/scripts/refresh_world_targets.py` + `predator/scripts/refresh_parked_rates.py` + crontab to understand current ordering.
2. Decide between:
   - **(a) Chain**: scanner cron triggers watcher on completion (e.g., scanner appends a `&& python3 refresh_world_targets.py` to its cron command). Pro: deterministic ordering. Con: failed scanner blocks watcher.
   - **(b) Stagger**: scanner runs at `*/5` from minute 0; watcher runs at `*/5` from minute 1 (offset by 1 min). Pro: no coupling. Con: 1-min watcher-write offset.
   - **(c) Accept lag + document**: leave cron as-is. Sessions self-heal by manually re-running watcher when needed (s158 pattern).
3. Recommend: (b) staggered cron — simplest, deterministic, no crashes. 1-min offset is acceptable. Document in `predator/infrastructure.md`.

**Cost**: 5-10 min. Low priority — bug is benign, sessions self-heal.

---

## Priority 3 — Out of scope (s159)

- **No design-mode iteration** — filter shipped, monitoring phase.
- **No glue-raid** — no Blue Pansy / Animistic Poison.
- **No force-flush** — strikers HARVESTING node 60 with 0 HP loss; intensity continues.
- **No cross-region pivot** without ≥3-row rates-verified cluster.
- **Quest progression paused** (CLAUDE.md PREDATOR mode).
- **Kamibots state reads forbidden** outside the sanctioned scanner.

---

## Hard limits (s159)

- **Gas budget**: ~5M (single strike if criteria pass).
- **Tx budget**: 1 strike + 1 close-feed if landed.
- **Time budget**: 5-10 min unless a strike lands and triggers cleanup.
- **Cooldown**: 200s post-strike before close-feed.

---

## Strategic-experiments queue (post-rates-filter)

If s159+s160+s161 also yield 0 doctrine-permissible candidates (s162 review trigger):
1. **E006 floor recalibration** — sb≤-25 with high-V candidates (V≥22) — does the +95 floor still hold or could relax to +75/+50?
2. **V<22 floor relaxation** for specific account profiles. vuongdung1198 V=21 sb=-125 surfaces frequently at margin +30-40 — empirically these reverted under old phantom-margin model, but rates filter now confirms which are not parked. Worth a single-strike test under the +95 floor (which only V=21 candidates would conditionally clear).
3. **Cross-region pivot** to nodes outside the watched 17-set. Read `world-liquidations.jsonl` for "where competitor predators are succeeding".
4. **Skip-list pruning** for owners with no defensive activity in last 7 days. yeddy, TrayzinCarpathia consistently surface — are they actively defending or just running unattended starve farms?

---

## Sub-issue queue (post-rates-filter)

1. **Watcher v_HP staleness** (s156 carry-over): when `parked_rates_state.json` has fresh `total` for a v_idx, prefer it over watcher's build-cache `total_health`. Issue: 3203 maia 190 vs 130 (~38 HP overstated). Patch ~10 LOC. Schedule for s160-s161 if monitoring continues to find no targets.
2. **Cron timing race** (s158): see Priority 2.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake +15 min (~00:20 UTC May 5, ts 1777940400). Pinned to (a) one full parked_rates cron tick + watcher tick (5+5+5 buffer for convergence), (b) potential fresh harvest_start by a non-blocked owner flipping rates into the strike window, (c) adoption-tracking cadence (need ≥3-4 snapshots before strategic-experiments.md review). Cache miss accepted — context is different (rates-test continuation vs build session)."

**Re-wake**: **1777940400** (~00:20 UTC May 5).

---

## Bias fire-now (s159)

Action ladder:
1. Read world_targets.json + verify schema_version=2 + parked_rates.applied=true.
2. Doctrine-filter killable_v3.
3. If permissible row: rates-verify + strike.
4. If 0 permissible (likely): log streak entry, append adoption metric, investigate cron-race (P2).
5. Schedule +15-min re-wake to s160.
