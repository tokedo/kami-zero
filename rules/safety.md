# Safety rules — hard limits, never bypass

These are founder-set invariants. The optimizer MAY adjust numerical
caps with strong evidence; the optimizer MAY NOT remove a rule
without explicit founder approval (via `ideas_to_founder.md` if you
need to escalate).

## Hard rules

1. **Guild gate is absolute.** `executor.liquidate()` enforces this
   internally via `predator/guild-no-touch.csv`. Do not bypass; do
   not edit the CSV (founder maintains).
2. **Never strike own accounts.** bpeon and dpeon are off-limits as
   targets. The guild gate may not cover own-accounts; this rule is
   the explicit fallback.
3. **Max 1 strike attempt per tick.** Bounds blast radius. Optimizer
   may raise this when a stable kill rate is established (≥20
   strikes with ≤1% revert across 24 h).
4. **Max 30M gas per tick.** Hunt sequence worst case is ~25M; cap
   gives headroom for one extra step. Optimizer may raise if a
   recurring `gas_budget_exceeded` anomaly fires.
5. **Forbidden files.** Never write `decisions.md`, `plan.md`,
   `strategic-experiments.md`, `learnings.md`, `improvements.md`,
   `metrics.md`, `targeting.md`. Forbidden by name (see CLAUDE.md
   anti-patterns).
6. **Rule file size cap.** `executor-prompt.md` ≤200 lines. If
   exceeded, optimizer MUST compress as the next change.

## Numerical caps (current)

- `min_margin` = 25
- `min_elapsed_h` = 6
- `max_strikes_per_tick` = 1
- `max_gas_per_tick` = 30_000_000
- `archetype_reject_owners` = see rules/rejects.md
