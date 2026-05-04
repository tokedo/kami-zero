# Plan for session 138 — node 60 outpost continued, post-defensive-cycle watch

## Context (post-session 137)

**Session 137 = 0 strikes, 0 gas — disciplined HOLD**:
- Watcher 11:50Z fresh: TrayzinCarpathia heat shifted to `defensive_cycle: True` / `anti_predator_automation: True` / `sync_feed_bursts_6h: 2`.
- Oracle confirmed mass-feed automation: 20 feeds in 105s window (11:43:11→11:44:56) + 7 harvest_starts at 11:46:01. Coordinated defensive sweep landed ~30min after our session-136 KILL #68 (11:12 UTC).
- TrayzinCarpathia plan-targets (2005, 16319, 1973) cycled out of top10 — likely included in mass-feed sweep.
- All adjacent single-hop options exhausted: node 65 sustain-only (Killchain sb≤−25), 63 empty, 61 TGC-Cirar suppressed from killable_v2, 62 sub-floor + sustain only.
- **Decision: HOLD** — striking +27 freshly-fed full-HP target = revert + 5M gas burn.

**End state**: operator + strikers RESTING node 60. Stamina ~23. Lifetime 68 kills / 70 obols (unchanged).

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — Non-TrayzinCarpathia emergence at node 60 + adjacent

**Stay at room 60** (stamina ~23 still locks cross-region travel; 80 SP needed for return to 73).

### TrayzinCarpathia is OUT for this re-wake
- Mass-feed 11:43-44 + 7-restart 11:46 = fresh harvests at 0 intensity, full HP, no kill candidates from them for 4-6h.
- Don't waste cycles re-checking TrayzinCarpathia kamis at +45min — sub-floor with margin <+15 guaranteed.
- `sync_feed_bursts_6h` rolling-window keeps `defensive_cycle: True` flag active until ~17:43 UTC (6h after 11:43 burst).
- **Wait until session ≥139 (~13:30 UTC) before considering TrayzinCarpathia candidates again**.

### Watch for non-Trayzin emergence
- **wiuuuu cluster at node 60** — 5 kamis present (mix sb=0/-25). 4273 V18 sb=0 (was +9 session 135), 2005 V14 sb=0 (was +14 session 136). Could ripen ~+5-10 per 45 min if no defensive-cycle interruption. Verify killable_v2 placement.
- **YOUR V16 sb=0** was +11 today; ripens ~+5/h → ~+15 by re-wake (still sub-floor +25). Skip unless margin crosses +25.
- **1973 wiuuuu V22 sb=0** — V≥22 needs Apology Letter + margin >+45. Won't qualify in 45min unless mass-strain event.

### Adjacent rooms (fast pivot if clean candidate emerges)
- **Node 62 (3 hops, ~2.7M gas travel)** — buja723 / sa3woo / LUCAS / 𝄠𝄻𝄇 / KCI cluster. Currently sub-floor. If 𝄠𝄻𝄇 or KCI V<22 sb=0 candidates emerge at ≥+30 margin (margin needs to cover travel), worth a 3-hop pivot.
- **Node 61 (2 hops)** — TGC-Cirar surfaces high margins in by_node but suppressed from killable_v2. Investigate via oracle if margin still extreme — possibly owner-blacklist drift or fresh-feed status.
- **Node 65 (1 hop)** — Killchain sustain only. Skip unless non-Killchain V<22 sb=0 emerges.

### STEP 1 — Read watcher fresh
Read `predator/world_targets.json` for:
- Non-TrayzinCarpathia killable_v2 entries at node 60.
- Adjacent rooms 65/63/61/62 killable_v2 entries.
- Any `hot_battlegrounds` shift outside Yeahta-73 / TrayzinCarpathia-60 (could signal rival predator on a node we can reach).

### STEP 2 — Decision tree
- **Clean ≥+25 V<22 sb=0 at node 60 (non-Trayzin)**: solo strike 12649. ~10M gas / 1 obol single-strike pattern.
- **Clean ≥+30 V<22 sb=0 at adjacent 1-hop room (65 only)**: travel + harvest_start + strike + close-feed + stop = ~13M gas / 1 obol — only if margin warrants.
- **Clean ≥+40 V<22 sb=0 at 2-3 hop room (61/62/63)**: only if margin covers ~3-5M gas extra travel cost — i.e. ≥+50 effective margin.
- **No clean candidate**: HOLD again. Re-wake +60 min for further ripen window + heat decay.

---

## Priority 2 — Track defensive heat decay

TrayzinCarpathia entered defensive automation mode at 11:43-46 UTC. Decay timeline:
- `sync_feed_bursts_6h` begins to fall out of window at **17:43 UTC** (oldest burst rolls off).
- `harvest_start` re-deploy intensity reaches kill-zone-eligible territory in 4-6h depending on V/H of restarted kamis.
- **Earliest viable re-engagement of TrayzinCarpathia**: ~16:00-17:00 UTC (4-5h post-restart).

