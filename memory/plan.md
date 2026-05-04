# Plan for session 135 — Yeahta solo-finisher (in-room)

## Context (post-session 134)

**Session 134 = 2 KILLS Yeahta cluster (lifetime 64→66)** — different-striker no-chain pair:
- 11224 → 6104 (V13 H22 sb=0, margin +38, EERIE/SCRAP efficacy 2.0).
- 12649 → 6485 (V11 H22 sb=0, margin +38, NORMAL/SCRAP efficacy 1.7).
- Pre-stage + 200s wait + parallel pair (one nonce-collision retry, 5s lossless) + close-feed + stop.
- ~18.10M gas / 2 obols = **0.110 obols/Mgas**.

**Yeahta cluster remaining clean (post-session 134, snapshot 09:30:12Z then strikes)**:
- **1500 V12 H24 sb=0 margin +33 elap 4.7h** — sole sb=0 V<22 candidate above floor, 12649 striker per watcher fix.
- 1374 V15 H19 sb=0 margin +15 elap 2.4h — sub-floor passive, ripening.
- 6505 V19 H21 sb=-50 — sustain off-limits.
- 3699 V11 H23 sb=-50 — sustain off-limits.
- 1847 V10 H20 sb=-25 — sustain off-limits.

**Striker state (post-134 stop, ts 1777887754)**:
- 11224 RESTING node 73 sync 100/140 (rest: ~7 min to top off).
- 12649 RESTING node 73 sync 100/170 (rest: ~12 min to top off).

**Arsenal**: 423 cookies, 4 Apology Letters, 1 Hostility Potion, 66 Obols, ~530.2k MUSU (+ unindexed spoils ~1800 since session 132).

---

## Priority 1 — Yeahta solo-finisher 1500 (in-room)

**Target**: 1500 V12 H24 sb=0 — projected margin ~+35-40 by 10:07 (assuming +5/h ripen). 12649 likely best striker (kz against H24 should be ~+5 better than 11224 for this stat profile).

### STEP 0 — NO `harvest_start` for unused strikers
Only the chosen striker pre-stages. Solo plan = pre-stage 12649 only → 200s wait → fire → close-feed → stop. ~7.7M gas, 1 obol. Skip 11224 (no chain opportunity, no need to deploy).

### STEP 1 — Verify state
- Watcher refresh (cron auto, fresh by 10:07).
- Read `killable_v2`/`top10` for node 73. Confirm 1500 still HARVESTING and ripened ≥+30.
- Yeahta heat re-verify (will be ~25-30 min idle after this session's 2 kills at 09:36 — heat counter restart from 0).
- Striker HP 12649 via slim — should be 100→160-170 over 25 min rest.

### STEP 2 — Decision tree
- **1500 ≥+30 + heat clean + 12649 sync ≥150**: solo strike (pre-stage 12649 → 200s wait → strike → close-feed → stop). ~7.7M gas / 1 obol.
- **1500 sub-+30 (defensive feed by Yeahta)**: HOLD. Re-wake +30 min for ripen / feed clearance.
- **Heat shifted (defensive automation engaged)**: HOLD, vacate at session 136.
- **12649 sync still <150**: solo with 11224 instead (compute margin first; if 11224's kz vs 1500 H24 has margin ≥+25, fire 11224).

### STEP 3 — Striker choice
Compute 11224 vs 1500 V12 H24 max_hp ~190 dts=0 BEFORE pre-stage. Pick whichever striker has higher margin AND ≥150 sync. If tie, prefer 12649 (higher max_hp = more recoil tolerance).

---

## Priority 2 — Watcher cluster scan (cross-region emergence)

Read `killable_v2` for any new non-guild clean candidates outside Yeahta. Cross-region cluster threshold unchanged: ≥3 sb=0 V<22 candidates with average margin ≥+30 OR single V≥22 sb=0 ≥+40 + owner-passive.

**Carry-over from session 133 watcher fix**:
- yeddy node 53: 4768 V11 sb=0 +104, 7263 V13 sb=0 +92 (2 clean — marginal).
- popo node 26: 13964 V11 sb=0 +67, 8962 V12 sb=0 +52, 7476 V10 sb=0 +44 (3 clean — qualifies as cluster).
- TrayzinCarpathia node 60: 898 V14 sb=0 +75 (single).

**popo node 26** is the next-most-ripe cross-region. Worth a pre-trip oracle drill on owner heat next session if Yeahta cluster exhausts (only 1500 + 1374 left at 73).

---

## Priority 3 — Striker affinity-aware planning (carry-over from 134 doctrine)

**EERIE hand vs SCRAP body = 2.0 efficacy** (vs NORMAL/SCRAP 1.7). 11224 (EERIE) is more competitive vs Yeahta cluster than the watcher's striker_idx assignment suggests. **At plan time, manually compute alternate striker margins using `executor.hp_projection.kill_threshold` when a chain opportunity exists.** Watcher's static `striker_idx` only picks one — it hides pair / chain options.

## Priority 4 — Nonce-serialization harness improvement (deferred, low priority)

If parallel-strike nonce collisions recur (saw 1× this session, 5s retry was lossless), draft harness fix in `ideas_to_founder.md`: serialize `_send_tx` per-account internally so MCP callers can fire in parallel safely. Not blocking — skip for now.

---

## Hard limits (unchanged)

- **Gas budget session 135**: ~5M monitor OR ~7.7M if solo fires.
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
- **NEW (134)**: **never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially to avoid nonce collisions. (Or fix the harness.)

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+25 min** (~10:07 UTC May 4, ts 1777889254). Pinned to: (a) 1500 V12 sb=0 ripening from +33 → +35-40 (cross +35 confidence threshold). (b) Striker recovery — 12649 100→160-170 over 25 min rest, 11224 100→140 over 7 min. (c) Watcher refresh ×5 cycles catches Yeahta defensive heat shift after 4 kills/13h. **Bias fire-now**: in-room cluster, only delay is striker-HP wait + ripen window."

**Re-wake**: ~10:07 UTC May 4, ts **1777889254**.

---

## Out of scope (session 135)

- Cross-region travel (Yeahta still has 1500 in-room; popo node 26 worth a pre-trip oracle drill but not commit yet).
- Chain-2 (only 1 valid Yeahta candidate; 1374 sub-floor).
- Sub-floor strikes (1374 +15 ripening but not at floor).
- sb=-50 / sb=-25 strikes (6505/3699/1847).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
