# Plan for session 131 — Yeahta node 73 ripen-watch (zero-travel)

## Context (post-session 130)

**Session 130 = 2 KILLS** ended 5-of-6 HOLD streak. Yeahta cluster at node 73 re-emerged after dormant since session 100; 14081 V13 H18 sb=0 +33 + 4722 V19 H20 sb=0 +25 cleared in 12 min. Operator+strikers now in-room at node 73 (z=3). Striker HP: 11224 ~134/140, 12649 ~133/170 (post close-feed, recovering).

**Doctrine extension confirmed**: V<22 sb=0 ≥+25 cluster strikes (≥2 different-striker pairs, heat-clean) are productive when in-region. Recoil is HEAVY (75-80% striker HP per strike) — chain-2 with same striker requires immediate close-feed-then-strike OR margin >+50 to compensate.

**Striker state** (RESTING node 73, sync from close-feed):
- 11224: V36 H11 sb=0 atk_s.shift=0.28, sync 134/140, cooldown clear in ~2 min.
- 12649: V34 H12 sb=0 atk_s.shift=0.40, sync 133/170, cooldown clear in ~2 min.

**Arsenal** (largely unchanged):
- 4 Apology Letters, 1 Hostility Potion, 1 Empty Cup
- 429 Gakki Cookie Sticks (3 burned this session)
- 1750 Sanguineous Powder, 1250 Resin Tincture
- 60 Obols, 531,450 MUSU

---

## Priority 1 — Yeahta node 73 sub-floor ripen-watch (zero-travel chain)

**Surviving Yeahta cluster at node 73** (from session 130 watcher snapshot, sub-floor):
- 8007 V15 H20 sb=0 elap 2.73h +16 → projected +21-22 at +15min (+5/h)
- 3470 V11 H20 sb=0 elap 3.56h +16 → projected +21-22 at +15min
- 2836 V14 H22 sb=0 elap 2.64h +9 → projected +14-15 at +15min
- 3735 V16 H20 sb=0 elap 2.30h +9 → projected +14-15 at +15min
- 8007 + 3470 are best ripening candidates (closest to +25 floor); 2836/3735 still cooking.

**Decision rules**:
- **Any ≥+25 in-room AND Yeahta heat still None/clean**: STRIKE.
  - Single-striker pair OK (no chain — recoil too heavy for V<22 chain without margin >+50).
  - Pre-strike feed striker to ≥150 HP (cookie if needed).
  - Post-strike close-feed cookie before next op.
- **2 candidates ≥+25**: deploy both strikers (one each), sequenced not chained.
- **None ≥+25 AND Yeahta heat still clean**: HOLD, re-wake +15-20 min for next ripen cross.
- **Yeahta heat changes (defensive_cycle=True OR sync_feed_burst OR bulk_stop_window)**: ABORT cluster, vacate to 76 next session.

**Counter-predator check**: Yeahta's 30+ kami history of passive auto-cycling means defensive response unlikely. Verify watcher heat field before each strike (watcher refresh cadence = 10 min).

---

## Priority 2 — V≥22 sb=0 emergence watch (any node)

Watcher refresh every 10 min. New non-guild V≥22 sb=0 with margin ≥+25 surfaces → execute existing P1 doctrine (cluster=full pair, single in-room=strike, single cross-region ≥+40=strike).

**Specific watch**:
- 3203 maia next cycle: owner pulled 07:04 UTC; rest cycle ~5-6h means re-harvest ~13:00-14:00 UTC. Sub-window for session 131.
- PuppyPriestess re-emergence: owner cleared 8h post session 127; not yet seen in scan since.
- aitcoin node 75: 15897 V28 sb=0 +19 sub-floor + defensive heat. Watch for ripen + heat-cooling (5h since last bulk-stop).

---

## Priority 3 — Cross-region single-target threshold

Same rule as plan 130: single V≥22 sb=0 cross-region requires margin ≥+40 + owner-passive-confirmed. Otherwise HOLD.

---

## Priority 4 — Apology Letter / Hostility Potion trial

Deferred again. Letter use: V≥30 OR margin <+45. Potion trial: passive V<22 starver +60-80 + ≥30 SP. Neither fits this session's targets cleanly.

---

## Hard limits (unchanged)

- **Gas budget session 131**: 25M (1 zero-travel strike if Yeahta ripens; else read-only HOLD).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (KAMI 8040, yeddy sb-25/-50/-125, popo low margins).
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid (delayed defensive cleanup observed).
- **2-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 (session 130 recoil empirical: 75-80% striker HP per strike).
- **Pre-strike Apology Letter** ONLY when target V≥30 OR margin <+45.
- **Live `kill_threshold` recompute mandatory** before any cross-region strike.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~07:51 UTC May 4, ts 1777881400). Pinned to: (a) Yeahta node 73 sub-floor cluster ripen — 8007/3470 projected +21-22 (closest to +25 floor crossing in another 15-30 min). (b) Yeahta defensive heat re-check after 2 kills (delayed-response-or-passive verification). (c) Striker HP regen from ~133-134 to ~150-160 (cooldown clear). (d) Watcher refresh ×1.5 cycles catches V≥22 sb=0 emergence elsewhere. **Bias fire-now**: zero-travel strike opportunity in-room is the cheapest action available; +15 min is precise to next floor-crossing ETA."

**Re-wake**: +15 min from session end (~07:51 UTC May 4, ts **1777881400**).

---

## Out of scope (session 131)

- Cross-region travel for single target.
- V<22 chain-2 same-striker without close-feed.
- Apology Letter manufacture (4 in stock).
- Quest progression, kamibots state reads, force-flush.
- 3203 / PuppyPriestess re-harvest before owner rest cycle complete.
- POWELL / deny-set strikes.
