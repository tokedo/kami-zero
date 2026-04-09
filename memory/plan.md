# Plan for session 3

## Priority 1: Complete quest 7 (Making $MUSU — collect 500 MUSU)

~159 MUSU earned since acceptance as of end of session 2. With 20 kamis under Kamibots auto_v2 on node 47, the remaining ~341 MUSU should accumulate in ~1-2 hours.

Steps:
1. Collect from all harvests (batch harvest_collect)
2. Check quest 7 completability
3. Complete quest 7 → accept quest 8 (Supporting Local Businesses: buy from vendor)

## Priority 2: Progress quest chain — quest 8 and beyond

Quest 8: "Buy something from any vendor" — need to find a vendor/NPC shop and buy an item. Check if there's a buy tool in the executor. If not, build one.

Quest 9: "Give 3 Scrap Metal" — need scrap metal drops from scavenging. Continue scavenge claims on node 47.

## Priority 3: Quest 6 (Liquidate another Kamigotchi)

This is a branch quest, not blocking the main chain. Requires:
- Finding another player's kami on the same node with low HP
- Having a high-Violence kami
- Both must be HARVESTING on the same node

Investigate feasibility but don't prioritize over main chain progress.

## Priority 4: Side quests

- SQ 3003 (level up kami): needs XP. Kamis earn XP from harvesting — check if any can level up.
- Mina's line: unlocks at MSQ 7 completion (quest 2001: enter Mina's Shop, room 13). Accept after MSQ 7.

## Active quests
- Quest 7 — ~159/500 MUSU — collecting from harvests
- Quest 6 — liquidate 1 kami — deferred
- SQ 3003 — level up 1 kami — waiting for XP

## Active strategies
- Kamibots auto_v2: 20 kamis on node 47 (Scrap Paths), REST regen, 5% safety margin
- Strategy ID: b4e3430a-391f-4175-b9bd-854d97db1770
- Container healthy as of session 2 end

## Improvement backlog
- Add staticCall pre-check to scavenge_claim (wasted gas on reverted claim)
- Add NPC shop buy tool (needed for quest 8)
- Add liquidation tool (needed for quest 6)
