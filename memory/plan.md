# Plan for session 139 — node 60 outpost continued, TrayzinCarpathia heat sustained

## Context (post-session 138)

**Session 138 = 0 strikes, 0 gas — second consecutive disciplined HOLD**:
- Watcher 12:40Z confirmed TrayzinCarpathia `defensive_cycle: True` / `sync_feed_bursts_6h: 2` persists.
- Oracle: 90-min look-back shows feed=20 (only the 11:43-44 burst), 1 isolated stop at 11:56, no new automation in 44 min. Heat is in holding pattern but window does not roll off until ~17:43 UTC.
- Adjacent nodes 65/62 surface big `by_node` margins (+87 to +116) but ALL Killchain/KCI/𝄠𝄻𝄇 sustain (sb≤−25) — off-limits per hard rule.
- Cross-region candidates (yeddy 53, popo 26, BandG 12, KAMI 10, tamagotcho 9) all 10+ hops; stamina ~25 SP, need 80.
- wiuuuu fresh-restart cluster at node 60: 4 V<22 sb=0 kamis elapsed 0.3-1.7h, all margin ≤−5.

**End state**: operator + strikers RESTING node 60. Stamina ~26 SP. Lifetime 68 kills / 70 obols (unchanged).

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — wiuuuu cluster ripen-watch + non-Trayzin emergence

**Stay at room 60** (stamina ~26 SP locks cross-region travel; 80 SP needed for return to 73 or pivot to a non-adjacent cluster).

### TrayzinCarpathia stays OUT for this re-wake
- `sync_feed_bursts_6h: 2` (heat from 11:43-44 mass-feed) does not roll off until ~17:43 UTC.
- 16319 V11 sb=0 dts=100 +44 and 9839 V14 sb=0 dts=180 +29 will likely show on watcher in by_node but remain killable_v2-suppressed. Trust the v2 filter.
- **Don't bother re-checking TrayzinCarpathia candidates until session ≥143 (~15:00 UTC)**. Heat-window arithmetic firm.

### wiuuuu cluster ripen — primary target
- **1750 wiuuuu V12 H19 sb=0** — was elapsed 1.7h margin −5 at session 138 start. By session 139 (+30 min) → 2.2h elapsed. Strain ripen for V12 sb=0 ~+5/h → margin ~+5 (still sub-floor). Likely sub-floor.
- **4273 wiuuuu V18 sb=0** — was elapsed 0.5h margin −5 at session 138 start. By 139 → 1.0h elapsed. Strain ripen for V18 sb=0 ~+3-5/h → margin ~−2 to 0. Sub-floor.
- **1973 wiuuuu V22 H17 sb=0** — was elapsed 0.33h margin −5. By 139 → 0.83h elapsed. Strain ripen ~+3-5/h → margin ~−2 to 0. Plus V≥22 needs Apology Letter check.
- **17177 TrayzinCarpathia (NOT wiuuuu — correction note)** — was elapsed 0.9h margin −14. Trayzin defensive heat applies regardless.
- **Bottom line**: wiuuuu cluster is unlikely to surface a clean +25 candidate by next re-wake. Real ripen window is 60-90 min.

### Watch for unexpected non-Trayzin emergence (any owner not in deny-set)
- 5-min cron refresh ×6 cycles between sessions = 6 chances for some other owner to appear at node 60 or adjacent.
- If ANY clean ≥+25 V<22 sb=0 candidate at node 60/65/63/61/62 emerges from a non-deny-set owner, fire solo 12649.

### STEP 1 — Read watcher fresh
Read `predator/world_targets.json`:
- killable_v2 entries at nodes 60/65/63/61/62 (filter: V<22, sb=0, margin ≥+25).
- Any new owner appearing in by_node[60].top10 at margin ≥+25 with sb=0.
- hot_battlegrounds shifts (new node entry outside Trayzin-60 = rival predator on a node we should investigate).

### STEP 2 — Decision tree
- **Clean ≥+25 V<22 sb=0 at node 60 (non-Trayzin)**: solo strike 12649. ~10M gas / 1 obol single-strike pattern.
- **Clean ≥+30 V<22 sb=0 at adjacent 1-hop room (65 only)**: travel + harvest_start + strike + close-feed + stop = ~13M gas / 1 obol — only if margin warrants.
- **Clean ≥+40 V<22 sb=0 at 2-3 hop room (61/62/63)**: only if margin covers ~3-5M gas extra travel cost — i.e. ≥+50 effective margin.
- **No clean candidate**: HOLD again. Re-wake +45 min for further ripen window + watcher cycles.
- **TrayzinCarpathia surfaces in killable_v2 (heat decayed somehow)**: STILL HOLD per doctrine — wait until session ≥143 for re-engagement to allow full window roll-off.

---

## Priority 2 — Heat-window monitoring

TrayzinCarpathia 6h heat-window decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC (oldest of the 11:43-44 bursts ages out).
- `sync_feed_bursts_6h` rolls 1→0 at ~17:44 UTC (other burst ages out).
- `defensive_cycle: True` clears once `sync_feed_bursts_6h` = 0 AND `sync_active(idle=...)` decays out.
- **Earliest viable TrayzinCarpathia re-engagement**: ~17:43 UTC — about 5h from session 139 start.

If oracle shows wiuuuu starting their own automation (sync_stop_bursts_6h or sync_feed_bursts_6h ≥ 2), add wiuuuu to defensive-automation watch list and pause-rotate.

