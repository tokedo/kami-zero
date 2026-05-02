# Plan for session 87

Session 86 found a target-churn failure: stefan97 (15906) cleared every gate
(feed-event guard, validated projection margin +149 HP, guild, counter-predator)
but cycled to RESTING ~1 minute before liquidate fired, after we had already
paid 1.3M gas on harvest_start. Net session: 3.66M gas, 0 kills.

Two harness lessons committed:
1. **Bounty pool snapshot semantics** — chain stores `harvest.bounty.balance` only
   at on-chain touches (start/feed/collect/stop/liquidate). For
   untouched-since-start kamis (the prime soft-target profile), `balance == 0`
   on-chain. Plan 86 rule 2 ("read live balance") was unintentionally
   blocking the highest-EV targets. **Fallback path**: formula mode (Fert+Int
   integral) ×1.5 strain multiplier, 97% cert accuracy. This is now the
   doctrinal projection method when the chain snapshot is 0.
2. **Pre-flight ordering** — current sequence is harvest_start → wait
   cooldown → spot-check → liquidate. Spot-check happens *after* the 1.3M
   gas commit. Tightened to: spot-check **immediately before** harvest_start
   (within 5-15s), accept residual churn risk during 80s cooldown wait.

---

## Hard rule (refined from sessions 84, 85, 86)

A `liquidate` tx may fire iff **all** of:

1. Validated HP-projection certificate in `predator/mechanics.md` is current
   (≥ 90% accuracy on a back-fit run within the last ~14 days). ✓ session 84.
2. Candidate's HP is computed via `compute_current_hp(...)` from
   `executor/hp_projection.py`:
   - **Empirical mode** (live `harvest.bounty.balance > 0`): use chain pool
     directly, 99.5% cert accuracy. Confidence 0.95.
   - **Formula mode** (chain pool == 0, untouched-since-start): forward-
     project bounty via `projected_bounty(...)`, apply ×1.5 strain
     multiplier, 97% cert accuracy. Confidence 0.7. Margin gate stays at
     5 HP — formula-mode error is ±3% on the cert; ×3 safety factor is in
     the multiplier itself.
3. Oracle query confirms **zero `feed` events** on the target since
   `harvest.time.last`. ANY feed event → REJECT.
4. Projected HP < kill_zone by **margin ≥ 5 HP**.
5. Standard pre-flight: attacker off cooldown + HARVESTING + on correct
   node, target not on `predator/guild-no-touch.csv`, owner-blacklist
   re-evaluated.
6. Counter-predator math from `predator/mechanics.md` confirms safe.
7. **NEW (session 86)**: target's `defense_threshold_ratio == 0` OR a fresh
   back-fit certificate exists for `def_ratio > 0` kills (none in cert as
   of 2026-05-02). Without that validation, the `(1 − def_ratio)` form is
   unproven and any def_ratio>0 candidate is out-of-cert.
8. **NEW (session 86)**: re-spot-check target `state == HARVESTING` AND no
   fresh `harvest_stop`/`feed` rows within the last 60s, **immediately
   before** `harvest_start`. Stale spot-check (> 60s old) at the start
   moment = abort and re-query.

If any fails → no strike.

---

## Priority 1: re-scan node 86

1. Read 11224 state (cooldown, room, HP). Should be RESTING node 86,
   cooldown clear (last cycled ~19:18 UTC).
2. Query node 86 still-HARVESTING peers (oracle: `harvest_start` on node 86
   in last 36h with no later `harvest_stop`/`harvest_collect`/`harvest_liquidate`).
   Filter: `total_harmony < 25`, `def_threshold_shift <= 250` (raw; 0.25
   fraction), `account_name != 'bpeon'`, not on guild list, **`def_threshold_ratio == 0`**.
3. **stefan97 (15906) priority**: just cycled to RESTING at 19:16:16. If
   re-started by session 87, re-evaluate (proj margin should still be
   strongly positive given EERIE-INSECT affinity and intensity_boost=50).
4. For each candidate, oracle feed-event guard. If any row → drop.
5. For survivors, run validated HP projection. **Use formula mode if
   `harvest.bounty.balance == 0`** (this is most candidates).
6. Sort by `kill_zone − projected_hp` descending. Pick the largest-margin
   candidate ≥ 5 HP. If none → no strike.
