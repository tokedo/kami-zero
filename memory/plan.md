# Plan for session 82

Predator mode. Founder doctrine corrections (Block F + current-HP + co-location + cadence) now codified in CLAUDE.md.

## Priority 1 — Live re-scan node 86, fire if any rtvvvvv non-guild candidate flipped

Repeat session 81's scan + spot-check loop on the three known marginal candidates:

| idx  | owner    | V/H    | def_shift | def_ratio | base_HP | margin@s81 |
|------|----------|--------|-----------|-----------|---------|------------|
| 7884 | rtvvvvv  | 14/19  | 0.20      | 0         | 190     | +11        |
| 15327| rtvvvvv  | 15/20  | 0.20      | 0         | 180     | +11        |
| 4618 | rtvvvvv  | 13/26  | 0.10      | 0         | 230     | +13        |

For each, live `get_kami_state_slim` to confirm still HARVESTING + read current sync HP.

**Strike rule:** if `current_HP < threshold_ratio × max_HP × (1 − def_ratio)` (margin negative), fire with 11224 attacker. Co-located at node 86 already. Use 7884 first (smallest base HP, simplest revert path if wrong).

**Cooldown re-check** before firing: 11224's cooldown was clear at session 81 close; verify still clear (op time 1777729276, ~13:41 UTC — should be far past by session 82).

## Priority 2 — Refresh non-guild candidate pool

The session 81 scan was filtered to `def_ratio=0` for the strict-zero-defense bucket. Re-run with broader filter: `def_ratio ≤ 0.10 AND def_shift ≤ 0.15` to catch farmers who skipped the Armor tree entirely. Cross-reference guild csv. If 5+ new non-guild candidates appear, spot-check them in priority order of `(strain_minutes × HP_base) / threshold_ratio` (largest first = most strain biting hardest).

## Priority 3 — Predator/mechanics.md reconciliation (carried from session 80 P1, deferred again)

Replace empirical-derived sections in `predator/mechanics.md` with cross-references to `systems/liquidation.md` + `systems/harvesting.md`. Add the H-tier strain rate empirical row (≤0.072 HP/min for H≥25 skill-boosted; ≈0.075 for H~20). Add the REVIVE-type item finding from session 81. Do this only if Priority 1–2 produce no action.

## Priority 4 — 11224 SP allocation (still gated)

3 SP unspent. Founder rule: hold until first kill. Do not allocate this session.

## Priority 5 — Self-schedule

- After kill: 15 min re-wake (chain on same node).
- After live targets confirmed but margin still positive: 35–45 min.
- After full scan with no live non-guild candidates and no revert opportunities: 60–90 min, log reasoning.

## Out of scope

- Cluster moves (node 60/62/25/88 all dead per session 78–80).
- Quest progression (paused).
- Operator move > 1 hop without `harvest_stop` on every predator first.
- Striking rtvvvvv farms at margin > +5 HP without a fresh strain-rate measurement that justifies the gas burn.

## Roster (session 81 close)

- 12649 (V34/H12, HP 170, sync 10/170 RESTING node 86) — revived, needs ~3 cheeseburgers to fight-shape if redeployed.
- 11224 (V36/H11, HP 140, sync 139/140 RESTING node 86) — primary striker, 3 SP unspent.
- 6058 (SCRAP-hand) RESTING node 86.
- 12225, 15540, 10705 (INSECT-hand) RESTING node 86.

Operator room 86. All 6 co-located.

## Knowledge sources to consult before any cross-cutting change

- `systems/liquidation.md` for kill formula
- `systems/harvesting.md` for strain mechanics
- `catalogs/items.csv` for item effects (no "mechanism unverified" defers)
- `predator/mechanics.md` for empirical refinements
- `predator/targeting.md` for current scan filters and owner blacklist evidence
