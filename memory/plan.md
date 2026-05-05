# Plan for session 161 — MONITOR + maybe BUILD (v_HP staleness fix candidate)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~7.0h+ at s161 start). Other 4 strikers RESTING.

**Streak**: s152-s160 = 9 consecutive 0-strike sessions (s157 build, s158 test, s152-s156+s158-s160 = 8 attempt-eligible 0-strike).

**s160 outcome**: 0 doctrine-permissible across 46 v3 rows (skip 4, deny 15, dung_V<22 9, E006 floor 9, sub-30 9). **Coverage-gap fix shipped (commit 75480ae)** — scanner now reads v2∪v3 deduped, TOP_N 100. Validated: 72 candidates/cycle scan, all 72 parked. Coverage convergence in-progress (2 ticks done; 3 more for full sync).

---

## Priority 1 — Adoption tracking continuation

### Step 1.1 — Read snapshot + integrity check

```python
import json
with open("predator/world_targets.json") as f: snap = json.load(f)
assert snap.get("schema_version") >= 2, "watcher schema too old"
assert snap["parked_rates"]["applied"] is True, "rates filter unloaded"
```

If `parked_rates.applied=false`: re-run watcher manually first.

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
- If `parked_rates.parked_bool == False AND rates_intensity_avg > 0`: strike immediately.
- If `parked_rates is None` (unscanned): one slim re-confirm via Kamibots is acceptable (sanctioned per `ideas_to_founder.md § 6.3`).
- Strike: `liquidate(target=v_idx, target_handle=v_acct)` with `striker_idx`.

### Step 1.4 — Empty case (likely)

If 0 doctrine-permissible: log streak entry (s161 = 9th attempt-eligible 0-strike). Move to P2.

**Strategic-experiments review trigger**: if s161 also 0-permissible, **fires at s162** (queue: E006 floor recalibration, V<22 floor relaxation for V=21, cross-region pivot beyond watched 17 nodes, skip-list pruning).

---

## Priority 2 — Watcher v_HP staleness fix (build, ~10-15 LOC)

**Trigger**: ship if P1 empty AND coverage-gap convergence is now stable (≥80% of v3 rows have parked_rates entries) AND ≥5 min budget remaining.

**Problem (s156 carry-over)**: watcher's `v_HP` is computed from `kami_static.total_health` (build cache). When `parked_rates_state.json` has a fresher `total` for the same v_idx (from a recent slim call), it should be preferred. Concrete failure mode: s156 maia 3203 had watcher-claimed v_HP=190 but slim-actual total=130 (38 HP overstatement). Phantom margin would be wider than reality.

**Fix design**: in `refresh_world_targets.py`, after attaching `parked_rates` per row, override `v_HP` (and recompute `margin`) when `parked_rates.total` differs and `parked_rates.last_checked_ts > <build_refresh_cutoff>`. Alternative: surface a separate `v_HP_slim` field for transparency without overriding the existing column.

**Verify**:
- Run `python3 predator/scripts/refresh_world_targets.py` manually post-edit.
- Spot-check a known-stale entry (e.g. recent maia 3203 if surfaced).
- Confirm doctrine triage outputs are consistent (no new permissible candidates appearing solely from corrected v_HP).

**Document**: append a note to `predator/infrastructure.md` § watcher integration section.

---

## Priority 3 — Out of scope (s161)

- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** — strikers HARVESTING node 60 with 0 HP loss; intensity continues.
- **No cross-region pivot** without ≥3-row rates-verified cluster.
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No cron stagger** — demoted; coverage-gap fix supersedes.

---

## Hard limits (s161)

- **Gas budget**: ~5M (single strike if criteria pass) OR 0 (build-only).
- **Tx budget**: 1 strike + 1 close-feed if landed; 0 if no permissible candidate.
- **Time budget**: 5-10 min unless a strike or build extends.
- **Cooldown**: 200s post-strike before close-feed.

---

## Strategic-experiments queue (s162 review trigger)

s158+s159+s160 = 3 consecutive 0-permissible. If s161 also 0-permissible, fires at s162:
1. **E006 floor recalibration** — sb≤-25 with high-V (V≥22) — does +95 still hold or relax to +75/+50?
2. **V<22 floor relaxation** for V=21 candidates with rates-confirmed (vuongdung1198 V=21 sb=-125 surfaces frequently +30-40).
3. **Cross-region pivot** beyond watched 17 nodes (read `world-liquidations.jsonl` for competitor success).
4. **Skip-list pruning** for owners with no defensive activity in last 7 days (yeddy, TrayzinCarpathia patterns).

---

## Sub-issue queue (post-coverage-gap)

1. **Scanner coverage gap (s159)** — ✅ shipped s160 (commit 75480ae). Convergence ticks ongoing.
2. **Watcher v_HP staleness (s156)** — see Priority 2 above. Ship in s161 if P1 empty AND coverage converged.
3. **Cron timing race (s158)** — demoted further. Stagger fix produces 1-tick reduction in convergence latency. Defer to s163+.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake +25 min (~01:05 UTC May 5, ts 1777943100). Pinned to (a) coverage-gap convergence completion (5+ alternating cron ticks across 25 min); (b) potential fresh harvest_start by non-blocked owner flipping rates into strike window; (c) v_HP staleness fix shipping window (~5 min build + verify if P1 empty)."

**Re-wake**: **1777943100** (~01:05 UTC May 5).

---

## Bias fire-now (s161)

Action ladder:
1. Read world_targets.json + verify schema_v=2 + parked_rates.applied=true.
2. Doctrine-filter killable_v3 (the doctrine logic above).
3. If permissible row: rates-verify + strike.
4. If 0 permissible AND ≥80% v3 coverage: ship v_HP staleness fix (Priority 2).
5. Schedule +20-25 min re-wake to s162.
