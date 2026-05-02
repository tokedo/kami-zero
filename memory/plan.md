# Plan for session 80 — node 62 cluster move (Plan A: 6058 vs buja723)

Context: session 79 closed with 0 kills but high-value intel. Two
clusters live-confirmed for the move-and-strike playbook:

- **Node 62 (Centipedes, INSECT)**: 8 non-guild buja723 INSECT-body
  softs. Matches 6058 (SCRAP-hand). Typical V14/H23/HP110–160 →
  kill_zone ~95–125, very mid-HP-friendly.
- **Node 60 (Scrap Trees, SCRAP)**: 7 non-guild softs (6× wiuuuu SCRAP
  + pranshu.init SCRAP + TrayzinCarpathia NORMAL). Matches 11224
  (EERIE-hand). V14/H24/HP180 → kill_zone ~169, needs ~3h strain wait.

Plan A favors node 62 because buja723 targets are killable at higher
HP fractions — first-kill probability per strike is higher there.

Roster: **5 healthy** (12649 DEAD; revive deferred). All RESTING at
room 86 except spot-state TBD next session.

**Read at start**:
- `memory/alerts.md` — founder may have replied
- `predator/guild-no-touch.csv` `# Updated:` ≤ 7 days check
- `predator/mechanics.md` § "Hidden defense — `defense.threshold.ratio`"
- `predator/mechanics.md` § "Oracle build-snapshot staleness"
- `predator/targeting.md` § "Soft-target filter v2"
- `predator/targeting.md` § "Cluster intel — session 79 oracle scan"
- `predator/learnings.md` § "Session 79"

## Priority 0 — Sanity / freshness

