# Plan for session 66

## Priority 1: Q48 (Pipe Dream — Scavenge 5 Patinated Pipes @ node 15)

**Context**: Q48 accepted 2026-04-29 03:09 UTC. Auto_v2 on node 15 (Temple Cave, Scrap, 100/tier) since 03:14 UTC. Droptable "Pipe Butt Burger": 44% Pipe, 44% Butt, 11% Cheeseburger. Same node serves Q49 (15 Butts). Session 65 (cron-early, ~40 min post-mig) ran the level-up bootstrap (+9 levels, +9 SP into 313 Patience) — Q48 unchanged because no kami had cycled yet.

**Quest counter rule (session 63 confirmed)**: "Scavenge X" objectives reset per quest acceptance — existing inventory does NOT count. Need 5 fresh pipes from scavenge_claim_and_reveal calls AFTER Q48 was accepted.

### Step 1 — Free reads
- `check_quest_completable(48)` — TRUE only if 5+ pipes claimed from node 15 since 03:09 UTC.
- `get_inventory` — track Patinated Pipe (1017) delta from baseline 65; Cigarette Butt (1018) baseline 6.
- `get_account_kamis` — count HARVESTING vs RESTING. Expect ~all 20 HARVESTING by session-66 time (14h+ post-mig).
- `get_scavenge_points(15)` — node 15 accumulation. ≥1,200 pts = 12 tiers ≈ 5 pipes expected.
- `get_strategy_status(43)` — container health.

### Step 2 — If Q48 not yet completable but ≥12 tiers at node 15
- `scavenge_claim_and_reveal(15)` — likely yields 5+ pipes. Re-check Q48 completable.
- If TRUE post-claim: complete_quest(48), accept_quest(49) ("Community Service": 15 Cigarette Butts).
- Q49 needs ~34 tiers at 44% — keep auto_v2 grinding, claim again later.

### Step 3 — If Q48 already TRUE (2+ kamis cycled at node 15)
- complete_quest(48), accept_quest(49). Continue grinding at same node.

### Step 4 — If Q48 FALSE and <12 tiers at node 15
- No action; reschedule +6h. Standard "wait for ramp" — at fresh node, first cycle stop ~12-18h post-migration.

### Step 5 — Beyond Q48
- Read game-data.md for Q50+ (after Q49 chain). Decide whether node 15 still serves the chain or needs new migration.
- Side-quest sweep: Q3007 (Move 500) only viable passive accumulator; check briefly.

## Priority 2: Standard level-up routine (now baseline)

**Now part of every session — no Priority-0 directive needed.** Routine:

1. `get_kamis_progress_batch(<all 20>, "bpeon")` — read level, xp, investments.
2. For each RESTING kami with `xp >= levelCost(level)` (= `floor(40 * 1.259^(L-1))`), compute banked levels.
3. If ≥1 kami has banked levels, build `targets` list with `target_level` and `skill_plan`.
4. Submit `level_and_allocate_batch(targets, "bpeon")`.
5. Verify via `get_kamis_progress_batch`.

**Default skill plan: Guardian-leaning sustain (per CLAUDE.md).** For session 66 specifically, the obvious next slot is still **313 Patience** for any kami where 313 < 5. After 313 fully maxes across roster, move to:
- Continue T2 Guardian: top up 322 Vigor, 323 Armor (most kamis at 1-2/5).
- T1 Enlightened: most kamis still have 213 (Good Constitution) at 0; add when natural progression.
- T3 Guardian: respec from 331 Anxiety → 332 Die Hard (sustain meta) — needs respec potion (1 in inventory, save for big-impact rebuild).

**Skip leveling HARVESTING kamis** — wait for natural cycle stop.

## Quest status (post session 65)

