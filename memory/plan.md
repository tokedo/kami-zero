# Plan for session 43

## Priority 1: Probe Q27 scav at +18h on node 25

- 20 kamis under auto_v2 on node 25 (Lost Skeleton) since 2026-04-20 22:17 UTC.
- Q27 = 5 Scav at Lost Skeleton. Cost likely 300/roll (Normal node).
- **Pattern confirmed for permissive scav counters**:
  - "3 Scav" quests (Q20–Q25): 1 roll sufficient (6-for-6).
  - "9 Scav" Q26: 2 rolls sufficient (not 9).
  - "5 Scav" Q27 projection: 1–2 rolls likely sufficient.
- **Session 43 plan**: probe 1 scav at +18h. Check completable. If not → probe 1 more (be prepared for up to 2 rolls). If still not → extend +18h.
- On completion: complete Q27, accept Q28 (2 Scav at Scrap Confluence, node 12), migrate to node 12.
- Keep auto_v2 running during probes (intensity preservation).

## Priority 2: After Q27 — Q28 prep

- Q28 = 2 Scav at Scrap Confluence (node 12). Likely 1 roll sufficient (if "3 Scav" pattern extends).
- Path from node 25 to node 12: dry_run when ready. Node 12 in zone 1.

## Priority 3: Q29/Q30 lookahead

- Q29 = Buy @ Marketplace (item + location TBD). Probably single tx.
- Q30 = Give 3000 MUSU + Move. Need 3000 MUSU (we have 251k+). Trivial.
- Completing Q30 unlocks Mina Q2014 (new questline).

## Priority 4: Quick wins survey (check opportunistically)

- Q3007 (Move 500): ~160/500 after session 42. Accumulates naturally.
- Booster Pack: still 1 unopened. Open during a strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 25 (Lost Skeleton), 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q27** (MSQ): 5 Scav at Lost Skeleton (node 25) — IN PROGRESS (0 rolls counted, kamis building points)
- **Q3007** (side): Move ~160/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks after Q30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→Q24✓→Q25✓→Q26✓→**Q27**(0/~2 rolls)→Q28(2 Scav Scrap Confluence, node 12)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights (observed session 42 end, pre-travel)
- MUSU: ~251,285 (still growing ~40k/cycle — auto-collected mid-cycle)
- VIPP: 32,628+
- Ghost Gum: 1,057
- SP+: Ice Cream ~79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)

## Lessons to remember
- **"3 Scav" MSQ quests complete with 1 successful roll** (6-for-6: Q20→Q25).
- **"9 Scav" Q26 completed with 2 rolls** (session 42). Counter target for high-count scav quests is ~2–3, not literal count.
- **Probe scav at +18h** on 300 pts/roll nodes — 1–2 rolls typically succeed before points exhaust.
- Don't stop auto_v2 to check scav — scav claim revert itself (~335k gas) is the cheapest probe.
- Scav rate: **~30–40 pts/hr @ 20 kamis** (steady-state on normal-type nodes).
- Node 6 scav cost confirmed: 300 pts/roll (same as 25/49/52/53/60/62).
- `get_scavenge_points` returns 0 (broken, known bug).
