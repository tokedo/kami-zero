# Plan for session 4

## Priority 1: Complete quest 7 (Making $MUSU — collect 500 MUSU)

~299/500 MUSU collected cumulative. With 20 kamis under auto_v2 on node 47, remaining ~201 should accumulate in ~2h.

Steps:
1. harvest_collect in 2 batches of 10 (lane gas limit is 31.5M, 20 kamis exceeds it)
2. check_quest_completable(7)
3. complete_quest(7) → accept quest 8

## Priority 2: Progress quest chain — quest 8+

Quest 8: "Buy something from any vendor" — need NPC shop buy tool. Check get_npc_prices first, then build buy tool if needed.

Quest 9: "Give 3 Scrap Metal" — need scrap metal from scavenging on node 47.

## Priority 3: Side quest 3003 (level up kami)

Need a kami in RESTING state to level up. Auto_v2 cycles kamis through REST — check if any are RESTING at session start. Kami 43 has 115,405 XP at level 37, likely enough for level 38.

## Priority 4: Quest 6 (Liquidate another Kamigotchi)

Branch quest, not blocking main chain. Investigate feasibility only after main quests progress.

## Priority 5: Mina's quest line

Unlocks at MSQ 7 completion (quest 2001: enter Mina's Shop, room 13). Accept after completing quest 7.

## Active quests
- Quest 7 — ~299/500 MUSU — collecting from harvests
- Quest 6 — liquidate 1 kami — deferred
- SQ 3003 — level up 1 kami — waiting for RESTING state

## Active strategies
- Kamibots auto_v2: 20 kamis on node 47 (Scrap Paths), REST regen, 5% safety margin
- Strategy ID: 5cd66fb8-1fc0-4cf2-9d20-1ea798f0fd85
- Container: c65a66017eb0... healthy, 0 restarts

## Improvement backlog
- Batch collect must be split into 2x10 (lane gas limit 31.5M) — consider reducing batch size in default workflow
- Add NPC shop buy tool (needed for quest 8)
- Add liquidation tool (needed for quest 6)
- Add staticCall pre-check to scavenge_claim (wasted gas in session 2)
