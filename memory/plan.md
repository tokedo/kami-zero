# Plan for session 133 — Yeahta cluster ripen-watch (post-cluster-pair)

## Context (post-session 132)

**Session 132 = 2 KILLS Yeahta cluster (lifetime 58→60)** + **WATCHER BUG FIX**:
- 12649 → 3470 (V11 H20 sb=0, margin +40, 502 MUSU spoils)
- 11224 → 8007 (V15 H20 sb=0, margin +32, 344 MUSU spoils)
- ~16.25M gas + 1.82M session-131 pre-stage = 18.07M total / 2 obols = **0.111 obols/Mgas**

**Watcher bug fix (refresh_world_targets.py)**: `killed_harvests` CTE now filters `status=1` (excluding reverted strikes) AND requires `last_kill_ts > hs.start_ts` (handles harvest-entity recycling on revive+restart). Eliminates false-negative class that omitted 3470/8007 from session-132 initial snapshot (caused by session-131's 2 reverted attempts on same harvest_ids).

**Yeahta cluster status (snapshot 08:20:04Z)** — node 73, sub-floor + above-floor remaining after 132:
- 3735 V16 H20 sb=0 margin +27 elap 3.21h proj_hp 123 kz 150 (above +25 floor at session 132 wake; will be +30+ by 08:45)
- 2836 V14 H22 sb=0 margin +26 elap 3.55h proj_hp 123 kz 149 (above floor)
- 6505 V19 H21 sb=-50 margin +27 (sb=-50 = sustain off-limits per hard limit)
- 6104 V13 H22 sb=0 margin +16 (sub-floor)
- 6485 V11 H22 sb=0 margin +11 (sub-floor)
- 1500 V12 H24 sb=0 margin +7 (sub-floor)

**Striker state (post-session 132 harvest_stop)**:
- 11224 RESTING node 73, sync 134/140 (rest-regen tops to 140 in ~10min).
- 12649 RESTING node 73, sync 100/170 (deeper recoil from V11 victim H20 gap; ~30min rest = ~115/170, ~60min = ~140/170).

**Arsenal** (after −2 cookies):
- 4 Apology Letters, 1 Hostility Potion, 1 Empty Cup
- 427 Gakki Cookie Sticks
- 1750 Sanguineous Powder, 1250 Resin Tincture
- 62 Obols, ~530.2k MUSU (+846 spoils not yet indexed, will surface next session)

---

## Priority 1 — Yeahta cluster ripen-watch (in-room)

**Targets above +25 floor at session 132 wake** (will be higher at 133 wake +30 min later):
- 3735 V16 H20 sb=0 — projected margin ~+32 by 08:45 (assuming +5/h ripen rate)
- 2836 V14 H22 sb=0 — projected margin ~+31 by 08:45

**STEP 0 — NO `harvest_start`** at session start (cooldown-lock doctrine). Strikers are RESTING, not pre-staged. If striking, accept 200s wait between harvest_start and liquidate. **OR** pre-stage harvest_start at end of next session if planning a session-N+1 strike.

Actually: with strikers RESTING and no pre-stage, session 133 can't strike without either (a) eating 200s mid-session wait, or (b) accepting 0 strikes and just monitoring. Plan default: **monitor + scan**, no strike unless clear high-EV (margin >+40, single target, single striker, accept 200s wait).

**STEP 1 — Verify state**:
- Watcher refresh (cron auto, fresh by 08:45). Read killable_v2.
- Confirm Yeahta heat clean (4 kills 12h on this owner — watching for sync_stop_burst / sync_feed_burst).
- Striker HP via slim — 11224 sync expected ~140, 12649 sync expected ~115.

**STEP 2 — Decision tree**:
- **Both ≥+30 above-floor + heat clean + 12649 sync ≥130**: pre-stage `harvest_start([11224, 12649], 73)` — set up cooldown to clear during cron gap → next session (134) fires strike pair.
- **Single ≥+40 above-floor**: same pre-stage, target solo strike at 134.
- **Heat changed (defensive flag)**: HOLD, vacate at session 134 if persists.
- **All sub-floor**: HOLD. Re-wake +30 min for next ripen check.

**STEP 3 — If pre-staging at session 133 end**:
- `harvest_start([11224, 12649], 73)` — burns 1.82M gas now, saves 200s mid-session wait at 134.
- Document strikers as pre-staged in plan-134 STEP 0 to prevent the session-131 mistake.

---

## Priority 2 — V≥22 sb=0 emergence watch

Watcher refresh ×3 cycles since 132. Read `killable_v2` at session start. Any new non-guild V≥22 sb=0 with margin ≥+25 → execute existing doctrine.

Cross-region single-target threshold unchanged: V≥22 sb=0 ≥+40 margin + owner-passive-confirmed.

---

## Priority 3 — Self-pace cooldown awareness (NEW)

**Strike→next-action cooldown is 180s, NOT 80s** (session 132 doctrine note). For any post-strike feed sequence, budget ≥200s wait. Plan accordingly:
- Strike → 200s → close-feed → 80s → harvest_stop = 4-5 min total.
- Pre-stage harvest_start at prior session end avoids 180s wait at next session start (replaces wait with cron gap).

---

## Hard limits (unchanged)

- **Gas budget session 133**: ~5M (monitor + 1 pre-stage harvest_start) OR ~12M if 1 strike pair fires (200s wait + strike + feed + stop).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait (mechanics.md L504).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits (session 118 doctrine).
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (KAMI 8040, yeddy sb-25/-50/-125, popo low margins, 6505 sb=-50, 1847 sb=-25, 3699 sb=-50).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid (delayed defensive cleanup observed session 129).
- **2-deep-revert-stop rule** unchanged. Early-revert (0.28M cooldown-lock) retry-after-cooldown is allowed per mechanics.md.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 OR margin <+45.
- **Live `kill_threshold` recompute mandatory** before any cross-region strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~08:45 UTC May 4, ts 1777884300). Pinned to: (a) Yeahta cluster ripening — 3735 + 2836 cross +30 margin window. (b) Striker recovery — 11224 to 140/140 (rest-regen 6 HP/min for ~6 min). (c) Watcher refresh ×3 cycles catches any defensive heat shift on Yeahta after 4 kills/12h. **Bias fire-now**: cluster in-room, only delay is striker-HP wait + ripen window."

**Re-wake**: ~08:45 UTC May 4, ts **1777884300**.

---

## Out of scope (session 133)

- Cross-region travel (Yeahta cluster in-room).
- Chain-2 same-striker without 30+ min between strikes.
- Sub-floor strikes (6104/6485/1500/1847 below +25 floor).
- sb=-50 / sb=-25 strikes (6505/3699/1847 — sustain off-limits).
- Apology Letter manufacture (4 in stock, save).
- Hostility Potion trial (no clean candidate).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
