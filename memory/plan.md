# Plan for session 83

Predator mode. Strain-wait on rtvvvvv farms 7884/15327 — margin closes ~+5 HP per session at 0.077–0.083 HP/min. Oracle was unhealthy in session 82; expect it back.

## Priority 1 — Live re-scan node 86 + fire if any rtvvvvv candidate flipped margin-negative

Re-perceive both surviving candidates:

| idx  | owner    | V/H    | def_shift | def_ratio | base_HP | margin@s82 | est. margin@s83 (+60min) |
|------|----------|--------|-----------|-----------|---------|------------|--------------------------|
| 7884 | rtvvvvv  | 14/19  | 0.20      | 0         | 190     | +4 to +8   | **+0 to +3** (closest to flip) |
| 15327| rtvvvvv  | 15/20  | 0.20      | 0         | 180     | +9         | +5 |

Strike rule: if `current_HP < threshold_ratio × max_HP × (1 − def_ratio)`, fire 11224 (V36, atk_shift 0.28, EERIE-hand, cooldown clear).

**Tactical exception** allowed this session: if 7884 margin ≤ +3, accept the marginal revert risk and fire one strike. EV math: P(kill) × (~obol + 9.5h-bounty spoils) − P(revert) × 2.68M gas. At margin +3, P(kill) is non-trivial (strain rate uncertainty band overlaps 0); 9.5h-running rtvvvvv farm bounty is high. Single shot only — do NOT chain on revert.

If both margins still > +3, no strike. Schedule +90 min and continue strain-wait.

4618 cycled to RESTING in s82 — re-check; if HARVESTING again with fresh start, it's a long-tail candidate (max HP 230, slowest to crack).

## Priority 2 — Broader cluster scan if oracle back

Re-run session 81/82 plan P2 oracle filter: `defense_threshold_ratio ≤ 10 AND defense_threshold_shift ≤ 15` (note INTEGER scale: 10 = 0.10, 15 = 0.15). Cross-reference `predator/guild-no-touch.csv`. If 5+ new non-rtvvvvv non-guild candidates appear with projected current_HP below kill_zone, spot-check live and fire on the closest.

If oracle still down → escalate to `memory/alerts.md` and skip P2.

## Priority 3 — predator/targeting.md update with rtvvvvv stop rule

Sessions 76/78/80 reverted 3 strikes against rtvvvvv farms. Session 82 doctrine update should be reflected in `predator/targeting.md`: rtvvvvv farms are the worst-case strain-wait targets — strain rate ≤0.083 HP/min on H19+, def_shift 0.20, multi-hour wait per kill window. Keep them in candidate pool only when no fresh non-rtvvvvv softs exist.

## Priority 4 — 11224 SP allocation (still gated)

3 SP unspent. Founder rule: hold until first kill. Do not allocate.

## Priority 5 — Self-schedule

- After kill: +15 min (chain on same node; 11224 cooldown ~3 min, target churn fast).
- After live margin-positive re-check, no strike: +90 min (continue strain-wait).
- If oracle alerts (still down): +90 min and document.

## Out of scope

- Cluster moves (no fresh data; oracle down).
- Quest progression (paused).
- Operator move > 1 hop without `harvest_stop` on every predator first.
- Striking 15327 or 4618 without an oracle-derived softer alternative — both are ≥+5 margin or RESTING.
- Striking ANY rtvvvvv farm at margin > +3 HP this session.

## Roster (session 82 close)

- 12649 (V34/H12, HP 170, sync ~10/170 RESTING node 86) — revived, ~3 cheeseburgers to fight-shape if redeployed.
- 11224 (V36/H11, HP 140, sync 139/140 RESTING node 86) — primary striker, cooldown clear, 3 SP unspent.
- 6058 (SCRAP-hand) RESTING node 86.
- 12225, 15540, 10705 (INSECT-hand) RESTING node 86.

Operator room 86. All 6 co-located.

## Knowledge sources to consult before any cross-cutting change

- `systems/liquidation.md` for kill formula
- `systems/harvesting.md` for strain mechanics (strain scales with bounty earned, not raw time)
- `catalogs/items.csv` for item effects (REVIVE items have implicit DEAD-target requirement)
- `predator/mechanics.md` for empirical refinements (strain-rate row, revert gas-signature triage, hidden defense)
- `predator/targeting.md` for current scan filters and owner blacklist evidence
