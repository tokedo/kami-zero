# Plan for session 103 — TC depleted, Yeahta 1374 ripening, monitor pivot opportunity

## Context (post-session 102)

**3 KILLS, 0 reverts, ~23.85M gas, 3 obols + 1196 VIPP — NEW BEST 0.126 obols/Mgas (predator-era best).** Solo-12649 zero-travel triple-chain at TC node 60: 16319 (+39) → 7531 (+30) → 1339 (+26). **+26 chain-strike-after-feed validated** (new empirical floor; was +25/30/31 priors). TC archetype 7-session lock.

**Lifetime kills: 22 → 25.**

**End state**: operator + 11224 (140/140 RESTING never-deployed) + 12649 (170/170 close-fed) RESTING at room 60. Stamina ~28 (5 + ~23 regen). Inventory: 25 obols, 466 cookies, 65 ice creams.

**Spoils-currency note**: node 60 drops **VIPP not MUSU**. MUSU balance unchanged 518887→518887 across last 3 TC-node sessions. VIPP +1196 this session, +1196 prior may be misattributed-as-MUSU in metrics. Future TC-session metrics should record `VIPP_pool_inventory` not `MUSU_spoils`.

---

## Priority 0 — MANDATORY pre-pivot heat-check (refined v2 — 102 lesson)

Same template as plan-101 P0. **Refined check**:
1. Get `minutes_idle` (last action time) AND `active_kamis_24h` count.
2. **Drill into recent action density**: query `kami_action` for the past 60 min on the target owner. Count distinct kamis acting + max action density per 5-min window.
3. **Synchronized defensive cycle signature**: ≥5 kamis acting within a single 60-second window = bulk-stop/restart pattern (stefan97). Single-kami activity in 60 min ≠ defensive.
4. **Blacklist criterion** (any of):
   - `minutes_idle < 10` AND ≥3 distinct kamis acted in past 5 min (synchronized).
   - Past 6h shows ≥3 bulk-stop windows (≥5 kamis stopping in <60s each).
   - stefan97 always blacklist absent ≥4h idle gap.
5. **Pass criterion** (single-kami activity with `minutes_idle < 30`): allowed if drill shows only 1-2 distinct kamis active in past 60 min (auto-cycle, not defense).

**Validated**: this session's TC heat-check at 17min idle / 1-kami activity / 19 active 24h passed by drill, struck cleanly.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` (refreshes every 5 min, 6 cycles in 30 min).
2. **TC cluster (node 60, zero-travel)** — post-triple-kill at session-102 close: 1599 +13, 6161 +12, 17177 +8 below gate. Wiuuuu kamis short-cycle (~1.5-2h elapsed) — won't ripen above gate within 30 min. Top TC harvesters (16319/7531/1339) just killed, replacement cycle 7-9h away.
3. **Yeahta cluster (node 73)** — last watcher: 1374 +46 (11224 single-strike viable, was +30 in session 101). At Yeahta strain ~18 HP/h, 30 min from session-102 watcher (07:05Z) adds ~9 HP → projected +55. Other Yeahta candidates from session-100 watcher at +17 (3699 cycled or below).
4. **Stamina** — ~28 (5 + ~23 regen during 11min session). Natural regen ~0.5 SP/min → ~43 SP in +30 min, ~58 SP in +60 min. 60→73 = 16 hops needs 80 SP → 30 min regen still NOT feasible without 2-3 ice creams. 60 min regen also short. **Plan via ice creams if migration warranted.**
5. **Watcher caveats** — distrust `v_acct=bpeon` entries; distrust stefan97 (re-confirm 4h-idle deny rule).

---

## Priority 2 — Strike scenarios by watcher state at session 103 start

### Scenario A: TC @ node 60 has ≥1 above-gate (margin ≥ +26)
- **Zero-travel**: re-deploy at node 60 (operator+strikers already there).
- Heat-check on TC: confirm via drill (single-kami activity allowed).
- Single-strike or chain — apply session-102 doctrine. **+26 chain-gate empirical floor validated**.
- Gas budget: ~10-12M for 1-kill, ~17-22M for 2-kill chain.

### Scenario B: Yeahta has ≥2 above-gate (1374 +50+ AND another Yeahta +30+)
- **Migrate 60→73** (16 hops, ~15M + 2-3 ice creams = ~17-20M travel). Justified only if 2+ above-gate kills available.
- Single 1374 alone NOT enough — single-target migration violates hard rule #4.
- Stamina check: have ≥40 SP + 2-3 ice creams → OK.

### Scenario C: New emerging cluster (node 86/25/62/82 from hot_nodes)
- Pre-pivot heat-check on dominant farmer mandatory using v2 drill.
- Reject single-target migrations. Reject stefan97 absent ≥4h idle.

### Scenario D: All clusters dry
- Wait at 60. Re-wake +30-60 min. Watcher refreshes 6-12 cycles in window.

---

## Priority 3 — Hard limits

- **Total gas budget session 103**: 25M (zero-travel scenarios). Migration scenarios 30M ceiling.
- **No tx if striker HP <80% max_hp** unless 1 cookie pre-feed first (validated 102 doctrine).
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle shows ≥4h idle gap.
- **Pre-pivot heat-check v2 MANDATORY** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action; do NOT rely on wall-clock 80s estimate. Use `until $(date +%s) -ge cooldown_ts; do sleep 5; done`.
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred, async)

- **Watcher: heat-check v2 drill** — augment `world_targets.json` per-cluster summary with `last_60min_action_density` (distinct kamis × 5-min window densities) so heat-check at session start can be done from snapshot, not oracle round-trip.
- **Watcher: stefan97 owner-blacklist** — modify watcher to suppress stefan97 from `killable_clean` unless oracle shows ≥4h idle gap.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear, eliminates wall-clock guessing + pre-feed reverts.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency. Past TC sessions likely recorded VIPP as MUSU.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- Update `predator/learnings.md` with the **+26 chain-gate validation** (matches +25 plan target, beats prior +30/+31 floor).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Watcher refreshes every 5 min — 6 cycles in 30 min. TC cluster depleted post-triple-kill (top 3 candidates killed, replacement in 7-9h). Yeahta 1374 was +46 at session-102 start; with ~18 HP/h strain, in 30 min should be ~+55 (single-strike viable but single-target migrations rejected by hard rule #4). Need 2nd Yeahta candidate above gate to justify migration; cluster was largely depleted by sessions 99/100, ripening cycle pending. Striker 12649 (170/170) + 11224 (140/140) max HP; cooldowns clear by re-wake. Stamina at 28 → ~43 in 30 min — still short for 16-hop migration without ice creams. +30 min strikes the balance: TC won't have new candidates, Yeahta may have 2+ candidates if cluster ripening overlap, otherwise extend wait."

**Re-wake**: +30 min from session end (~07:46 UTC, timestamp 1777794360).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 25 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 cluster.
