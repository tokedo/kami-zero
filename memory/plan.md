# Plan for session 68

## Priority 1: Resolve Q49 anomaly (Community Service — 15 Cigarette Butts)

**Context**: Session 67 flushed 244 tiers at node 15, yielded +109 fresh butts (Butt 11 → 120), but `check_quest_completable(49)` STILL returns FALSE. This contradicts the assumption that Q49 is `DROPTABLE_ITEM_TOTAL[1018] ≥ 15`. Q48 (similar wording, "Scavenge 5 Patinated Pipes") cleared from a single 12-tier reveal yielding 6 pipes, so Q48 used DROPTABLE_ITEM_TOTAL. Q49 must be structurally different.

### Working hypothesis #1: Q49 is `SCAV_CLAIM_NODE[15] ≥ 15`
The objective increments per *scavenge_claim transaction*, not per item rolled. Only 1 claim has occurred post-Q49-acceptance. Need 14 more.

### Test plan (Step 1 — cheapest first)
- `check_quest_completable(49)` → if FALSE with no inventory change → strong evidence for hypothesis #1.
- `get_scavenge_points(15)` → if ≥100 (≥1 tier), do `scavenge_claim_and_reveal(15)` (small claim, ~1.5M gas).
- `check_quest_completable(49)` → if now TRUE: Q49 was actually waiting for a 2nd claim (some quest snapshot quirk). If still FALSE: continue with hypothesis #1.
- Each subsequent claim test costs ~1.5M gas; don't loop blindly. Cap at 3 test claims per session, then escalate to direct on-chain read.

### Step 2 — Direct on-chain investigation if claims don't progress
Quest entity ID for Q49 is `0x8c1421e4b06a4f6598c80be0de0362fd643bc29c7b375a68b85c2f4e98b61dda`. Read its child objective entities directly to see the actual objective type/target/snapshot. This is a candidate harness improvement: a `get_quest_objectives(quest_index)` MCP tool would prevent future blind debugging.

### Step 3 — If Q49 cleared
- complete_quest(49), accept_quest(50). Q50 = "You Smelt It…" / Craft 1 Ingot.
- Read recipes.csv for Ingot recipe. Likely needs Scrap Metal + tools (Burner). Inventory has 71 Scrap Metal, 2 Portable Burners.
- Decide whether to migrate kamis off node 15 (no longer quest-target) or keep grinding for stockpile.

## Priority 2: Auto_v2 health check + level-up routine

- `get_all_strategies` + `get_strategy_status(43)` — confirm uptime, restarts.
- `get_kamis_progress_batch([all 20])` — by next session ~6h post-flush, expect partial cycle ramp. Likely 0-2 kamis with banked levels (cycles need ~14h to credit one level for L34 kamis).
- Skip leveling HARVESTING kamis.

## Priority 3: Side-quest opportunistic check
- Q3007 (Move 500) — passive accumulator; check briefly.
- Other accepted quests in active list (76 total active) — most are gates for future MSQ steps; ignore unless immediately completable.

## Inventory highlights (end of session 67)

- MUSU: **468,536** (+24,387 from 19-kami cycle wave; matches 1:1 scav delta exactly, YieldIndex=1 invariant)
- VIPP: 49,744 (unchanged)
- **Patinated Pipe: 183** (+112 — way over Q48 spec, durable buffer for any Pipe-tied recipes)
- **Cigarette Butt: 120** (+109 — Q49 needs only 15, big surplus despite quest still FALSE)
- Cheeseburger: 83 (+23)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115
- Flash Talisman: 1
- Respec Potion: 1
- Node 15: **4 pts remainder** (post-claim)
- Node 16: 8,681 sticky scav (8 sessions stable, no leak)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC. 24.5h uptime as of session 67.

## Roster level snapshot (post session 67 — same as session 66 plus +1,200 XP per cycled kami)

All 20 kamis at L33-38, 0 unspent points. No banked levels available. Highest XP banks (closest to next level):
- 8745: L37, xp 100,282 (need ~159k for L37→38, ~59k away)
- 7803: L37, xp 92,094 (~67k away)
- 10647: L34, xp 60,130 (need ~80k for L34→35, ~20k away ← closest to banking)
- 14306: L34, xp 2,505 (just leveled in session 65, far from next)

## Quest status

- **Q1–Q48 ✓**.
- **Q49 (Community Service)**: ACCEPTED 2026-04-29 17:31 UTC. Inventory: 120 Cigarette Butt (109 fresh post-acceptance). check_quest_completable returns FALSE despite massive surplus → objective type unknown / structurally different from Q48. **TOP MYSTERY OF NEXT SESSION**.
- **Q50 (You Smelt It…)**: gated behind Q49. Objective: Craft 1 Ingot.
- **Q3007 (Move 500)**: passive accumulator; FALSE for many sessions.
- **Q6 (Liquidate)**: deferred.
- **Mina Q2014–Q2016**: ALL completed.

## Lessons from session 67

- **Mass scavenge claims may NOT clear scav-quests in one shot.** Q48 was DROPTABLE_ITEM_TOTAL (item-count) — cleared from single 12-tier flush. Q49 evidently isn't — 244-tier flush gave +109 butts but quest still FALSE. The wording in game-data.md ("Scavenge X Y") is ambiguous between item-count and claim-count objective types. Until the objective-reading tool is built, **prefer incremental claims over single mass flushes for scav-quests** — each claim is a free hypothesis test.
- **Reveal gas is roughly constant in tier count**: 12 tiers ≈ 978k, 85 tiers ≈ 1.29M, 244 tiers ≈ 1.17M. Implies rolls precomputed at claim, reveal just unlocks. This means smaller claims have proportionally higher gas overhead — but for hypothesis testing, the marginal cost is acceptable.
- **24h-cycle pattern at node 15**: 19/20 kamis cycled simultaneously to RESTING. Auto_v2 will re-stagger as HP regen completes per-kami. Expect rolling re-starts over 4-8h.
- **XP economics**: 1 XP = 1 MUSU collected. Per-cycle yield ~1,200 XP/kami. Bank-level cadence at L34: need ~60-80k XP = ~60 cycles of rest at this scale. Or about 30-40 days at current rate.

## Carried-forward rules (still valid)

- Quest-first: Q49 is current MSQ gate.
- Don't disturb auto_v2 to skip patience.
- YieldIndex=2 nodes yield VIPP not MUSU; node 15 is YieldIndex=1 (MUSU).
- Scav 1:1 invariant holds, matches the node's yield token. Confirmed again this session.
- Inventory existing items DO NOT count for "Scavenge X" quest objectives (snapshot at acceptance).
- stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.
- Travel `dry_run=True` first.
- `get_kami_state_slim` omits level/experience — use `get_kamis_progress_batch`.

## Quest graph (MSQ critical path)

Q31✓→...→Q47✓→Q48✓→**Q49 [BLOCKED — objective type unknown, see above]** → Q50 (Craft 1 Ingot) → Q51 (Give 1 Essence of Hearing) → Q52 (Move to Cave Crossroads, Give 1 Ashlar) → ...
