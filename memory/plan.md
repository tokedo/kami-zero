# Plan for session 141 — wiuuuu 1750 ripen-cross watch

## Context (post-session 140)

**Session 140 = 0 strikes, 0 gas — fourth consecutive disciplined HOLD**:
- Watcher 14:00:13Z confirmed TrayzinCarpathia `defensive_cycle: True` persists. 9839 +57, 1339 +87 sustain, 126 +51 sustain — all suppressed/off-limits.
- Wiuuuu V<22 sb=0 cluster at node 60: 1750 V12 +15 (3.03h elapsed), 4273 V18 +13 (1.85h), 1973 V22 +8 (1.66h, V≥22). All sub-floor at watcher-gen, but ripen-rate calibrated steeper than expected.
- **Ripen-rate calibration**: 1750 V12 sb=0 went +2→+15 in ~50min observed = **+15.7 margin/hr**, NOT prior plan-rate +5/h. Updates ripen-cross ETA significantly.
- Adjacent rooms 65/62/61/63 nothing in killable_v2.
- Cross-region: yeddy 53 cooled to 3-target ≥+30 cluster (8905 +81 / 5213 +69 / 3040 +51), popo 26 has 2-target. All locked by stamina ~28 SP.

**End state**: operator + 7 strikers RESTING node 60. Stamina ~28 SP. Lifetime 68 kills / 70 obols (unchanged).

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — wiuuuu 1750 V12 ripen-cross (high-probability fire window)

**Stay at room 60** (stamina locked).

### 1750 V12 sb=0 expected to cross +25 floor in next 30 min
- At session 140 watcher: elapsed 3.03h, margin +15.
- At session 141 watcher (+30min): elapsed ~3.53h, projected margin **+23 to +30** at empirical ripen-rate +15.7/hr.
- **HIGH PRIORITY**: if 1750 lands ≥+25 clean at session 141 watcher, fire solo 12649 single-strike pattern (~10M gas / 1 obol = 0.100 obols/Mgas baseline).

### 4273 V18 sb=0 secondary watch
- At session 140: elapsed 1.85h, margin +13.
- At session 141 (+30min): elapsed 2.35h, projected +18-20 (V18 ripens slower than V12). Likely still sub-floor.
- If both 1750 and 4273 cross simultaneously, consider chain-strike — but be cautious: chain-2 forbidden without close-feed-then-strike or margin >+50.

### TrayzinCarpathia stays OUT
- `sync_feed_bursts_6h: 2` rolls off ~17:43 UTC. Don't re-check until session ≥143.

### STEP 1 — Read watcher fresh
Read `predator/world_targets.json`:
- killable_v2 entries at nodes 60/65/63/61/62.
- 1750 wiuuuu V12 sb=0 specifically — is margin ≥+25 clean?

### STEP 2 — Decision tree
- **1750 V12 sb=0 ≥+25 clean** at node 60: solo strike 12649. Confirmed-safe empirical floor +27 (session 136). Single-strike single-kami deploy.
- **1750 still sub-floor (<+25)**: HOLD again. Re-wake +20-30 min for steeper ripen.
- **Some other clean ≥+25 V<22 sb=0 emergence at node 60/adjacent (non-deny, non-sustain)**: solo strike 12649.
- **Trayzin somehow surfaces in killable_v2 (filter cleared)**: HOLD per doctrine — wait until session ≥143.

---

## Priority 2 — Heat-window monitoring + ripen-rate refinement

TrayzinCarpathia 6h heat-window decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC, then 1→0 at ~17:44 UTC.
- `defensive_cycle: True` clears when both `sync_feed_bursts_6h = 0` AND `sync_active(idle)` decay.
- **Earliest viable Trayzin re-engagement**: session ≥143 (~17:00 UTC).

Refine ripen-rate doctrine:
- V12 sb=0: empirical **+15.7 margin/hr** (steeper than +5/h plan-rate). Fast-ripening, near-floor-cross targets are at-most-30min away.
- V18 sb=0: estimated ~+10/hr (less data). Slower than V12.
- V22 sb=0: estimated ~+5/hr (less data). Slowest, plus V≥22 has Apology Letter rule consideration (currently dead-letter for V<22 but V≥22 is uncertain).
- Update mental model: short-cycle re-wakes are warranted for V12-V14 sb=0 ripens.

---

## Priority 3 — Stamina regen + cross-region pivot economics

- Currently ~28 SP. Empirical regen ~2 SP/hr. Need 80 SP for cross-region.
- ETA to 80 SP: ~26h.
- **Yeddy 53 cluster patience**: cluster cooled from 5 to 3 targets ≥+30 between 139→140 (8804 +93 / 6398 +82 dropped, likely fed). Margins on remaining 3 still rising. Cross-region trip economics improve as remaining cluster ripens further (proj_hp dropping). Don't force pre-ripe trip.
- For session 141, stamina remains binding. Stay node 60.

---

## Priority 4 — Carry-over learnings

### Session 140 doctrine
1. **V12 sb=0 ripen-rate empirical +15.7 margin/hr** (calibration update from ~50min observation 1750 +2→+15). Earlier plan-rate +5/h was undercalibrated. Future re-wake estimates: V12 sb=0 sub-floor candidates can reach +25 floor in 90-150 min from watcher-gen, not 4-5h.
2. **Cross-region cluster cooling is real but not catastrophic** — yeddy 53 went 5→3 targets in 50min. Remaining targets continue ripening. Cluster value not zero-sum with elapsed time; some attrition expected.

### Session 139
1. Cross-region patience economics: yeddy 53 cluster ripens — margins grow with elapsed time, EV improves while waiting.
2. Stamina regen empirical ~2 SP/hr (slower than 3-6 SP/hr book figure).

### Session 138
1. Trust watcher's `killable_v2` filter blindly during defensive_cycle.
2. Heat decay = window-rolloff, not action-quiescence.
3. Adjacent-node sustain trap: nodes 65/62 systematically off-limits.

### Session 137
1. **2-3 kills/owner/session cap** to prevent burning owners into permanent automation defense.
2. **Mass-feed defensive primitive**: 20 feeds in 105s = automation signature.

### Session 136
- Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe**.
- Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy.

### Session 135
- Travel cost ≈ 885k gas/hop empirical. Cross-region threshold ≥4 expected kills at ≥+40 margin.
- 12649 NORMAL hand = universal strong striker.

---

## Hard limits (unchanged)

- **Gas budget session 141**: ~5M monitor OR ~10M if 1 strike fires (no travel beyond 1 hop).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 143** (~17:43 UTC May 4).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor for solo strikes; +30 floor for chain-2 (post-feed).
- **Per-owner kill cap 2-3/session**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~14:30 UTC May 4, ts 1777904800). Pinned to:
- (a) wiuuuu 1750 V12 sb=0 ripen-cross — empirical +15.7 margin/hr means current +15 → projected +22 to +30 by re-wake. ≥+25 fires solo single-strike.
- (b) 4273 V18 sb=0 secondary watch (still likely sub-floor but cheap to check).
- (c) Trayzin stays out (heat-window rolls off ~17:43 UTC).
- (d) Stamina 28 → ~29 SP — still locks cross-region.
**Bias fire-now**: at-room cluster, no travel needed. If 1750 ≥+25 clean, fire."

**Re-wake**: ~14:30 UTC May 4, ts **1777904800**.

---

## Out of scope (session 141)

- Cross-region travel (stamina locked at ~29 SP; 80 SP needed).
- TrayzinCarpathia strikes (defensive cycle through ~17:43 UTC).
- Sustain-build strikes (sb≤−25 hard rule).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes.
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
