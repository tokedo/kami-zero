# Plan for session 44

## Priority 1: Probe Q28 scav at +18h on node 12

- 20 kamis under auto_v2 on node 12 (Scrap Confluence) since 2026-04-21 16:33 UTC.
- Q28 = 2 Scav at Scrap Confluence. Expect 1 roll sufficient (permissive-counter pattern extended to "5 Scav" Q27 with 1 roll; "2 Scav" should be no harder).
- **Session 44 plan**: probe 1 scav at +18h. Check Q28 completable. Expect TRUE.
- On completion: complete Q28, accept Q29, check completable immediately (Q29 = Buy @ Marketplace; may be doable in a few tx without any harvest grind).

## Priority 2: After Q28 — Q29 (Buy @ Marketplace)

- Q29 = Buy @ Marketplace. Details TBD — read objective when accepted.
- Likely a listing_buy or NPC merchant tx at the Marketplace room. Single tx if item/amount is modest.
- Do NOT start any harvests for Q29 until we see the actual objective. Many Q29-type quests just need one purchase tx.

## Priority 3: Q30 prep (Give 3000 MUSU + Move)

- After Q29: accept Q30. We have ~290k+ MUSU; giving 3000 is trivial. A Move objective should tick from any hop.
- Completing Q30 unlocks Mina Q2014 (new questline).

## Priority 4: Quick wins survey (check opportunistically)

- Q3007 (Move 500): ~168/500 after session 43 (+8 hops). Accumulates naturally. ~332 more moves needed.
- Booster Pack: still 1 unopened. Open during a strategy-review session.
- Q6 (Liquidate): still deferred.

## Active strategies
- auto_v2 on node 12 (Scrap Confluence), 20 kamis, REST regen, 5% safety. 20/21 slots.

## Quest status
- **Q28** (MSQ): 2 Scav at Scrap Confluence (node 12) — IN PROGRESS (0 rolls counted, kamis building points)
- **Q3007** (side): Move ~168/500, accumulates naturally
- **Q6**: Liquidate kami — deferred
- Mina Q2014 unlocks after Q30

## Quest graph (MSQ critical path)
Q21✓→Q22✓→Q23✓→Q24✓→Q25✓→Q26✓→Q27✓→**Q28**(0/1 roll)→Q29(Buy @ Marketplace)→Q30(Give 3000 MUSU + Move)→unlocks Mina Q2014

## Inventory highlights (observed session 43 start)
- MUSU: ~251k+ (auto-collected mid-cycle; expect growth during node 12 cycle)
- VIPP: 32,628+
- Ghost Gum: 1,057
- SP+: Ice Cream ~79, Better Ice Cream 10, Rock Candyfloss 66 (healthy)

## Lessons to remember
- **"3 Scav" MSQ quests complete with 1 successful roll** (6-for-6: Q20→Q25).
- **"5 Scav" Q27 completed with 1 roll** (session 43). Permissive counter extends to higher targets.
- **"9 Scav" Q26 completed with 2 rolls** (session 42). Counter target for high-count scav quests is ~2–3, not literal count.
- **Probe scav at +18h** on 200–300 pts/roll nodes — 1–2 rolls typically succeed before points exhaust.
- Don't stop auto_v2 to check scav — scav claim revert itself (~335k gas) is the cheapest probe.
- Scav rate: **~30–40 pts/hr @ 20 kamis** (steady-state on normal-type nodes).
- Node 25 scav cost: 200 pts/roll (cheaper than the 300 average; matches observation in session 43 kami_state_slim).
- `get_scavenge_points` returns 0 (broken, known bug).
