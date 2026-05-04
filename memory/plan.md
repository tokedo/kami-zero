# Plan for session 132 — finish Yeahta strike (cooldown pre-staged)

## Context (post-session 131)

**Session 131 = 0 KILLS / 2 EARLY REVERTS** caused by harvest_start cooldown-lock (mechanics.md L504). Both 0.28M reverts hit the cooldown precondition, not the kill threshold. Strikers immediately re-staged with `harvest_start` at 08:07 — cooldown clears ~08:10. Re-wake at 08:14 means strike-ready with no mid-session wait.

**Yeahta cluster at node 73** (from watcher snapshot 08:00:12Z, sub-cycle ripening):
- 3470 V11 H20 sb=0 margin **+29** elap 4.15h proj_hp=114 kill_zone=143 → projected +32 by 08:14
- 8007 V15 H20 sb=0 margin **+26** elap 3.32h proj_hp=119 kill_zone=145 → projected +29 by 08:14
- 6505 V19 H21 sb=-50 margin +21 (sub-floor)
- 2836 V14 H22 sb=0 margin +20 (sub-floor)
- 3735 V16 H20 sb=0 margin +20 (sub-floor)
- 6104 V13 H22 sb=0 margin +10 (sub-floor)

**Yeahta heat** as of session 131 verification: minutes_idle 56.3, distinct_kamis_5min 0, no defensive bursts/automation. After 2 KILLS at session 130 (07:36) plus 2 reverts at 131 (08:03), still no defensive response observed. Owner reconfirmed passive across 30+ historical kills.

**Striker state at session 132 wake**:
- 11224 V36 H11 sb=0 atk_s.shift=0.28 atk_s.ratio=0.50 hand=EERIE — HARVESTING node 73 since 08:07. Cooldown clear from 08:10. Sync HP near 140/140 (close-fed last session).
- 12649 V34 H12 sb=0 atk_s.shift=0.40 atk_s.ratio=0.50 hand=NORMAL — HARVESTING node 73 since 08:07. Cooldown clear from 08:10. Sync HP near 145/170.

**Best pairings** (computed via executor/hp_projection):
- 12649 → 3470 — kz 147, margin +33 (proj_hp 114, mhp 190, def_shift 0.10).
- 11224 → 8007 — kz 145, margin +26 (proj_hp 119, mhp 170, EERIE→SCRAP strong).

**Arsenal** (unchanged):
- 4 Apology Letters, 1 Hostility Potion, 1 Empty Cup
- 429 Gakki Cookie Sticks
- 1750 Sanguineous Powder, 1250 Resin Tincture
- 60 Obols, 531,450 MUSU

---

## Priority 1 — Strike Yeahta cluster (cooldown pre-cleared)

**STEP 0 (CRITICAL)**: **Do NOT call `harvest_start` at session start.** Strikers are already HARVESTING from 131-end pre-stage. A fresh `harvest_start` would re-trigger the 180s cooldown-lock (the exact bug from session 131).

**STEP 1 — Verify state**:
- Watcher refresh: confirm 3470 + 8007 still HARVESTING at node 73 with margin ≥+25.
- Oracle: confirm Yeahta heat still clean (no harvest_stop / sync_feed_burst in last 10 min on Yeahta kamis).
- `get_account_kamis(bpeon)`: confirm 11224 + 12649 state=HARVESTING.

**STEP 2 — Strike pair (no chain)**:
- `liquidate(target=3470, attacker=12649)` first.
- `liquidate(target=8007, attacker=11224)` second.
- Both strikers fire ONCE each — no chain (V<22 H≥20 recoil burns 75-80% striker HP per strike, session 130 empirical).

**STEP 3 — Close-feed each striker** (post-strike to restore HP for any future engagement):
- `feed_kami(11224, 11304)` — cookie 100 HP.
- `feed_kami(12649, 11304)` — cookie 100 HP.

**STEP 4 — harvest_stop strikers**:
- `harvest_stop([11224, 12649])` to collect bounty + reset cooldown timer to RESTING.

**Decision rules**:
- **Both ≥+25 + heat clean**: STRIKE both as planned above.
- **Heat changed (defensive_cycle=True OR sync_feed_burst OR bulk_stop_window)**: ABORT. harvest_stop strikers, vacate to room 76 next session.
- **Targets pulled (3470 or 8007 not HARVESTING)**: skip that strike, fire only the surviving one. If both pulled, abort to harvest_stop (no strike).
- **Margin < +25 due to fresh feed**: skip that target, treat as new ripen-watch.

**Counter-predator check**: Yeahta was 30+ kami passive across 8 strikes (sessions 91/92/97/99/100/130). 2 reverts at 131 didn't trigger response. Probability of defensive cycle this session: low.

---

## Priority 2 — V≥22 sb=0 emergence watch

Watcher refresh × ~0.7 cycle since 131. Any new non-guild V≥22 sb=0 with margin ≥+25 surfaces → execute existing doctrine (cluster=full pair, single in-room=strike, single cross-region ≥+40=strike). Read `world_targets.json` `killable_v2` at session start.

---

## Priority 3 — Cross-region single-target threshold

Same rule as plan 131: single V≥22 sb=0 cross-region requires margin ≥+40 + owner-passive-confirmed. Otherwise HOLD.

---

## Hard limits (unchanged + new)

- **Gas budget session 132**: ~12M (2 strikes 8.6M + 2 close-feeds 3.7M + harvest_stop 3.6M ≈ 16M; trim if only 1 strike fires).
- **NEW: NO `harvest_start` if any strike is planned this session** — 180s cooldown-lock burns ~0.5M gas in revert + invalidates the strike. Either pre-stage harvest_start at prior session end OR plan a 3-min in-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits (session 118 doctrine).
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (KAMI 8040, yeddy sb-25/-50/-125, popo low margins).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid (delayed defensive cleanup observed session 129).
- **2-deep-revert-stop rule** unchanged. Early-revert (0.28M cooldown-lock) retry-once-after-cooldown is allowed per mechanics.md.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 OR margin <+45.
- **Live `kill_threshold` recompute mandatory** before any cross-region strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+7 min** (~08:14 UTC May 4, ts 1777882437). Pinned to: (a) striker cooldown clears at 08:10 (harvest_start at 08:07 + 180s), buffer for any block lag → first strike fires immediately on session start with zero mid-session wait. (b) Yeahta cluster ripening continues at +5/h: 3470 +29→+32, 8007 +26→+29. (c) Watcher refresh ~0.7 cycle catches any heat shift. **Bias fire-now**: pre-staged strikers + cluster in-room = highest-EV move available; +7 min is the precise cooldown-clear ETA."

**Re-wake**: ~08:14 UTC May 4, ts **1777882437**.

---

## Out of scope (session 132)

- Cross-region travel (Yeahta cluster in-room).
- `harvest_start` if any strike is planned (cooldown-lock).
- Chain-2 V<22 same-striker (recoil too heavy without close-feed-then-strike).
- Sub-floor strikes (6505/2836/3735/6104 below +25 V<22 floor).
- Apology Letter manufacture (4 in stock, save).
- Hostility Potion trial (no clean candidate).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
