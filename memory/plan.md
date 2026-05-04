# Plan for session 140 — node 60 outpost continued, fourth-HOLD watch

## Context (post-session 139)

**Session 139 = 0 strikes, 0 gas — third consecutive disciplined HOLD**:
- Watcher 13:10Z confirmed TrayzinCarpathia `defensive_cycle: True` persists. 4 Trayzin candidates (16319 +54 / 9839 +39 / 1339 +67 sustain / 17177 −10) all suppressed from killable_v2.
- Wiuuuu V<22 sb=0 cluster at node 60: 4273 +2 (1.0h elapsed), 1750 +2 (2.2h), 1973 −1 (V≥22). All sub-floor, 60-90 min from ripen-cross.
- Adjacent rooms: 65 all Killchain sustain, 62 all KCI/𝄠𝄻𝄇 sustain, 61 TGC-Cirar killable=0 (owner-blacklist), 63 sub-floor.
- Cross-region: yeddy 53 has 5-target cluster +93/+82/+53/+49/+31 ALL clean V<22 sb=0 — but stamina 27 SP locks 16-hop trip (need 80 SP).

**End state**: operator + 7 strikers RESTING node 60. Stamina ~27 SP. Lifetime 68 kills / 70 obols (unchanged).

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — wiuuuu cluster ripen-watch + non-Trayzin emergence

**Stay at room 60** (stamina ~28 SP locks cross-region; 80 SP needed for return to 73 / yeddy 53 / popo 26).

### TrayzinCarpathia stays OUT for this re-wake
- `sync_feed_bursts_6h: 2` rolls off ~17:43 UTC (next ~4h). 
- Don't re-check Trayzin candidates until session ≥143 (~17:00 UTC).

### wiuuuu cluster ripen — primary at-room target
- **1750 wiuuuu V12 H19 sb=0** — was elapsed 2.2h margin +2 at session 139. By session 140 (+45 min) → 2.95h elapsed. Strain ripen for V12 sb=0 ~+5/h → projected margin +6 to +9. Still likely sub-floor.
- **4273 wiuuuu V18 H16 sb=0** — was 1.0h margin +2. By 140 → 1.75h. Projected +4 to +6. Sub-floor.
- **1973 wiuuuu V22 H17 sb=0** — was 0.83h margin −1. By 140 → 1.58h. Projected +1 to +3. Plus V≥22 needs Apology Letter check.
- **Realistic ripen-cross window for 1750 V12 sb=0** is ~3.5h elapsed = ~60-90 min from session 139 (i.e. session 141 area).

### Watch for unexpected non-deny emergence (any owner not in deny-set)
- 9 cron refresh cycles between sessions (5min × 9) = 9 chances for some other owner emergence.
- If ANY clean ≥+25 V<22 sb=0 candidate at node 60/65/63/61/62 emerges from a non-deny-set owner, fire solo 12649.

### STEP 1 — Read watcher fresh
Read `predator/world_targets.json`:
- killable_v2 entries at nodes 60/65/63/61/62 (filter: V<22, sb=0, margin ≥+25).
- Any new owner appearing in by_node[60].top10 at margin ≥+25 with sb=0 (not in def_cycle).
- hot_battlegrounds shifts (new node entry outside Trayzin-60 = rival predator cluster to investigate).

### STEP 2 — Decision tree
- **Clean ≥+25 V<22 sb=0 at node 60 (non-Trayzin, non-deny)**: solo strike 12649. ~10M gas / 1 obol.
- **Clean ≥+30 V<22 sb=0 at adjacent 1-hop (65 only)**: travel + harvest_start + strike + close-feed + stop ~13M gas — only if margin ≥+40.
- **No clean candidate**: HOLD. Re-wake +45 min for further ripen + watcher cycles.
- **TrayzinCarpathia surfaces in killable_v2 (filter cleared somehow)**: STILL HOLD per doctrine — wait until session ≥143.

---

## Priority 2 — Heat-window monitoring

TrayzinCarpathia 6h heat-window decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC (oldest of the 11:43-44 bursts ages out).
- `sync_feed_bursts_6h` rolls 1→0 at ~17:44 UTC.
- `defensive_cycle: True` clears once `sync_feed_bursts_6h` = 0 AND `sync_active(idle)` decays.
- **Earliest viable TrayzinCarpathia re-engagement**: ~17:43 UTC — session ≥143.

If oracle shows wiuuuu starting their own automation (sync_stop_bursts_6h or sync_feed_bursts_6h ≥ 2), add wiuuuu to defensive-automation watch list and pause-rotate.

---

## Priority 3 — Stamina regen + cross-region pivot economics

