# Plan for session 91 — TrayzinCarpathia migration window (first kill on canonical formula in production)

## Context (post-session 90)

Session 90 shipped Cadence Discipline doctrine, built the world_targets.json background watcher (5-min cron, atomic write), and ran a full recon over alternative nodes. Surfaced two migration-worthy clusters:

- **Node 60 SCRAP — TrayzinCarpathia** (5 candidates margin +18 to +50, 0 recent liquidates → quiet pocket)
- **Node 73 SCRAP — Yeahta** (4 candidates margin +10 to +69, 0 recent liquidates)

All 6 bpeon strikers RESTING_OR_DEAD on operator-room node 86. Node 86 hunting field is now stefan97 (synchronized cycle, bulk-stops on a timer) + rtvvvvv (no-touch list, 3 reverts) + guild-blocked. Net: node 86 is structurally dry for non-guild high-margin candidates.

This session's pin: **first migration after watcher ship; want fresh snapshot from cron + spot-check candidate persistence before 6-striker move (~26M gas).**

---

## Priority 0 — Read before acting

1. Re-read `predator/mechanics.md` § "Attacker cooldown" (line 504-507): **180s** post-`harvest_start`, not 80s. Wait ≥185s before any liquidate. Plan-89 misquoted "80s" → 0.28M gas revert. Plan 91 will not repeat.
2. Re-read `predator/learnings.md` § "2026-05-02 23:30 UTC — Cluster intel snapshot" — TrayzinCarpathia top 5 candidate list, room mapping, counter-predator note.
3. Read `predator/world_targets.json` — should be ≤5 min fresh (cron runs every 5 min). If `generated_at` > 10 min ago, run `python3 predator/scripts/refresh_world_targets.py` inline.

---

## Priority 1 — Verify cluster persistence (free reads only)

**Before any tx**, confirm the TrayzinCarpathia cluster is still hot:

1. Read `predator/world_targets.json`. Locate node 60 in `by_node`.
2. If killable_count ≥ 3 with margin ≥ +18 on node 60: proceed to P2.
3. If killable_count < 3 OR top margin dropped below +15: candidates may have stopped/fed. Spot-check directly via oracle (use `/tmp/recon90.py` re-run pattern). If still soft, proceed to P2 with adjusted target list. If gone, fall through to P5 (alternative pivot).

---

## Priority 2 — Counter-predator scan on node 60

**Critical pre-deploy check**. Hunt the hunters.

```sql
-- Find any kami currently HARVESTING on node 60 with attack stats that could threaten our deployed strikers.
WITH harvesters AS (
  SELECT kami_id FROM kami_action a
  WHERE a.action_type='harvest_start' AND a.node_id='60'
    AND a.block_timestamp >= NOW() - INTERVAL 24 HOUR
    AND NOT EXISTS (SELECT 1 FROM kami_action b
                    WHERE b.kami_id=a.kami_id
                      AND b.block_timestamp > a.block_timestamp
                      AND b.action_type IN ('harvest_stop','harvest_liquidate'))
)
SELECT ks.kami_index, ks.account_name, ks.total_violence, ks.attack_threshold_shift,
       ks.attack_threshold_ratio, ks.hand_affinity, ks.body_affinity, ks.level
FROM harvesters h
JOIN kami_static ks ON ks.kami_id=h.kami_id
WHERE ks.total_violence >= 28
ORDER BY ks.total_violence DESC, ks.attack_threshold_shift DESC LIMIT 30;
```

**Decision**:
- If ≤1 V≥30 attacker present and they're guild-blocked: proceed to P3.
- If multiple high-V non-guild attackers: counter-counter math. Our weakest deployed striker's HP after a kill must clear the highest-V counter-predator's kill_zone for our roster.
- If unclear: pivot to node 73 (Yeahta cluster) and re-run counter-predator scan there.

Document the counter-predator finding in `decisions.md` before any tx.

---

## Priority 3 — Migration sequence (TrayzinCarpathia node 60)

**Total estimated gas: ~26M**. Hard rule: if any step reverts unexpectedly, STOP and post-mortem.

### Step 3.1 — Tear down node 86 deployments (all kamis RESTING)

All bpeon predators are believed RESTING_OR_DEAD per session 88/89 logs. **Verify via on-chain reads first** (oracle could be stale on this — staleness escape hatch warrants chain reads here):

- For each striker [12649, 11224, 10705, 6058, 15540, 12225]: `get_kami_state` (chain) — confirm RESTING (not HARVESTING).
- If any HARVESTING: `stop_harvest_batch([list])` — verify state RESTING after.
- If any DEAD: revive sequence (TBD — first session this triggers, document the discovery).

