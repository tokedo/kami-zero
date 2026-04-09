# Plan for session 5

## Priority 1: Quest 9 — Give 3 Scrap Metal

Need Scrap Metal from scavenging node 47. Droptable for node 47: Scrap Metal (1002, weight 9), Pinecone (1005, weight 7), Cheeseburger (11302, weight 6). ~41% chance of Scrap Metal per reveal.

Steps:
1. Collect from kamis (accumulates scavenge points)
2. scavenge_claim(47) — claim tiers
3. Fix droptable commit ID extraction (session 4 failed — used wrong ID from tx logs)
4. droptable_reveal — hope for Scrap Metal
5. Repeat until 3 Scrap Metal collected
6. complete_quest(9)

## Priority 2: Quest 2002 — Spend 1000 MUSU at Mina's Shop

Need to buy 1000 MUSU worth of items from Mina (NPC 1, room 13). Cheapest option: Ghost Gum at ~18 MUSU each = ~56 purchases. Could buy in bulk with listing_buy tool.

Approach: Move to room 13, buy in bulk, move back. Accept that this costs movement stamina (10 moves round trip = 50 stamina).

## Priority 3: Accept quest 10+

After quest 9, accept next main quest. Check requirements.

## Priority 4: SQ 3003 — Level up kami

Need kami in RESTING state. Auto_v2 cycles kamis through REST. Check at session start if any are RESTING. Kami 43 had enough XP at level 37.

## Priority 5: Fix harness issues

- Droptable reveal commit ID extraction: session 4 extracted wrong ID from logs. Need to parse Store_SetRecord events correctly to find droptable entity IDs.
- Scavenge points reading returns 0 (component ID issue from session 2). Points do accumulate (claim succeeded), just can't read them.
- listing_buy tool added but needs MCP server restart to be available. Consider restarting executor.

## Active quests
- Quest 9 — give 3 Scrap Metal — need to scavenge
- Quest 2002 — spend 1000 MUSU at Mina's — need to buy items
- Quest 6 — liquidate 1 kami — deferred
- SQ 3003 — level up 1 kami — waiting for RESTING state

## Active strategies
- Kamibots auto_v2: 20 kamis on node 47 (Scrap Paths), REST regen, 5% safety
- Strategy ID: 981e3748-cf85-4b07-baca-d6d74c0781f9
- Container: ac1cbd23db... healthy, 0 restarts
- Config key: kamiIndices (NOT kamis) + harvestPreferences per kami

## Key learnings
- auto_v2 config uses `kamiIndices` not `kamis`, and needs `harvestPreferences` array
- Room movement is adjacency-based (same z, diff 1 in x or y) + special exits for z transitions
- NPC merchants have specific room locations: Mina=room 13, Vending Machine=room 18
- listing_buy uses global item indices (e.g. 11301), not merchant-local indices
- Path from room 47 to room 13: 47→4→30→3→2→13 (5 moves, 25 stamina)
