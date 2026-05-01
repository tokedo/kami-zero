# Plan for session 75

## Context

Session 74 force-stopped all 17 in-flight harvests (29.55M gas, zero silent-skips). Roster is **20/20 RESTING** and transferable. `ideas_to_founder.md` item 2 is **READY for founder action — Standing**. kami-zero is in PREDATOR mode (CLAUDE.md), quests paused, auto_v2 halted since session 73.

The next session is gated on whether the founder has executed the predator team transfer. Cron may fire before the founder wakes kami-zero manually — handle both cases.

## Priority 0 — Read founder signals first

1. `cat memory/alerts.md` — any new founder reply on Q49 or anything else?
2. `cat ideas_to_founder.md` — has item 2 been Resolved (transfer done) or status updated?
3. `mcp__kamigotchi__get_account_kamis("bpeon")` — does the roster look the same as session 74's snapshot, or has the founder swapped kamis?

## Priority 1 — Branch on transfer status

### Branch A: Transfer landed (new predator roster present)

Doctrine first: **data work, not movement**. Do NOT move or strike on first sight.

1. Per-kami base-stat read: `get_kami_state` (full, not slim) on each new kami. Capture base_violence, base_power, body_affinity, hand_affinity, current room, level, equipment.
2. Oracle scan: `oracle_kami_summary(kami_index)` for each new kami over 7d if any history exists, plus `oracle_top_nodes(7d, 20)` for current node activity.
3. Cross-reference against `predator/guild-no-touch.csv` — confirm no new kami's owner is on the no-touch list (would be weird but worth a check).
4. Draft initial hunt plan in `predator/learnings.md`: candidate nodes, candidate target clusters, counter-predator awareness for those nodes. **No tx this session unless plan is in writing first.**
5. Skip on-chain liquidation tx until session 76 — first tx happens only after the plan is reviewed (founder approves or kami-zero re-reads the doctrine).

### Branch B: Transfer not yet landed

Do not idle. Invest the session in mechanics homework:

1. Inspect `executor/server.py` for any system-resolution path that exposes `system.harvest.liquidate`. Document the ABI sig (params, return) in `predator/mechanics.md`. If the system isn't pre-registered in executor, derive its ID from `integration/ids/systems.json` and confirm via `_resolve_system`.
2. Map the harvest entity → kami_id and harvest entity → node_id traversal so `harvest_liquidate` oracle rows can be enriched. Pick 2–3 sample harvest IDs from oracle's `kami_action` table and verify the chain reads.
3. If oracle window has grown, retry `kami_static` lookup for the 38 unresolved guild-no-touch handles. Update `guild-no-touch.csv` and refresh the `Updated:` line.
4. Cap recon at ~30 min. Quality over completeness.

## Priority 2 — Hard rules (non-negotiable)

- **No on-chain hunt tx** until: (a) transfer landed, (b) `predator/learnings.md` has a written plan, (c) `predator/guild-no-touch.csv` `Updated:` line is ≤7 days old.
- **No quest progression** — paused indefinitely.
- **No auto_v2 relaunch** — strategy stays halted.
- **Counter-predator math required before every strike** — never freelance.

## Active strategies
- None. (Auto_v2 halted session 73, all 20 kamis RESTING since session 74.)

## Active quests
- All paused. Q49 escalation in `memory/alerts.md` still open (founder territory).

## Reschedule
- Default `+72h` from session 74 (set in `memory/next-run-at`). Founder will likely wake kami-zero manually before then.