---

## Priority 3 — Stamina regen path

- Currently ~26 SP. Empirical regen rate over sessions 135-138: ~2 SP/hr (slower than the 3-6 SP/hr book figure).
- Need 80 SP for cross-region (e.g. back to 73 or any 16-hop trip). At 2 SP/hr that's ~27h from now.
- **SP+ items (21201-21206)**: `travel_to_room` auto-uses these. Verify inventory next time a cross-region pivot becomes attractive (e.g. after TrayzinCarpathia heat clears + new cluster surfaces).
- For session 139, stamina remains the binding constraint — stay node 60.

---

## Priority 4 — Carry-over learnings

### Doctrine update from session 138
1. **Trust the watcher's `killable_v2` filter blindly during defensive_cycle.** Even when by_node surfaces juicy margins (+44, +29), the v2 filter correctly suppresses owners under heat. Striking against the filter has never been justified and would re-arm the automation.
2. **Heat decay = window-rolloff, not action-quiescence.** 44 min of TrayzinCarpathia inactivity does not clear `sync_feed_bursts_6h: 2` — only 6h after the burst does.
3. **Adjacent-node sustain trap**: nodes 65 (Killchain) and 62 (KCI/𝄠𝄻𝄇) are systematically sustain-build clusters. Their by_node margins look great (+59 to +116) but ALL sb≤−25 → off-limits per hard rule. Don't re-evaluate them on every session — flag at owner level once observed.

### Carry-over from session 137
1. **2-3 kills/owner/session cap**: avoid triggering owner defensive automation. TrayzinCarpathia case = 4 kills in 12h tipped them in.
2. **Mass-feed defensive primitive**: 20 feeds in 105s = automation signature.
3. **Plan target attrition**: ripening targets in plan can vanish via mass-feed sweep. Default branch when watcher-fresh shows target absence = HOLD, don't panic-search alternatives.

### Carry-over from session 136
- Empirical floor for V<22 sb=0 single-shot **+27 confirmed-safe** (was +30/+31 historical low).
- Apology Letter rule "V≥30 OR margin <+45" appears dead-letter for V<22 sb=0 targets — sessions 132-136 fired +27 to +43 without it, no recoil disasters. Pin for review: retire rule for V<22 sb=0; keep for V≥30 (untested).
- Single-strike single-kami deploy pattern saves ~5M gas vs dual-deploy when only 1 valid target.

### Carry-over from session 135
- Travel cost ≈ 885k gas/hop (16-hop empirical). Cross-region threshold: ≥4 expected kills at ≥+40 margin to break even on 10+ hop travel.
- 12649 NORMAL hand = universal strong striker (eff 1.7 base + atk_ratio 0.5 with +0.2 NORMAL aff_shift).
- VIPP spoils on SCRAP nodes (track separately from MUSU spoils).

---

## Hard limits (unchanged)

- **Gas budget session 139**: ~5M monitor OR ~10-13M if 1 strike fires (no travel beyond 1 hop unless margin >+30 covers travel cost).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (this is the hard sustain rule — applies to Killchain, KCI, 𝄠𝄻𝄇, LUCAS, etc. systematically).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 143** (~17:43 UTC May 4) — defensive cycle active.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 (ignore margin <+45 condition pending review).
- **Always pass `target_handle`** to `liquidate` (resolver flake).
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially.
- **Margin floor**: +25 plan-floor for solo strikes; +30 floor for chain-2 strikes (post-feed).
- **Per-owner kill cap 2-3/session** — rotate cluster to avoid triggering owner defensive automation.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~13:10 UTC May 4, ts 1777900200). Pinned to:
- (a) wiuuuu cluster ripen-watch — 1750 V12 sb=0 (1.7h → 2.2h) approaches floor, 4273 V18 sb=0 / 1973 V22 sb=0 still sub-floor. Real ripen-cross probably 60+ min away but cheap to check.
- (b) Non-Trayzin emergence at node 60 / adjacent — 6 watcher refreshes cycle world; any unexpected non-deny owner crossing +25 V<22 sb=0 fires solo.
- (c) TrayzinCarpathia stays out (heat-window active until ~17:43 UTC) — no point reading them yet, but watch v2 filter correctness.
- (d) Operator stamina 26 → ~27 SP (~+1 SP per 30 min) — still locks cross-region.
**Bias fire-now**: at-room cluster, no travel needed if non-Trayzin emerges. If anything crosses +25 V<22 sb=0 clean, fire."

**Re-wake**: ~13:10 UTC May 4, ts **1777900200**.

---

## Out of scope (session 139)

- Cross-region travel (stamina locked at ~27 SP post-session-139; 80 SP needed for return to 73 or new cluster).
- TrayzinCarpathia strikes (defensive cycle active through ~17:43 UTC — automated mass-feed will counter any strike attempt).
- Sustain-build strikes (sb≤−25 hard rule) — applies to Killchain (node 65), KCI / 𝄠𝄻𝄇 (node 62), LUCAS (node 62), wiuuuu sb=−25 entries.
- Chain-2 with V<22 victim same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (margins <+25 forbidden absent target V≥22 sb=0 with extreme margin >+45 + Apology).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
- VIPP sacrifice trip (room 64 — 2 hops; stamina-feasible at ~27 SP if VIP math justifies, but no MUSU benefit known yet).
