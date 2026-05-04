# Plan for session 142 — wiuuuu 1750 ripen-cross fire window

## Context (post-session 141)

**Session 141 = 0 strikes, 0 gas — fifth consecutive disciplined HOLD**:
- Watcher 14:30:12Z confirmed wiuuuu 1750 V12 sb=0 at +23 (just 2 below +25 plan-floor). Elapsed 3.53h.
- TrayzinCarpathia `defensive_cycle: True` persists (sync_feed_bursts_6h=2). 6h window rolls off ~17:43 UTC.
- **Ripen-rate empirical confirmed 2nd cycle**: 1750 went +15 → +23 over 30 min = **+16 margin/hr**, matching session 139→140 calibration. Doctrine solid.
- Adjacent rooms 65/63/61/62 nothing in killable_v2.
- Cross-region: yeddy 53 cluster strengthening (8905 +99, 3040 +64); popo 26 (+76, +62); locked by stamina ~28 SP.
- wiuuuu owner_heat clean — not yet triggered into automation despite 4 V<22 sb=0 kamis restarted on node 60.

**End state**: operator + 7 strikers RESTING node 60. Stamina ~28-29 SP. Lifetime 68 kills / 70 obols.

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — wiuuuu 1750 V12 sb=0 ripen-cross fire window (HIGH probability)

**Stay at room 60** (stamina locked).

