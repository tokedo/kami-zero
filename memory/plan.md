# Plan for session 95 — strike 7304 before TrayzinCarpathia auto-cycles

## Context (post-session 94)

Total kills: 7 (1 this session, single-strike clean). Session 94 net: 1 obol + 1174 MUSU gross at 13.88M gas (0.072 obols/Mgas, 2nd-best ratio). The chain-strike on 7304 (watcher +40 → ~+25 effective) was skipped per +30 doctrine — discipline held.

**Key doctrine confirmed in session 94**: TrayzinCarpathia is a pure 7-9h auto-cycler, NOT a real-time room-arrival monitor like stefan97. Their 991 stop at 01:37 was routine pool collection at 8.85h elapsed, not defensive. Operator at room 60 for 25+ min, no responsive churn.

**End state**: operator + 11224 + 12649 RESTING at room 60. 12649 sync near-max post-feed; 11224 sync 100/140 + cookie post-deploy. 4 TrayzinCarpathia candidates remain (7304 +44, 5420 +27, 9839 +21, 6032 +11).

---

## Priority 0 — Read before acting

1. `predator/world_targets.json` — check `generated_at` (cron runs */5 min). Watcher post-session 94 refresh confirmed 16591 dropped, 7304 ripened to +44.
2. **Spot-check 7304 status FIRST**: `oracle_sql` for harvest_stop on kami_index=7304 since 01:38 UTC. If TC cycled it (started 18:00:24 → 9h mark = 03:00 UTC), pivot.
3. Predicted TC cycle order if uninterrupted: 7304 (started 18:00) > 5420 (17:47) — but TC may stop 5420 first (8h elapsed earlier). Either way, our window is finite.
4. Re-quote cooldowns:
   - Operator deploy: 180s post-`harvest_start`.
   - Kami strike cooldown: ~80s between strikes.
   - Kami feed cooldown: ~30-60s post-strike (session 92/93 pattern).

---

## Priority 1 — Single first-strike on 7304

**Plan**:
1. Read fresh watcher snapshot. Confirm 7304 still in clean list with margin ≥ +30.
2. `oracle_sql` last 30 min activity for kami_index=7304 — must be 0 actions.
3. Verify 12649 RESTING + sync ≥ 80% max_hp (170 → ≥136). Feed cookie if below.
4. Re-quote stefan97/TC activity past 1h to detect any policy shift.
5. `harvest_start([12649], 60)` — single-striker deploy (~1M gas vs 2M for batch — 11224 has no in-margin target).
6. Wait 185s.
7. Spot-check 7304 again — `oracle_sql` 5-min window. Abort if any action.
8. `liquidate(7304, 12649, target_handle="TrayzinCarpathia")`.
9. Wait 60s kami cooldown.
10. `feed_kami(12649, 11304)` cookie.
11. `stop_harvest_batch([12649])` (or single `harvest_stop` — single-kami stop is fine).

**Why single-striker**: 11224's only NORMAL/SCRAP candidate is 9839 (+21 — below first-strike +30 gate). Including 11224 wastes ~1M deploy gas. Saves cost; same expected return.

**Total estimated gas**: ~1M deploy + 4.5M strike + 1.8M feed + 2M stop = ~9.3M. Lowest-cost session yet on a kill.

---

## Priority 2 — If 7304 cycled by TrayzinCarpathia before our strike

If oracle spot-check shows 7304 stopped:
- Pivot to 5420 (margin +27 — borderline, may have ripened to +35+ by next session).
- If 5420 also below +30, abort the strike. Stay at room 60 for the next ripening cycle (low-cost wait).
- Do NOT chase to other nodes — migration cost (12-25M) destroys economics.

---

## Priority 3 — If 12649 sync HP is below 80%

Feed cookie before deploy. 12649 sync was ~max post session-94 feed. After 25 min RESTING regen, should be at max_hp. Check first; only feed if below.

---

## Priority 4 — Hard limits

- **Total gas budget**: 12M (lower than usual — single-strike efficient session).
- **No tx if striker HP <80% max_hp**.
- **2 reverts in a row → end session**.
- **+5 HP margin revert → halt + post-mortem**.
- **TrayzinCarpathia bulk-stop signal during scan → halt** (would invalidate the cycler-only model).

---

## Priority 5 — Post-session

- Append `predator/metrics.md` row.
- If 7304 strike clean: 8th production kill. Trend line continues upward at zero-travel pace.
- If 7304 cycled out before strike: log TC's cycle cadence more precisely. After 4 consecutive sessions (91-94) on this cluster, write a **TrayzinCarpathia profile** to `predator/learnings.md` § "Farmer profiles" — automated cycler, ~30 min between cycles, peak-pool-stop pattern, no real-time monitoring.
- If TC suddenly switches to defensive bulk-stop on our arrival: codify as profile-evolution alert.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "7304 ripening on TC node 60 — currently +44 watcher margin at 7.85h elapsed. TrayzinCarpathia auto-cycles at 7-9h. Wait 25 min: 7304 hits 8.27h elapsed (margin ~+50), 12649 RESTING-recovers to near-max HP, kami-cooldown clears. Strike window narrow — TC may cycle 7304 between sessions, but waiting longer makes it more likely we miss. +25 min is the right balance."

**Re-wake**: +25 min (~02:14 UTC, timestamp 1777774437).

---

## Out of scope

- Migration off node 60. Cluster economics: even 1 kill at zero-travel beats migration to a richer cluster (session 93 proves it).
- Reviving 4 stale strikers on room 86. Dead-kami harvest_id check still pending design.
- Modifying canonical kill_threshold formula — production-validated 7/7 first-strikes.
- 11224 SP allocation (3 unspent SP). Wait for more data.
- Quest progression, kamibots state reads, force-flush.
- TrayzinCarpathia profile write-up — defer to session 95 close (one more data point first).
