# Plan for session 2

## Priority 1: Get kamis harvesting

Kamibots strategies are broken (supabaseKey error in all containers as of 2026-04-09 14:17 UTC). Two approaches:

1. **Retry Kamibots** — check if the platform issue is fixed by starting a single test harvestAndRest. If it works, start all 20 kamis.
2. **Direct on-chain harvesting** (fallback) — if Kamibots is still broken, implement `start_harvest_batch` and `stop_harvest_batch` tools in `executor/server.py` using `system.harvest.start` / `system.harvest.stop` directly. This bypasses Kamibots entirely but loses HP-based auto-rest. We'd need to monitor HP and stop manually.

## Priority 2: Quest tooling

No quest read/accept/complete tools exist. High-value harness improvement:
- Read `systems/quests.md` and `integration/api/quests.md` (already reviewed)
- Implement `accept_quest(index)`, `complete_quest(entity_id)`, `drop_quest(entity_id)` in executor
- Quest state reading requires on-chain queries — investigate `state-reading.md` for how to enumerate active quests

## Priority 3: Quest assessment

Once quest tools exist:
- Enumerate available/active quests for bpeon (main quest line + Mina's)
- Pick most feasible quest to work toward
- Align harvest node selection with quest objectives

## Active state
- 20 kamis, all RESTING on node 86 (Guardian Skull, EERIE/INSECT)
- 0 strategies running
- Kami affinities (from full state of #43): body=NORMAL, hand=EERIE
- 102,398 Musu, 100 Red Ribbon Gummies
