# Plan for session 72

## Priority 0 — Read alerts.md FIRST

Founder may have replied with off-chain Q49 objective inspection. Possible responses:
- **Q49 objective is X (not what catalog says)** → run the matching action (e.g., burn, scavenge at different node, give to NPC). Re-test.
- **Q49 is structurally broken — drop it** → call `drop_quest(49, "bpeon")` and either re-accept (registry redeploy) or skip to Q50 directly via founder-provided escape path.
- **Catalog correct but registry mis-deployed — wait for redeploy** → continue auto_v2 grind, no Q49 action.

If no founder reply: continue with hold pattern below.

## Priority 1 — Q49 hold pattern (no force-flush, no hypothesis testing)

Discipline rule still in force: **catalog ≥15 butts vs 197 owned + 6 cumulative post-acceptance claims at node 15 = exhausted local-state probing.**

1. `quest_state(49, "bpeon")` — should still return `active_blocked / objs_not_met`. If state changed (e.g., `active_ready`), proceed to complete.
2. `get_scavenge_points(15, "bpeon")` — natural rate ~1,200 pts/hr/account → 12h elapsed ≈ 14k+ pts ≈ 140+ tiers from natural cycling.
3. If ≥1 tier (≥100 pts) from natural cycling, do ONE `scavenge_claim_and_reveal(15)` (~1.87M gas) as a low-cost data point. Re-check Q49 via `quest_state(49)`. **Stop after one claim regardless** — discipline rule still applies.
4. **Do NOT force-flush. Do NOT test alternate hypotheses.**

## Priority 2 — Standard level-up routine

`get_account_kamis("bpeon")` first. Read which kamis are RESTING (probably the previously-HARVESTING-10: 2553, 6096, 10011, 43 [Zephyr], 1064, 7803, 8745, 12459, 13235, 13390 — with 43 the most-likely-banked kami at L37, 139,934 XP last session).

`get_kamis_progress_batch([all_resting_kami_ids])`. Eligibility:
- `level` ≥ 33 and `xp ≥ levelCost(level)` where `levelCost(L) = floor(40 * 1.259^(L-1))`.
- Reference table: L33→34: ~63,428; L34→35: ~79,856; L35→36: ~100,540; L36→37: ~126,580; L37→38: ~159,364; L38→39: ~200,600.

Most likely candidates next session:
- **Kami 43 "Zephyr"** L37 with 139,934 XP at session 70 + 1 cycle ≈ 140k+ XP — needs ~159k for L38. Possibly still 15-20k short. Recheck.
- **10647** L34, 61,576 XP — needs 79,856 for L35. After 1 more cycle (~1k XP/cycle short cycle, ~10k+ XP/cycle long cycle), should bank by next session.
- Others well short.

For each kami with banked level(s), use `level_and_allocate_batch`. Default skill plan per CLAUDE.md: Guardian-leaning sustain.
- Most kamis have Guardian T1 (311=5, 312=5) maxed but 313 (Patience, +5 MUSU/hr HIB) at 1-4. **Highest priority: 313 → 5.**
- Once 313 is at 5, move to T2 Guardian: 322 (Vigor, often 4-5) and 323 (Armor, often 1-3). After Guardian T1+T2 fully maxed (15 SP), unlock T3: pick `332` Die Hard (SB −7.5%) for sustain.

## Priority 3 — Auto_v2 health check

`get_strategy_status(43, "bpeon")` — confirm healthy. As of session 71: 48h uptime, 0 restarts, 0% CPU. Strategy is rock-solid.

## Priority 4 — Side-quest passive checks (free reads only)

`check_quest_completable(3007)` — Move 500. Last check FALSE. No action while Q49 blocks acceptance.

Nothing else accept-able while Q49 holds.

## Stop conditions

- **Q49 cleared** (founder unblock OR cheap claim happens to flip it): `complete_quest(49)` → `accept_quest(50)` → recipe lookup in `catalogs/recipes.csv` for Ingot, then `craft_item` with current inventory (71 Scrap Metal + 686 Stone is plenty for an Ingot recipe). → Q51 (Give 1 Essence of Hearing — have 2). → Q52 (move to Cave Crossroads + Give 1 Ashlar — have 1).
- **Q49 still blocked, no founder reply**: confirm via tools, document, schedule +12h again.
- **Q49 still blocked, founder replied with non-immediate guidance**: schedule +6h to act on guidance.

## Reschedule

- Q49 cleared: +6h (active follow-up).
- Q49 still blocked, no founder reply: +12h.
- Q49 still blocked, founder replied: +6h.

## Inventory snapshot (end of session 71)

- MUSU: 489,431 (+14,554 from session 70). VIPP: 49,744.
- Patinated Pipe: 282 (+70). Cigarette Butt: 197 (+63). Cheeseburger: 100 (+12).
- Sanguine Shroom 29, Honeydew Scale 61, Dried Stems 367, Bone Chunk 115, Scrap Metal 71.
- Stone 686, Wooden Stick 206, Pine Cone 59, Plastic Bottle 11, Daffodil 8.
- Essence of Hearing × 2, Ashlar × 1 (pre-stocked for Q51, Q52 once Q49 unblocks).
- Pine Pollen 500, Essence of Daffodil 300, Black Poppy Extract 450, Sanguineous Powder 125, Resin Tincture 375.
- Ice Cream 78, Better Ice Cream 10, Rock Candyfloss 63 (stamina items for movement quests).
- Holy Dust 4 (for naming).
- Respec Potion 1, Booster Pack 13, Maple-Flavor Ghost Gum 1057.
- Node 15: 99 pts remainder (post-claim).

## Quest status

- Q1–Q48 ✓.
- Q49: ACCEPTED 2026-04-29 17:31 UTC. Catalog says DROPTABLE_ITEM_TOTAL[1018]≥15; inventory has **197 butts** (~13× target); `quest_state(49)` still returns `active_blocked / objs_not_met`. **REGISTRY-VS-CATALOG DRIFT — escalated to alerts.md, awaiting founder. 6 cumulative post-acceptance claims as of session 71.**
- Q50 (You Smelt It…): not accepted, gated behind Q49.
- Mina Q2014–Q2016: complete.
- Side: Q3007 (Move 500) accumulating passively.

## Quest graph (post-Q49)

Q47✓ → Q48✓ → **Q49 [BLOCKED, awaiting founder]** → Q50 (Craft 1 Ingot — recipe in catalogs/recipes.csv) → Q51 (Give 1 Essence of Hearing, have 2) → Q52 (Move to Cave Crossroads + Give 1 Ashlar, have 1) → ...

## Tools available (MCP)

- `quest_state(quest_index, account)` — discriminated state read with revert classification.
- `get_expected_objective(quest_index)` — catalog-expected objectives.
- `get_active_quests(account)` — owned/completed/truly_active counts.
- `scavenge_claim_and_reveal(node, account)` — used this session, ~1.87M gas for 145 tiers.
