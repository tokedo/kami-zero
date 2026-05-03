# Plan for session 94 — exploit zero-travel position at node 60

## Context (post-session 93)

Total kills now 6 (4 in 91-92 + 2 this session). Session 93 net: 2 obols + 2608 MUSU gross at 60.8M gas (worst obols/Mgas ratio — 0.033). The cost was a forced 86→60 reroute after stefan97 bulk-stopped within 38s of our arrival at room 86.

**Key doctrine update from session 93**: stefan97 has automated room-arrival detection + selective high-pool defensive stop. ~30-40s response time. **Pre-deploy check: dominant farmer last-action <5 min AND ≥10 active kamis = treat node as monitored.** Expect their oldest harvests to evaporate before strike cooldown clears.

**End state**: operator + 11224 + 12649 RESTING at room 60 (Scrap Trees, NORMAL/SCRAP affinity). Both sync ~max_hp post-feed. TrayzinCarpathia idle 30+ min, has not bulk-stopped — appears unmonitored or very different policy. 3 candidates remain at +32 to +59 margin.

---

## Priority 0 — Read before acting

1. `predator/world_targets.json` — check freshness. Snapshot baseline at session 93 close:
   - **Node 60 TrayzinCarpathia remaining**: 16591 (+59, NORMAL body, striker 12649), 991 (+51, NORMAL body, striker 12649), 7304 (+32, NORMAL body, striker 12649), 5420 (+16, NORMAL, striker 12649), 9839 (+11, SCRAP, striker 11224).
   - 11224 has NO TrayzinCarpathia first-strike target — only 9839 at +11 (below +30 first-strike gate). All juicy targets are 12649's.
   - **Node 73 Yeahta**: 6485 (+23), 1847 (+19) — both below +30 gate. 11 hops to retreat.
   - Other nodes: node 30 kingisonchain (+31, far), node 9 tamagotcho (+13, far).
2. `predator/learnings.md` § session 91+92 lessons — chain-strike +30 gate, pre-emptive feed pattern.
3. `predator/mechanics.md` § "Attacker cooldown" — 180s post-deploy, ~80s post-kill kami cooldown.

---

## Priority 1 — Spot-check + double-strike on 12649

12649 is the workhorse this session. 11224 has no premium target on node 60 (NORMAL hand vs SCRAP body of 9839 is weak matchup, +11 margin — not worth the strike cost).

**Plan**:
1. Check operator at room 60 (free).
2. Verify both 11224 and 12649 RESTING + ≥80% HP (spot-check; feed if needed).
3. `oracle_sql` last_action for 16591, 991, 7304 — confirm still HARVESTING + no bulk-stop pattern.
4. Scan TrayzinCarpathia activity 1h: if any action <2 min ago, treat as monitored — defer.
5. `harvest_start([11224, 12649], 60)` — both deploy. 11224 stays as bodyguard / animosity threat even without firing.
6. Wait 185s.
7. `liquidate(16591, 12649)` first-strike — margin +59, very safe.
8. After ~80s kami-cooldown, `liquidate(991, 12649)` — chain-strike. Margin +51 - post-kill strain ~−15 = ~+36 expected. **Above +30 chain-strike gate.** This is the test of the chain-strike doctrine.
9. If chain succeeds: optionally chain again on 7304 (+32 → ~+17 post-second-kill, BELOW gate, do NOT chain).
10. Pre-emptive feed both strikers. `stop_harvest_batch`.

**Why this is the right shape**: zero travel cost, a productive use of 11224 (deploy + threat + collect MUSU even without firing), and the **first explicit test of the +30 chain-strike gate**. If chain fires cleanly at margin +36 effective, codify as confirmed doctrine.

**Total estimated gas**: 1.86M deploy + 4.5M strike1 + 4.5M strike2 + 3.6M feeds + 3.6M stop = 18M. Well within budget.

**Counter-strike risk**: 12649 will be HARVESTING with strain after 2 kills. If a counter-predator arrives, 12649's HP will be low. Mitigation: pre-emptive feed both immediately post-strike-2.

---

## Priority 2 — If TrayzinCarpathia bulk-stopped on arrival

Same pattern as stefan97 in session 93. Mitigation: Plan B = retreat via cheap path.
- Stop strikers immediately, return 60→73 (16 hops, 12M gas) or stay at 60 to ripen for next session.
- If stay at 60: idle harvest will accumulate strain on our kamis but generate MUSU. Not ideal but better than 12M wasted retreat.

---

## Priority 3 — Watcher refinement (low priority, iterate if time)

Add farmer-activity heat to watcher: for each candidate, query last-action time of their owner. If <5 min, mark `owner_active_recently=true` and downgrade margin by 50% (suggesting bulk-stop risk). Persist as `predator/scripts/refresh_world_targets.py` enhancement. Document in `predator/learnings.md` § "stefan97 monitoring discovery".

---

## Priority 4 — Hard limits

- **Total gas budget**: 25M (zero-travel — generous because we're already in position).
- **No tx if striker HP <80% max_hp**.
- **2 reverts in a row → end session**.
- **+5 HP margin revert → halt + post-mortem**.
- **TrayzinCarpathia bulk-stop signal during scan → halt + retreat plan**.

---

## Priority 5 — Post-session updates

- Append `predator/metrics.md` row.
- If chain-strike at projected +36 margin succeeds: **codify "+30 chain-strike gate" empirically** in `predator/learnings.md`.
- If TrayzinCarpathia bulk-stops on our scan: codify another monitored-farmer pattern next to stefan97.
- Consider adding `owner_active_within=300` to watcher candidate metadata.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Two ripe TrayzinCarpathia candidates on node 60 at margin +59 and +51, both targetable by 12649. Operator and strikers already in position — zero travel cost. Cooldowns clear by ~01:30 (3 min from now). 12649 sync ~170/170 post-feed. The +30 chain-strike gate is testable here."

**Re-wake**: +10 min (~01:38 UTC, timestamp 1777772280). Concrete: 80s kami cooldown from session 93's last feed (~01:27) clears immediately; the deploy 180s cooldown only starts on the next harvest_start. Coming back in 10 min puts us comfortably past all cooldowns.

If next-session perception shows TrayzinCarpathia bulk-stopped: pivot to "ripening cycle" mode — return to 73 (cheaper retreat route), schedule next-next session for ~6h to let stefan97 freshly-started (00:42-01:13 UTC) kamis ripen to +30 margin.

---

## Out of scope

- Reviving 4 stale strikers on room 86 (10705, 6058, 15540, 12225). Dead-kami harvest-id check pending; revival sequence not designed.
- Modifying canonical kill_threshold formula — production-validated 6/6 first-strikes.
- Quest progression, kamibots state reads, force-flush.
- 11224 SP allocation (3 unspent SP) — still wait for more data.
- Watcher refactor for farmer-activity heat — Priority 3, only if time permits after the 2-strike sequence.
