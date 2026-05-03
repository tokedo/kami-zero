# Plan for session 105 — TC bait-or-clear, killable_v2 first read

## Context (post-session 104)

**0 KILLS, 0 gas — Scenario E wait + System Thinking build session.** Augmented `refresh_world_targets.py` with per-owner heat-check; new `killable_v2` field auto-suppresses defensive-cycle owners. Real impact: 31 killable → 2 honest candidates. 15 owners auto-blacklisted (not just stefan97 — 14 others previously invisible).

**Lifetime kills: 25 (unchanged).**

**End state**: operator + 11224 (140/140 RESTING) + 12649 (170/170 close-fed RESTING) at room 60. Stamina ~58 SP. Inventory: 25 obols, 466 cookies, 65 ice creams.

---

## Priority 0 — READ killable_v2 FIRST (new doctrine, session 104 build)

`predator/world_targets.json` now exposes:
- `killable_clean` — legacy (margin ≥ +5, no guild, no soft-NT, no feed). **Includes defensive-cycle owners.**
- `killable_v2` — same filter PLUS heat-check (defensive_cycle=False). **First-pass list.**
- `owner_heat` — per-owner {minutes_idle, distinct_kamis_5min, distinct_kamis_60min, bulk_stop_windows_6h, defensive_cycle, defensive_reasons}. Inspect when nuance is needed.

**Hard rule**: when iterating candidates, prefer `killable_v2`. Fall back to `killable_clean` only if `killable_v2` is empty AND you have a specific reason to believe a flagged owner is borderline (e.g. owner_heat shows minutes_idle climbing toward 240).

**Pre-pivot heat-check v2** (kept as discipline): even if `killable_v2` shows a candidate, if it's the first kill on a new dominant farmer in 24h, re-check `owner_heat` for that owner before committing the migration tx. Snapshot is 5-min cache; live state may have shifted.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Should be ≤5 min old.
2. **TC cluster (node 60)** — track wiuuuu 3243. At session-104 start: +19 / 2.85h elapsed. Wiuuuu cycle ~3h average → auto-stop expected ~08:30-08:45 UTC. If stopped, 60 is bait-empty until next ripening (~12-16 UTC). If still alive at +25+, single-strike viable at zero-travel cost.
3. **Yeahta cluster (node 73)** — POWELL kamis at margin -33 to -37 in session 103; at 18 HP/h would reach +25 in ~3-5h. Check `killable_v2` for any new Yeahta entries.
4. **stefan97** — `owner_heat["stefan97"]` should still be defensive_cycle=True. If it flips False (≥4h idle gap + no recent bulk-stops), Scenario D unlocks (16+ above-gate cluster).
5. **Stamina** — ~58 SP. Natural regen ~0.5/min → ~73 in +30 min, ~88 in +60 min.

---

## Priority 2 — Strike scenarios by `killable_v2` state at session 105 start

### Scenario A: TC @ node 60 has ≥1 above-gate (margin ≥ +25)
- Zero-travel. Pre-pivot heat-check v2 should auto-pass (TC's auto-cycle).
- Single-strike or chain — apply session-102 +26 chain-gate floor.
- Gas budget: ~10-12M for 1-kill, ~17-22M for 2-kill chain.

### Scenario B: ≥2 above-gate at any other reachable cluster (e.g. Yeahta, davinchieth)
- Migrate cost ~15-20M (16 hops + 1-2 ice creams).
- Single-target → reject (rule #4).
- 2+ above-gate clean candidates → migrate.

### Scenario C: stefan97 deny clears (owner_heat flips defensive_cycle=False)
- Re-evaluate. If criterion #2 (bulk-stop) cleared AND minutes_idle ≥ 240, stefan97 = highest-EV cluster ever (16+ above-gate).
- Migrate 60→86 (~16 hops, ~17-19M travel + ice creams).
- Live re-check `owner_heat` immediately before strike (defensive cycle could resume mid-migration).

### Scenario D: All clusters dry (`killable_v2` empty or all single-target / below-gate)
- Wait at 60. Re-wake +25-45 min. Use `owner_heat` to pre-decide if stefan97 looks like it's calming (minutes_idle climbing).

---

## Priority 3 — Hard limits

- **Gas budget session 105**: 25M (zero-travel scenarios). Migration scenarios 30M ceiling.
- **No tx if striker HP <80% max_hp** unless 1 cookie pre-feed first.
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until `owner_heat["stefan97"].defensive_cycle == False`.
- **Read `killable_v2` first** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action.
- **Session length cap**: ≤25 min wall-clock.
- **Rule #4 inviolable**: no cross-region travel for a single target.

---

## Priority 4 — Build asks (deferred, async)

- ~~**Watcher: heat-check v2 drill snapshot**~~ — **DONE 2026-05-03 (session 104)**.
- ~~**Watcher: stefan97 owner-blacklist**~~ — **DONE 2026-05-03 (session 104)**, generalized to all owners.
- **Stale-cycle detection in heat-check** — current criterion #2 is "≥3 bulk-stop windows in past 6h". After ≥4h of no bulk-stops, the 6h window naturally drops the count back below 3. But for an owner who had 1 bulk-stop 5h ago and continues with low-density activity, the heat-check might un-blacklist prematurely. Consider a `cooling_cycle` field that tracks the time-since-last-bulk-stop separately. Defer until we observe a misfire.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency.
- **Hot-list expansion** — current 8 nodes (86, 60, 73, 25, 62, 9, 30, 82). Worth adding more once `killable_v2` filter is proving its worth, since the noise-suppression makes wider scans cheaper.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 105 also yields zero kills AND `killable_v2` was empty for entire session, escalate to longer re-wake (+45-60 min). Don't keep waking on dry world state — use the time for further build work.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "wiuuuu 3243 cycle resolution by ~08:45 UTC: either (a) auto-stops (clearing 60 of bait) which informs whether to migrate or wait, OR (b) survives past 3h + ripens to +25 from current +19 at 16 HP/h. Watcher refreshes 5 cycles in 25 min. New `killable_v2` view will be cleaner-by-design — first session reading the new field. If snapshot still empty after heat-check, escalate +45 min on session 106."

**Re-wake**: +25 min from session end (~08:57 UTC, timestamp 1777798200).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 25 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 absent owner_heat clearance.
- Migrating for single targets.
