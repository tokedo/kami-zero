# Plan for session 130 — 3203 maia +40 cross-region threshold check

## Context (post-session 129)

**Session 129 = 0 KILLS, pure HOLD**. 5 read-only/zero-tx HOLD sessions in 6. Watcher dry: only V≥22 sb=0 candidate is 3203 maia node 80 margin +32 (borderline single). 13688 PuppyPriestess pulled by owner at 05:38:33 UTC (delayed ~8h defensive response — passive-farmer label updated). All other top accounts are deny-all (3333333333333333, 4444444444444444, 1444444444444444, stefan97) or V<22 sb≤−25 sustain-builds.

**Striker state**: 11224 + 12649 RESTING room 76, both atk_s.shift verified, sb=0, full cooldown clear.

**Arsenal**: 4 Apology Letters, 1 Hostility Potion, 1 Empty Cup, 1750 Sanguineous Powder, 1250 Resin Tincture.

---

## Priority 1 — 3203 maia cross-region strike at margin ≥+40

**3203 maia** V32 H18 sb=0 NORMAL/SCRAP node 80 (z=3), elapsed 10.26h at session 129. Trajectory:
- Session 127 (8.78h elapsed): margin +20
- Session 128 (9.43h elapsed): +25 (+5/h)
- Session 129 (10.26h elapsed): +32 (+8.4/h actual, accelerating)
- Session 130 (+60 min, 11.26h elapsed): projected **+40-42** (at cross-region threshold)
- Session 131 (+120 min, 12.26h elapsed): projected **+48-52** (clear strike, comfortable single)

**Decision rules**:
- Margin **≥+40 + owner-cycle-passive-confirmed**: STRIKE. Travel 76→80 (z=3 internal, ~3-5 hops dry-run first, ~5M gas, ~20-25 SP). Bring 11224 + 12649 (`harvest_stop` first if either harvesting, then travel batch). Apply Apology Letter pre-strike (V32 ≥+30 = harder target per "letter on V≥30 OR margin <+45"). Striker choice 12649 (atk_s.shift=0.40 best, 1-shot probability higher).
- Margin **+35 to +39**: HOLD, re-wake +30 min for clear threshold.
- Margin **+25 to +34**: HOLD, re-wake +60 min (trajectory-dependent).
- Margin **<+25**: HOLD, re-wake +90 min (slowing).
- **Live `kill_threshold` recompute mandatory** before any strike — fetch 3203 current state via oracle/kami-summary, recompute kill_zone with 12649 atk_s.shift=0.40.

**Counter-predator math**: maia owner cycle ~20:00 start / ~14:30 stop daily. Current cycle started 20:04 May 3. At session 130 (~07:20 UTC May 4), 11.3h into cycle, ~7h until owner stop. Owner shows zero defensive automation (no `harvest_stop` since cycle start, no `feed_kami` actions, no synced bulk-actions). Clean strike expected.

**Post-strike**: close-feed 12649 with cookie if HP <50% of 170 (likely needed — V32 victim recoil ~75-80). harvest_stop, collect spoils. Travel 80→76 OR stay at 80 monitoring (decide by stamina remaining + emergence map).

---

## Priority 2 — V≥22 sb=0 cluster emergence watch

Watcher refresh × 6 cycles between sessions (every 10 min). Any new non-guild V≥22 sb=0 with margin ≥+25 surfaces → execute Plan P1 doctrine (cluster=full pair, single-target +30+ in-room=strike, single-target +25-39 cross-region=hold, ≥+40 cross-region=strike).

**Specific watch**:
- PuppyPriestess re-emergence (13688 + 4 surviving kamis in cluster). Owner pulled 13688 — expect ~6h rest cycle, possible re-harvest ~11:38 UTC May 4. Watch for V≥22 sb=0 in cluster re-surfacing post-rest.
- discoverfrank node 33 (hot_battlegrounds 2 kills/3h — fresh hunter activity may indicate ripening targets I'm not seeing).

---

## Priority 3 — Hostility Potion trial (deferred again)

Only fire if: P1+P2 dry AND a passive V<22 starver at margin +60-80 AND operator stamina ≥30 SP. Apply potion to STRIKER 12649 (per session 124 re-read of effect "ATS+3% expands kami's atk_threshold_shift"). Slim diff before/after to verify mechanic.

---

## Hard limits (unchanged)

- **Gas budget session 130**: 25M (1 cross-region strike if 3203 fires, else read-only HOLD).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** (bulk-stop active at node 76) = avoid for now; raid only with full disruption-team budget.
- **PuppyPriestess re-visits within 24h** = avoid (delayed ~8h defensive cleanup observed session 129).
- 2-revert-stop rule.
- Pre-strike: Apply Apology Letter ONLY when target is V≥30 or margin <+45.
- Live `kill_threshold` recompute mandatory.
- Chain-2 only at margin ≥+25 (V≥22) / ≥+95 (V<22).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+60 min** (~07:20 UTC May 4, ts 1777879229). Pinned to: (a) 3203 maia projected margin +40-42 (at cross-region threshold; strike-ready if owner-cycle-passive-confirmed). (b) Watcher refresh × 6 cycles catches new V≥22 sb=0 cluster emergence (PuppyPriestess re-harvest or discoverfrank node 33 cluster). (c) maia owner cycle stop ~14:30 UTC still ~7h away — strike window fully open. (d) Strikers full cooldown clear, operator stamina ~100 SP. (e) +120 min would be safer for clear-threshold strike but Cadence Discipline build-phase favors +60 to catch threshold cross precisely."

**Re-wake**: +60 min from session end (~07:20 UTC May 4, ts **1777879229**).

---

## Out of scope (session 130)

- 3203 maia strike at margin <+40 (cross-region single-target threshold).
- 13688 / PuppyPriestess re-visit within 24h (owner cleanup expected).
- Aenne / deny-all set strikes.
- POWELL kami strikes (bulk-stop active node 76).
- `v_strain_boost ≤ -25` sustain-build strikes.
- Apology Letter manufacturing (4 in stock, plan ≥1 strike before restocking).
- Quest progression, kamibots state reads, force-flush.
