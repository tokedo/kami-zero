# Plan for session 134 — Yeahta sub-floor ripen-watch (in-room)

## Context (post-session 133)

**Session 133 = 2 KILLS Yeahta cluster (lifetime 60→62)** + **WATCHER STRIKER-CONFIG BUG FIX**:
- 3735 → killed by 11224 (V16 H20 sb=0, margin +36, planned-pair primary).
- 2836 → killed by 12649 (V14 H22 sb=0, margin +38, planned-pair secondary; possible only after watcher fix surfaced 12649 as superior striker for both).
- Pre-stage [11224, 12649] + chain-2 different-striker pair + post-strike close-feed both + stop. ~17.85M gas / 2 obols = **0.112 obols/Mgas**.

**Watcher fix** (`predator/scripts/refresh_world_targets.py` STRIKERS[12649].atk_s 300→400): prior config under-rated 12649's atk_threshold_shift by 0.10. Post-fix margins for 12649 jumped massively across population — yeddy node 53 clean candidates +104/+92, popo node 26 +67/+52, TrayzinCarpathia node 60 +75. Most cross-region with marginal cluster mass (≤2 sb=0 targets), but world view richer.

**Yeahta cluster remaining (snapshot 09:00:39Z)** — node 73:
- 6104 V13 H22 sb=0 margin +34 elap 4.0h (above floor, ripening)
- 6485 V11 H22 sb=0 margin +28 elap 4.0h (above floor, ripening)
- 1500 V12 H24 sb=0 margin +24 elap 4.3h (right at floor)
- 6505 V19 H21 sb=-50 margin +53 — sustain off-limits
- 3699 V11 H23 sb=-50 margin +37 — sustain off-limits
- 1847 V10 H20 sb=-25 margin +19 — sustain off-limits
- 1374 V15 H19 sb=0 margin +6 — passive sub-floor

**Striker state (post-session 133 stop)**:
- 11224 RESTING node 73 sync ~134/140 (post close-feed). Cooldown clear.
- 12649 RESTING node 73 sync ~125/170 (post close-feed). Cooldown clear.

**Arsenal** (after −2 cookies): 425 Gakki Cookie Sticks, 4 Apology Letters, 1 Hostility Potion. 64 Obols. ~530.2k MUSU (+spoils not yet indexed: ~600-1000 from 132 + ~600-1000 from 133).

---

## Priority 1 — Yeahta sub-floor ripen-watch (in-room)

**Targets at +25 floor entry threshold by 09:26**:
- 6104 V13 H22 sb=0 — projected margin ~+38-40 by 09:26 (assuming +5-8/h ripen rate)
- 6485 V11 H22 sb=0 — projected margin ~+33 by 09:26

Both eligible for V<22 sb=0 doctrine. With watcher fix, 12649 is likely best striker for at least one (was previously assigned to 11224 due to misconfigured atk_s).

### STEP 0 — NO `harvest_start` at session start
Strikers are RESTING. To strike, EITHER (a) accept 200s wait, OR (b) recognize that pre-stage was NOT done at session 133 end (operator chose immediate fire path). For session 134 strike: must pre-stage in-session and accept 200s wait. Same gas cost as pre-stage at prior end; no regret.

### STEP 1 — Verify state
- Watcher refresh (cron auto, fresh by 09:26).
- Read `killable_v2` for node 73. Confirm 6104/6485 still HARVESTING and ripened ≥+30.
- Yeahta heat re-verify (will be ~30 min idle now after the 2 kills at 08:55 — heat counter restarts).
- Striker HP via slim — both should be regen'd to 140/170 over 25 min rest + previous close-feed sync.

### STEP 2 — Decision tree
- **Both 6104 + 6485 ≥+30 + heat clean**: pre-stage harvest_start([11224, 12649]) → wait 200s → fire pair (compute optimal striker assignment using corrected watcher) → post-strike close-feed both → stop.
- **Only 6104 ≥+30, 6485 sub-+30**: solo-strike 6104 with best striker (likely 12649 per fix). Save 6485 for next session.
- **Heat changed (defensive flag)**: HOLD, vacate at session 135 if persists.
- **All sub-+30**: HOLD. Re-wake +30 min for next ripen check.

### STEP 3 — Striker assignment (use corrected watcher)
Trust `world_targets.json` `striker_idx` post-fix. For session 134, expect 12649 paired with high-margin sb=0 V<22 target since corrected efficacy gives 12649 better numbers for many V<22 cases.

---

## Priority 2 — V≥22 sb=0 emergence + cross-region scan

Watcher refresh ×5 cycles since 133. Read `killable_v2` for any new non-guild V≥22 sb=0 with margin ≥+25. Cross-region single-target threshold unchanged: V≥22 sb=0 ≥+40 + owner-passive-confirmed.

**Post-fix world surfaces (cross-region, NOT actionable as solo)**:
- yeddy node 53: 4768 V11 sb=0 +104, 7263 V13 sb=0 +92 (2 clean sb=0 — marginal cluster)
- popo node 26: 13964 V11 sb=0 +67, 8962 V12 sb=0 +52, 7476 V10 sb=0 +44 (3 clean sb=0 — minimum cluster mass)
- TrayzinCarpathia node 60: 898 V14 sb=0 +75 (1 clean sb=0 — single)

**popo node 26 borderline qualifies as cluster** (3 sb=0 targets). Worth a pre-trip oracle drill on owner heat next session if Yeahta drops below cluster mass first.

---

## Priority 3 — Self-pace cooldown awareness (carry-over)

**Strike→next-action cooldown is 180s** (NOT 80s). Budget ≥200s wait between strike and feed. Plan post-strike sequences accordingly. Pre-stage harvest_start at session-end is a valid optimization but only if NEXT session is genuinely committed to firing — otherwise gas waste.

**Owner-resolver flake**: ALWAYS pass `target_handle` (from watcher `v_acct`) to `liquidate` — saves a likely-failing Playwright resolution call.

---

## Hard limits (unchanged)

- **Gas budget session 134**: ~5M monitor OR ~18M if pair fires (pre-stage + 200s wait + 2 strikes + 2 feeds + stop).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits (session 118 doctrine).
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (KAMI 8040, yeddy sb-25/-50/-125, popo low margins, 6505 sb=-50, 1847 sb=-25, 3699 sb=-50).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 OR margin <+45.
- **Always pass `target_handle`** to `liquidate` (resolver flake).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+25 min** (~09:26 UTC May 4, ts 1777886827). Pinned to: (a) Yeahta sub-floor ripening — 6104 + 6485 cross +35/+30 margin window. (b) Striker recovery — 11224 to ~140/140, 12649 to ~140/170 over 25 min rest. (c) Watcher refresh ×5 cycles catches any defensive heat shift on Yeahta after 4 kills/15h. **Bias fire-now**: cluster in-room, only delay is striker-HP wait + ripen window."

**Re-wake**: ~09:26 UTC May 4, ts **1777886827**.

---

## Out of scope (session 134)

- Cross-region travel (Yeahta cluster in-room, popo node 26 worth a pre-trip oracle drill but not commit yet).
- Chain-2 same-striker without close-feed.
- Sub-floor strikes (1500 V12 sb=0 +24 right at floor — borderline).
- sb=-50 / sb=-25 strikes (6505/3699/1847).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
