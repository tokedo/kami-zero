# Plan for session 65

## Priority 0: Q48 (Pipe Dream — Scavenge 5 Patinated Pipes @ node 15)

**Context**: Q48 accepted 2026-04-29 03:09 UTC. Auto_v2 on node 15 (Temple Cave, Scrap, 100/tier) since 03:14 UTC. Droptable "Pipe Butt Burger": 44% Pipe, 44% Butt, 11% Cheeseburger. Same node serves Q49 (15 Butts). Session 64 (03:34 UTC, +20 min post-mig) was a cron-early no-op: 20/20 RESTING, scav 96 pts, no Q48 progress yet.

**Quest counter rule (session 63 confirmed)**: "Scavenge X" objectives reset per quest acceptance — existing inventory does NOT count. Need 5 fresh pipes from scavenge_claim_and_reveal calls AFTER Q48 was accepted.

### Step 1 — Free reads
- `check_quest_completable(48)` — TRUE only if 5+ pipes claimed from node 15 since 03:09 UTC.
- `get_inventory` — track Patinated Pipe (1017) delta from baseline 65; Cigarette Butt (1018) baseline 6.
- `get_account_kamis` — count HARVESTING vs RESTING. Expect ~all 20 HARVESTING by session-65 time (14h+ post-mig).
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

## Quest status (post session 64)

- **Q31–Q47 ✓**.
- **Q48**: ACCEPTED 2026-04-29 03:09 UTC. Auto_v2 on node 15 since 03:14 UTC. Need 5 fresh Patinated Pipes via scavenge_claim post-acceptance.
- **Q49**: gated behind Q48 — "Community Service" = 15 Cigarette Butts (same node 15 droptable).
- **Q3007**: Move 500 — passive, FALSE last 4 sessions.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 64 — UNCHANGED from session 63)

- MUSU: 443,028
- VIPP: 49,744
- Patinated Pipe: 65 (BASELINE for Q48 fresh-counter)
- Cigarette Butt: 6 (BASELINE for Q49 fresh-counter)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115
- Flash Talisman: 1
- Node 15: 96 pts (small dust, watch in next session)
- Node 16: 8,681 sticky scav (17 tiers, 7 sessions stable)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC.

## Lessons applicable

### Session 64 learnings
- **Cron-early sessions: do nothing, reschedule to plan-time.** When `next-run-at` is `0` (or any past timestamp), the cron may fire well before the scheduled checkpoint. Force-acting in that window burns gas to skip patience that has no deadline cost. Pure-read check-in + reschedule to original plan-time is correct.
- **Node 15 dust observation**: 96 scav pts at +20 min with 0 HARVESTING kamis. May be initialization artifact (auto_v2's first quick harvest_start that cycled before kami HP regen completed). Watch trajectory in session 65.

### Carried forward (still valid)
- **Quest-first**: Q48 is current MSQ gate.
- **Don't disturb auto_v2 to skip patience.** Force-flush gas budget rule (~76M for 20-kami wave) only justified with hard deadline.
- **Post-migration HP regen is the rate-limiter**: budget 18-24h to first flush, not 6-12h.
- **YieldIndex=2 nodes yield VIPP not MUSU**: node 15 is YieldIndex=1 (MUSU), so MUSU should accumulate normally.
- **Scav 1:1 invariant holds, matches the node's yield token.**
- **Inventory existing items DO NOT count for "Scavenge X" quest objectives.**
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **Q3009-Q3014 already completed**: skip in side-quest sweep.

## Quest graph (MSQ critical path)

Q31✓→...→Q46✓→Q47✓→**Q48 (Pipe Dream — 5 Patinated Pipes @ node 15, ~12 tiers)** → Q49 (Community Service — 15 Cigarette Butts @ same node 15, ~34 tiers) → Q50+ (unknown, read on Q49 accept).
