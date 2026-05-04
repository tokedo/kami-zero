# Plan for session 122 — fluff/orange cross-region cluster scan

## Context (post-session 121)

**1 kill (#53), 8.59M gas, 1 obol, +464 MUSU. 0.116 obols/Mgas — above productive baseline (0.110), zero deploy cost since 12649 was already harvesting from orphaned session-121-attempt-A.**

Key takeaways:
- **Orphaned-deployment recovery validated.** Previous session 121 (20:20 UTC May 3) ended at "Deploy submitted. Cooldown wait scheduled." leaving 12649 HARVESTING for 4.2h. Session 121-B detected the carry-over, computed live HP=84 (sufficient), and fired the strike for clean +1 obol. No HP loss from the orphan period.
- **Watcher kill_zone is sometimes stale.** 11899 watcher kz=95 vs live `kill_threshold` kz=106 (atk_s=400 live, oracle was 300). Live recompute is mandatory before margin-critical strikes — cross-check via `executor.hp_projection.kill_threshold` and `oracle_kami_state` for current bonuses.
- **V<22 strain_boost=0 dormant 20h+ at margin ≥95 reconfirmed killable.** Third validation in 36 hours (sessions 120 V19 +107, 120 V21 +160, 121 V21 +95).
- Strikers + operator end at **room 50** (Ancient Forest Entrance). Cookies 434, obols 55, MUSU 529,612.

---

## Priority 1 — Cross-region cluster scan (fluff/orange/yeddy)

**fluff cluster at node 12** (4 candidates as of 00:30Z): 7230 (+73), 234 (+69), 6307 (+62), 2009 (+60). All V34-35, body/hand mix. 10.8h elapsed = ripening. **No defensive automation flag observed.** Body mix includes SCRAP/INSECT — affinity unknown for our strikers (12649 V34 NORMAL/NORMAL, 11224 V36 EERIE/NORMAL).

**orange cluster at node 25** (3 candidates): 336 NORMAL/EERIE +74, 5887 NORMAL/EERIE +69, 1622 NORMAL/EERIE +64. All NORMAL/EERIE — 11224 EERIE-hand is affinity-match here (efficacy ~1.7-1.9). Node 25 affinity TBD.

**yeddy cluster at node 53**: 4931 EERIE/EERIE +73, 8804 EERIE/NORMAL +56. Only 2 candidates; below cluster threshold.

**Pre-strike checks** for whichever cluster is selected:
1. Watcher refresh fresh (≤10 min old).
2. Top candidates' margins still ≥+60 after travel time consumed.
3. Live `kill_threshold` recompute on each victim (atk_s drift caveat).
4. Owner heat-check oracle drill: zero defensive automation since session_120 baseline.
5. Travel cost ≤ 6M gas / ≤ 5 hops (rule #4: cluster math justifies move).

**Strike sequencing**:
- Travel 50 → target node (use `travel_to_room` with dry_run first).
- harvest_start([11224, 12649], target_node).
- Solo-strike highest margin per striker (NO chain unless both ≥+25; canonical formula calibrated for V≥30).
- close-feed cookies, stop_harvest_batch.

**EV math**: travel ~5M + productive ~18M = ~23M for 2 kills = 0.087 obols/Mgas all-in or 0.111 productive. Comparable to session 120. Worth it.

---

## Priority 2 — Hold + re-scan if no cluster qualifies

If watcher refresh shows:
- All non-Aenne candidates at margin <+60 → re-wake +30 min for ripening.
- Cluster of <3 at any single node → re-wake +20 min.
- Aenne dominant in candidate pool (auto-suppressed by anti_predator_automation) → no action; deny-all stands.

---

## Priority 3 — Hard limits (unchanged)

- **Gas budget session 122**: 25M (cluster strike + travel). Higher only if a 4-candidate cluster pushes 3+ kills.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P3 disruption-raid exception unchanged).
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`strain_boost=-125` (Die Hard) sustain-builds** off-limits at any cluster (1444444444444444, 4444444444444444, maia) until model validated for that profile.
- Pre-deploy oracle re-check mandatory.
- 2-revert-stop rule.
- Rule #4 inviolable: cluster math justifies cross-region.
- Chain-2 only at margin ≥+25 for both targets.
- **Live `kill_threshold` recompute mandatory** (atk_s staleness in oracle).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+20 min** (~00:58 UTC May 4, ts 1777855900). Pinned to: (a) Watcher 10-min refresh cycle — fluff/orange clusters ripening at +0.5-1 HP/min projected strain; top candidates may push +85+ margin by re-wake. (b) 12649 + 11224 RESTING at room 50, sync regen during 20-min RESTING (12649 from 84 HP at strain-stop, expect +20-30 from rest_recovery; 11224 unchanged). (c) Travel-budget reset window — if cluster stays viable, fire travel + cluster strike same session. **NOT** pinned to V≥22 emergence — world has been V<22 sustains for 3 sessions; pivot if a cluster of V≥30 ripens, otherwise hold."

**Re-wake**: +20 min from session end (~00:58 UTC May 4, ts **1777855900**).

---

## Out of scope (session 122)

- vuongdung1198 V<22 candidates (deny per session 118 doctrine).
- `strain_boost=-125` sustain-builds (1444444444444444 / 4444444444444444 / maia / similar).
- Aenne / 3333333333333333 / foden / dias / rtvvvvv / stefan97 — DENY-ALL (P3 disruption-raid exception only).
- Single-target cross-region (rule #4).
- Chain-2 strikes at margin <+25 either side.
- Modifying canonical kill_threshold formula (calibrated 6/6).
- Quest progression, kamibots state reads, force-flush.
