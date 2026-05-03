# Plan for session 101 — single-striker chain doctrine continuing; watch 1374 ripening

## Context (post-session 100)

**2 KILLS, 0 reverts, ~17.36M gas, 2 obols + 1343 MUSU.** Zero-travel same-striker chain on Yeahta node 73 (both targets +31 watcher gate). **0.115 obols/Mgas — top-tier ratio**, beats session 96's 0.107.

**Lifetime kills: 17 → 19.** Yeahta archetype 4-session lock validated (sessions 91/92/97/99/100, no defensive evolution).

**End state**: operator + 11224 (140/140 close-fed) + 12649 (170/170, never deployed this session) RESTING at room 73. Stamina ~23 (unchanged).

---

## Priority 0 — MANDATORY pre-pivot heat-check (codified, validated 99/100)

Same template as plan-100 P0. Skip unless `minutes_idle ≥ 30` for general targets, `≥ 240` (4h) for stefan97. **DO NOT engage stefan97** absent ≥4h idle gap (re-confirmed via session 98 trap).

```sql
SELECT COUNT(DISTINCT a.kami_id) AS active_kamis,
       MAX(a.block_timestamp) AS last_action,
       EXTRACT(EPOCH FROM (NOW() - MAX(a.block_timestamp))) / 60.0 AS minutes_idle
FROM kami_action a JOIN kami_static s ON a.kami_id = s.kami_id
WHERE s.account_name = '<OWNER>'
  AND a.action_type IN ('harvest_start', 'harvest_stop')
  AND a.block_timestamp > NOW() - INTERVAL '24 hours';
```

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` (refreshes every 5 min, 6 cycles in 30 min).
2. **Yeahta cluster (node 73)** — post-session-100 chain-kill: 1500/4722 dead. Carry-over candidate **1374 was +17 SCRAP@elapsed_h=2.72 in last watcher**. At Yeahta strain ~18 HP/hr, 30 min adds ~9 HP → projected ~+26 by session start (still below +31 chain-gate, near single-strike margin). Other below-gate Yeahta (e.g., 6485+) may have ripened.
3. **TC cluster (node 60)** — at last watcher: 3334 +56 (11224, SCRAP), 126 +54 (12649, NORMAL). Auto-cycler — by session 101 may have natural cycles or new in-margin candidates. 73→60 travel is multi-hop (16-25 hops); stamina ~23 prohibits without ice creams.
4. **Stamina** — currently ~23. By session 101 wake (+30 min): ~33-43 SP via natural regen (~0.5 SP/min). Still tight for 73→60 travel.
5. **Watcher caveats** — distrust `v_acct=bpeon` entries (chain-vs-watcher conflicts). Distrust stefan97 (synchronized auto-restart cycles, 4h-idle deny rule).

---

## Priority 2 — Strike scenarios by watcher state at session 101 start

### Scenario A: Yeahta @ node 73 has ≥1 fresh candidate above +30 gate
- **Zero-travel**: in-place re-deploy on node 73.
- Heat-check: confirm Yeahta still ≥30 min idle (very likely YES).
- Single-strike (single deploy) if 1 candidate, same-striker chain if 2+ (per session-100 doctrine).
- Minimum gas budget: ~10M for 1-kill, ~17M for 2-kill chain.

### Scenario B: 1374 @ node 73 reaches +25 (single-strike viable, below chain-gate)
- **Zero-travel single-strike on 11224**. Marginal cost ~9.78M for 1 obol + ~500 MUSU = ~0.10 obols/Mgas. Acceptable but not great. **Only fire if** no above-gate target (Scenario A) is available.
- If +25-30 with another Yeahta also above +30: prefer Scenario A's chain doctrine.

### Scenario C: TC @ node 60 has ≥3 above-gate candidates
- 73→60 travel ~16-25 hops. Stamina prohibitive without ice creams (each +20 SP, ~1.5M gas).
- Reject unless ≥3 candidates in margin (justifies travel cost ≥10M). Ideal: 3-4 candidates (quad-kill amortizes travel).
- Heat-check on TC: should pass (5-session lock, no defensive evolution).

### Scenario D: All clusters dry — wait at 73
- Re-wake +30-60 min. Watcher refreshes 6-12 cycles in window.
- DO NOT engage stefan97 regardless of watcher.

### Scenario E: New cluster emergence (node 25, 62, 82 from hot_nodes)
- Pre-pivot heat-check on dominant farmer mandatory.
- Reject single-target migrations (CLAUDE.md hard rule).

---

## Priority 3 — Hard limits

- **Total gas budget session 101**: 25M (post-recovery discipline; session 100 stayed within budget).
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first. Plan: pre-flight check sync HP, feed if needed.
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle shows ≥4h idle gap.
- **MANDATORY pre-pivot heat-check** (P0).
- **80-85s kami cooldown after harvest_start AND post-strike** — strict.
- **Session length cap awareness**: if action plan exceeds ~25 min wall-clock, trim.

---

## Priority 4 — Build asks (deferred, async)

- **Watcher: stefan97 owner-blacklist** — modify watcher to suppress stefan97 from `killable_clean` unless oracle shows ≥4h idle gap. Eliminates session-98 trap class.
- **Watcher: dominant-farmer-monitored flag** — for each node's top owner, attach `minutes_idle` to candidates, downgrade or hide candidates from monitored farmers.
- **Single-striker chain orchestrator** — when watcher shows 2+ above-gate per single striker, auto-suggest chain-kill plan. Already documented in doctrine; implementation optional.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- Update `predator/learnings.md` if any new doctrine emerges (e.g., single-strike on +25-30 Yeahta validation).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Watcher refreshes every 5 min — 6 cycles in 30 min. Yeahta 1374 ripening from +17 → ~+26 (still under +31 chain-gate but approaching single-strike viability +5 canonical). Other below-gate Yeahta (1500/4722 are dead, 6485 was +73 sess 97 — already gone, may have new ones cycle through in 30 min). Strikers HP fed, cooldowns clear. +30 min strikes the right balance: meaningful ripening, lets one full Yeahta natural cycle complete (8-9h cycler), gives TC a tick."

**Re-wake**: +30 min from session end (~06:18 UTC, timestamp 1777789080).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed. Stamina prep required.
- Modifying canonical kill_threshold formula — production-validated through 19 kills.
- 11224 SP allocation (3 unspent SP).
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 cluster.
