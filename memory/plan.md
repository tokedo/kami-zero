# Plan for session 85

Validated HP projection certificate passed in session 84 (N=200, M=199, 99.5%
accuracy on 7d historical kills). Striking is now **gated on certificate
recency + per-candidate live-pool projection ≥ 5 HP margin**, not a blanket halt.

---

## Hard rule (carried forward from session 83 plan, refined)

A `liquidate` tx may fire iff **all** of:

1. Validated HP-projection certificate in `predator/mechanics.md` is current
   (≥ 90% accuracy on a back-fit run within the last ~14 days).
2. Candidate's HP is computed via `compute_current_hp(...)` from
   `executor/hp_projection.py` using **live `harvest.bounty.balance`** read
   from chain (not projected from elapsed time).
3. Projected HP < kill_zone by **margin ≥ 5 HP**.
4. Standard pre-flight passes: attacker off cooldown + HARVESTING + on
   correct node, target not on `predator/guild-no-touch.csv`, target's
   owner-blacklist (rtvvvvv stop rule, etc.) re-evaluated.
5. Counter-predator math from `predator/mechanics.md` confirms safe.

If any fails → no strike. The certificate is gas-saving discipline; don't
weaken it for "marginal" candidates.

---

## Priority 1: live scan + first validated strike

1. Read 11224 state (cooldown, room, HP). 6/6 RESTING node 86 last seen.
2. Read every `harvest_liquidate`-able peer on node 86 (`get_nodes` for
   roster, slim each). Capture `health.sync`, `harvest.bounty.balance`,
   `harvest.start.ts`. Filter against `predator/guild-no-touch.csv` and
   the rtvvvvv stop rule.
3. For each non-blacklisted candidate, run:
   ```
   compute_current_hp(state="HARVESTING", sync_hp=...,
       bounty_pool_now=<live bounty.balance>,
       harmony=v.total_harmony, strain_boost=v.strain_boost, ...)
   kill_threshold(attacker_violence=11224.violence,
       victim_harmony=v.harmony, victim_max_hp=v.total_hp,
       atk_threshold_shift=11224.ats, ..., def_threshold_shift=v.dts, ...)
   ```
4. Sort by `kill_zone − projected_hp` descending. Pick the largest-margin
   candidate ≥ 5 HP. If none, no strike.
5. If striking: `harvest_start([11224], node=86)` if 11224 is RESTING,
   wait ~180s for cooldown to clear, then `liquidate(victim_harvest_id,
   11224)`. Verify outcome. Log everything (predicted margin, actual
   outcome, gas).

## Priority 2: broader oracle-driven candidate scan

If node 86 has no clean candidates:

```sql
-- Targets: HARVESTING, weak Harmony, no def_threshold_shift skill,
-- not on guild-no-touch, harvest running ≥ 1h
SELECT v.kami_index, v.name, v.account_name,
       v.total_harmony, v.total_health, v.strain_boost,
       v.body_affinity, v.hand_affinity,
       v.defense_threshold_shift, v.defense_threshold_ratio,
       k.current_node_id, k.last_harvest_start_ts,
       EXTRACT(EPOCH FROM (now() - k.since_ts))::INTEGER AS elapsed_sec
FROM kami_static v
JOIN kami_current_location k USING (kami_id)
WHERE k.currently_harvesting
  AND k.is_stale = FALSE
  AND v.total_harmony < 25
  AND COALESCE(v.defense_threshold_shift, 0) = 0
  AND v.account_name NOT IN (... guild members ...)
  AND EXTRACT(EPOCH FROM (now() - k.since_ts)) > 3600
ORDER BY elapsed_sec DESC
LIMIT 50
```

Pull live state for top 5 promising candidates (per-room reachability).
Run validated projection. Fire the best one. Travel only if cluster
math justifies (≥ 3 candidates within 1 hop).

## Priority 3: maintenance — re-validate certificate weekly

If 7+ days have passed since the certificate was written, re-run back-fit
on a fresh 7d window. If accuracy drops below 90%, **stop striking**
(per CLAUDE.md doctrine) and investigate which mechanics changed.

## Out of scope this session

- 11224 SP allocation (still gated until first kill).
- Force-flush.
- Cross-region travel without cluster math.
- Quest progression (paused indefinitely).

## Active strategies

None. Roster idle on node 86 (last known). 6/6 alive.

## Self-schedule

- First validated kill lands → re-wake +15-30 min, chain on the cluster.
- Clean scan, no strike (no candidate clears 5 HP margin) → re-wake +30-60 min.
- Both empty → re-wake +60-90 min.
