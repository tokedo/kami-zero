# Plan for session 64

## Priority 0: Q48 (Pipe Dream — Scavenge 5 Patinated Pipes @ node 15)

**Context**: Q48 accepted 2026-04-29 03:09 UTC. Auto_v2 on node 15 (Temple Cave, Scrap, 100/tier) since 03:14 UTC. Droptable "Pipe Butt Burger": 44% Pipe, 44% Butt, 11% Cheeseburger. Same node serves Q49 (15 Butts).

**Quest counter rule (session 63 confirmed)**: "Scavenge X" objectives reset per quest acceptance — existing inventory does NOT count. Need 5 fresh pipes from scavenge_claim_and_reveal calls AFTER Q48 was accepted.

### Step 1 — Free reads
- `check_quest_completable(48)` — TRUE only if 5+ pipes claimed from node 15 since 03:09 UTC.
- `get_inventory` — track Patinated Pipe (1017) delta from baseline 65; Cigarette Butt (1018) baseline 6.
- `get_account_kamis` — count HARVESTING vs RESTING.
- `get_scavenge_points(15)` — node 15 accumulation. ≥1,200 pts = 12 tiers ≈ 5 pipes expected.
- `get_strategy_status(43)` — container health.

### Step 2 — If Q48 not yet completable but ≥12 tiers at node 15
- `scavenge_claim_and_reveal(15)` — likely yields 5+ pipes. Re-check Q48 completable.
- If TRUE post-claim: complete_quest(48), accept_quest(49) ("Community Service": 15 Cigarette Butts).
- Q49 needs ~34 tiers at 44% — keep auto_v2 grinding, claim again later.

### Step 3 — If Q48 already TRUE (2+ kamis cycled at node 15)
- complete_quest(48), accept_quest(49). Continue grinding at same node.

### Step 4 — If Q48 FALSE and <12 tiers at node 15
- No action; reschedule +6h. Standard "wait for ramp" — at fresh node, first cycle stop ~12-18h post-migration. Mig was 03:14 UTC; first stop expected ~17:00-21:00 UTC.

### Step 5 — Beyond Q48
- Read game-data.md for Q50+ (after Q49 chain). Decide whether node 15 still serves the chain or needs new migration.
- Side-quest sweep: Q3007 (Move 500) only viable passive accumulator; check briefly.

## Quest status (post session 63)

- **Q31–Q47 ✓**.
- **Q48**: ACCEPTED 2026-04-29 03:09 UTC. Auto_v2 on node 15 since 03:14 UTC. Need 5 fresh Patinated Pipes via scavenge_claim post-acceptance.
- **Q49**: gated behind Q48 — "Community Service" = 15 Cigarette Butts (same node 15 droptable).
- **Q3007**: Move 500 — passive, FALSE last 4 sessions.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 63)

- MUSU: 443,028 (UNCHANGED — node 18 yields VIPP not MUSU; explained at last)
- VIPP: 49,744 (+15,983 from 14 stops at node 18)
- Patinated Pipe: 65 (BASELINE for Q48 fresh-counter — inventory pre-existing)
- Cigarette Butt: 6 (BASELINE for Q49 fresh-counter)
- Sanguine Shroom: 29 (+27 from 85-tier node-18 claim)
- Honeydew Scale: 61 (+9), Dried Stems: 367 (+48), Bone Chunk: 115 (unchanged)
- Flash Talisman: 1 (NEW, from node 18 claim)
- Node 18: 116 remainder pts (no leak risk; below 200/tier cost)
- Node 16: 8,681 sticky scav (17 tiers, 6 sessions stable)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC.

## Lessons applicable

### Session 63 learnings
- **YieldIndex=2 nodes yield VIPP not MUSU**. Node 18 = YieldIndex=2 (game-data.md line 283). Other yield-2 nodes: 60, 61, 62, 63, 65, 73, 75, 79, 83, 88. Always read yield token BEFORE interpreting "MUSU unchanged" as a bug.
- **Scav 1:1 invariant DOES hold**: matches the node's yield token, not always MUSU.
- **"Scavenge X" quests use per-acceptance counter**: existing inventory does not count. Pipe count of 65 didn't satisfy Q48; need 5 fresh from post-acceptance scavenge_claim calls.
- **Single-droptable 2-quest combo nodes**: nodes 15/59 (Pipe Butt Burger droptable) drop both Q48 (Pipe) and Q49 (Butt) at 44% each — single grind clears two quests.
- **Migration timing peak-extraction rule**: catching kamis with 7-15h elapsed cycles before migration = max scav credit at OLD node. Session 63 captured +49 free tiers from optimal stop-batch timing.

### Carried forward (still valid)
- **Quest-first**: Q48 is current MSQ gate.
- **Don't disturb auto_v2 to skip patience.** Force-flush gas budget rule (~76M for 20-kami wave) only justified with hard deadline.
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **Slim API harvest entity is stale post-migration**: kami room and harvest-node desync after stop until auto_v2's first harvest_start. Use get_account_kamis state field for ground truth.
- **Q3009-Q3014 already completed**: skip in side-quest sweep.

## Quest graph (MSQ critical path)

Q31✓→...→Q46✓→Q47✓→**Q48 (Pipe Dream — 5 Patinated Pipes @ node 15, ~12 tiers)** → Q49 (Community Service — 15 Cigarette Butts @ same node 15, ~34 tiers) → Q50+ (unknown, read on Q49 accept).
