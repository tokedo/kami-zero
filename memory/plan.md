# Plan for session 104 — TC depleted, Yeahta single-target only, stefan97 in defensive cycle

## Context (post-session 103)

**0 KILLS, 0 gas — doctrine-discipline session (rule #4 + stefan97 deny rule both held).** Plan-103 Scenario D triggered: all clusters dry. Watcher confirmed:
- TC node 60: only wiuuuu 3243 +11 (below +25 gate); top TC kamis (16319/7531/1339) killed in session 102, replacement 7-9h away.
- Yeahta node 73: only 1374 +62 (single-target, rule #4 deny). POWELL at -33 to -37 won't ripen in 30-60 min.
- stefan97 node 86: 17 above-gate but oracle drill found 3 bulk-stop windows in past 6h (max 12 kamis in 1 sec) — defensive cycle, deny per Plan-103 P0 v2 criterion #2.

**Lifetime kills: 25 (unchanged).**

**End state**: operator + 11224 (140/140 RESTING) + 12649 (170/170 close-fed RESTING) at room 60. Stamina ~43 SP. Inventory: 25 obols, 466 cookies, 65 ice creams.

---

## Priority 0 — MANDATORY pre-pivot heat-check (refined v2 — unchanged from plan-103)

1. Get `minutes_idle` (last action time) AND `active_kamis_24h` count for the dominant farmer at the candidate node.
2. **Drill into recent action density**: query `kami_action` for past 60 min on the target owner. Count distinct kamis acting + max action density per 5-min window.
3. **Synchronized defensive cycle signature**: ≥5 kamis acting within a single 60-second window = bulk-stop/restart pattern (stefan97).
4. **Blacklist criterion** (any of):
   - `minutes_idle < 10` AND ≥3 distinct kamis acted in past 5 min (synchronized).
   - Past 6h shows ≥3 bulk-stop windows (≥5 kamis stopping in <60s each).
   - stefan97 always blacklist absent ≥4h idle gap.
5. **Pass criterion** (single-kami activity with `minutes_idle < 30`): allowed if drill shows only 1-2 distinct kamis active in past 60 min (auto-cycle).

**Production-validated session 103**: stefan97 drill correctly triggered criterion #2 (3 bulk-stop windows in 6h). Doctrine working.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` (refreshes every 5 min).
2. **TC cluster (node 60)** — top wiuuuu 3243 was at +11 with 2.3h elapsed at session-103 start. Wiuuuu cycles ~1.5-2.5h then auto-stop; might reset before reaching gate. foden 16719 at 7.8h elapsed ~ auto-stop imminent, then ~7h re-ripen cycle. Realistic next TC strike window: ~12-16 UTC.
3. **Yeahta cluster (node 73)** — 1374 was +62 single-strike. POWELL at -33/-37 with 18 HP/h strain need ~110-180 min to flip — not unlocked within +30 min.
4. **stefan97 deny check** — re-run oracle drill for past 6h bulk-stop windows. If <3 bulk-stop windows AND last action ≥4h ago, criterion clears. Most likely still active.
5. **Stamina** — ~43 SP estimate. Natural regen ~0.5 SP/min → ~58 in +30 min, ~73 in +60 min. 60→73 = 16 hops (80 SP) — needs 1-2 ice creams to pad.

---

## Priority 2 — Strike scenarios by watcher state at session 104 start

### Scenario A: TC @ node 60 has ≥1 above-gate (margin ≥ +25)
- Zero-travel. Heat-check via P0 drill (single-kami activity allowed).
- Single-strike or chain — apply session-102 +26 chain-gate floor.
- Gas budget: ~10-12M for 1-kill, ~17-22M for 2-kill chain.

### Scenario B: Yeahta has ≥2 above-gate (1374 +50+ AND another Yeahta +25+)
- Migrate 60→73 (16 hops, ~15M + 1-2 ice creams = ~17-19M travel).
- Single 1374 alone → reject per rule #4.
- Stamina: have ≥40 SP + ice creams → OK.

### Scenario C: New emerging cluster (any hot_node)
- Pre-pivot heat-check on dominant farmer mandatory using v2 drill.
- Reject single-target migrations.

### Scenario D: stefan97 deny clears (≥4h idle in oracle, no recent bulk-stops)
- Re-evaluate with drill — if criterion #2 clears AND criterion #1 clears, stefan97 16+ above-gate becomes the highest-EV target cluster of all time.
- Migrate 60→86 (~16 hops, similar to Yeahta — ~17-19M travel + ice creams).
- Heat-check repeated immediately before strike (defensive cycle could resume).

### Scenario E: All clusters dry
- Wait at 60. Re-wake +30-60 min. Maximum delay before re-check: 90 min.

---

## Priority 3 — Hard limits

- **Total gas budget session 104**: 25M (zero-travel scenarios). Migration scenarios 30M ceiling.
- **No tx if striker HP <80% max_hp** unless 1 cookie pre-feed first.
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle drill clears criterion #2 (no ≥3 bulk-stop windows in past 6h) AND ≥4h idle gap.
- **Pre-pivot heat-check v2 MANDATORY** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action.
- **Session length cap**: ≤25 min wall-clock.
- **Rule #4 inviolable**: no cross-region travel for a single target. 1374 alone is bait.

---

## Priority 4 — Build asks (deferred, async)

- **Watcher: heat-check v2 drill snapshot** — augment `world_targets.json` per-cluster summary with `last_60min_action_density` and `bulk_stop_count_6h` so heat-check can be done from snapshot, not oracle round-trip. **High leverage** — saves 1 oracle round-trip per session.
- **Watcher: stefan97 owner-blacklist** — modify watcher to suppress stefan97 from `killable_clean` unless oracle drill confirms ≥4h idle gap AND no bulk-stop pattern. Currently 17/27 of `killable_clean` is stefan97 noise.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 104 also yields zero kills, consider building Priority 4 watcher enhancements rather than continuing to wait — System Thinking doctrine: 3+ same-derivation = build.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Session 103 was zero-tx wait. Realistic next strike windows: (a) TC ripening ~12-16 UTC (4-8 hours from now), (b) stefan97 defensive cycle ends — no ETA but oracle bulk-stops in past 6h have stopped within 12-24h historically, (c) Yeahta needs 90+ min for 2nd candidate. +30 min check is optimistic for new candidates but NOT unreasonable per Cadence Discipline build-phase mode (sub-10-min normally; +30 is conservative when world is genuinely quiet). If session 104 also dry, escalate to +60 min and consider build work on Priority 4."

**Re-wake**: +30 min from session end (~08:24 UTC, timestamp 1777796640).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 25 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 absent oracle-confirmed deny clearance.
- Migrating for single Yeahta 1374.
