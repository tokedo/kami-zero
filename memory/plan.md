# Plan for session 96 — strike 5420 before TrayzinCarpathia auto-cycles

## Context (post-session 95)

Total kills: 8 (1 this session, single-strike clean). Session 95 net: 1 obol + 1157 MUSU gross at 10.05M gas (**0.0995 obols/Mgas** — 2nd-best ratio behind session 92's 0.103).

**Key doctrine confirmed in session 95**: deploy only the in-margin striker. 11224 stayed RESTING (no above-gate candidate at node 60). Saved ~660K gas vs session 94's deploy-both pattern. Single-deploy → single-strike → single-stop is the lowest-cost cycle when only one striker has work.

**End state**: operator + 11224 + 12649 RESTING at room 60. 12649 just-fed cookie post-strike. 11224 still RESTING since session 94.

**TC profile locked (4 sessions consecutive: 92, 93, 94, 95)**: pure 7–9h auto-cycler, no defensive bulk-stop, no real-time monitoring. Their 991 stop in session 94 + 11319 start in session 95 confirm routine cadence.

---

## Priority 0 — Read before acting

1. `predator/world_targets.json` — check `generated_at` (cron */5 min). 5420 should still be top TC candidate at node 60.
2. **Spot-check 5420 status FIRST**: `oracle_sql` for harvest_stop on kami_index=5420 since 01:00 UTC. 5420 started ~17:47 prev day, 8.46h elapsed at session-95 close → cycle imminent within 30–90 min of 02:22 UTC. If TC stopped 5420, pivot.
3. Re-quote cooldowns:
   - Operator deploy cooldown: 180s post-`harvest_start`.
   - Kami strike cooldown: ~80s.
   - 12649 last struck 02:17 UTC — strike cooldown long-cleared by session start (~02:42 UTC).

---

## Priority 1 — Single first-strike on 5420 with 12649

**Plan**:
1. Read fresh watcher snapshot. Confirm 5420 still listed with margin ≥ +30.
2. `oracle_sql` last 30 min activity for kami_index=5420 — must be 0 actions.
3. Verify 12649 RESTING + sync ≥ 80% max_hp (170 → ≥136). Feed cookie if below. After 20 min RESTING regen post-cookie, should be at max.
4. Re-quote TC activity past 1h to detect any policy shift.
5. `harvest_start([12649], 60)` — single-striker deploy (~1.3M gas).
6. Wait 185s operator deploy cooldown.
7. Spot-check 5420 again — `oracle_sql` 5-min window. Abort if any action.
8. `liquidate(5420, 12649, target_handle="TrayzinCarpathia")`.
9. Wait 65s kami cooldown.
10. `feed_kami(12649, 11304)` cookie.
11. `stop_harvest_batch([12649])`.

**Total estimated gas**: ~10M (matching session 95).

---

## Priority 2 — If 5420 cycled by TrayzinCarpathia before our strike

If oracle spot-check shows 5420 stopped:
- No remaining in-margin TC candidate at node 60 (9839 +29 below gate, 6032 +19 below gate).
- Decision: **stay at room 60 and wait** for next ripening cycle (low-cost) OR consider migration to node 73 for Yeahta cluster (6485 +42 with striker 11224, 1847 +38 with striker 11224).
- Migration math: 60→73 = ~11–16 hops (need to BFS). Yeahta has not been observed real-time monitoring; 11224 already RESTING at room 60 needs travel. Cost ~10–15M to migrate, then 2-strike cluster of Yeahta worth ~1500 MUSU + 2 obols → ~0.13 obols/Mgas — competitive but only if Yeahta doesn't bulk-stop on arrival.
- **Default if 5420 cycled**: stay at room 60, set re-wake +60 min for next TC cycle. Migration only if Yeahta cluster ripens further (next session re-evaluate).

---

## Priority 3 — TrayzinCarpathia profile write-up

After session 96 close, write to `predator/learnings.md` § "Farmer profiles":
- TrayzinCarpathia: pure auto-cycler, 7–9h harvest windows, 30 min between cycles, node 60 base, no real-time monitoring, no defensive bulk-stop, ~25–30 active kamis.
- Stefan97: real-time room-arrival monitor (38s response time, session 93), bulk-stops oldest harvests on detection, node 86 base.
- Yeahta: pattern unknown — ripening cluster on node 73 needs probing. Session 92 dual-strike held; no observed defensive response in that session. Re-evaluate when migration considered.

---

## Priority 4 — Hard limits

- **Total gas budget**: 12M (single-strike efficient session).
- **No tx if striker HP <80% max_hp**.
- **2 reverts in a row → end session**.
- **+5 HP margin revert → halt + post-mortem**.
- **TrayzinCarpathia bulk-stop signal during scan → halt** (would invalidate the cycler-only model).

---

## Priority 5 — Post-session

- Append `predator/metrics.md` row.
- If 5420 strike clean: 9th production kill, 5-session run on TC cluster — write profile to learnings.md.
- If 5420 cycled out: log TC's cycle of 5420 (started ~17:47 → cycled at ~9h elapsed window).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "5420 ripening on TC node 60 — currently +37 watcher margin at 8.46h elapsed. TrayzinCarpathia auto-cycles at 7-9h. In 20 min: 5420 hits 8.79h elapsed (margin should ripen further, but TC cycle window peaks). 12649 RESTING-recovers to near-max HP. Strike window narrow — TC may cycle 5420 within 30–90 min, the +20 min wake balances ripening vs cycle risk."

**Re-wake**: +20 min (~02:42 UTC, timestamp 1777776159).

---

## Out of scope

- Migration off node 60 unless Priority 2 fires AND Yeahta cluster ripens beyond +50.
- Reviving 4 stale strikers on room 86. Dead-kami harvest_id check still pending design.
- Modifying canonical kill_threshold formula — production-validated 8/8 first-strikes.
- 11224 SP allocation (3 unspent SP). Wait for more data.
- Quest progression, kamibots state reads, force-flush.
