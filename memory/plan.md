# Plan for session 2

## Priority 1: Build quest tooling (blocks everything else)

Session 1 tried to start harvests before checking quests — that was backwards. Quests tell us WHERE to harvest and WHICH drops to farm. Fix by building quest tooling first, then use it to drive all other decisions this session.

No quest read/accept/complete tools exist in the executor. Build them:
- `get_account_quests(account)` — list accepted + available quests for the account
- `get_quest_details(quest_index_or_entity_id)` — requirements, progress, rewards
- `accept_quest(quest_index, account)` — accept a quest from NPC
- `complete_quest(quest_entity_id, account)` — submit completion
- `drop_quest(quest_entity_id, account)` — abandon (rarely needed)

References:
- `systems/quests.md` — game mechanics
- `integration/api/quests.md` — API patterns (if present)
- `state-reading.md` — how to enumerate on-chain entities by component

Commit new tools with `harness:` prefix. Document in `memory/improvements.md`.

## Priority 2: Quest-driven plan for bpeon

Once quest tools exist:
- Enumerate bpeon's accepted + available quests (main quest line + Mina's)
- For each quest, extract: target item, target node, time required, kami requirements
- Pick ONE quest to work toward this session
- Determine which node(s) satisfy it — this drives harvest location

## Priority 3: Execute harvest for the chosen quest

- Move kamis to the quest-required node (only if different from node 86)
- Retry Kamibots `auto_v2` — if still broken (see `memory/alerts.md` for session-1 outage), implement direct on-chain `start_harvest_batch` / `stop_harvest_batch` using the `system.harvest.start` / `system.harvest.stop` ABIs as fallback. This bypasses Kamibots entirely but loses HP-based auto-rest — you'd need to stop manually before HP runs out.
- Kamis may sit idle for part of this session while quest tools are built — that's fine and correct. Idle-in-right-place beats harvesting-in-wrong-place.

## Active state (end of session 1)
- 20 kamis, all RESTING on node 86 (Guardian Skull, EERIE/INSECT) — this may or may not be the right node; decide after quest analysis
- 0 strategies running, 21 strategy slots available
- Kami affinities (sample, kami #43): body=NORMAL, hand=EERIE
- 102,398 Musu, 100 Red Ribbon Gummies

## Kamibots outage reminder
See `memory/alerts.md`. As of 2026-04-09 14:17 UTC, all Kamibots strategy containers crashed with `Error: supabaseKey is required` (server-side Supabase init failure in the strategy container image). Human operator has been notified and is filing a bug report with the Kami team. Retry Kamibots at the start of Priority 3 — if still broken, use the direct on-chain fallback described above.
