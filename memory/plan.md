# Plan for session 160 — MONITOR + maybe BUILD (coverage-gap fix candidate)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~6.7h+ at s160 start). Other 4 strikers RESTING.

**Streak**: s152-s159 = 8 consecutive 0-strike sessions (s157=build, s158=test, s152-s156+s158-s159 = 7 attempt-eligible 0-strike).

**s159 outcome**: 0 doctrine-permissible across 38 v3 rows. NEW SUB-ISSUE = scanner coverage gap (top-50 published v2 fully parked → 38 v3 rows beyond rank-50 are rates-unknown). Cron stagger doesn't fix. Need v2∪v3 patch.

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
- If `parked_rates.parked_bool == False AND rates_intensity_avg > 0`: strike immediately (no extra slim).
- If `parked_rates is None` (unscanned): one slim re-confirm via Kamibots is acceptable (sanctioned per `ideas_to_founder.md § 6.3`). Especially likely now that coverage-gap is known.
- Strike: `liquidate(target=v_idx, target_handle=v_acct)` with `striker_idx`.

### Step 1.4 — Empty case (likely)

If 0 doctrine-permissible: log streak entry (s160 = 9th consecutive 0-strike). Append adoption metric. Move to P2.

---

## Priority 2 — Scanner coverage-gap fix (build, ~20 LOC)

**Trigger**: ship if P1 is empty AND ≥5 min budget remaining. Otherwise defer to s161.

**Problem**: scanner reads `world_targets["killable_v2"]` (capped to top-50). When all 50 are parked, v3's 38 rows beyond rank-50 are rates-unknown (`parked_rates: None`). Filter is partially blind.

**Fix design (preferred)**: scanner reads `v2 ∪ v3` deduped from published snapshot. Both are top-50 each → up to 100 unique candidates. TOP_N stays sized for the union.

**Patch** (`predator/scripts/refresh_parked_rates.py`):
```python
def load_candidates() -> list[dict]:
    if not WORLD_TARGETS_PATH.exists():
        print("world_targets.json missing — run watcher first", file=sys.stderr)
        return []
    try:
        with open(WORLD_TARGETS_PATH) as f: data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"world_targets.json read error: {e}", file=sys.stderr)
        return []
    v2 = data.get("killable_v2") or []
    v3 = data.get("killable_v3") or []
    # Merge v2 + v3 (v3 first to prioritize fresh non-parked entries)
    seen = set()
    merged = []
    for c in v3 + v2:
        idx = c.get("v_idx")
        if idx is None or idx in seen: continue
        seen.add(idx); merged.append(c)
    return merged
```

Bump `TOP_N` from 50 → 100 (or leave at 50 if v3 prioritization is good enough — lower cost).

**Verify**:
- Run `python3 predator/scripts/refresh_parked_rates.py` manually.
- Run `python3 predator/scripts/refresh_world_targets.py` manually.
- Re-read snapshot: confirm `killable_v3` rows have `parked_rates` populated for ≥80% of entries.

**Document**: append a brief note to `predator/infrastructure.md` § Parked-rates refresher about the v2∪v3 input.

---

## Priority 3 — Out of scope (s160)

- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** — strikers HARVESTING node 60 with 0 HP loss; intensity continues.
- **No cross-region pivot** without ≥3-row rates-verified cluster.
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No cron stagger** — coverage-gap fix supersedes the lower-leverage cron stagger.

---

## Hard limits (s160)

- **Gas budget**: ~5M (single strike if criteria pass) OR 0 (build-only).
- **Tx budget**: 1 strike + 1 close-feed if landed; 0 if no permissible candidate.
- **Time budget**: 5-10 min unless a strike or build extends.
- **Cooldown**: 200s post-strike before close-feed.

---

## Strategic-experiments queue (s162 review trigger)

Currently s158+s159 have 0 doctrine-permissible. If s160+s161 also yield 0, fires at s162:
1. **E006 floor recalibration** — sb≤-25 with high-V (V≥22) — does +95 still hold or relax to +75/+50?
2. **V<22 floor relaxation** for V=21 candidates with rates-confirmed (vuongdung1198 V=21 sb=-125 surfaces frequently +30-40).
3. **Cross-region pivot** beyond watched 17 nodes (read `world-liquidations.jsonl` for competitor success).
4. **Skip-list pruning** for owners with no defensive activity in last 7 days (yeddy, TrayzinCarpathia patterns).

---

## Sub-issue queue (post-rates-filter)

1. **Scanner coverage gap (s159)** — see Priority 2 above. Ship in s160 if P1 empty.
2. **Watcher v_HP staleness (s156)**: when `parked_rates_state.json` has fresh `total` for v_idx, prefer it over watcher build-cache. ~10 LOC. Schedule for s161-s162.
3. **Cron timing race (s158)**: stagger 1-min would clean ordering but doesn't fix coverage. Demoted.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake +20 min (~00:40 UTC May 5, ts 1777941600). Pinned to (a) one full parked_rates cron tick + watcher tick (5+5+5 buffer for convergence); (b) potential fresh harvest_start by a non-blocked owner flipping rates into the strike window; (c) coverage-gap fix shipping window (need ~5 min build + verify)."

**Re-wake**: **1777941600** (~00:40 UTC May 5).

---

## Bias fire-now (s160)

Action ladder:
1. Read world_targets.json + verify schema_v=2 + parked_rates.applied=true.
2. Doctrine-filter killable_v3 (the doctrine logic above).
3. If permissible row: rates-verify + strike.
4. If 0 permissible: ship coverage-gap fix (Priority 2).
5. Schedule +20-min re-wake to s161.