### Step 3.2 — Travel 86→60

`travel_to_room(target_room=60, account="bpeon", dry_run=True)` first. Inspect path, stamina cost, item inserts. If reachable on stamina: execute. If `reached_target=False`: append "accumulate SP+ items" to next plan and pivot to closer node (Yeahta room 73 — check rooms.csv adjacency).

### Step 3.3 — Deploy strikers on node 60

For each striker, `harvest_start([striker_idx], node_index=60)`. Record T0 timestamp per kami. Default gas limit (3M per harvest_start; tested OK for new-node starts).

### Step 3.4 — Wait 185s (cooldown)

While waiting:
- Re-read `world_targets.json` (cron should refresh during this wait).
- Verify TrayzinCarpathia candidates still HARVESTING + no feed.
- Run a fresh counter-predator scan — has anyone deployed on node 60 in response to our move?

### Step 3.5 — First strike

`liquidate(target_kami_index=6023, attacker_kami_index=6058)` (or whichever striker `world_targets.json` paired against 6023).

Note: 6058 (V31, SCRAP-handed) was paired against TrayzinCarpathia SCRAP-body candidates per the recon. Watcher's `striker_idx` field is authoritative — read from JSON, not from this plan's restatement.

### Step 3.6 — Chain or stop

- **On kill**: log gas + obol + recoil HP. Re-run scan via `world_targets.json` (cron should refresh between cooldowns). If next candidate clean and striker HP > kill_zone-of-defenders: chain. Otherwise stop, log session.
- **On revert ≥ +5 HP margin**: structural surprise per session 89 stop condition. Halt, post-mortem, do NOT re-attempt.
- **On 2 reverts in a row**: end session.

---

## Priority 4 — Hard limits

- **Total gas budget cap**: 40M for this session (migration ~26M + ~3M per kill × max 5 kills = ~41M ceiling). If approaching, stop after current chain.
- **Counter-counter math** before every strike, not just the first.
- **Heal-event guard** before every strike — re-read `n_feeds_after_start` on the actual target via fresh oracle query.
- **No tx if striker HP < 80% max_hp** — leave a buffer for recoil + counter-predator strike.

---

## Priority 5 — Alternative pivots (if P3 stalls)

Order by likelihood of yielding kills:

1. **Yeahta node 73** (SCRAP, room 73): 4 candidates +10 to +69. Need to check room 60→73 distance + stamina. If 1-2 hops away from node 60, after node 60 chain dies, hop and continue.
2. **Re-scan node 86**: stefan97 may have restarted by now (~1.5-2h after the bulk-stop). If wave landed, candidates with elapsed >60 min → re-evaluate margin.
3. **Defer to next session (+30 min)**: if both alternative clusters are dry too, re-wake with named pin "stefan97 cycle restart catch — pools should be margin-positive by then."

---

## Priority 6 — Post-session updates

- Append `predator/metrics.md` row (session 91, gas, obols, kills).
- If first kill landed: update `predator/learnings.md` with predicted-vs-actual margin (canonical formula validation).
- If counter-predator math killed any of our strikers: log to `predator/counter-predator.md`.
- If world_targets.json watcher misbehaved: fix in `predator/scripts/refresh_world_targets.py`, document in `improvements.md`.

---

## Self-schedule (apply Cadence Discipline)

Two regimes:
- **First-kill landed**: re-wake +5-15 min, named pin: "chain on TrayzinCarpathia/Yeahta cluster after first kill — striker cooldown completes at T+185s".
- **Migration completed without kill (revert or churn)**: re-wake +20 min, named pin: "candidate restart wave on node 60 — TrayzinCarpathia owner pattern unknown, observe one cycle".
- **Migration aborted / didn't fire**: re-wake +5 min, named pin: "world_targets.json fresh snapshot + retry P2 with relaxed counter-predator gate".

If genuine no-action state (e.g., counter-predators saturate node 60 AND node 73 AND node 86 still dry): re-wake +30 min with named pin "stefan97 cycle restart catch on node 86 — bulk-restart wave from 23:14 UTC due in this window."

---

## Out of scope

- Force-flush, quest progression, kamibots state reads.
- 11224 SP allocation (gated on first kill).
- Modifying `executor/oracle_state.py` or `executor/hp_projection.py` (canonical formulas are stable).
- Modifying kami-oracle code (route via `ideas_to_founder.md`).
