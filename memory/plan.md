# Plan for session 84

Predator mode, post-finding-cascade. Session 83 yielded three doctrine corrections — strain rate ~2.5× higher than modeled, harvest_start triggers attacker cooldown (~180s), sync HP stale during HARVESTING. Apply them.

## Priority 1 — Re-strike rtvvvvv on cooldown-clear, not strain-wait

The rtvvvvv "stop rule" written this session needs updating already: with corrected strain rate (~0.19–0.25 HP/min for intensity_boost ≥ 20 builds), the issue was never that they're too tough — it was that my model was undercounting strain by 2–3×.

**Live re-check at session start** (read `get_kami_state_slim` for each):

| idx  | last seen state | last cycle ts | sync after cycle | re-start expected? |
|------|-----------------|---------------|------------------|--------------------|
| 7884 | RESTING (s83)   | ~1777734795   | 87/190 (low)     | After full rest cycle |
| 15327| RESTING (s83)   | 1777738974    | 58/180 (very low)| After substantial rest |
| 4618 | RESTING (s82)   | 1777733332    | 88/230 (low)     | Rested longest, may restart soon |

**Strike rule (updated)**: if any of these is HARVESTING again, project current HP using `(sync_at_start) − 0.20 HP/min × elapsed_harvest_min`. Fire IF projected current HP < kill_HP. Use `0.25` rate for 4618-class (high intensity_boost), `0.19` for 15327-class.

**11224 cooldown gating**: 11224's cooldown was reset by session 83's harvest_start to 1777739193 — clear by session 84 start. **Do NOT call harvest_start on 11224 just before strike** — the harvest_start triggers a fresh ~180s cooldown that blocks immediate liquidate. Either:
- Strike from already-HARVESTING state (preserved across sessions if we leave 11224 in flight), OR
- harvest_start ≥ 3 min before strike (different cron tick), OR
- harvest_start, accept 0.28M revert tax, retry after `time.cooldown` elapses.

Plan-suggested approach: **at session start, harvest_start([11224]) on node 86 immediately** (gives 11224 an active harvest), then check candidates — by the time we project + decide + strike, the 180s cooldown should have elapsed (or close to). If margin is tight, do a single 0.28M-tax retry after explicit cooldown read.

## Priority 2 — Broader scan if oracle is back

Oracle was down sessions 82 and 83. If it's back at session 84:

```sql
WITH recent_starts AS (
  SELECT kami_id, MAX(timestamp) AS last_start
  FROM kami_action
  WHERE action_type = 'harvest_start'
    AND timestamp > NOW() - INTERVAL '24 hour'
  GROUP BY kami_id
)
SELECT s.kami_index, s.account_name, s.body_affinity, s.hand_affinity,
       s.total_violence, s.total_harmony, s.total_health,
       s.defense_threshold_shift, s.defense_threshold_ratio,
       s.harvest_intensity_boost, s.strain_boost,
       r.last_start
FROM kami_static s
JOIN recent_starts r ON r.kami_id = s.kami_id
WHERE s.account_name != 'bpeon'
  AND s.defense_threshold_ratio = 0
  AND s.defense_threshold_shift <= 20  -- 0.20 max
  AND s.harvest_intensity_boost >= 20  -- targets that have already strained heavily
  AND r.last_start < extract(epoch from NOW()) - 3 * 3600  -- ≥3h elapsed
ORDER BY r.last_start ASC  -- oldest harvest first (most strained)
LIMIT 30
```

Cross-reference `predator/guild-no-touch.csv`. Any non-guild candidate at elapsed ≥ 3h with intensity_boost ≥ 20 is **probably below kill_zone already** — strike priority over strain-wait planning.

If oracle still down → skip P2, continue P1 live monitoring.

## Priority 3 — 11224 SP allocation (still gated)

3 SP unspent. Founder rule: hold until first kill. **0 kills across sessions 76–83.** Still gated.

## Priority 4 — Self-schedule

- After kill: +15 min (fast cycle, look for next opening on same node).
- After live HARVESTING re-start spotted but cooldown-blocked: +5 min retry.
- After live re-check, no HARVESTING rtvvvvv: +60 min (wait for any to restart).
- After multiple sessions with no kill opportunities: continue +60 min, do not extend further — target restart cadence is on the hours-not-half-day timescale.

## Out of scope

- Cluster moves (no fresh data; oracle down).
- Quest progression (paused).
- Operator move > 1 hop without `harvest_stop` on every predator first.
- Striking guild members (predator/guild-no-touch.csv enforces — gate is in code).
- Re-trying a same-session strike that hit deep-revert (2.68M gas) — that's a real threshold-not-met, not a cooldown miss.

## Roster (session 83 close)

- 12649 (V34/H12, sync 10/170 RESTING node 86) — revived, needs feed before redeployment.
- 11224 (V36/H11, sync 140/140 RESTING node 86) — primary striker, cooldown 1777739193 clear by session 84, 3 SP unspent.
- 6058 (SCRAP-hand) RESTING node 86.
- 12225, 15540, 10705 (INSECT-hand) RESTING node 86.

Operator room 86. All 6 co-located.

## Knowledge sources to consult before any cross-cutting change

- `systems/liquidation.md` for kill formula
- `systems/harvesting.md` for strain mechanics (strain scales with bounty earned, NOT raw time — this is the root of the rate-undercount)
- `catalogs/items.csv` for item effects (REVIVE items have implicit DEAD-target requirement)
- `predator/mechanics.md` — read the new "harvest_start cooldown" + "sync HP stale" + "strain rate vs intensity_boost" sections
- `predator/targeting.md` — read the rtvvvvv stop rule, but reapply with corrected strain rate context

## Carry-forward concerns

- Two consecutive oracle outages logged in `alerts.md`. If session 84 makes it three, demote to working-around-it (no further outage logging) but flag in `ideas_to_founder.md` that oracle reliability is hurting hunt cadence.
- The session-83 rtvvvvv stop rule appended to `predator/targeting.md` was written under the wrong-strain-rate model. Once a confirmed kill validates the corrected rate, **rewrite that section** to reflect that rtvvvvv farms ARE killable on the right cadence, not last-resort.
