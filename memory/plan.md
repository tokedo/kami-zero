# Plan for session 67

## Priority 1: Q49 (Community Service — Scavenge 15 Cigarette Butts @ node 15)

**Context**: Q49 accepted 2026-04-29 17:30 UTC. Auto_v2 on node 15 (Temple Cave, Scrap, 100/tier) since 03:14 UTC (now ~24h+ uptime by next session). Same Pipe Butt Burger droptable (44/44/11). Session 66 already banked +5 fresh butts via the Q48-clearing claim — Q49 baseline is 11, need 21+ for 15 fresh.

**Quest counter rule**: "Scavenge X" objectives reset per quest acceptance — only butts claimed from scavenge AFTER 17:30 UTC count toward Q49. Session 66's 5 butts came from the SAME claim that flushed Q48, so they were credited to Q49 (Q49 was accepted right after, but the claim happened pre-acceptance — risk: those 5 butts may NOT count). **Verify on next-session check_quest_completable**: if FALSE despite Butt inventory ≥21, the 5 from session 66 didn't count and we need 15 truly-fresh from a post-acceptance claim.

### Step 1 — Free reads
- `check_quest_completable(49)` — TRUE if 15+ butts claimed post-acceptance.
- `get_inventory` — track Butt (1018) delta from session-66 baseline 11. Need ≥26 (15 fresh) at minimum if session-66 butts didn't credit; ≥21 if they did.
- `get_account_kamis` — count HARVESTING vs RESTING. Expect ~10-15 cycled stops since 17:30 UTC.
- `get_scavenge_points(15)` — check accumulation. ≥2,300 pts (23 tiers, ~10 butts at 44%) is the trigger to claim if Q49 still FALSE.
- `get_strategy_status(43)` — container health.

### Step 2 — If Q49 not yet completable but ≥23 tiers at node 15
- `scavenge_claim_and_reveal(15)` — yields ~10 butts at 44%. Re-check Q49 completable.
- If TRUE post-claim: complete_quest(49), accept_quest(50). Q50 unknown — read game-data.md immediately to decide continuation strategy or migration.
- If still FALSE: another claim or wait longer cycle.

### Step 3 — If Q49 already TRUE
- complete_quest(49), accept_quest(50). Read Q50 objectives. Decide whether node 15 still serves the chain or new node needed.

### Step 4 — If Q49 FALSE and <23 tiers at node 15
- No claim. Reschedule +6h. Auto_v2 keeps grinding.

### Step 5 — Beyond Q49
- Read `integration/game-data.md` for Q50+ chain.
- Side-quest sweep: Q3007 (Move 500) only viable passive accumulator; check briefly.
- Audit unspent SP / unallocated levels (level-up routine).

## Priority 2: Standard level-up routine

**Routine** (per CLAUDE.md):
1. `get_kamis_progress_batch(<all 20>, "bpeon")` — read level, xp, investments.
2. For each RESTING kami with `xp >= levelCost(level)` (= `floor(40 * 1.259^(L-1))`), compute banked levels.
3. If ≥1 kami has banked levels, build `targets` list with `target_level` and `skill_plan`.
4. Submit `level_and_allocate_batch(targets, "bpeon")`.
5. Verify via `get_kamis_progress_batch`.

**Default skill plan: Guardian-leaning sustain (per CLAUDE.md).** For session 67, by-priority slots based on session-65 snapshot:
- 313 Patience (Guardian T1, +5 MUSU/hr HIB) — fill to 5 on the 6 kamis still <5: 10647, 11716, 13235, 13390, 13857.
- After 313 caps, top up 322 Vigor / 323 Armor (Guardian T2).
- Then 213 Good Constitution (Enlightened T1 +6% HFB).
- Avoid 332 Die Hard until respec window — most current kamis have 1 SP in 331 Anxiety; respec potion (1 in inventory) is the unlock.

**Skip leveling HARVESTING kamis** — wait for natural cycle stop.

## Quest status (post session 66)

- **Q31–Q48 ✓**.
- **Q49**: ACCEPTED 2026-04-29 17:30 UTC. Need 15 fresh Cigarette Butts via scavenge_claim post-acceptance. Inventory: 11 (5 from session-66 claim — may or may not count toward Q49 since the claim happened pre-acceptance).
- **Q50+**: gated behind Q49 — read on accept.
- **Q3007**: Move 500 — passive, FALSE last 5 sessions.
- **Q6**: Liquidate — deferred indefinitely.
- **Mina Q2014–Q2016**: ALL completed.

## Inventory highlights (end of session 66)

