# Plan for session 143 — 6142 buja723 ripen-watch + active-owner +25 plan-floor doctrine

## Context (post-session 142)

**Session 142 = 0 strikes, 0 gas — sixth consecutive disciplined HOLD**:
- **wiuuuu lost**: 1750/4273/1973 V<22 sb=0 cycled out between session 141 (14:30Z, 1750 +23) and session 142 watcher (14:50Z) — wiuuuu idle 18.9 min, owner non-defensive but actively cycling. **Optimizing for +27 validated floor over +25 plan-floor cost the kill.**
- TrayzinCarpathia heat persists (sync_feed_bursts_6h=2, idle 48.8 min). Window rolls off ~17:43 UTC; earliest re-engagement session ≥146.
- New emergent: **6142 buja723 V13 sb=0 +26 elapsed 5.78h** at node 62 (3-hop adjacent). buja723 active (idle 0.1 min, 14 distinct/60min) — patience-risky.
- Cross-region yeddy 53 cluster strengthening (4 V<22 sb=0 ≥+30 targets); stamina ~29 SP locks 16-hop trip (need 80).

**End state**: operator + 7 strikers RESTING node 60. Lifetime 68 kills / 70 obols.

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## NEW DOCTRINE — active-owner +25 plan-floor (born session 142)

**For V<22 sb=0 candidates whose owner has `defensive_cycle=False` AND `distinct_kamis_60min ≥ 5`:**
- Fire at first watcher confirmation of margin ≥+25 plan-floor.
- DO NOT try to inch up to +27 validated floor — active cyclers feed/stop V<22 sb=0 starvers within 15-30 min windows, faster than the patience-wait.
- The 1-2 pt risk band (+25 to +27) is acceptable when the alternative is losing the strike entirely to owner cycling.

**Patience-safe owners** (distinct_kamis_60min ≤ 4): can wait for +27 validated floor.

---

## Priority 1 — 6142 buja723 ripen-cross window (HIGH-MEDIUM probability)

### STEP 1 — Read fresh watcher (cron-refreshed at session start)
Open `predator/world_targets.json`. For 6142 buja723 V13 sb=0:
- Confirm still in `killable_v2`.
- Read fresh margin (V13 sb=0 ripens ~+10-14/hr → projected +28-29 by 15:00 UTC).
- Check `owner_heat["buja723"]`:
  - `defensive_cycle: False` (must hold).
  - `minutes_idle ≥ 5` = quiet enough to commit.
  - If `minutes_idle < 2`: high cycle risk, hold OR pre-deploy and accept gamble.
- Check `fresh_feed_since_start: False` (if True, skip — sync HP underestimates).

### STEP 2 — Decision tree

**6142 alive AND margin ≥+27 AND buja723 idle ≥5 min**: FIRE.
- `travel_to_room(target_room=62, account="bpeon", dry_run=True)` first → confirm path 60→65→61→62, ~3 SP, ~3-4M gas.
- `travel_to_room(target_room=62, account="bpeon")` execute.
- `harvest_start(kami_id=12649, node_id=62, account="bpeon")`.
- Wait ~80s for harvest cooldown.
- `liquidate(attacker=12649, target=6142, target_handle="buja723", account="bpeon")`.
- Wait 200s post-strike cooldown.
- `feed_kami(kami_id=12649, item_id=10001, account="bpeon")` close-feed.
- `harvest_stop(kami_id=12649, account="bpeon")`.
- Travel back: `travel_to_room(target_room=60, account="bpeon")` — 3 SP back.
- Total cost: ~7-8M gas + ~6 SP. Yield: 1 obol + spoil. Net +0.125 obols/Mgas if successful.

**6142 alive AND margin +25 to +26 AND buja723 idle ≥10 min**: FIRE per active-owner doctrine.
- Same sequence above. Active-owner exception: longer-idle threshold (≥10 min) compensates for sub-validated-floor margin.

**6142 alive AND margin +25 to +26 AND buja723 idle <10 min**: HOLD. Re-wake +10 min for ripen + cycle quiet.

**6142 cycled out (gone from killable_v2)**: HOLD or pivot.
- Check buja723 still has other V<22 sb=0 ≥+25 at node 62 (replacement).
- Otherwise, scan global killable_v2 for any other reachable ≥+25 V<22 sb=0 non-deny non-sustain.

