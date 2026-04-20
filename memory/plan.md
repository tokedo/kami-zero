# Plan for session 42

## Priority 1: Continue Q26 grind — probe scav again at 18h+

- 20 kamis under auto_v2 on node 6 since 2026-04-19 09:48 UTC.
- Q26 (9 Scav at Labs Entrance) is NOT as permissive as the "3 Scav" MSQ pattern.
  - Session 41 (at 18.2h): 1 roll succeeded → Q26 still FALSE. 2nd probe reverted (insufficient pts).
  - Rolls counted toward Q26 so far: **1**. Counter target: probably 9 but may be lower (test each session).
- **Session 42 plan**: probe 1–2 rolls at +18h, then `check_quest_completable(26)` after EACH success.
  - Stop probing as soon as either: (a) Q26 becomes completable, or (b) a probe reverts (points exhausted).
  - If completable → complete Q26, accept Q27, migrate to node 25.
  - If not → log rolls-counted and schedule +18h.
- Keep auto_v2 running on node 6 (never stop it for Q26 probing — intensity reset is too expensive).

## Priority 2: Plan for Q26 total duration

- Scav rate @ 20 kamis on node 6: ~30-40 pts/hr → 1 roll per ~8-10h of accumulation.
- If Q26 counter truly needs 9 rolls: ~72-90h total, or ~4-5 more probe sessions at +18h cadence.
- If counter is partially permissive (e.g., 3 or 5 rolls): fewer sessions.
- Update this section after session 42 based on observed rolls-counted-per-probe.

## Priority 3: After Q26 — Q27 prep (not this session)

- Q27 = 5 Scav at Lost Skeleton (node 25).
- Path from node 6 to node 25: dry_run when ready.

## Priority 4: Quick wins survey (check opportunistically)

- Q3007 (Move 500): ~153/500 after session 40 (no new moves session 41). Accumulates naturally.
- Booster Pack: still 1 unopened. Open during a strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 6 (Labs Entrance), 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q26** (MSQ): 9 Scav at Labs Entrance (node 6) — IN PROGRESS (1 roll counted; counter target unknown but >1)
- **Q3007** (side): Move ~153/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks at MSQ 30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→Q24✓→Q25✓→**Q26**(1/~9 rolls)→Q27(5 Scav Lost Skeleton, node 25)→Q28(2 Scav Scrap Confluence, node 12)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights (observed session 41)
- MUSU: 251,285 (growing ~40k per 18h auto_v2 cycle)
- VIPP: 32,628
- Ghost Gum: 1,057
- SP+: Ice Cream 79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)
- Stone 420, Scrap Metal 53, Wooden Stick 205, Pine Cone 25 (scav/harvest drops)

## Lessons to remember
- **"3 Scav" MSQ quests complete with 1 successful roll** (6-for-6: Q20→Q25).
- **"9 Scav" Q26 requires multiple rolls** (session 41: 1 roll did NOT complete). Real grind.
- Probe scav at 18h+ elapsed on 300 pts/roll nodes — 1 roll typically succeeds, 2nd typically reverts.
- Don't stop auto_v2 to check scav — scav claim revert itself (~335k gas) is the cheapest probe.
- Scav rate: **~30-40 pts/hr @ 20 kamis** (steady-state on normal-type nodes).
- Node 6 scav cost: **300 pts/roll** (confirmed session 41, matches 49/52/53/60/62).
- `get_scavenge_points` returns 0 (broken, known bug).
