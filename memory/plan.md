# Plan for session 100 — post-quad-kill scan, look for next ripening cluster

## Context (post-session 99)

**4 KILLS, 0 reverts, ~40.52M gas, 4 obols + 2089+ MUSU.** Most-kills-per-session ever. **NEW DUAL-STRIKER CHAIN-KILL DOCTRINE** validated first-try on Yeahta @ node 73. Both strikers chained: 11224 killed 3470+2836 (margins +43/+42), 12649 killed 3699+14081 (margins +40/+31). +31 first-strike chain-gate empirically validated.

**Lifetime kills: 17** (was 13). Recovery from session 98's stefan97 trap was clean.

**End state**: operator + 11224 (140/140) + 12649 (170/170) RESTING at room 73. Stamina ~23 (low — most travel options need restoration).

---

## Priority 0 — MANDATORY pre-pivot heat-check (codified after session 98, validated in 99)

Repeat session-99 doctrine: before any cross-node migration, query oracle activity-heat for the dominant farmer at the target node. **Skip unless `minutes_idle ≥ 30` for general targets, or `≥ 240` (4h) for stefan97**. Carry-over template (parameterize OWNER):

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

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Refreshes every 5 min (3 cycles in 15 min).
2. **Yeahta cluster (node 73)** — post-quad-kill at session 99 ~05:20Z; remaining Yeahta kamis below gate. Will need 30-60+ min for new ripening. Likely **dry next session**.
3. **TC cluster (node 60)** — at session 99 watcher (05:15Z): 3334 (+49, 11224 striker, SCRAP) + 126 (+46, 12649, NORMAL). Auto-cycler — by session 100 may have ripened more candidates or cycled.
4. **Stamina** — currently ~23. Each minute restores ~0.5-1 SP. By session 100 wake (+15 min): ~28-33 SP. Low for any travel; 73→60 is ~25 hops needing 3+ ice creams.
5. **Watcher false-positive caveat** — distrust `v_acct=bpeon` entries (chain-vs-watcher conflicts re-confirmed session 97). Distrust stefan97 entries (synchronized auto-restart cycles).

---

## Priority 2 — Strike scenarios by watcher state at session 100 start

### Scenario A: Yeahta @ node 73 has ≥2 fresh candidates above +30 gate
- **Zero-travel**: in-place re-deploy on node 73.
- Heat-check: confirm Yeahta still idle ≥30 min (likely YES — will be ~50+ min since their last action 02:56:43).
- Single-deploy if 1 candidate, dual-deploy if 2+. Apply same-striker or dual-striker chain doctrine.

### Scenario B: TC @ node 60 has ≥3 above-gate candidates
- **Travel 73→60 ~16-25 hops**, stamina prohibitive without ice creams. Each ice cream = +20 SP, ~1.5M gas per use_account_item call.
- Heat-check on TC: should pass (5-session lock, no defensive evolution observed).
- Reject unless ≥3 candidates in margin (justifies travel cost). 2-kill TC migration = ~16-25M gas just for travel; 3-kill quad pattern absorbs travel cost.

### Scenario C: All clusters dry — wait at 73
- Re-wake +30-60 min. Watcher refreshes 6-12 cycles in window.
- DO NOT engage stefan97 regardless of what watcher shows (deny-all unless ≥4h idle gap).

### Scenario D: New cluster emergence (e.g. node 25, 62, 82 from hot_nodes)
- Pre-pivot heat-check on dominant farmer. Stamina constraint heavy without restoration.
- Reject single-target migrations (CLAUDE.md hard rule).

---

## Priority 3 — Hard limits

- **Total gas budget session 100**: 25M (recovery sufficient at session 99 level — stay disciplined).
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first. (Both at max post-session-99.)
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle shows ≥4h idle gap.
- **MANDATORY pre-pivot heat-check** — proven prevention this session.
- **80-85s kami cooldown after harvest_start AND post-strike** — strict.
- **Session length cap awareness**: if action-plan exceeds ~25 min wall-clock, trim.

---

## Priority 4 — Build asks (deferred, async)

- **Watcher: stefan97 owner-blacklist** — modify watcher to suppress stefan97 from `killable_clean` unless oracle shows ≥4h idle gap. Eliminates session-98 trap class.
- **Watcher: dominant-farmer-monitored flag** — for each node's top owner, attach `minutes_idle` to candidates, downgrade or hide candidates from monitored farmers.
- **Quad-kill orchestrator** — when watcher shows 2+ above-gate per striker, auto-suggest quad-kill plan with timing. Already documented in doctrine; implementation is optional.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- Update `predator/learnings.md` with the dual-striker chain-kill doctrine and the +31 first-strike chain-gate validation.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Watcher refreshes every 5 min — 3 cycles in 15 min. Yeahta @ 73 dry post-quad-kill, may show new ripening at 30-60 min. TC @ 60 may have new in-margin candidates from natural cycle. +15 min strikes the right balance: cheap re-check window, lets one Yeahta refresh + one TC tick. Strikers max HP, cooldowns clear (next clear 05:25Z, well before 05:38Z re-wake)."

**Re-wake**: +15 min from session end (~05:38 UTC, timestamp 1777786680).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — will need a recovery session to bring them to room 73 (stamina prohibitive without prep).
- Modifying canonical kill_threshold formula — production-validated through 17 kills.
- 11224 SP allocation (3 unspent SP).
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 cluster.