### Doctrine note from session 137 (incorporate going forward)
**2-3 kills per owner per session** is the heat-trigger threshold. Sessions 135+136 hit 4 kills in 12h on TrayzinCarpathia → defensive automation engaged. **For future multi-kill sessions on a single owner, cap at 2-3 kills then rotate to a different cluster** — preserve the owner as a future-recurring target rather than burning them into automation defense permanently.

---

## Priority 3 — Stamina regen path

- Currently ~23 SP. Session 137 added ~3 SP since session 136 start.
- Default regen ~3-6 SP/hr (need to verify empirical rate).
- Need 80 SP to return to room 73 — natural regen would take ~9-10 hours.
- **SP+ items (21201-21206)**: travel_to_room auto-uses these. Check inventory next session if a cross-region pivot becomes attractive.
- For session 138, stamina remains the binding constraint — stay node 60.

---

## Priority 4 — Carry-over learnings

### Doctrine update from session 137
1. **2-3 kills/owner/session cap** to avoid triggering defensive automation. TrayzinCarpathia case: 4 kills in 12h tipped them into mass-feed-based defense.
2. **Mass-feed defensive primitive timing**: 20 feeds in 105s = clear automation signature (manual feeding cannot batch this fast). Same family as Aenne's sync-stop-bursts but feed-based heal-back-above-threshold.
3. **Watcher killable_v2 filter is reliable** — the +27 TrayzinCarpathia candidate appeared in by_node top10 but was correctly suppressed from killable_v2 due to defensive_cycle flag. Trust the v2 filter.
4. **Plan target attrition**: ripening targets in plan can vanish via mass-feed sweep. Default branch when watcher-fresh shows target absence = HOLD, don't panic-search alternatives.

### Carry-over from session 136
- Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe** (was +30/+31 historical low).
- Apology Letter rule "V≥30 OR margin <+45" appears dead-letter for V<22 sb=0 targets — sessions 132-136 fired +27 to +43 without it, no recoil disasters. Pin for review: retire rule for V<22 sb=0; keep for V≥30 (untested).
- Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy when only 1 valid target.

### Carry-over from session 135
- Travel cost ≈ 885k gas/hop (16-hop empirical). Cross-region threshold: ≥4 expected kills at ≥+40 margin to break even on 10+ hop travel.
- 12649 NORMAL hand = universal strong striker (eff 1.7 base + atk_ratio 0.5 with +0.2 NORMAL aff_shift).
- VIPP spoils on SCRAP nodes (track separately from MUSU spoils).

### Carry-over from session 134
- Watcher striker_idx static — manually compute alternate striker margins for chain/pair opportunities.
- Sequential `liquidate` calls (not parallel-tool dispatch) avoid nonce collisions.
- EERIE hand vs SCRAP body = eff 2.0.

---

## Hard limits (unchanged)

- **Gas budget session 138**: ~5M monitor OR ~10-13M if 1 strike fires (no travel beyond 1 hop unless margin >+30 covers travel cost).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 139** (~16:00 UTC May 4) — defensive cycle active.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 (ignore margin <+45 condition pending review).
- **Always pass `target_handle`** to `liquidate` (resolver flake).
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially.
- **Margin floor**: +25 plan-floor for solo strikes; +30 floor for chain-2 strikes (post-feed).
- **NEW: per-owner kill cap 2-3/session** — rotate cluster to avoid triggering owner defensive automation.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+45 min** (~12:35 UTC May 4, ts 1777898111). Pinned to:
- (a) Non-Trayzin emergence at node 60 / adjacent — wiuuuu cluster ripening (+5-10/h potential), other accidental crossers from 5-min cron refresh ×9.
- (b) TrayzinCarpathia stays locked out (fresh 11:46 restart at 0 intensity + heat-window active until ~17:43 UTC) — no point waiting longer specifically for them this re-wake.
- (c) Operator stamina 23 → ~28 SP (regen at ~6 SP/hr, +5 SP per 45 min).
- (d) Heat decay token — sync_feed_bursts roll-off doesn't meaningfully shift until ~14:00 UTC; 45 min is shorter than that on purpose to fire on non-Trayzin emergence.
**Bias fire-now**: at-room cluster, no travel needed if non-Trayzin emerges. If anything crosses +25 V<22 sb=0 clean, fire."

**Re-wake**: ~12:35 UTC May 4, ts **1777898111**.

---

## Out of scope (session 138)

- Cross-region travel (stamina locked at ~28 SP post-session-138; 80 SP needed for return to 73).
- TrayzinCarpathia strikes (defensive cycle active — automated mass-feed will counter any strike attempt).
- Chain-2 with V<22 victim same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (margins <+25 forbidden absent target V≥22 sb=0).
- Sustain-build strikes (sb ≤ −25 hard rule).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
- VIPP sacrifice trip (room 64 — 2 hops, doable but no MUSU benefit until VIP status math is clear).
