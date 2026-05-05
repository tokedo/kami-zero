# Safety rules — hard limits, never bypass

Founder-set invariants. Optimizer MAY adjust numerical caps with
strong evidence. Optimizer MAY NOT remove a rule without explicit
founder approval.

## Hard rules

1. **Guild gate is absolute.** `executor.liquidate()` enforces this
   internally via `predator/guild-no-touch.csv`. If a strike returns
   `blocked: true`, accept and move on. Do not bypass; do not edit
   the CSV (founder maintains).
2. **Never strike own accounts.** bpeon and dpeon are off-limits as
   targets.
3. **Max 1 strike attempt per tick.** Bounds blast radius. Optimizer
   may raise this when a stable kill rate is established (≥20
   strikes with ≤1% revert across 24 h).
4. **Max 30M gas per tick.** Hunt sequence worst case is ~25M; cap
   gives headroom. Optimizer may raise if a recurring
   `gas_budget_exceeded` anomaly fires.
5. **State invariant**: all 7 strikers RESTING with operator at start
   of every hunt. Heal scatter before doing anything else.
6. **Forbidden files.** Never write `decisions.md`, `plan.md`,
   `strategic-experiments.md`, `learnings.md`, `improvements.md`,
   `metrics.md`, `targeting.md`. Forbidden by name (CLAUDE.md).
7. **Rule file size cap.** `executor-prompt.md` ≤200 lines. If
   exceeded, optimizer MUST compress as the next change.

## Numerical caps (current)

- `min_margin` = 25
- `max_strikes_per_tick` = 1
- `max_gas_per_tick` = 30_000_000
- `striker_cooldown_base_sec` = 180
- `archetype_reject_owners` = (empty — see rules/rejects.md)
