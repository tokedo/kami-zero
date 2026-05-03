# Plan for session 99 — recover from 86 stefan97 trap; cautious re-pivot

## Context (post-session 98)

**0 kills, 19.72M gas burnt.** Worst predator session yet. Cause: mid-session pivot from plan-98 Yeahta-wait to stefan97 cluster at node 86 without running session-93 pre-deploy heat-check. stefan97 has automated room-arrival defense **with auto-restart** — they bulk-stop+bulk-start every <2h, capping max strain accumulation. Session-93 doctrine ("avoid unless asleep ≥30 min") was too generous; **effective rule: skip stefan97 entirely unless oracle shows a multi-hour idle gap**.

**Total kills lifetime: 13** (no change from session 97).

**End state**: operator + 11224 (140/140) + 12649 (170/170) RESTING at room 86. Stamina 20 (low). Cooldowns long-cleared. Both strikers fresh from cookie feeds.

---

## Priority 0 — MANDATORY pre-pivot heat-check (codified after session 98)

**Before any movement to a new target node, run an oracle activity-heat query on the dominant farmer at that node.** If the farmer's `MAX(block_timestamp) > NOW() - INTERVAL '5 minutes'` AND they have ≥10 active kamis at the node, **abort the pivot** and either wait or pick a different node.

```sql
-- Activity heat query template (parameterize OWNER, NODE):
SELECT
  COUNT(DISTINCT a.kami_id) AS active_kamis,
  MAX(a.block_timestamp) AS last_action,
  EXTRACT(EPOCH FROM (NOW() - MAX(a.block_timestamp))) / 60.0 AS minutes_idle
FROM kami_action a JOIN kami_static s ON a.kami_id = s.kami_id
WHERE s.account_name = '<OWNER>'
  AND a.action_type IN ('harvest_start', 'harvest_stop')
  AND a.block_timestamp > NOW() - INTERVAL '24 hours';
```

**Skip unless `minutes_idle ≥ 30` for general targets, or `≥ 240` (4h) for stefan97.**

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. **Distrust stefan97 entries entirely** — they're all false-positives from kami_static reset_ts lag.
2. **Yeahta cluster (node 73)** — was 3699 +25 / 2836 +26 / 3470 +25 at session 98 start (gen 04:25Z). +56 min minimum elapsed by session 99 → expect 3699 ≈ +33-37, 2836 ≈ +30+, 3470 ≈ +27+. Live-spot-check before committing travel back.
3. **TC cluster (node 60)** — was 3334 +34 (11224 SCRAP) and 126 +31 (12649 NORMAL) at last watcher. +56 min elapsed → margins continuing to grow if uninterrupted.
4. **Stamina**: currently 20. Each minute restores ~0.5-1 SP. By session 99 wake (~+45 min), expect 25-30 SP. **Low for travel** — 11 hops requires ~55 SP, will need 1-2 ice creams.

---

## Priority 2 — Strike scenarios by watcher state at session 99 start

### Scenario A: Yeahta @ node 73 has ≥1 candidate above +30 gate
- **Travel 86→73 = 11 hops, stamina 55 needed**. With 25-30 SP available, need 2 ice creams (each +20 SP).
- Travel cost ~10M gas + 2 ice cream tx ~3M = ~13M.
- Then deploy + pre-feed (HP should still be max from session 98 closure) + chain-strike.
- Single kill estimate: 13M travel + 1.34M deploy + 4.5M strike + 1.8M feed + 2.34M stop = ~23M for 1 obol + ~700 MUSU. Ratio ~0.043 obols/Mgas (poor).
- **2 kills via chain-strike**: same +3.6M (extra strike + feed) for +1 obol +600 MUSU = +0.087 marginal. Worth it if chain target is +30+.
- **Heat-check**: Yeahta last action time. Yeahta has been benign across sessions 91-92-97 (no defensive pattern). Heat-check: skip if active in last 5 min AND ≥10 active kamis. Otherwise proceed.

### Scenario B: TC @ node 60 has ≥2 candidates above +30 gate
- **Travel 86→60 unknown hops** (was 25 hops via 86→...→60 in session 93). Stamina prohibitive without 3+ ice creams. ~25M+ gas travel.
- Reject unless TC cluster shows ≥3 in-margin candidates AND stamina restoration cheap.

### Scenario C: All clusters dry — wait at 86
- Re-wake +30-60 min. Watcher refreshes, scenarios refresh.
- DO NOT engage stefan97 regardless of what watcher shows.

### Scenario D: Yeahta cluster shows defensive shift (multiple stops past 30 min)
- Halt; write to alerts.md. Yeahta has been the most reliable archetype — defensive shift would be a major intel update.

---

## Priority 3 — Hard limits

- **Total gas budget session 99**: 25M (need to claw back from session 98 deficit).
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first. (Both at max post-session-98.)
- **2 reverts in a row → end session.**
- **stefan97 deny-all** until oracle shows ≥4h idle gap.
- **MANDATORY pre-pivot heat-check** — enforced this session, plan-99 P0.
- **80s kami cooldown after harvest_start** — strict.
- **Session length cap awareness**: if action-plan exceeds ~25 min wall-clock, trim.

---

## Priority 4 — Build asks (deferred)

- **Watcher: stefan97 owner-blacklist.** Modify `scripts/watcher.py` (or wherever the watcher cron lives) to suppress stefan97 from `killable_clean` unless oracle shows ≥4h idle gap. Eliminates the trap I fell into this session.
- **Watcher: dominant-farmer-monitored flag.** For each node's top owner, run the activity-heat query at watcher refresh time, attach `minutes_idle` to candidates, and downgrade or hide candidates from monitored farmers.
- See `ideas_to_founder.md` for visibility (async, non-blocking).

---

## Priority 5 — Post-session

- Append `predator/metrics.md`.
- If session 99 yields 0 kills again, re-evaluate cluster/cluster intel. Yeahta may have evolved a defensive pattern (the +25 ceiling for ~50 min suggests they may be self-cycling at ~6-8h cadence).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Stamina regen ~45 min to reach 25-30 SP for return travel. Watcher refreshes 9 times in 45 min. Yeahta candidates were +25-26 at 04:25Z — should cross +30 first-strike gate at +50-60 min. stefan97 cycle locks them out for hours."

**Re-wake**: +45 min (~05:21 UTC, timestamp 1777785300).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — re-investigate when reunified.
- Modifying canonical kill_threshold formula — production-validated.
- 11224 SP allocation (3 unspent SP).
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 cluster.
