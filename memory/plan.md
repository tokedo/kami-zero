# Plan for session 74

> **Mode**: PREDATOR (since 2026-05-01). Read `predator/README.md` first. Quest progression is paused. Hard rules in `CLAUDE.md` block C are inviolable without founder approval.

## Priority 0: Read first
1. `memory/alerts.md` — founder reply on Q49 / pivot? (treat as superseding this plan if so)
2. `ideas_to_founder.md` — has the predator transfer landed (item 2)?
3. `predator/README.md` + recent entries in `predator/learnings.md` + `predator/mechanics.md`.

## Priority 1: Decide based on transfer status

### If predator transfer is COMPLETE:
- `get_account_kamis("bpeon")` — confirm new roster.
- `get_kamis_progress_batch([...new ids])` — capture base/total stats, levels, current skills.
- Read each new kami's `total_violence`, `attack_threshold_shift/ratio`, `attack_spoils_ratio` via oracle `kami_static`. These define their predator profile.
- **Do NOT strike this session.** Doctrine: targeting is data work, not movement. Draft the hunt plan in `predator/learnings.md` based on the new roster's affinities + current node positions.
- If kamis are not at a target-rich node, plan the cluster move BUT log the obol-per-tx math in `decisions.md` first per Hard Rule 4.

### If predator transfer is NOT yet complete:
- **No movement, no harvest, no strikes.** Idle on the kamibots side; in-flight harvests continue to passively resolve.
- Use the session for `predator/mechanics.md` deepening:
  1. Look up `system.harvest.liquidate` via `_resolve_system` in `executor/server.py`. Find the ABI (system contract → executeTyped signature). Document in mechanics.md.
  2. Pick one historical liquidation event (oracle: `SELECT * FROM kami_action WHERE action_type='harvest_liquidate' ORDER BY block_timestamp DESC LIMIT 5`). Read attacker's `kami_static` row and the liquidation event's `amount` to triangulate the obol/musu formula.
  3. Use `harvest_id` from a liquidation row to fetch the harvest entity on-chain (via `_resolve_component('component.id.kami')` against the harvest entity ID) → recover the target kami → cross-reference its base stats. Map out the attacker-vs-target stat spread for surviving kills.
  4. Cap at ~30 minutes of recon. Quality > completeness.
- Retry the 38 unresolved handles in `predator/guild-no-touch.csv` against `kami_static` — oracle window grows; some may now be indexed.

## Priority 2: Hygiene
- `get_all_strategies("bpeon")` should still be empty. If anything sneaks back, stop it.
- No level-up scan this session — predator-build SP plan is undecided until transfer lands.

## Active strategies
(none — auto_v2 halted at session 73 start)

## Active hard constraints
- **No on-chain tx until predator transfer lands.** This is the bright line for sessions 73+ until founder reverses.
- **Guild no-touch gate**: `predator/guild-no-touch.csv` has 44/82 IDs resolved. Until the build of `is_target_protected()` (P4 of session 73), the agent is the gate — every potential strike target's account_id AND handle must be checked against the CSV before any liquidation tx is even drafted.
- File staleness: `Updated: 2026-05-01`. As of session 74 (~24h later), still fresh. After 2026-05-08 the gate must hard-fail to deny-all per CLAUDE.md hard rule 1.

## Schedule
- This session: +24h from session 73 (2026-05-02 22:48 UTC, ts 1777762091).
- Founder may wake earlier when predator transfer is done.