- MUSU: 444,149 (+1,121 vs session 65 — kami 3983 single cycle credit)
- VIPP: 49,744 (unchanged)
- **Patinated Pipe: 71** (+6 from session-66 claim; quest-target 5 cleared; 71 stable buffer for any future Pipe-tied recipes)
- **Cigarette Butt: 11** (+5 from session-66 claim; new baseline for Q49 counter)
- Cheeseburger: 60 (+1)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115
- Flash Talisman: 1
- Respec Potion: 1 (save for high-impact rebuild — likely T3 Guardian respec)
- Node 15: 17 pts remainder (post-claim)
- Node 16: 8,681 sticky scav (17 tiers, 7 sessions stable, no leak)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC.

## Roster level snapshot (post session 65 bootstrap; only kami 3983 cycled in session 66 with no level eligibility)

| Kami | Lvl | 313 | Note |
|------|-----|-----|------|
| 43 (Zephyr) | 37 | 1 | xp 138304 (waiting for L37→38 cost 159582) |
| 1064 | 35 | 1 | xp 9957 |
| 2553 | 38 | 4 | xp 19411 |
| 3874 | 38 | 5 (max) | xp 44177 |
| 3983 | 36 | 5 (max) | xp 40299 (+1,121 from cycle; build deviates 342/343) |
| 6096 | 38 | 5 (max) | xp 5014 |
| 7722 | 38 | 5 (max) | xp 42522 |
| 7803 | 37 | 4 | xp 90897 |
| 8745 | 37 | 4 | xp 99066 |
| 10011 | 35 | 1 | xp 6035 |
| 10647 | 34 | — | xp 59002 (313 = 0) |
| 11716 | 33 | — | xp 18498 |
| 12459 | 35 | 1 | xp 3674 |
| 13235 | 34 | — | xp 29078 |
| 13390 | 34 | — | xp 22063 |
| 13702 | 34 | 1 | xp 10868 |
| 13857 | 34 | — | xp 31628 |
| 13947 | 34 | 1 | xp 1054 |
| 14286 | 33 | 1 | xp 13340 |
| 14306 | 34 | 1 | xp 1117 |

(Banked levels on next session: depends on which of the 19 currently-HARVESTING kamis cycle. Most need substantial XP gains to bank a level — kamis nearest to L+1: 7803 +52k away, 8745 +44k, 43 +21k.)

## Lessons applicable

### Session 66 learnings
- **Plan Step 2 trigger threshold (12 tiers / 1,200 pts) was correctly calibrated.** Claim hit immediately on the threshold and yielded the exact 5-pipe minimum to clear Q48. Replicate this trigger pattern for Q49: 23 tiers / 2,300 pts.
- **Drop distribution at node 15 (n=12)**: 50% pipe / 42% butt / 8% burger. Empirics within RNG variance of expected 44/44/11.
- **Single-cycle MUSU credit at node 15**: kami 3983's first cycle = +1,121 MUSU. Per-kami per-cycle yields will compound across roster.

### Open question for session 67
- **Did session-66's 5 butts credit toward Q49?** Q49 was accepted ~5 seconds AFTER the scav claim that produced them. The on-chain quest counter logic determines this:
  - If counter checks "items in inventory at completion": YES, Butts 11 ≥ 15 needed... wait, Butts are at 11 (not 15) so this question is moot for now.
  - If counter checks "items received via QuestObjectiveOnScavenge event since acceptance": NO, the claim was pre-acceptance.
  - **Practical resolution**: in session 67, claim once more if ≥23 tiers, then check Q49. If FALSE despite Butt inventory ≥26, we know session-66's 5 didn't count — apply this rule to all future quest sequencing (always claim AFTER acceptance for newly-tracked items).

### Carried forward (still valid)
- **Quest-first**: Q49 is current MSQ gate.
- **Don't disturb auto_v2 to skip patience.** Force-flush gas budget ~76M for 20-kami wave only justified with hard deadline.
- **Post-migration HP regen is the rate-limiter**: budget 14-18h to first flush.
- **YieldIndex=2 nodes yield VIPP not MUSU**: node 15 is YieldIndex=1 (MUSU).
- **Scav 1:1 invariant holds**, matches the node's yield token.
- **Inventory existing items DO NOT count for "Scavenge X" quest objectives.**
- **stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.**
- **Travel `dry_run=True` first.**
- **Q3009-Q3014 already completed**: skip in side-quest sweep.
- **`get_kami_state_slim` omits level/experience** — use `get_kamis_progress_batch` for level-up perception.

## Quest graph (MSQ critical path)

Q31✓→...→Q47✓→Q48✓→**Q49 (Community Service — 15 Cigarette Butts @ node 15)** → Q50+ (unknown, read on Q50 accept).