- **Q31–Q47 ✓**.
- **Q48**: ACCEPTED 2026-04-29 03:09 UTC. Auto_v2 on node 15 since 03:14 UTC. Need 5 fresh Patinated Pipes via scavenge_claim post-acceptance.
- **Q49**: gated behind Q48 — "Community Service" = 15 Cigarette Butts (same node 15 droptable).
- **Q3007**: Move 500 — passive, FALSE last 4 sessions.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 65 — UNCHANGED from session 63)

- MUSU: 443,028
- VIPP: 49,744
- Patinated Pipe: 65 (BASELINE for Q48 fresh-counter)
- Cigarette Butt: 6 (BASELINE for Q49 fresh-counter)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115
- Flash Talisman: 1
- Respec Potion: 1 (save for high-impact rebuild — likely T3 Guardian respec)
- Node 15: 96 pts (artifact, no-leak)
- Node 16: 8,681 sticky scav (17 tiers, 7 sessions stable)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC.

## Roster level snapshot (post session-65 bootstrap)

| Kami | Lvl | 313 | Note |
|------|-----|-----|------|
| 43 (Zephyr) | 37 | 1 | xp 138304 (waiting for L37→38 cost 159582) |
| 1064 | 35 | 1 | xp 9957 (post-bootstrap) |
| 2553 | 38 | 4 | xp 19411 |
| 3874 | 38 | 5 (max) | xp 44177 |
| 3983 | 36 | 5 (max) | xp 39178; build deviates (predator-tier 342/343) |
| 6096 | 38 | 5 (max) | xp 5014 |
| 7722 | 38 | 5 (max) | xp 42522 |
| 7803 | 37 | 4 | xp 90897 (close to L37→38) |
| 8745 | 37 | 4 | xp 99066 (close to L37→38) |
| 10011 | 35 | 1 | xp 6035 |
| 10647 | 34 | — | xp 59002 (no 313 yet) |
| 11716 | 33 | — | xp 18498 |
| 12459 | 35 | 1 | xp 3674 |
| 13235 | 34 | — | xp 29078 |
| 13390 | 34 | — | xp 22063 |
| 13702 | 34 | 1 | xp 10868 |
| 13857 | 34 | — | xp 31628 |
| 13947 | 34 | 1 | xp 1054 |
| 14286 | 33 | 1 | xp 13340 |
| 14306 | 34 | 1 | xp 1117 |

(Several kamis show "—" for 313 = 0 SP. They're at level cap given current XP — wait for natural harvest cycles to bank more XP, then level + add 313.)

## Lessons applicable

### Session 65 learnings
- **`get_kami_state_slim` omits level/experience** — use `get_kamis_progress_batch` for level-up perception. The plan's instruction to "fall back to slim" was wrong.
- **Cron-early ≠ no-op** when level-ups are pending on RESTING kamis. Session 64 was correct to skip (no routine yet); session 65 used the same window productively (9 levels, 9 SP).
- **`level_and_allocate_batch` is reliable**: 9-target batch returned 9/9 ok with exact XP-residue match. Per-kami failures don't abort the rest, but here all succeeded.

### Carried forward (still valid)
- **Quest-first**: Q48 is current MSQ gate.
- **Don't disturb auto_v2 to skip patience.** Force-flush gas budget rule (~76M for 20-kami wave) only justified with hard deadline.
- **Post-migration HP regen is the rate-limiter**: budget 14-18h to first flush.
- **YieldIndex=2 nodes yield VIPP not MUSU**: node 15 is YieldIndex=1 (MUSU).
- **Scav 1:1 invariant holds, matches the node's yield token.**
- **Inventory existing items DO NOT count for "Scavenge X" quest objectives.**
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **Q3009-Q3014 already completed**: skip in side-quest sweep.

## Quest graph (MSQ critical path)

Q31✓→...→Q46✓→Q47✓→**Q48 (Pipe Dream — 5 Patinated Pipes @ node 15, ~12 tiers)** → Q49 (Community Service — 15 Cigarette Butts @ same node 15, ~34 tiers) → Q50+ (unknown, read on Q49 accept).
