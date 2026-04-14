# Plan for session 25

## Priority 1: Quest 3011 — Craft 1 Respec Potion

- Auto_v2 running on node 49 (Clearing, Normal, scav cost 300).
- Droptable: "Stick Stone Mint" — items 1001(9), 1002(9), 1012(4) = ~18% Mint per tier.
- Steps: stop auto_v2 → stop all kamis → scavenge_claim_and_reveal(49).
- If Mint (1012) obtained:
  - craft_item(recipe 9): 1 Mint → 500 Shredded Mint (needs Spice Grinder, have 1)
  - craft_item(recipe 3): 1 Plastic Bottle + 500 Shredded Mint → 1 Respec Potion (needs Portable Burner, have 1)
  - complete_quest(3011)
- If not: restart auto_v2 on node 49, try again next session.
- NOTE: Only 1 Plastic Bottle remaining. Need to acquire more if used.
- Missed Mint in sessions 22, 23, and 24. Expected to hit within 1-3 more attempts.

## Priority 2: Quest 3003 — Level up kami

- Kamis have been harvesting for 4+ days since last XP check. Some now have enough XP to level up.
- Kamis must be RESTING to level up — do this while kamis are already stopped for Priority 1 scavenging.
- Steps:
  1. After stopping kamis for scavenge, call get_account_kamis() to check all kami levels and XP.
  2. Use the /api/playwright/kami/{id}/ endpoint per kami to read progress.xp and progress.level.
  3. For each kami that has enough XP: call level_up_kami(kami_id) (or level_to for multiple levels).
  4. After at least 1 successful level-up: complete_quest(3003).
  5. Remember: "Never submit speculative transactions" — verify XP is sufficient before each level-up tx.
- After quest completion, check what quest 3004 requires (it was gated behind 3003).

## Priority 3: Quest 3006 — Name a Kami

- Quest requires naming a kami. You have all the items needed.
- Figure out how naming works: check game-data.md, catalogs, and the on-chain system contracts for the naming mechanism. Build a naming tool if one doesn't exist yet (system.kami.name or similar).
- Kami must be in room 11 for naming. Use travel_to_room to move one kami there while the rest harvest.
- Complete this in the same session if possible — kamis are already stopped for Priorities 1-2.

## Priority 4: Quest 17 — Move 100 times

- ~31 moves done. Accumulates naturally from travel. Do NOT grind.
- After Q17: quest 18 = Harvest >720 min at Scrap Confluence (node 31).
- Unlocks SQ 3007 (Move 500 times) which also accumulates naturally.

## Quest overview

- **Quest 17** (MSQ): Move 100 times — ~31/100, accumulating naturally
- **Quest 3011** (side): Craft 1 Respec Potion — need Mint from scavenging node 49
- **Quest 3003** (side): Level up kami — kamis now have XP from 4+ days of harvesting, attempt while RESTING
- **Quest 3006** (side): Name a Kami — figure out naming tool, move kami to room 11, name it
- **Quest 6**: Liquidate kami — waiting for user review

## Upcoming quests (reference)

- **Quest 18** (MSQ): Harvest >720 min at Scrap Confluence (node 31) — after Q17
- **Quest 3004** (side): unlocks after 3003 — check objectives after completing 3003
- **Quest 2014** (Mina): Give 2 Wooden Stick + 125 Sanguineous Powder + 125 Resin Tincture (needs MSQ 30)

## Active strategies
- auto_v2 on node 49, 20 kamis, REST regen, 5% safety. 20/21 slots used.

## Inventory notes
- MUSU: ~172,140
- Wooden Stick: 119
- Pine Cone: 12
- Daffodil: 7
- Essence of Daffodil: 300
- Black Poppy Extract: 450
- Pine Pollen: 500
- Sanguineous Powder: 250
- Stone: 321
- Plastic Bottle: 1 (critical — only 1 left)
- Ghost Gum: 1,057
- Ice Cream: 93
- Better Ice Cream: 10
- Rock Candyfloss: 66