1. `predator/guild-no-touch.csv` updated_at ≤ 7 days? If not, abort
   all hunts (deny-all per CLAUDE.md hard rule #1) and write to
   `alerts.md`.
2. Re-perceive 11224, 6058, 10705, 12225, 15540 — confirm states +
   HP. 11224 should be RESTING with sync HP ≥ 130/140 by wake time
   (~3h post-stop). If 6058 / others are RESTING with banked XP,
   note for level-up at end.

## Priority 1 — Node 62 cluster move (6058 vs buja723)

### Step 1 — Live verify the cluster (no oracle alone)

For each buja723 kami still listed harvest_start within 24h, fetch
`get_kami_state_slim`. Confirm for ≥ 4 candidates:

- `state == HARVESTING` and `node.index == 62`
- `defense.threshold.shift == 0 AND defense.threshold.ratio == 0`
- skills_json contains no SP in 323 or 341 (both grant def_ratio)
- account_id NOT in `predator/guild-no-touch.csv`

If ≥ 4 candidates pass, cluster is live and the move is justified.
If < 4 pass, fall back to **Priority 2 — node 60 (wiuuuu)**.

Session 79 candidate list to start from (8 buja723 INSECT-body
non-guild on node 62, oracle 2026-05-02T11:56 scan):

| index | V | H | HP | started |
|-------|---|---|----|---------|
| 757 | 14 | 23 | 110 | 10:14 |
| 1250 | 16 | 21 | 140 | 10:26 |
| 1671 | 17 | 24 | 140 | 10:58 |
| 1785 | 11 | 22 | 160 | 09:35 |
| 4557 | 16 | 23 | 160 | 11:18 |
| 4672 | 10 | 25 | 140 | 11:14 |
| 5973 | 13 | 21 | 150 | 10:39 |
| 7784 | 11 | 25 | 130 | 11:41 |

**Best targets for 6058** (V32 from oracle, atk_shift 0.28, SCRAP-hand):
1671 (V17 H24), 4557 (V16 H23), 1250 (V16 H21), 5973 (V13 H21).

### Step 2 — Counter-predator scan for node 62

```sql
WITH latest AS (...) -- standard pattern
SELECT s.kami_index, s.account_name, s.total_violence,
       s.attack_threshold_shift, s.attack_threshold_ratio
FROM last_act la JOIN kami_static s ON s.kami_id = la.kami_id
WHERE la.action_type = 'harvest_start'
  AND la.node_id = '62'
  AND (s.total_violence >= 28 OR s.attack_threshold_shift >= 200)
  AND s.account_name NOT IN ('bpeon')
```

Critically scan for hit-and-run threats (account_name = 'Assassins',
or any kami with cooldown_shift much-negative and recent kills).
If a known predator is on or arriving at 62, abort and consider
node 60 instead.

### Step 3 — Cluster math (write to `decisions.md` BEFORE travel)

- Travel cost: 26 hops × ~1M gas = ~26M.
- Required uses: 4× Ice Cream (21201) — inventory has 78, no constraint.
- Strike budget: ≥ 2 successful kills at 7.5M each = 15M, ideally 3+
  to amortize travel. Plus reverts at ~2.7M each — budget for 1–2.
- Total 6h-window budget cap: 50M gas. Hard exit if exceeded.
- **Justification**: cluster has 8 candidates, multiple in kill_zone
  even at full HP per math (kill_zone ~125 vs HP 110–160). At least
  one pass through the cluster yields ≥ 2 kills with high prob.

### Step 4 — Migration teardown

`harvest_stop_batch` is for ALL bpeon kamis still HARVESTING on
node 86 — verify state per kami, only stop those actually mid-harvest.
Per session 79 close, only 11224 was HARVESTING and was already
stopped. 6058 etc were RESTING. **Verify at session start, do not
assume.**

### Step 5 — Travel + deploy

```
travel_to_room(target_room=62, account="bpeon", dry_run=False)
# 26 hops, 4× Ice Cream consumed automatically
```

Then:
- `harvest_start([6058], node_index=62)` — primary striker.
- Optional second-line: 11224 (EERIE-hand on INSECT body is the
  WEAK affinity matchup → skip). 12225 / 15540 (NORMAL hand,
  affinity-neutral) — cheap deployment, fine to bring along.

### Step 6 — First strike with 6058

For each buja723 candidate, predict:
```
threshold_ratio = GaussianCDF(ln(V_atk/H_vic)) + 0.28 (atk_shift)
                  − def_shift (0) − def_ratio (0 confirmed)
                  + AFFINITY_BONUS (≤ 0.07 per session 78 null finding)
kill_zone = threshold_ratio × maxHP
```

For 6058 V32 vs 1671 H24: ln(32/24) = 0.288, CDF ≈ 0.613 + 0.28 = 0.893.
kill_zone ≈ 0.893 × 140 = 125. If sync HP < 125 at strike time → fire.

Pick the lowest sync_HP / max_HP fraction. Strike. Verify post-tx:
6058 HP/strain delta, inventory obol delta, target's harvest state
(should be INACTIVE).

### Step 7 — Repeat strikes

After cooldown clears (empirical observation pending), pick next
candidate. Cycle until: cluster exhausted, gas budget hit, or
counter-predator arrives.

## Priority 2 — Node 60 fallback (11224 vs wiuuuu)

If node 62 cluster live-verifies < 4 candidates:

- Same workflow but target_room=60 (25 hops).
- 6× wiuuuu SCRAP-soft, V13–19 H15–24 HP150–180.
- 11224 V36 atk_shift 0.28 — kill_zone vs H24 H15 = 0.937 × 180 = 169
  / 0.96 × 150 = 144. Some candidates need ~3h strain wait, others
  killable closer to full HP.
- pranshu.init #3334 SCRAP V12 H19 HP250 — high HP but low V/H, kill_zone
  ~218. Strikes only at ≤ 87% HP.

## Priority 3 — Stay-on-86 retreat

If both clusters fail live-verify or counter-predator scan:

- 11224 RESTING + 4 others RESTING — node 86 has multiple low-V
  Guardian-defended targets (11332, 13253). Strain-wait math killed
  these in session 79; **do not retry strain wait on Guardian-ratio
  targets**. End session.
- Schedule next session +6h to let buja723 cluster strain accumulate
  + give time for the guild deny-list to refresh if founder sends an
  update.

## Priority 4 — 12649 revive (still deferred)

- `revive_kami` requires 33 Onyx Shards (item not in inventory).
- Red Ribbon Gummy (99) and Melkarth Spell Card (1) are REVIVE-type
  — mechanism unverified.
- Action: query `executor/server.py` for revive item paths if any;
  query oracle for recent successful revives via Red Ribbon Gummy
  to learn pattern. Defer if research budget exhausted.

## Priority 5 — 11224 SP (still deferred)

3 SP unspent. Founder rule still applies: only after 11224 produces
a kill in real hunt. Session 79 didn't produce one (11224 was on a
node where it was the prey, not the predator). Defer again.

## Priority 6 — Metrics + commit

Append session 80 row to `predator/metrics.md`. Two commits:
- `predator: session 80 — <one-line outcome>`
- `session: 80 — <one-line outcome>`

## Priority 7 — Next session cadence

- 1+ kill: short re-wake (60–90 min) — cluster persistence + cooldown
  reset.
- 0 kills, no move: 4–6h next wake, plan refined cluster scan.
- 0 kills, move executed but no strike landed: 3h next wake, retry
  with strain-decayed candidates.
- Counter-predator detected on 62 / 60: 8–12h next wake, monitor for
  predator's withdrawal, revisit.

## Hard exits

- Total session gas > 50M without a kill → end session, document.
- Any unexpected kami DEAD state (besides 12649) → write to
  `alerts.md`, end session.
- Guild CSV stale (> 7 days) → deny-all hunts.
