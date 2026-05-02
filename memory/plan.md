# Plan for session 77 — re-strike on strain-decayed node 86 prey

Context: session 76 built and end-to-end tested the `liquidate` tool but the first strike reverted with `kami lacks violence (weak)` — V34/H21 vs full-HP target sat ~1% above the kill threshold. We're now camped on node 86 (account at room 86), 12649 HARVESTING, 3764 still HARVESTING. Strain decay over 60+ minutes should drop 3764's HP enough to clear the threshold.

**Read at start**: `predator/mechanics.md` § "Empirical: revert messages observed (session 76)" + § "Practical pre-flight checklist", `predator/learnings.md` § "Session 76 — first hunt", `memory/decisions.md` last entry.

## Priority 1 — Pre-flight: confirm strain decay landed us in the kill zone

1. `get_kami_state_slim(3764)` — read `health.sync` (CURRENT HP, not max).
   - If `sync < 198` → green light, threshold cleared.
   - If `sync ≥ 198` → either wait longer OR pivot to a different target.
2. `get_kami_state_slim(12649)` — confirm still HARVESTING node 86, HP healthy, not on cooldown.
3. Re-derive the threshold quickly:
   - `combatRatio = ln(34 / target_H)`; `animosity ≈ GaussianCDF(combatRatio)`
   - `threshold ≈ animosity × 1.0 (NORMAL/NORMAL) + 0.30 (12649 atk_shift) − target_def_shift_normalized`
   - `kill_zone = threshold × max_HP`. If `current_HP < kill_zone` → fire.
4. Re-check guild gate freshness: `predator/guild-no-touch.csv` `# Updated:` line must be ≤ 7 days old (currently 2026-05-01, fresh through 2026-05-08).

## Priority 2 — First successful strike

1. **Pop Hostility Potion (item 11410) on 12649 BEFORE the strike** — read 12649's `bonuses.attack` block via slim, fire `use_account_item(11410)`, re-read slim. **Capture the delta** — this is the only single-shot consumable for the test, and the strike is the ideal context to characterize it.
   - Note: session 76 found Hostility Potion is kami-targeted not account-targeted; check if `use_account_item` actually applies to 12649. If it reverts as "not for ACCOUNT", skip — the bonus may need a kami-targeted variant we haven't built. **Do not build a new tool just for this single test.** Strike anyway, characterize the potion later.
2. `liquidate(target_kami_id=3764, attacker_kami_id=12649, account="bpeon", target_account_id="538526038351110879045229412559851121974983005580", target_handle="rtvvvvv")`.
3. Verify: `get_inventory("bpeon")` for obol delta (item 1015 should appear or +1). `get_kami_state_slim(12649)` for HP/strain post-recoil.

## Priority 3 — Chain a second strike if conditions hold

If kill 1 succeeds AND 12649 is still HARVESTING with HP ≥ 60% AND not on cooldown:

1. Pick the next-best low-H target from node 86 oracle scan. rtvvvvv has multiple farmers; 15440 (V16/H18/HP190, def_shift 100) and others may now be in strain-decay zone too. Re-run the oracle active-harvest scan filtered by `account_id != bpeon` and current strain decay estimates.
2. Strike. Verify obol +1, MUSU spoils.

If 12649 cooldown blocks re-strike, consider deploying 11224 to node 86:
- Travel cost 0 (account already at room 86).
- 11224 still RESTING — `harvest_start(11224, node_index=86)`.
- Then `liquidate` with 11224 (V36, EERIE hand → bonus vs SCRAP-body targets).

**Bail-out conditions** (do NOT chain):
- 12649 HP < 50% after first strike (recoil was higher than expected — characterize before chaining).
- A top-15 7d-liquidator appeared on node 86 (counter-predator scan).
- Gas spent > 25M total this session without a clean read on yields.

## Priority 4 — Allocate 11224's 3 SP IFF 11224 actually struck this session

Same founder rule: only allocate after observing in real hunt. If 11224 strikes:
- Note recoil HP cost vs 12649's strike on a comparable target.
- Tentative plan (refine per observation):
  - 113 Mercenary 4→5 (+1 SP)
  - 132 Vampire 1 OR 133 Bandit 1 (tier 3 entry — Vampire if recoil is severe, Bandit if MUSU spoils dominate yields).
- Write the rationale to `predator/learnings.md` BEFORE allocating.

If 11224 doesn't strike → 3 SP stay unspent. Document the deferral in learnings.md.

## Priority 5 — Metrics + commit

Append session 77 row to `predator/metrics.md`:
- gas_spent (sum of all on-chain tx)
- musu_spent / musu_balance_end
- obols_earned (count of successful liquidations)
- musu_earned (spoils credited via harvest bounty pickup)
- kamis_liquidated
- items_consumed (Hostility:1 if it fired)
- nodes_visited (just 86 unless something forced movement)

Commit discipline (separate commits):
- `predator: session 77 hunt result` (mechanics/learnings/metrics)
- `session: 77 — first successful liquidation` (or `0 kills, strain still pending` if we waited)

## Priority 6 — Next session schedule

Set `next-run-at` based on outcome:
- 1+ kill: short re-wake (45-90 min) — repeat-strike before prey scatters.
- 0 kills with valid recon (3764 HP still > threshold): 2-3h to let strain decay further.
- Tool blew up unexpectedly: write to `alerts.md`, longer wake (12h) for founder visibility.

## Read at start

- `memory/alerts.md` — founder may have replied
- `ideas_to_founder.md` — async items
- `predator/README.md` — doctrine refresher
- `predator/mechanics.md` — kill formula reference + § "Empirical: revert messages observed (session 76)" + § "Practical pre-flight checklist"
- `predator/learnings.md` — § "Session 76 — first hunt"
- `predator/guild-no-touch.csv` — verify `# Updated:` line ≤ 7 days old before any strike
