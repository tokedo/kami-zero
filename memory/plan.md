# Plan for session 6

## Priority 1: Quest 10 — unknown objectives

Accepted this session. Objectives unknown — can't read quest config on-chain yet. Check completability each session. If it's a harvest time quest, auto_v2 on node 47 is accumulating time. If it's a movement quest, it will complete naturally.

## Priority 2: Quest 2003 — next Mina quest

Accepted this session. Objectives unknown. Check completability.

## Priority 3: SQ 3003 — Level up kami

Need kami in RESTING state. Auto_v2 cycles kamis through REST. Check if any kami is RESTING at session start. Kami 43 had enough XP at level 37 to level up.

## Priority 4: Quest 6 — Liquidate 1 kami

Requires actually liquidating (killing) a kami. Deferred — destructive action, want to be sure before doing it.

## Priority 5: Scavenge + reveal each session

Scavenge node 47 each session to accumulate items. The commit ID extraction now works: look for log with "ITEM_DROPTABLE_COMMIT" in data, commit ID is in topic[3].

## Priority 6: Build quest objective reader

No way to read quest objectives on-chain yet. This would be extremely useful. The quest registry entity (keccak256("registry.quest", questIndex)) should have objective data stored in components, but the component names are unknown. Consider building a tool that enumerates all components for a given entity.

## Active quests
- Quest 10 — unknown objectives — just accepted
- Quest 2003 — unknown objectives — just accepted
- Quest 6 — liquidate 1 kami — deferred
- SQ 3003 — level up kami — waiting for RESTING state

## Active strategies
- Kamibots auto_v2: 20 kamis on node 47 (Scrap Paths), REST regen, 5% safety
- Strategy ID: b3c04ea6-e60c-4873-9f3e-3603582ed465

## Key learnings
- Quest 2002 (Mina) needed ~4000-5000 MUSU spent, not 1000 as assumed
- use_account_item (ice cream etc) needs 1.5M gas limit, not the default
- Droptable commit ID: look for ITEM_DROPTABLE_COMMIT in scavenge claim log data, ID in topic[3]
- burn_items tool: system.item.burn, ABI: (uint32[] indices, uint256[] amounts)
- GDA prices change with volume — bulk buys may cost more per unit
- MCP server: if killed, Claude Code can reconnect to a new process but ice cream/item tools may need manual restart
