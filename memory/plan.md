# Plan for session 78 — affinity hunt with 11224 on node 86

Context: session 77 confirmed the empirical kill formula (`threshold_ratio = animosity + atk_shift − def_shift`, additive, no atk_ratio multiplier) but failed to land a strike — node 86 is Guardian-saturated (every harvester at H ≤ 18 carries def_shift ≥ 0.10). 12649's Hostility Potion buff (+0.03 shift) wasn't enough to overcome that. The remaining lever we haven't tested is **affinity multiplier** — 11224's EERIE hand vs a SCRAP-body target.

**Read at start**: `predator/mechanics.md` § "Empirical formula refinement (session 77)" + § "Practical pre-flight checklist", `predator/learnings.md` § "Session 77", `memory/decisions.md` last entry.

## Priority 1 — Pre-flight: pick the SCRAP-body target

1. `oracle_sql("SELECT s.kami_index, s.name, s.account_name, s.account_id, s.body_affinity, s.hand_affinity, s.total_health, s.total_violence, s.total_harmony, s.total_power, s.harvest_intensity_boost, s.attack_threshold_shift FROM kami_static s WHERE s.last_action_node_index = 86 AND s.last_action_type = 'HARVEST_START' AND s.body_affinity = 'SCRAP' ORDER BY s.total_harmony ASC LIMIT 20")` — find SCRAP-body active harvesters on node 86 ranked by lowest H (easiest threshold).
2. For top 3-5 candidates, `get_kami_state_slim(<idx>)` to verify still HARVESTING node 86, get current HP, check def_shift (`bonuses.defense.threshold.shift`).
3. Filter against `predator/guild-no-touch.csv` (account_id then handle).
4. Compute kill_zone for each: `animosity = GaussianCDF(ln(36/H_target))`; `threshold_ratio = animosity + 11224.atk_shift − target.def_shift + AFFINITY_BONUS_UNKNOWN`. Pick the candidate with the largest `kill_zone − current_HP` margin (most slack for affinity-bonus uncertainty).
5. If no SCRAP-body candidate exists on node 86, fall back to Option B (cluster move) — see Priority 4.

## Priority 2 — Deploy 11224 + strike

1. Verify 11224 is RESTING and at room 86 (account already there). If RESTING but room mismatches, that's a state bug — investigate before moving.
2. `harvest_start(11224, node_index=86)` — ~1.5M gas. Read 11224 slim post-start to capture baseline `attack.threshold.shift` and confirm HARVESTING.
3. `liquidate(target_kami_id=<chosen>, attacker_kami_id=11224, account="bpeon", target_account_id="<...>", target_handle="<...>")` — ~7.5M gas if it lands or ~2.7M if it reverts.
4. Verify: `get_inventory("bpeon")` for obol delta. `get_kami_state_slim(11224)` for HP/strain post-recoil — **this is the first real recoil reading we'd get**.

## Priority 3 — Chain only if (a) the strike landed AND (b) 11224 HP ≥ 60% AND (c) no cooldown

If chain conditions hold, pick next-best SCRAP-body candidate from the oracle scan; same flow.

**Bail-out conditions** (do NOT chain):
- 11224 HP < 60% (recoil heavy — characterize before risking another).
- Cooldown active on 11224.
- Any top-15 7d-liquidator appeared HARVESTING on node 86 (counter-predator scan).
- Total session gas > 20M without a clean read on yields.

## Priority 4 — Fallback: Option B (cluster scan elsewhere)

If Priority 1 finds zero SCRAP-body harvesters on node 86, use oracle to find another node with **multiple zero-defender harvesters** (def_shift = 0 OR ≤ 0.05) and at least 1 SCRAP-body if we want to keep affinity in play:

```
SELECT a.node_index, COUNT(*) AS targets,
       SUM(CASE WHEN s.body_affinity='SCRAP' THEN 1 ELSE 0 END) AS scrap_targets
FROM kami_action a
JOIN kami_static s ON s.kami_index = a.kami_index
WHERE a.action_type = 'HARVEST_START'
  AND a.block_timestamp > now() - interval 24 hour
  AND s.attack_threshold_shift <= 0.05
  AND s.account_name != 'bpeon'
GROUP BY a.node_index
HAVING targets >= 3
ORDER BY scrap_targets DESC, targets DESC
LIMIT 10;
```

For any candidate node: write the cluster math to `decisions.md` BEFORE traveling (per doctrine — no cross-region travel without justification). Travel cost dominates: 6+ hops = ~6M gas. Need ≥ 3 strike opportunities to amortize.

## Priority 5 — Allocate 11224's 3 SP IFF 11224 strikes successfully

Founder rule: only allocate after observing in real hunt.
- Note recoil HP cost vs the 12649 baseline (no successful strike yet — this would be our first datapoint).
- Tentative tier 3 entry: `132 Vampire 1` if recoil ≥ 30% (HP-restore-on-kill priority), else `133 Bandit 1` if MUSU spoils dominate observed yield.
- Write rationale to `predator/learnings.md` BEFORE allocating.

If 11224 doesn't strike → 3 SP stay unspent. Document deferral.

## Priority 6 — Metrics + commit

Append session 78 row to `predator/metrics.md`:
- gas_spent (sum of all on-chain tx)
- musu_balance_end / obols_earned / musu_earned
- kamis_liquidated (per kill: target_idx)
- items_consumed (none expected — Hostility Potion already burned)
- nodes_visited (86 only unless Option B fires)

Commit discipline:
- `predator: session 78 hunt result` (mechanics/learnings/metrics)
- `session: 78 — <one-line outcome>`

## Priority 7 — Next session schedule

Set `next-run-at` based on outcome:
- 1+ kill: short re-wake (45-90 min) — repeat-strike before prey scatters or before cooldown locks us out.
- 0 kills, affinity hypothesis disproven: 4-6h, then plan a cluster move (Option B).
- Tool/gas anomaly: write to `alerts.md`, longer wake (12h) for founder visibility.

## Read at start

- `memory/alerts.md` — founder may have replied
- `ideas_to_founder.md` — async items
- `predator/README.md` — doctrine refresher
- `predator/mechanics.md` — § "Empirical formula refinement (session 77)" + § "Practical pre-flight checklist"
- `predator/learnings.md` — § "Session 77"
- `predator/guild-no-touch.csv` — verify `# Updated:` line ≤ 7 days old before any strike