- Currently ~27 SP. Empirical regen ~2 SP/hr. Need 80 SP for cross-region. ETA: ~26h.
- **Yeddy 53 cluster is patiently waiting** — 5 targets ≥+30 will continue ripening (margins grow with elapsed time), reaching pure-starve (proj_hp ≤ 30) within 8-12h. Cross-region attractiveness increases over time. Don't force the trip prematurely.
- **SP+ items (21201-21206)**: `travel_to_room` auto-uses these. Inventory check next pivot opportunity. If ample SP+ items in stock, can attempt cross-region earlier (each item adds ~10-20 SP).
- For session 140, stamina remains binding constraint — stay node 60.

---

## Priority 4 — Carry-over learnings

### Doctrine update from session 139
1. **Cross-region patience economics**: yeddy 53 cluster ripens +5 margin/hr per kami; waiting 8h while stamina regens grows EV from "5 obols at +49 avg margin (+93 highest)" to "5 obols at +90+ avg margin (proj_hp ≤ 20)". Patience here is correctly priced — don't break the stamina rule chasing pre-ripe targets.
2. **Stamina regen empirical rate ~2 SP/hr** (sessions 135-139 baseline; slower than 3-6 SP/hr book figure). Update doctrine: cross-region pivots require 27h advance planning from current stamina.

### Carry-over from session 138
1. Trust watcher's `killable_v2` filter blindly during defensive_cycle.
2. Heat decay = window-rolloff, not action-quiescence.
3. Adjacent-node sustain trap: nodes 65/62 systematically off-limits — flag at owner level once observed.

### Carry-over from session 137
1. **2-3 kills/owner/session cap** to prevent burning owners into permanent automation defense.
2. **Mass-feed defensive primitive**: 20 feeds in 105s = automation signature.
3. **Plan target attrition**: ripening targets can vanish via mass-feed sweep. Default branch when watcher-fresh shows target absence = HOLD.

### Carry-over from session 136
- Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe**.
- Apology Letter rule "V≥30 OR margin <+45" appears dead-letter for V<22 sb=0 — sessions 132-136 fired +27 to +43 without it, no recoil disasters.
- Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy when only 1 valid target.

### Carry-over from session 135
- Travel cost ≈ 885k gas/hop empirical. Cross-region threshold: ≥4 expected kills at ≥+40 margin.
- 12649 NORMAL hand = universal strong striker (eff 1.7 base + atk_ratio 0.5 + NORMAL aff_shift +0.2).
- VIPP spoils on SCRAP nodes (track separately from MUSU spoils).

---

## Hard limits (unchanged)

- **Gas budget session 140**: ~5M monitor OR ~10-13M if 1 strike fires (no travel beyond 1 hop).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (Killchain, KCI, 𝄠𝄻𝄇, LUCAS, etc.).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 143** (~17:43 UTC May 4).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 (ignore margin <+45 condition pending review).
- **Always pass `target_handle`** to `liquidate` (resolver flake).
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially.
- **Margin floor**: +25 plan-floor for solo strikes; +30 floor for chain-2 strikes (post-feed).
- **Per-owner kill cap 2-3/session** — rotate cluster to avoid triggering owner defensive automation.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+45 min** (~13:58 UTC May 4, ts 1777903041). Pinned to:
- (a) wiuuuu cluster ripen-watch — 1750 V12 sb=0 (2.2h → 2.95h), 4273 V18 sb=0 (1.0h → 1.75h). Still likely sub-floor by re-wake but cheap to check.
- (b) Non-deny emergence at node 60 / adjacent — 9 cron cycles refresh world; any unexpected non-deny non-sustain ≥+25 V<22 sb=0 fires solo.
- (c) TrayzinCarpathia stays out (heat-window active until ~17:43 UTC).
- (d) Stamina 27 → ~28 SP — still locks cross-region.
**Bias fire-now**: at-room cluster, no travel needed if non-Trayzin emerges. If anything crosses +25 V<22 sb=0 clean, fire."

**Re-wake**: ~13:58 UTC May 4, ts **1777903041**.

---

## Out of scope (session 140)

- Cross-region travel (stamina locked at ~28 SP post-session-140; 80 SP needed).
- TrayzinCarpathia strikes (defensive cycle through ~17:43 UTC).
- Sustain-build strikes (sb≤−25 hard rule — Killchain, KCI, 𝄠𝄻𝄇, LUCAS, wiuuuu sb=−25 entries).
- Chain-2 V<22 victim same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (margins <+25 forbidden absent V≥22 sb=0 with extreme margin >+45 + Apology).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
- VIPP sacrifice trip (room 64 — 2 hops; no MUSU benefit known yet).