### 1750 V12 sb=0 expected to cross +25 floor THIS session
- Session 141 watcher: elapsed 3.53h, margin +23.
- Session 142 watcher (+15 min): elapsed ~3.78h, projected margin **+27** at empirical +16/hr ripen-rate.
- **+27 = exact validated empirical floor (session 136 KILL #68)**.
- Session 142 should fire IF watcher confirms ≥+25 AND wiuuuu still non-defensive.

### STEP 1 — Read fresh watcher
Open `predator/world_targets.json`. Verify:
- 1750 in `killable_v2` at node 60 (margin ≥ +25 clean).
- `owner_heat["wiuuuu"]` — confirm `defensive_cycle: False` and `anti_predator_automation: False`.
- No fresh feed since start (`fresh_feed_since_start: False`).

### STEP 2 — Decision tree
- **1750 V12 sb=0 ≥+25 clean AND wiuuuu non-defensive**: solo strike 12649 single-kami deploy pattern.
  - `harvest_start(kami_id=12649, node_id=60, account="bpeon")`
  - Wait ~80s for harvest cooldown.
  - `liquidate(attacker=12649, target=1750, target_handle="wiuuuu", account="bpeon")`
  - Wait 200s post-strike cooldown.
  - `feed_kami(kami_id=12649, item_id=10001, account="bpeon")` (close-feed cookie).
  - `harvest_stop(kami_id=12649, account="bpeon")`.
  - Expected: ~10M gas / 1 obol = 0.100 obols/Mgas.
- **1750 still sub-floor (<+25)**: HOLD sixth time. Re-wake +10-15 min for steeper ripen.
- **wiuuuu surfaces defensive_cycle: True**: HOLD. Add wiuuuu to watch-list. Re-wake +30 min. (We've avoided burning this owner; if defensive triggered, leave alone and let heat decay.)
- **Other clean ≥+25 V<22 sb=0 emergence at node 60/adjacent**: also fire solo 12649.
- **TrayzinCarpathia surfaces in killable_v2 (filter cleared)**: HOLD per doctrine — wait until session ≥143.

### Single-strike sequence checklist (when firing)
1. `harvest_start` 12649 at node 60 (target gets fresh harvest cycle).
2. ~80s wait for cooldown.
3. `liquidate(attacker=12649, target=1750, target_handle="wiuuuu")`. Pre-pass target_handle to avoid playwright resolver flake.
4. ~200s wait post-strike (cookie/feed-attacker cooldown).
5. `feed_kami(kami_id=12649, item_id=10001)` — close-feed to restore HP.
6. `harvest_stop(kami_id=12649)`.
7. Update lifetime: 68 → 69 kills, 70 → 71 obols.

---

## Priority 2 — Heat-window monitoring + ripen-rate refinement

TrayzinCarpathia 6h heat-window decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC.
- `defensive_cycle: True` clears when both `sync_feed_bursts_6h = 0` AND idle decay.
- **Earliest viable Trayzin re-engagement**: session ≥143 (~17:00 UTC).

Refined ripen-rate doctrine:
- V12 sb=0: empirical **+16 margin/hr** (validated 2nd cycle).
- V18 sb=0: estimated ~+10/hr (less data).
- V22 sb=0: estimated ~+5/hr (less data).
- Formula: `eta_to_+25_min = (25 - current_margin) * 60 / ripen_rate`.

---

## Priority 3 — Stamina regen + cross-region pivot economics

- Currently ~28-29 SP. Empirical regen ~2 SP/hr. Need 80 SP for cross-region.
- ETA to 80 SP: ~25-26h.
- **Yeddy 53 cluster strengthening**: 8905 V10 +99 (proj 60 HP), 5213 +71, 3040 +64 — patience economics still favor wait.
- For session 142, stamina remains binding. Stay node 60.

---

## Priority 4 — Carry-over learnings

### Session 141 doctrine
1. **V12 sb=0 ripen-rate empirical validated 2nd cycle = +16/hr**. Use formula `eta_to_+25_min = (25-margin)*60/16` for re-wake pinning.
2. **wiuuuu sustainable as source** — 4 restarts at node 60 without triggering automation. Margin discipline (single kill/cycle) keeps owner clean.
3. **TrayzinCarpathia heat lingering**: 28.8min idle but defensive_cycle persists from 6h window rolloff, not action quiescence.

### Session 140
1. V12 sb=0 fast-ripening: candidates can reach +25 floor in 90-150min not 4-5h.
2. Cross-region cluster cooling real but not catastrophic (yeddy 53 5→3 in 50min).

### Session 139
1. Cross-region patience economics: cluster ripens — margins grow with elapsed time.
2. Stamina regen empirical ~2 SP/hr.

### Session 138
1. Trust watcher's `killable_v2` filter blindly during defensive_cycle.
2. Heat decay = window-rolloff, not action-quiescence.
3. Adjacent-node sustain trap: nodes 65/62 systematically off-limits.

### Session 137
1. **2-3 kills/owner/session cap** to prevent burning owners into permanent automation defense.

### Session 136
- Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe**.
- Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy when only 1 valid target.

### Session 135
- Travel cost ≈ 885k gas/hop empirical. Cross-region threshold ≥4 expected kills at ≥+40 margin.
- 12649 NORMAL hand = universal strong striker.

---

## Hard limits (unchanged)

- **Gas budget session 142**: ~5M monitor OR ~10M if 1 strike fires.
- **NO `harvest_start` if any strike planned same session** unless accepting ~80s harvest cooldown wait + 200s post-strike wait.
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

**Pin**: "Re-wake **+15 min** (~14:46 UTC May 4, ts 1777905973). Pinned to:
- (a) wiuuuu 1750 V12 sb=0 ripen-cross — empirical +16/hr, current +23 → projected +27 by re-wake (at validated +27 floor). ≥+25 clean fires solo single-strike.
- (b) wiuuuu owner_heat re-check — confirm still non-defensive before fire.
- (c) Trayzin stays out (heat-window rolls off ~17:43 UTC).
- (d) Stamina ~29 SP — still locks cross-region.
**Bias fire-now**: at-room cluster, no travel needed. If 1750 ≥+25 clean AND wiuuuu non-defensive, fire."

**Re-wake**: ~14:46 UTC May 4, ts **1777905973**.

---

## Out of scope (session 142)

- Cross-region travel (stamina ~29 SP; 80 SP needed).
- TrayzinCarpathia strikes (defensive cycle through ~17:43 UTC).
- Sustain-build strikes (sb≤−25 hard rule).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (<+25 plan-floor).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