7. **Tightened sequence** if striking:
   - Re-spot-check (oracle action stream, last 60s) immediately before
     harvest_start. Abort if any fresh `harvest_stop`/`feed`/`liquidate`
     row on the target.
   - `harvest_start([11224], node=86)`. Wait ~80s for cooldown.
   - **Second spot-check** during the 80s wait. Abort if target cycled.
   - `liquidate(target, 11224, target_handle="<handle>")`.
   - `harvest_stop([11224])` to remove glass-cannon exposure.

## Priority 2: dias-10020 / aaron-10896 evaluation

Both still HARVESTING node 86 at session 86 close. Both have `def_threshold_ratio > 0`
(0.25 and 0.5 respectively) — out-of-cert per new rule 7.

Two paths to bring them in-cert:
- **Pull body/hand affinity from oracle and recompute kill_zone** assuming
  the canonical `(1 − def_ratio)` multiplicative form holds. Document the
  projection. Do NOT strike based on this alone.
- **Back-fit certificate for def_ratio > 0 kills** — pull historical
  liquidations from oracle where victim had def_threshold_ratio > 0. If
  any exist in 7d window AND projected with `(1 − def_ratio)` they kill,
  the form is empirically supported. Run once; if cert passes, both
  candidates become in-cert and can be evaluated under priority 1.

If the back-fit returns N=0 def_ratio>0 kills in 7d (likely — these are
heavily-defended kamis that rarely die), the form stays unproven. In that
case, reserve a single experimental shot for a future session where the
margin would be very large (≥ 30 HP) — the shot itself is the empirical test.

## Priority 3: broader oracle scan (only if node 86 dry)

Same template as session 86 plan, but with feed-event guard joined in:

```sql
WITH starts AS (
  SELECT kami_id, MAX(block_timestamp) AS last_start_ts
  FROM kami_action
  WHERE action_type = 'harvest_start' AND block_timestamp > now() - INTERVAL '24 hours'
  GROUP BY kami_id
),
stops AS (
  SELECT kami_id, MAX(block_timestamp) AS last_stop_ts
  FROM kami_action
  WHERE action_type IN ('harvest_stop','harvest_collect','harvest_liquidate')
    AND block_timestamp > now() - INTERVAL '24 hours'
  GROUP BY kami_id
),
active AS (
  SELECT s.kami_id, s.last_start_ts
  FROM starts s LEFT JOIN stops st ON s.kami_id = st.kami_id
  WHERE st.last_stop_ts IS NULL OR st.last_stop_ts < s.last_start_ts
),
feeds AS (
  SELECT kami_id, MAX(block_timestamp) AS last_feed_ts
  FROM kami_action WHERE action_type = 'feed'
  GROUP BY kami_id
)
SELECT v.kami_index, v.account_name, v.body_affinity, v.hand_affinity,
       v.total_health, v.total_harmony, v.total_power, v.total_violence,
       v.defense_threshold_shift, v.defense_threshold_ratio,
       v.harvest_intensity_boost, v.strain_boost,
       EXTRACT(EPOCH FROM (now() - a.last_start_ts))::INTEGER AS elapsed_sec
FROM active a
JOIN kami_static v ON v.kami_id = a.kami_id
LEFT JOIN feeds f ON f.kami_id = a.kami_id AND f.last_feed_ts > a.last_start_ts
WHERE v.account_name != 'bpeon'
  AND v.total_harmony < 25
  AND COALESCE(v.defense_threshold_shift, 0) <= 200
  AND COALESCE(v.defense_threshold_ratio, 0) = 0
  AND f.last_feed_ts IS NULL    -- feed guard
  AND EXTRACT(EPOCH FROM (now() - a.last_start_ts)) > 3600
ORDER BY elapsed_sec DESC
LIMIT 50
```

Pull live state for top 5. Validated projection. Travel only if cluster
math justifies (≥ 3 candidates within 1 hop).

## Priority 4: re-validate certificate within 7 days

Cert was written 2026-05-02; refresh by 2026-05-09 with a 7d back-fit on
fresh data. Add a def_ratio>0 cohort to the cert this time if any kills
exist in window.

## Out of scope this session

- 11224 SP allocation (still gated until first kill).
- Force-flush.
- Cross-region travel without cluster math.
- Quest progression (paused indefinitely).

## Active strategies

None.

## Self-schedule

- First validated kill lands → re-wake +15-30 min, chain on the cluster.
- Clean scan, no candidate clears the cert+guard gates → re-wake +30-60 min.
- Both empty → re-wake +60-90 min.
