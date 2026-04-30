# Plan for session 71

## Priority 0 — Read alerts.md FIRST

Founder may have replied with off-chain Q49 objective inspection. If so: act on their guidance directly. Possible founder responses:
- **Q49 objective is X (not what catalog says)** → run the matching action (e.g., burn, scavenge at different node, give to NPC). Re-test.
- **Q49 is structurally broken — drop it** → call `drop_quest(49, "bpeon")` and either re-accept or skip to Q50 directly via founder-provided escape path.
- **Catalog is correct but registry mis-deployed — wait for redeploy** → continue auto_v2 grind, no Q49 action.

If no founder reply: continue with the hold pattern below.

## Priority 1 — Q49 hold pattern (no force-flush, no hypothesis testing)

The new `quest_state` + `get_expected_objective` tools should now be live in MCP (server was restarted between session 70 and 71 by cron's invocation pattern). Use them:

1. `quest_state(49, "bpeon")` — should still return `state="active_blocked"`, `revert_kind="objs_not_met"`. If state changed (e.g., `active_ready`), proceed to complete.
2. `get_expected_objective(49)` — re-confirm catalog says `DROPTABLE_ITEM_TOTAL[1018] ≥ 15`. (If founder corrected the catalog, this will surface the change.)
3. `get_inventory("bpeon")` — confirm Cigarette Butt (1018) count. Last-known: 134.
4. `get_scavenge_points(15, "bpeon")` — if ≥100 pts (1+ tier from natural cycling, NO force-flush), do ONE `scavenge_claim_and_reveal(15)` (~1.76M gas) as a low-cost data point. Re-check Q49 via `quest_state(49)`. **Stop after one claim regardless** — discipline rule still applies.
5. **Do NOT force-flush. Do NOT test alternate hypotheses.** Catalog says ≥15 butts; we have 134. Chain says no. That's escalation territory.

## Priority 2 — Standard level-up routine

Read `get_account_kamis("bpeon")` first. For every RESTING kami, call `get_kamis_progress_batch([all_resting_kami_ids])`. Eligibility:

- `level` ≥ 33 and `xp ≥ levelCost(level)` where `levelCost(L) = floor(40 * 1.259^(L-1))`.
- Reference table for current roster levels (33-38):
  - L33→34: ~63,428 XP
  - L34→35: ~79,856
  - L35→36: ~100,540
  - L36→37: ~126,580
  - L37→38: ~159,364
  - L38→39: ~200,600

Session 70 found zero banked levels across 11 RESTING kamis. The 9 currently HARVESTING (13702, 13857, 3874, 7722, 10647, 11716, 13947, 14286, 14306) will likely cycle into RESTING with longer harvest XP — most likely candidate for banked levels next session.

For each kami with banked levels, use `level_and_allocate_batch`. Default skill plan per CLAUDE.md: Guardian-leaning sustain.

- Most kamis have Guardian T1 (311=5, 312=5) maxed but 313 (Patience, +5 MUSU/hr HIB) at 1-4. **Highest priority: 313 → 5.**
- Once 313 is at 5, move to T2 Guardian: 322 (Vigor) and 323 (Armor). Most kamis already at 322=4-5, 323=2-3.
- After Guardian T1+T2 fully maxed (15 SP), unlock T3: pick `332` Die Hard (SB −7.5%) for sustain.
- Kami 43 "Zephyr" is at L37 with 139,934 XP — needs ~19,500 more XP for L38. Likely to be the first kami with a banked level next session.

## Priority 3 — Auto_v2 health check

`get_strategy_status(43, "bpeon")` — confirm `health: "healthy"`, `restarts: 0`. If unhealthy or strategy gone, restart with the same config (20 kamis, node 15, REST, 5% safety). Note: 36h uptime as of session 70 — auto_v2 has been remarkably stable.

## Priority 4 — Side-quest passive checks (free reads only)

`check_quest_completable(3007)` — Move 500. Passively accumulates from any movement; no need to grind. Last check: FALSE.

Nothing else accept-able while Q49 holds.

## Stop conditions

- Q49 cleared (founder unblock OR cheap claim happens to flip it): complete_quest(49) → accept_quest(50) → if you have 1+ Scrap Metal + Stone (you do: 71 + 686), check `craft_item(recipe_index=?)` for Ingot. The catalog's recipes.csv will show the recipe index. Then complete Q50 → accept Q51 (Give 1 Essence of Hearing — you have 2). Then Q52 (move to Cave Crossroads + Give 1 Ashlar — you have 1).
- Q49 still blocked: confirm via tools, document in decisions.md, schedule +12h.

## Reschedule

- Q49 cleared: +6h (active follow-up).
- Q49 still blocked, no founder reply: +12h.
- Q49 still blocked, founder replied with non-immediate guidance: +6h to act on guidance.

## Inventory snapshot (end of session 70 / start of session 71 — no inventory changes)

- MUSU: 474,877. VIPP: 49,744.
- Patinated Pipe: 212. Cigarette Butt: 134. Cheeseburger: 88.
- Sanguine Shroom 29, Honeydew Scale 61, Dried Stems 367, Bone Chunk 115, Scrap Metal 71.
- Stone 686, Wooden Stick 206, Pine Cone 59, Plastic Bottle 11, Daffodil 8.
- Essence of Hearing × 2, Ashlar × 1 (pre-stocked for Q51, Q52 once Q49 unblocks).
- Pine Pollen 500, Essence of Daffodil 300, Black Poppy Extract 450, Sanguineous Powder 125, Resin Tincture 375.
- Ice Cream 78, Better Ice Cream 10, Rock Candyfloss 63 (stamina items for movement quests).
- Holy Dust 4 (for naming).
- Respec Potion 1, Booster Pack 13.
- Node 15: 45 pts remainder.

## Quest status

- Q1–Q48 ✓.
- Q49: ACCEPTED 2026-04-29 17:31 UTC. Catalog says DROPTABLE_ITEM_TOTAL[1018]≥15; inventory has 134 butts (~9× target); `quest_state(49)` still returns `active_blocked / objs_not_met`. **REGISTRY-VS-CATALOG DRIFT — escalated to alerts.md, awaiting founder.**
- Q50 (You Smelt It…): not accepted, gated behind Q49.
- Mina Q2014–Q2016: complete.
- Side: Q3007 (Move 500) accumulating passively.

## Quest graph (post-Q49)

Q47✓ → Q48✓ → **Q49 [BLOCKED, awaiting founder]** → Q50 (Craft 1 Ingot — recipe in catalogs/recipes.csv) → Q51 (Give 1 Essence of Hearing, have 2) → Q52 (Move to Cave Crossroads + Give 1 Ashlar, have 1) → ...

## New tools available (MCP, post-restart)

- `quest_state(quest_index, account)` — discriminated state read with revert classification.
- `get_expected_objective(quest_index)` — catalog-expected objectives.
- `get_active_quests(account)` — now reports owned/completed/truly_active counts.

Note: if MCP transport hasn't picked up the new tools yet (server-restart timing), reach them via `executor/.venv/bin/python -c "import sys; sys.path.insert(0,'.'); import server; print(server.quest_state(49,'bpeon'))"` from a Bash call. Same pattern works for any tool defined in server.py.
