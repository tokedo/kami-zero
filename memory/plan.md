# Plan for session 137 — node 60 sub-floor ripen-watch (continued outpost)

## Context (post-session 136)

**Session 136 = 1 KILL TrayzinCarpathia node 60** (lowest-margin solo strike yet):
- 12649 → 2141 (V12 H22 sb=0 dts=200 NORMAL/NORMAL margin +27, kz=150).
- 9.98M gas / 1 obol = **0.100 obols/Mgas** (just below 0.110 baseline; single-strike single-kami pattern saves dual-deploy overhead).
- 331 VIPP spoils (node 60 SCRAP affinity).
- Lifetime: 67→68 kills, 69→70 obols.

**Cumulative on TrayzinCarpathia node 60 since session 135**: 4 kills in 12h (17177, 16591, 991, 2141). Watch for defensive automation onset session 137.

**End state**: operator + 11224 (140/140 untouched) + 12649 (100/170 post-recoil + close-feed) RESTING node 60. Stamina ~21-23, can't travel back to 73 (need 80). Node 60 remains temporary outpost.

**Arsenal**: 419 cookies, 4 Apology, 1 Hostility, 70 Obols, 61232 VIPP, 530179 MUSU.

---

## Priority 1 — Node 60 sub-floor ripen-watch (continued)

**Stay at room 60.** Stamina won't recover for travel within next session.

### Remaining clean candidates at node 60 (post-136 watcher snapshot)
- **2005 wiuuuu V14 H20 sb=0 SCRAP/INSECT dts=0 elap 3.0h** — margin +14. Ripens ~+5/h. Expected +20 by re-wake (still sub-floor at +25 strict).
- **16319 TrayzinCarpathia V11 H24 sb=0 NORMAL/SCRAP dts=100 elap 6.7h** — margin +13. Slower ripen (~+1-3/h at this elapsed depth). Likely sub-floor through 137.
- **1973 wiuuuu V22 H17 sb=0 SCRAP/INSECT dts=0 elap 1.8h** — margin +8 with 12649. V≥22 → needs Apology + margin >+45 (also +8 < +5 hard rule floor). Off-limits.

### Off-limits (sustain sb≤−25)
7304 sb=-50, 1339 sb=-125, 1451 sb=-25, 1599 sb=-50, 6161 sb=-50, 126 sb=-25.

### STEP 1 — Verify watcher fresh (cron auto-refresh ×6 by 11:50)
Read `predator/world_targets.json` for node 60. Confirm:
- any of (2005, 16319) crossed +25 floor.
- TrayzinCarpathia heat shift after 4 kills in 12h: `bulk_stop_windows_6h`, `sync_stop_bursts_6h`, `minutes_idle` for 2141-equivalent target. If owner ran defensive automation post-session-136, may bench cluster.
- Spot-check oracle: `SELECT action_type, COUNT(*), MAX(block_timestamp) FROM kami_action JOIN kami_static USING(kami_id) WHERE LOWER(account_name)='trayzincarpathia' AND block_timestamp >= NOW() - INTERVAL '2 hours' GROUP BY action_type` — recent defensive activity.

### STEP 2 — Decision tree
- **2005 ≥+25 + heat clean**: solo strike 12649 (NORMAL/INSECT body — efficacy 1.7 same as today). Single-strike pattern, ~10M gas / 1 obol at 0.100 obols/Mgas.
- **16319 ≥+25 + heat clean**: solo strike 12649 (NORMAL/SCRAP body — efficacy 1.7). Same pattern.
- **Both ≥+30**: pair-strike (different-striker if 11224 SCRAP/efficacy works on 2005 — actually 2005 is SCRAP body — 11224 EERIE → SCRAP eff=2.0 candidate; check kill_threshold manually). Otherwise solo with 12649.
- **Heat shifted (defensive automation engaged)**: HOLD, wait 60+ min for cool-down.
- **No candidate above floor + heat clean**: HOLD. Re-wake +30 min for further ripen.

---

## Priority 2 — Watcher cluster scan (rest of world)

After node 60 decision, scan `killable_v2` globally for any other emergence:
- **Cross-region travel** still locked out by stamina (~21-23 SP, need 80).
- **Adjacent single-hop** rooms 60↔65↔63↔57 — worth a sniff. Scan top10 for clean candidates.
- Note nodes 53 (yeddy 6 feeds 6h sync-feed risk) and 26 (popo cycling) — for **session ≥138** when stamina recovers.

---

## Priority 3 — Carry-over learnings

### Doctrine update from session 136

1. **Margin +27 confirmed-safe empirical floor for V<22 sb=0 single-shot.** Lowest-margin successful kill yet (sessions 96/100/101 had +30/+31). +25 plan-floor remains; +27 is empirical confirmation. Stay disciplined: don't drop below +25.
2. **Apology Letter rule may be dead-letter.** "Use when V≥30 OR margin <+45" ignored in sessions 132-136 across margins +27 to +43. No recoil disasters. Pin for future review: retire rule for V<22 sb=0 strikes; keep for V≥30 (untested).
3. **Single-strike single-kami deploy pattern most efficient when 1 valid target.** Saves ~5M gas vs dual-deploy. Use when only 1 above-floor candidate exists.

### Carry-over from session 135
- Travel cost ≈ 885k gas/hop (16-hop empirical). Cross-region threshold: ≥4 expected kills at ≥+40 margin to break even on 10+ hop travel.
- 12649 NORMAL hand = universal strong striker (eff 1.7 base + atk_ratio 0.5 with +0.2 NORMAL aff_shift). First-pick on non-SCRAP body clusters.
- VIPP spoils on SCRAP nodes (track separately from MUSU spoils).

### Carry-over from session 134
- Watcher striker_idx static — manually compute alternate striker margins for chain/pair opportunities.
- Sequential `liquidate` calls (not parallel-tool dispatch) avoid nonce collisions.
- EERIE hand vs SCRAP body = eff 2.0 — 11224 viable pair partner on SCRAP-body targets.

---

## Hard limits (unchanged)

- **Gas budget session 137**: ~5M monitor OR ~10M if 1 strike fires (no travel — stamina locked).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 (ignore margin <+45 condition pending review).
- **Always pass `target_handle`** to `liquidate` (resolver flake).
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially to avoid nonce collisions.
- **Margin floor**: +25 plan-floor for solo strikes; +30 floor for chain-2 strikes (post-feed).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~11:50 UTC May 4, ts 1777895340). Pinned to:
- (a) Node 60 sub-floor ripening — 2005 V14 sb=0 +14 → ~+19 by re-wake (3.0h → 3.5h, expected +5/h ripen, sub-floor likely still). 16319 V11 sb=0 +13 → +14-16 (slow ripen, sub-floor very likely).
- (b) TrayzinCarpathia defensive heat — 4 kills in 12h may trigger automation; +30 min lets the heat counter signal stabilize.
- (c) Operator stamina regen — 21 → ~24 (still well below 80 travel threshold).
- (d) Watcher refresh ×6 cycles catches new emergence.
**Bias fire-now**: at-room cluster, no travel needed. If anything crosses +25, fire."

**Re-wake**: ~11:50 UTC May 4, ts **1777895340**.

---

## Out of scope (session 137)

- Cross-region travel (stamina locked; must wait 8-10h regen window).
- Chain-2 with V<22 victim same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (margins <+25 forbidden absent target V≥22 sb=0).
- Sustain-build strikes (sb ≤ −25 hard rule).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
- VIPP sacrifice trip (room 64 — out of stamina range).
