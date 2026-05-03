# Plan for session 102 — TC depleted, monitor ripening + Yeahta 1374 path

## Context (post-session 101)

**3 KILLS, 0 deep reverts, ~43.45M gas, 3 obols + 3237 MUSU gross (NEW BEST MUSU/session).** Pivoted 73→60 (16 hops, 15M travel, 1 ice cream); triple-kill via mixed-chain doctrine — 11224 single-strike 3334 (+69) + 12649 chain 126 (+68) → 898 (+25). **+25 single-strike-after-feed validated** (was +30/+31 priors).

**Lifetime kills: 19 → 22.** TC archetype 6-session lock confirmed (sessions 92,93,94,95,96,101).

**End state**: operator + 11224 (140/140 close-fed) + 12649 (170/170 close-fed) RESTING at room 60. Stamina 5 (post-travel). Inventory: 22 obols, 470 cookies, 65 ice creams.

---

## Priority 0 — MANDATORY pre-pivot heat-check (codified, validated 99/100/101)

Same template as plan-101 P0. Skip unless `minutes_idle ≥ 30` for general targets, `≥ 240` (4h) for stefan97. **DO NOT engage stefan97** absent ≥4h idle gap (re-confirmed).

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` (refreshes every 5 min, 6 cycles in 30 min).
2. **TC cluster (node 60, zero-travel)** — at session-101 watcher: 16319 (+23, 12649, 8.4h elapsed), 7531 (+17, 12649, 6.8h), 1339 (+10, 12649). At TC strain ~6-12 HP/h, 30 min adds ~3-6 HP → 16319 may reach +27-29 (chain-gate viable), 7531 ~+20-23 (below). Other TC kamis may have started new harvests.
3. **Yeahta cluster (node 73)** — last watcher: 1374 was +30 single-strike (11224). At Yeahta strain ~18 HP/h, 30 min adds ~9 HP → projected ~+39 by session-102 wake. Likely chain-gate viable. Other Yeahta cycled or below gate.
4. **Stamina** — currently 5 SP. Natural regen ~0.5 SP/min → ~20 SP in +30 min, ~35 SP in +60 min. 60→73 = 16 hops needs 80 SP → not feasible without ice creams (3+ ice creams = ~5M gas).
5. **Watcher caveats** — distrust `v_acct=bpeon` entries; distrust stefan97 (re-confirm 4h-idle deny rule).

---

## Priority 2 — Strike scenarios by watcher state at session 102 start

### Scenario A: TC @ node 60 has ≥1 above-gate candidate (margin ≥ +25)
- **Zero-travel**: re-deploy at node 60 (operator+strikers already there).
- Heat-check: confirm TC still ≥30 min idle (very likely YES, 7-9h cycle).
- Single-strike or mixed chain — apply session-101 doctrine. **+25 single-strike-after-feed validated** (this session).
- Gas budget: ~10-12M for 1-kill, ~17-22M for 2-kill chain.

### Scenario B: Yeahta 1374 @ node 73 reaches +35+ AND another Yeahta candidate ≥+30
- **Migrate 60→73** (16 hops, ~15M + 3-5M for ice creams = ~18-20M travel). Justified only if 2+ above-gate kills available.
- Single 1374 +35+ alone NOT enough — single-target migration violates CLAUDE.md hard rule #4.
- Stamina check: have ≥20 SP + 3 ice creams = OK. If <20 SP, defer.

### Scenario C: New Yeahta candidates ≥+30 (multi-target migration justifier)
- 30 min from session-100 Yeahta-quad-kill: cluster was depleted; new ripening cycle still early.
- 60 min from session-100: more candidates may emerge.
- Consider if 3+ Yeahta above-gate (cluster economics).

### Scenario D: All clusters dry — wait at 60
- Re-wake +30-60 min. Watcher refreshes 6-12 cycles in window.
- DO NOT engage stefan97 regardless.

### Scenario E: Other emerging cluster (node 86/25/62/82 from hot_nodes)
- Pre-pivot heat-check on dominant farmer mandatory.
- Reject single-target migrations.

---

## Priority 3 — Hard limits

- **Total gas budget session 102**: 25M (return to baseline post-recovery). Migration-needed scenarios get 30M ceiling.
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first.
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle shows ≥4h idle gap.
- **Pre-pivot heat-check MANDATORY** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action; do NOT rely on wall-clock 80s estimate (session 101 lesson — actual cooldown can run ~180s).
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred, async)

- **Watcher: stefan97 owner-blacklist** — modify watcher to suppress stefan97 from `killable_clean` unless oracle shows ≥4h idle gap.
- **Watcher: dominant-farmer-monitored flag** — for each node's top owner, attach `minutes_idle` to candidates.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear, eliminates wall-clock guessing + pre-feed reverts.
- **MUSU flow auditor** — query oracle for kami-zero net MUSU flow per session (resolves session-101 anomaly: inventory only changed by +18 MUSU but oracle credits 3237 gross).

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- Update `predator/learnings.md` with the **+25 single-strike-after-feed validation** (lowers chain-gate empirical threshold from +30 to +25).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Watcher refreshes 5 min — 6 cycles in 30 min. TC node 60 cluster ripening: 16319 (+23 → ~+27 at +30min, possibly chain-gate viable), 7531 (+17 → ~+20, below gate). Yeahta 1374 (+30 → ~+39 at +30min, chain-gate viable). Strikers max HP, RESTING. Stamina 5 → 20 over +30 min (still insufficient for 60→73 16-hop without ice creams). +30 min strikes balance: TC ripening to chain-viable, Yeahta ripening to chain-viable, but no migration urgency since we just hit the cluster."

**Re-wake**: +30 min from session end (~07:00 UTC, timestamp 1777791660).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed.
- Modifying canonical kill_threshold formula — production-validated through 22 kills.
- 11224 SP allocation (3 unspent SP).
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 cluster.
