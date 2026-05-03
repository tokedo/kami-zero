# Plan for session 106 — TC ripening + foden cycle break test, killable_v2 P0

## Context (post-session 105)

**0 KILLS, 0 gas — Scenario D doctrine-discipline hold (3rd consecutive zero-tx).** killable_v2 surfaced exactly 1 candidate (davinchieth 10838 +27 single-target) — rule #4 deny. TC node 60 zero-travel cluster has wiuuuu 1750 +1 ripening but won't cross +25 chain-floor in 35 min. foden cluster on node 60 newly mapped as defensive (34 bulk-stops/6h — heaviest signal).

**Lifetime kills: 25 (unchanged).**

**End state**: operator + 11224 (140/140 RESTING) + 12649 (170/170 close-fed RESTING) at room 60. Stamina ~73 SP. Inventory: 25 obols, 466 cookies, 65 ice creams.

---

## Priority 0 — READ killable_v2 FIRST (now production-validated)

`predator/world_targets.json`:
- `killable_v2` — heat-check filtered (defensive_cycle=False). **First-pass list — used in session 105.**
- `killable_clean` — legacy. Use only if killable_v2 empty AND specific edge-case applies.
- `owner_heat` — per-owner heat map. Inspect when nuance is needed.

**Hard rule (production-validated session 105)**: iterate `killable_v2` first. Session 105 confirmed it surfaces exactly the honest candidates. Trust the filter.

**Pre-pivot heat-check v2** still applies: even if killable_v2 shows a candidate, if it's the first kill on a new dominant farmer in 24h, re-check `owner_heat` for that owner before committing the migration tx.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Should be ≤5 min old.
2. **TC cluster (node 60)** — wiuuuu 1750 cycle resolution: at session 105 start +1 / 2.22h elapsed → cycle ~3h average → expected auto-stop ~09:00-09:25 UTC. If stopped, room for new wiuuuu cycle entries (1599 at 0.22h elapsed → ~3h to ripen). If alive at +6+ margin, still below chain-floor — wait.
3. **foden cluster** (node 60, defensive_cycle=True session 105) — check if `owner_heat["foden"].defensive_cycle` flips False or bulk_stop_windows_6h drops below 3. 34 bulk-stops/6h is highest signal observed; sustained or decaying?
4. **stefan97** — `owner_heat["stefan97"].defensive_cycle` should still be True. If flips False (≥4h idle gap + no bulk-stops), Scenario D unlocks for stefan97 cluster.
5. **Stamina** — ~73 SP. Natural regen ~0.5/min → ~88 in +30 min, +100 in +60 min.

---

## Priority 2 — Strike scenarios by `killable_v2` state at session 106 start

### Scenario A: TC @ node 60 has ≥1 above-gate (margin ≥ +25)
- Zero-travel. Pre-pivot heat-check v2 should auto-pass for TC (auto-cycle pattern).
- Single-strike (margin ≥ +25 floor). Chain-strike if 2nd target also above +26 (production-confirmed gate).
- Gas budget: ~10-12M for 1-kill, ~17-22M for 2-kill chain.

### Scenario B: ≥2 above-gate at any other reachable cluster
- Migration ~15-20M (16 hops + 1-2 ice creams).
- Single-target → reject (rule #4).
- 2+ above-gate clean candidates → migrate AFTER computing total-tx cost ratio (must clear ~0.06 obols/Mgas to avoid degrading rolling avg).

### Scenario C: foden defensive cycle clears
- foden has been a node 60 fixture; if defensive_cycle flips False AND bulk_stops drop < 3, scan top10 for above-gate kills. Zero-travel (already at 60).
- Same gate rules apply.

### Scenario D: stefan97 defensive cycle clears
- Re-evaluate full stefan97 above-gate cluster at node 86. Migrate 60→86 (~16 hops, ~17-19M travel).
- Live re-check `owner_heat["stefan97"]` immediately before strike.

### Scenario E: All clusters dry (`killable_v2` empty or single-target only)
- Wait at 60. Re-wake +60 min (escalate from +35) AND use the time for hot-node expansion build (P4).

---

## Priority 3 — Hard limits

- **Gas budget session 106**: 25M (zero-travel scenarios). Migration scenarios 30M ceiling.
- **No tx if striker HP <80% max_hp** unless 1 cookie pre-feed first.
- **2 reverts in a row → end session.**
- **stefan97 + foden deny-all** until `owner_heat[X].defensive_cycle == False`.
- **Read `killable_v2` first** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action.
- **Session length cap**: ≤25 min wall-clock.
- **Rule #4 inviolable**: no cross-region travel for a single target.
- **3+ consecutive zero-tx sessions = consider hot-node expansion build** (P4 ask).

---

## Priority 4 — Build asks (deferred, async)

- **Hot-list expansion** — current 8 nodes (86, 60, 73, 25, 62, 9, 30, 82). After 3 consecutive Scenario D/E sessions, this is the highest-leverage next build. Heat-check noise-suppression makes wider scans cheap. Target: extend to 15-20 nodes covering more SCRAP/EERIE/SPECTRAL biomes. Implementation: add to `predator/scripts/refresh_world_targets.py` `HOT_NODES` list.
- **Stale-cycle detection in heat-check** — current criterion #2 is "≥3 bulk-stop windows in past 6h". Consider `cooling_cycle` field for owners trending toward un-blacklist. Defer until misfire observed.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency.
- **A/B test infrastructure** — split kamis between TC stake-out vs. roving-strikes once Scenario E runs become routine.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 106 also yields zero kills AND killable_v2 single-target/empty entire session, escalate to +60 min re-wake AND devote session 107 wall-clock to hot-node expansion build (P4 top item).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "wiuuuu 1750 cycle approaching 3h elapsed (auto-stop expected ~09:00-09:25 UTC) clears bait + lets short-cycle wiuuuu 1599 ramp from 0.22h elapsed. foden defensive-cycle test: 34 bulk-stops/6h is heaviest signal — observe decay (or persistence) at next watcher cycle. Watcher refreshes 7 cycles in 35 min. killable_v2 second-read."

**Re-wake**: +35 min from session end (~09:28 UTC, timestamp 1777800300).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 25 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 absent owner_heat clearance.
- Engaging foden absent owner_heat clearance.
- Migrating for single targets.
