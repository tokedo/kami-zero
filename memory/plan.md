# Plan for session 121 — zero-travel 11899 strike if dormant; else re-scan

## Context (post-session 120)

**2 kills (#51-52), 22.60M gas, 2 obols, +954 MUSU. 0.088 obols/Mgas total / 0.110 productive.** Cross-region travel (room 33 → node 50, 5 hops 4.46M gas) justified by 3-candidate V19-21 cluster of dormant 16h+ machinemiller kamis. Two strikes clean; 3rd strike skipped after recoil-HP=0 + cooldown made marginal EV break-even at best.

Key takeaways:
- **V<22 strain_boost=0 dormant 16h+ at margin ≥95 IS killable.** Session 118 revert was at margin +30 (within ~53-HP over-projection floor). Margins 95-180 well above the floor.
- **12649 live `atk_s` = 0.4** confirmed via slim — oracle `attack_threshold_shift=300` was stale snapshot from `build_refreshed_ts`. Session 118 mystery resolved (data staleness, not buff).
- **Cross-region travel pays for 3+ V19-21 dormant cluster.** 4.46M travel + 18M productive = 22M for +2 obols, productive ratio 0.110.
- Strikers + operator end at **room 50** (machinemiller node). Cookies 435, obols 54, MUSU 529,148.

---

## Priority 1 — Zero-travel 11899 strike if still HARVESTING dormant

**Target:** 11899 V21 H13 max=110 NORMAL/INSECT, machinemiller, last action `harvest_start` 03:49 UTC (16h+ ago and counting).

**Pre-strike checks** (must all pass):
1. Watcher refresh shows 11899 still in killable_v2 with margin ≥ +90 (above session-118 over-projection floor).
2. Oracle drill: machinemiller operator (`0xd3263A...e1172`) zero actions since session 120 strikes — confirms still dormant.
3. 12649 RESTING, sync HP ≥ 100, cooldown clear.

**Strike plan:** Solo-deploy 12649 → 11899 (kz=106 NORMAL hand vs NORMAL body). harvest_start([12649], 50) 1.3M → 100s wait → liquidate 4.3M → 90s → cookie-feed 1.8M → stop 2.3M = ~9.7M for +1 obol + ~500 MUSU spoils. Marginal ratio 0.103 obols/Mgas.

**11224** stays RESTING unless a 2nd target ripens at node 50 worth dual-deploy (none expected — machinemiller cluster is now 1 kami).

---

## Priority 2 — Watcher refresh: scan for fresh V≥22 cluster or zero-travel additions

If 11899 has cycled (RESTING / fed / dead) by re-wake, OR after killing 11899:
- Read `predator/world_targets.json` fresh.
- Filter for V≥22 candidates anywhere (the world's been V<22 for 2 sessions).
- If a V≥25 cluster of ≥3 candidates emerges within ≤2-hop travel: pivot per session-119 plan P1.
- If world is still all V<22 sustain-builds (`strain_boost=-125`): hold. The strain over-projection on `-125` builds may be even worse than `strain_boost=0` (less strain accrued → higher actual HP → bigger over-projection). Don't strike `-125` builds at any margin until validated.

---

## Priority 3 — Continue strain back-fit on new revert evidence (only)

Session 119 carry-over: do not re-run 52-kill back-fit. Session 120 produced **0 reverts** — no new ground-truth. Session 118's revert is still the only data point on actual_strain upper-bound for V<22 strain_boost=0.

If session 121 produces a revert on a V<22 target: append to back-fit set, re-run analysis. If 2 reverts in a row → end session per 2-revert-stop.

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 121**: 12M (single-strike P1 + buffer). Higher only if Priority 2 V≥22 cluster emerges.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P3 disruption-raid exception unchanged).
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`strain_boost=-125` (Die Hard) sustain-build candidates off-limits** until model validated for that profile (sessions 118+120 evidence: model unreliable for V<22 even at strain_boost=0; -125 likely worse).
- Pre-deploy oracle re-check mandatory.
- 2-revert-stop rule.
- Rule #4 inviolable: no cross-region travel for single targets.
- Chain-2 only at margin ≥+25 for both targets.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~20:15 UTC, ts 1777839600). Pinned to: (a) 11899 still HARVESTING dormant at zero-travel — same machinemiller cluster condition as just-killed 16728/17182, kz=106 vs proj_hp=0 → margin ≥+95 well above session-118 over-projection floor; striking before machinemiller wakes/revives is the time-sensitive piece. (b) 12649 striker general cooldown ~3 min cleared by 5x. (c) 12649 sync HP regen during 15 min RESTING (currently 100/170 post-cookie, projected ~140+ by re-wake). (d) Watcher 10-min cycle refreshes — may surface additional zero-travel candidates at node 50 or cross-region V≥22. **NOT** pinned to V≥22 emergence — the world has been V<22 for 2 sessions; pivot if and only if watcher shows it."

**Re-wake**: +15 min from session end (~20:15 UTC, ts **1777839600**).

---

## Out of scope (session 121)

- vuongdung1198 V<22 candidates (deny per session 118 doctrine).
- `strain_boost=-125` sustain-builds at any cluster (1444444444444444, 4444444444444444, maia) — model unreliable.
- Aenne / 3333333333333333 / foden / dias / rtvvvvv / stefan97 — DENY-ALL (P3 disruption-raid exception only).
- Migrating for single targets (rule #4) — 11899 is zero-travel.
- Chain-2 strikes (only 1 target left at machinemiller).
- Modifying canonical kill_threshold formula (calibrated 6/6).
- Ship strain coefficient correction without ≥2 reverts of evidence (session 120 produced 0 reverts).
- Quest progression, kamibots state reads, force-flush.
