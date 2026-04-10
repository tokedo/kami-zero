# Priority 0 (read first): travel_to_room is now available

A new MCP tool ships in this session: `travel_to_room(target_room, account="bpeon", dry_run=True)`. It replaces manual pathfinding entirely. **DO NOT plan paths from `rooms.csv` adjacency in your head.** Session 4 burned ~730k gas on reverted moves doing exactly that — this tool exists so it never happens again.

- Always `dry_run=True` first to inspect the path, then execute without `dry_run` to act.
- Auto-uses SP+ items (21201–21206 ice creams / paste) from inventory when stamina would otherwise run out. Returns a clean partial result if it can't reach the target.
- See `CLAUDE.md` → "Movement: use travel_to_room" for full semantics, including the lower-bound `stamina_remaining` caveat and the 15s Kamibots cache gotcha.
- Backed by deterministic BFS in `executor/rooms_graph.py`. Static graph, zero tokens, always correct.

**Data fix shipped alongside:** rooms 19 (Temple of the Wheel, z=3) and 59 (Black Pool, z=1) were marked "To Update" in `catalogs/rooms.csv` and excluded from the graph. They're actually live on-chain and form a bidirectional z=1↔z=3 portal. This unlocks shorter cross-plane paths — e.g. room 79 → 12 dropped from 16 hops to 12 hops.

**Apply to Priority 2 below (1000 MUSU at Mina's, room 13):** start with `travel_to_room(13, account="bpeon", dry_run=True)` to see the path and stamina cost. Then execute. Then `travel_to_room(<return_room>, account="bpeon")` for the return leg. If `reached_target: False` comes back on either leg, append "accumulate SP+ items (21201–21206)" to next session's plan.md and stop the trip cleanly.

A new low-level helper `use_account_item(item_id, account="bpeon")` is also available — use it directly only when you want to top off stamina outside of a travel call.

---

# Plan for session 5

## Priority 1: Quest 9 — Give 3 Scrap Metal

**Check inventory first.** auto_v2 has been harvesting node 47 since session 4 — Scrap Metal (item 1002) may already be in bpeon's inventory from passive scavenge cycles or earlier sessions. Don't get stuck on the session-4 droptable extraction bug if you don't actually need to scavenge.

1. `get_inventory()` — read bpeon's inventory. Look at item index **1002** (Scrap Metal).
2. **If balance ≥ 3** → `complete_quest(9)` immediately. Done. Move to Priority 2.
3. **If balance < 3** → run the scavenge cycle below until you have 3:
   - `harvest_collect([...])` to bank MUSU and accumulate scavenge points on node 47
   - `scavenge_claim(47)` — this is the **commit** half of a commit-reveal. It returns commit IDs.
   - In a later block: `droptable_reveal(commit_ids)` — this is what actually drops items into inventory.
   - `get_inventory()` again, repeat until item 1002 ≥ 3.
   - Drop weights for node 47: Scrap Metal (1002, w=9), Pinecone (1005, w=7), Cheeseburger (11302, w=6) — ~41% Scrap Metal per reveal.
4. Then `complete_quest(9)`.

**Note on the droptable extraction bug:** session 4 pulled the wrong commit IDs out of the scavenge-claim tx logs and the reveal failed. **Only fix this if step 3 above turns out to be required.** If inventory already has enough, the bug fix is wasted work — defer it. The fix lives in Priority 5; pull it forward only if you're forced to.

## Priority 2: Quest 2002 — Spend 1000 MUSU at Mina's Shop

Need to buy 1000 MUSU worth of items from Mina (NPC 1, room 13). Cheapest option: Ghost Gum at ~18 MUSU each = ~56 purchases. Could buy in bulk with listing_buy tool.

Approach: Move to room 13, buy in bulk, move back. Accept that this costs movement stamina (10 moves round trip = 50 stamina).

## Priority 3: Accept quest 10+

After quest 9, accept next main quest. Check requirements.

## Priority 4: SQ 3003 — Level up kami

Need kami in RESTING state. Auto_v2 cycles kamis through REST. Check at session start if any are RESTING. Kami 43 had enough XP at level 37.

## Priority 5: Fix harness issues

- Droptable reveal commit ID extraction: session 4 extracted wrong ID from logs. Need to parse Store_SetRecord events correctly to find droptable entity IDs. **Do NOT pull this forward unless Priority 1 inventory check shows < 3 Scrap Metal AND scavenging is the bottleneck.** Otherwise this is a "nice to have" — defer.
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
