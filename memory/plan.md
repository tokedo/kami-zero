# Plan for session 70

## Priority 0 — Read alerts.md FIRST

`memory/alerts.md` has an ACTIVE Q49 BLOCKADE alert raised in session 69 with a request for founder off-chain quest-registry inspection. If the founder has responded (via a Priority 0 directive in this plan, or by editing alerts.md, or by providing direct guidance), follow that. If no founder response yet, follow Priority 1 below.

## Priority 1 — Cheap Q49 probe + level-up routine, NO force-flushing

**Hard rule**: do NOT force-flush kamis this session. Session 69 demonstrated `stop_harvest_batch` of 5 long-accumulated kamis costs ~8.5M gas (not the 1.5M budgeted), making continued hypothesis-testing on Q49 prohibitively expensive. Wait for founder input on Q49's actual objective.

### Routine (free reads + opportunistic cheap actions only)

1. `check_quest_completable(49)` — free baseline. Q49 expected FALSE.
2. `get_scavenge_points(15)` — free. If ≥100 (1+ tier from natural cycling), do ONE `scavenge_claim_and_reveal(15)` (~1.76M gas) as a low-cost data point. Re-check Q49. Stop after one claim regardless.
3. `get_account_kamis` — count states. Expect ramp post-session-69 force-flush. 9 kamis (43, 1064, 6096, 7803, 8745, 10011, 12459, 13235, 13390) were force-flushed and should now be RESTING/HARVESTING under auto_v2.
4. `get_kamis_progress_batch(<all 20>)` — note level + XP. With 9 freshly-flushed kamis having banked +579 XP each (avg) plus pre-existing residue from prior cycles, **expect multiple kamis with banked +1 level**.
5. `level_and_allocate_batch` for any RESTING kami with ≥1 banked level. Default skill plan: Guardian-leaning sustain (see CLAUDE.md). For most current kamis at L33–38, the next priority is finishing **313 Patience** (Guardian T1, +5 MUSU/hr per pt, max 5) for any kami below 5 SP there, then moving to T2 (321/322/323) once T1 sums to 5.
6. Auto_v2 health check: `get_all_strategies` + `get_strategy_status(43)`. Verify still ACTIVE and 2553 (silent-skip from session 69) not stuck. If 2553 has been ACTIVE for >24h with no progress, may need a single `stop_harvest_batch([2553])` to cycle it.
7. Side-quest passive checks (free): no work on Q3007/Q6 — leaf quests, deferred.

### Stop condition

- After completing the routine above, schedule next session +12h (or +6h if Q49 cleared via cheap claim).
- Do NOT escalate Q49 hypothesis testing this session. Wait for founder input.

## Priority 2 — If reveal-revert recurs at node 15

Session 69 had reveal reverts on both claims at node 15 — a regression from sessions 66/67/68. If the cheap claim (Priority 1 step 2) also reveal-reverts, this confirms a node-15-specific pattern. Note in decisions.md but no action — items continue to materialize via claim-direct grant.

## Inventory snapshot (end of session 69)

- MUSU: **474,877** (+5,208 from 9 force-flush cycle stops)
- VIPP: 49,744 (unchanged)
- **Patinated Pipe: 212** (+28 from 2 claims; Q48 long-cleared, durable buffer)
- **Cigarette Butt: 134** (+20; Q49 demands 15 fresh — supply not the issue)
- Cheeseburger: 88 (+4)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115, Scrap Metal: 71
- Maple-Flavor Ghost Gum: 1057, Ice Cream: 78, Better Ice Cream: 10, Rock Candyfloss: 63
- Pine Pollen: 500, Essence of Daffodil: 300, Black Poppy Extract: 450, Sanguineous Powder: 125
- Holy Dust: 4, Resin Tincture: 375, Resin: 25
- Booster Pack: 13, Spell Cards: misc
- Flash Talisman: 1, Respec Potion: 1, Hostility Potion: 1, Bless Potion: 1, Grace Potion: 1, XP Potion: 1
- Essence of Hearing: 2, Ashlar: 1, Timber: 1
- Key Items: Sextant, KW Maps, Unmarked Data Chip
- Node 15: 12 pts remainder (post-claim)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC. ~35h uptime as of session 69.

## Quest status

- **Q1–Q48 ✓**.
- **Q49 (Community Service)**: ACCEPTED 2026-04-29 17:31 UTC. **5 cumulative scavenge claims post-acceptance, STILL FALSE**. Hypotheses ruled out: DROPTABLE_ITEM_TOTAL[1018]≥15, ITEM_BURN[1018]≥15, SCAV_CLAIM_NODE[15]≥5. Live: SCAV_CLAIM_NODE[15]≥N for N≥6 (possibly 15). **BLOCKED — awaiting founder off-chain inspection.**
- **Q50 (You Smelt It…)**: gated behind Q49. Objective: Craft 1 Ingot.
- **Q3007 (Move 500)**: passive accumulator; FALSE. Deferred.
- **Q6 (Liquidate)**: deferred.
- **Mina Q2014–Q2016**: ALL completed.

## Carried-forward rules (still valid)

- Quest-first: Q49 is the active MSQ gate (currently blocked, awaiting founder).
- Don't disturb auto_v2 for hypothesis testing — gas was 5–6× budget on long-accumulated harvests.
- **NEW: budget force-flush at ≥10M gas per 5-kami batch when harvests are >6h accumulated.** Plan accordingly.
- YieldIndex=2 nodes yield VIPP; node 15 is YieldIndex=1 (MUSU).
- Scav 1:1 invariant: scav points ≈ MUSU/VIPP credited per cycle.
- Inventory existing items DO NOT count for "Scavenge X" objectives (snapshot at acceptance).
- stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.
- Travel `dry_run=True` first for any multi-hop move.
- `get_kami_state_slim` omits level/experience — use `get_kamis_progress_batch`.
- `component.id.parent` is known-broken on this World; do NOT re-investigate.

## Quest graph (MSQ critical path)

Q31✓→…→Q47✓→Q48✓→**Q49 [BLOCKED — awaiting founder objective inspection]** → Q50 (Craft 1 Ingot) → Q51 (Give 1 Essence of Hearing — already have 2!) → Q52 (Move to Cave Crossroads, Give 1 Ashlar — have 1!) → …

Note: Inventory already has Essence of Hearing × 2 and Ashlar × 1 — multiple downstream quests pre-stocked. Once Q49 unblocks, Q50–Q52 should clear quickly.
