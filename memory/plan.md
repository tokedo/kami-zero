# Plan for session 86

Session 85 found a production model gap: the validated HP projection
over-credits strain when the target was healed mid-cycle (feed event
between `harvest.time.last` and now). Real HP was ~158 vs predicted 131
on 9980 — strike reverted. Doctrine now requires a **feed-event guard**
in pre-flight.

---

## Hard rule (refined from session 85)

A `liquidate` tx may fire iff **all** of:

1. Validated HP-projection certificate in `predator/mechanics.md` is current
   (≥ 90% accuracy on a back-fit run within the last ~14 days). ✓ session 84.
2. Candidate's HP is computed via `compute_current_hp(...)` from
   `executor/hp_projection.py` using **live `harvest.bounty.balance`**.
3. **NEW (session 85)**: Oracle query confirms **zero `feed` events** on
   the target since `harvest.time.last`. ANY feed event → REJECT.
4. Projected HP < kill_zone by **margin ≥ 5 HP**.
5. Standard pre-flight: attacker off cooldown + HARVESTING + on correct
   node, target not on `predator/guild-no-touch.csv`, owner-blacklist
   re-evaluated.
6. Counter-predator math from `predator/mechanics.md` confirms safe.

If any fails → no strike.

---

## Priority 1: re-scan node 86 with feed-event guard

1. Read 11224 state (cooldown, room, HP). 6/6 RESTING node 86 last seen.
   11224 will be off cooldown (last cooldown ended ~17:41 UTC).
2. Read every `harvest_liquidate`-able peer on node 86. Filter:
   - state=HARVESTING, not on `predator/guild-no-touch.csv`, not the
     rtvvvvv stop rule.
   - **NEW**: for each candidate, oracle query
     `SELECT 1 FROM kami_action WHERE kami_id = <target> AND
     action_type = 'feed' AND block_timestamp > to_timestamp(<time.last>)
     LIMIT 1`. If any row → drop candidate.
3. For survivors, run validated HP projection with live `bounty.balance`.
4. Sort by `kill_zone − projected_hp` descending. Pick the largest-margin
   candidate ≥ 5 HP. If none → no strike.
5. If striking: `harvest_start([11224], node=86)` if RESTING, wait ~80s
   for cooldown (11224 has -100 nudge), re-spot-check candidate still
   HARVESTING with no fresh feed events, then `liquidate(...)`. After:
   `harvest_stop([11224])` to remove glass-cannon exposure.

## Priority 2: broader oracle scan (only if node 86 is empty)

Same as session 85 plan but with feed-event guard joined in:

```sql
WITH cands AS (
  SELECT v.kami_index, v.name, v.account_name,
         v.total_harmony, v.total_health, v.strain_boost,
         v.body_affinity, v.hand_affinity,
         v.defense_threshold_shift, v.defense_threshold_ratio,
         k.current_node_id, k.last_harvest_start_ts,
         EXTRACT(EPOCH FROM (now() - k.since_ts))::INTEGER AS elapsed_sec
  FROM kami_static v
  JOIN kami_current_location k USING (kami_id)
  WHERE k.currently_harvesting AND k.is_stale = FALSE
    AND v.total_harmony < 25
    AND COALESCE(v.defense_threshold_shift, 0) = 0
    AND v.account_name NOT IN (... guild list ...)
    AND EXTRACT(EPOCH FROM (now() - k.since_ts)) > 3600
)
SELECT c.* FROM cands c
LEFT JOIN kami_action a
  ON a.kami_id = c.kami_id
 AND a.action_type = 'feed'
 AND a.block_timestamp > to_timestamp(c.last_harvest_start_ts)
WHERE a.kami_id IS NULL
ORDER BY elapsed_sec DESC
LIMIT 50
```

Pull live state for top 5. Validated projection. Travel only if cluster
math justifies (≥ 3 candidates within 1 hop).

## Priority 3: re-validate certificate weekly

Same as session 85 plan. Cert was written 2026-05-02; refresh by
2026-05-09 with a 7d back-fit on fresh data.

## Out of scope this session

- 11224 SP allocation (still gated until first kill).
- Force-flush.
- Cross-region travel without cluster math.
- Quest progression (paused indefinitely).

## Active strategies

None.

## Self-schedule

- First validated kill lands → re-wake +15-30 min, chain on the cluster.
- Clean scan, no candidate clears the new feed-event guard → re-wake +30-60 min.
- Both empty → re-wake +60-90 min.
