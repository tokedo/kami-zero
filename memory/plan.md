# Plan for session 79 — cluster move evaluation (node 25 primary)

Context: session 78 confirmed affinity bonus contribution to threshold_ratio
is < 0.07 for our roster — insufficient to crack node 86 Guardian-defended
H≥20 farmers at 90%+ HP. Three sessions camped on node 86, ~24M gas burned,
zero kills. Doctrine says: change something. The change is moving off 86.

**Read at start**: `predator/mechanics.md` § "Affinity bonus — provisional
null finding (session 78)", `predator/targeting.md` § "Cross-node target
distribution (session 78 oracle scan)", `predator/learnings.md` §
"Session 78", `memory/decisions.md` last entry, `predator/guild-no-touch.csv`
freshness check.

## Priority 0 — Sanity / freshness

1. `predator/guild-no-touch.csv` `# Updated:` line ≤ 7 days old? If not,
   **abort all hunts** (deny-all per CLAUDE.md hard rule #1) and write
   to `alerts.md` for founder.
2. Re-read 11224 + 12649 slim — both should still be HARVESTING on node 86
   from session 78. Note current HP / strain accumulation.

## Priority 1 — Node 25 cluster math (primary candidate)

Node 25 (Lost Skeleton, Moonside, EERIE-INSECT) showed 49 zero-def
EERIE-body harvesters in the session 78 oracle scan. **10705 (INSECT-hand,
V32/H19/HP240) is the affinity-matched striker.**

### Step 1 — Non-guild filter the cluster

```sql
WITH latest AS (
  SELECT kami_id, MAX(block_timestamp) AS t FROM kami_action
  WHERE action_type IN ('harvest_start','harvest_stop','harvest_liquidate')
  GROUP BY kami_id
),
last_act AS (
  SELECT a.kami_id, a.action_type, a.node_id, a.block_timestamp
  FROM kami_action a JOIN latest l ON l.kami_id = a.kami_id AND l.t = a.block_timestamp
  WHERE l.t > now() - interval 24 hour
)
SELECT s.kami_index, s.name, s.account_name, s.account_id, s.body_affinity,
       s.hand_affinity, s.total_health, s.total_violence, s.total_harmony,
       s.attack_threshold_shift, s.defense_threshold_shift, s.strain_boost,
       la.block_timestamp AS started_at
FROM last_act la JOIN kami_static s ON s.kami_id = la.kami_id
WHERE la.action_type = 'harvest_start'
  AND la.node_id = '25'
  AND s.body_affinity = 'EERIE'
  AND s.defense_threshold_shift <= 50
  AND s.account_name != 'bpeon'
ORDER BY s.total_harmony ASC
LIMIT 50
```

Then drop guild matches (account_id then handle, case-insensitive). The
expected non-guild count is the cluster size that justifies the move.

### Step 2 — Cluster math (write to `decisions.md` BEFORE travel)

Travel cost: bpeon at room 86 → room 25. Use
`travel_to_room(target_room=25, account="bpeon", dry_run=True)` to get exact
hop count, stamina cost, gas estimate. Likely 5–7 hops = ~5–7M gas.

Striker deployment cost: stop 11224 + 12649 (~3M gas each in worst case),
harvest_start 10705 + 11224 + 6058 + others on node 25 (~1.5M each).

**Justification threshold**: total move + redeploy should be amortized by
the expected obol+spoils yield over the next 6–12h of hunting at node 25.
Estimate ≥ 3 strike opportunities per 6h to amortize ~12–15M gas.

If cluster math passes, proceed. If only 1–2 clean targets, fallback to
node 88 (10 SCRAP-soft, 11224's matchup).

### Step 3 — Move + deploy

Per `CLAUDE.md` § "Migrating strategies between nodes — verify end state":
- `harvest_stop([12649])` first; reverify INACTIVE.
- `harvest_stop([11224])`; reverify.
- `travel_to_room(target_room=25, account="bpeon", dry_run=False)`.
- `harvest_start([10705], node_index=25)` — primary striker.
- Optional: bring along 11224 / 6058 as second-line if cluster has
  matchups for them.

### Step 4 — First strike with 10705

Pick the lowest-H non-guild EERIE-body candidate, predicted
threshold_ratio = animosity (CDF(ln(32/H))) + 0.28 (10705 atk_shift) −
def_shift + AFFINITY. If predicted threshold_ratio × maxHP > current_HP,
fire.

Verify post-strike: 10705 HP/strain, inventory obol delta, 12649's
harvest still INACTIVE (we stopped it), 11224's state.

## Priority 2 — Node 88 fallback (11224's matchup)

If node 25 non-guild cluster < 5, scope node 88 instead. 10 SCRAP-soft
targets in scan. EERIE-hand 11224 is the matchup — just like session 78
but on a less guild-saturated node.

Same workflow: oracle scan → guild filter → cluster math → move
(if travel from current room < node 25 cost) → strike.

## Priority 3 — Bail-out conditions

- Both clusters non-guild < 3 → abort cluster move; **stay on node 86**
  and try strain-wait band on 11332 (need HP < 189 for kill_zone) or
  13253 (need HP < 180). Read their current HP at start of session.
- 11224 HP < 50% from session 78 strain accumulation → heal first or
  use a different attacker.
- Total session gas > 25M without a kill → end session, document.

## Priority 4 — 11224 SP allocation (still deferred)

3 SP unspent. Founder rule: only after observing 11224 in real hunt
(must produce a kill). Session 78's revert doesn't count. Defer again.

## Priority 5 — Metrics + commit

Append session 79 row to `predator/metrics.md` with the standard fields.

Commits:
- `predator: session 79 — <one-line hunt outcome>` (mechanics/learnings/
  metrics/targeting updates)
- `session: 79 — <one-line outcome>` (memory/)

## Priority 6 — Next session cadence

- 1+ kill: short re-wake (45–90 min) — repeat strike before prey
  scatters.
- 0 kills, cluster scan complete but cluster too small / Guardian-
  saturated like 86: 6–8h next wake, plan the next-best cluster.
- 0 kills, did NOT move (stayed on 86): 3–4h next wake, retry
  strain-wait kills on 11332 / 13253.

## Read at start (full list)

- `memory/alerts.md` — founder may have replied
- `ideas_to_founder.md` — async items
- `predator/README.md` — doctrine refresher
- `predator/mechanics.md` — § "Affinity bonus — provisional null finding"
- `predator/targeting.md` — § "Cross-node target distribution"
- `predator/learnings.md` — § "Session 78"
- `predator/guild-no-touch.csv` — verify `# Updated:` ≤ 7 days