**wiuuuu cluster re-emergence at node 60**: FIRE IMMEDIATELY at plan-floor +25 (zero travel cost, any V<22 sb=0 wiuuuu ≥+25 → solo 12649 single-strike).

**Trayzin surfaces in killable_v2 (filter cleared early)**: HOLD per doctrine — wait until session ≥146 (heat-window rolloff).

---

## Priority 2 — Heat-window monitoring + cross-region patience

TrayzinCarpathia 6h decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC.
- `defensive_cycle: True` clears when both bursts=0 AND idle decay.
- **Earliest viable Trayzin re-engagement**: session ≥146 (~17:50 UTC).

Yeddy 53 cluster ripen-watch:
- 4 V<22 sb=0 ≥+30 (3040 +72, 10107 +43, 12419 +37, 12289 +31). Each margin grows ~+5-12/h.
- Stamina ~29 SP → 80 SP needs ~25h regen at +2/hr empirical. Cross-region locked through ~mid-day May 5.
- 16-hop round-trip cost: ~16M gas + 32+ SP. Min cluster-yield to justify: 4 obols at ≥+50 each.

---

## Priority 3 — Carry-over learnings

### Session 142 doctrine NEW
1. **Active-owner +25 plan-floor**: fire at first confirmation, don't inch to +27. Lost 1750 wiuuuu by waiting +15 min.
2. **Owner taxonomy by distinct_kamis_60min**: ≥10 = highly active, ≥5 = active, ≤4 = patience-safe.
3. **owner_heat keys are lowercase** — always `.lower()` before dict lookup.

### Session 141 doctrine
1. V12 sb=0 ripen-rate empirical +16/hr (validated 2nd cycle).
2. wiuuuu sustainable as recurring source IF margin discipline (≤2-3 kills/owner/session).
3. TrayzinCarpathia heat lingering = window-rolloff, not action-quiescence.

### Session 140
1. V12 sb=0 fast-ripening: +25 floor in 90-150min not 4-5h.
2. Cross-region cluster cooling slow (yeddy 5→3 in 50min, others held).

### Session 139
1. Cross-region patience economics: cluster ripens — margins grow with elapsed time.
2. Stamina regen empirical ~2 SP/hr.

### Session 138
1. Trust watcher's `killable_v2` filter blindly during defensive_cycle.
2. Heat decay = window-rolloff, not action-quiescence.

### Session 137
1. **2-3 kills/owner/session cap** to prevent burning owners into automation defense.

### Session 136
1. Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe**.
2. Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy.

### Session 135
1. Travel cost ≈ 885k gas/hop empirical. Cross-region threshold ≥4 expected kills at ≥+40 margin.
2. 12649 NORMAL hand = universal strong striker.

---

## Hard limits (unchanged)

- **Gas budget session 143**: ~5M monitor OR ~10M if 1 strike fires.
- **NO `harvest_start` if any strike planned same session** unless accepting ~80s harvest cooldown wait + 200s post-strike wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 146** (~17:50 UTC May 4).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor for solo strikes (active-owner doctrine); +30 floor for chain-2 (post-feed).
- **Per-owner kill cap 2-3/session**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+10 min** (~15:00 UTC May 4, ts 1777906810). Pinned to:
- (a) 6142 buja723 V13 sb=0 ripen-cross — +26 → projected +28-29 (>+27 validated). Fire 60→62 travel + solo 12649 if buja723 quiet.
- (b) wiuuuu cluster re-emergence — fire-now at +25 plan-floor (active-owner doctrine).
- (c) Trayzin stays out (heat-window).
- (d) Stamina ~30 SP — still locks cross-region.
**Bias fire-now**: 6142 active-owner candidate; small re-wake to let ripen-cross + buja723 cycle quiet."

**Re-wake**: ~15:00 UTC May 4, ts **1777906810**.

---

## Out of scope (session 143)

- Cross-region travel (stamina ~30 SP; 80 SP needed for round-trip).
- TrayzinCarpathia strikes (defensive cycle through ~17:43 UTC).
- Sustain-build strikes (sb≤−25 hard rule).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
