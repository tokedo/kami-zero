# Plan for session 3

> **URGENT — ad-hoc session triggered by human operator (2026-04-09 ~17:24 UTC).**
> **Kamibots did a platform-wide infra reset after session 2 ended.** All strategies that
> were running (including ours: auto_v2 on node 47, 20 kamis, strategy ID
> `b4e3430a-391f-4175-b9bd-854d97db1770`) have been removed server-side. The kamis
> themselves should still be HARVESTING on-chain on node 47 — only the off-chain Kamibots
> management container is gone.
>
> **Priority 0 (before anything else):**
> 1. `get_account_strategies` to confirm the strategy is gone (expect 0 active).
> 2. `get_player_kamis` to confirm the 20 kamis are still harvesting on node 47.
> 3. Relaunch `auto_v2` for all 20 kamis on node 47 with 5% safety margin, same config
>    as session 2. Record the new strategy ID in plan.md for next session.
> 4. Only after the strategy is healthy, proceed to quest 7 (collect MUSU etc.) below.
>
> If the kamis are no longer harvesting (e.g. Kamibots reset somehow stopped them), use
> `harvest_start` to put them back on node 47 before starting the strategy.
>
> After this session, resume normal scheduling via `memory/next-run-at` — the human
> operator will not intervene again for the regular cadence.

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
- Strategy ID: b4e3430a-391f-4175-b9bd-854d97db1770 — **LIKELY WIPED by Kamibots infra reset; relaunch and update this ID**
- Container was healthy as of session 2 end; status now unknown

## Improvement backlog
- Add staticCall pre-check to scavenge_claim (wasted gas on reverted claim)
- Add NPC shop buy tool (needed for quest 8)
- Add liquidation tool (needed for quest 6)
