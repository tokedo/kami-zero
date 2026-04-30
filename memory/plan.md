# Plan for session 69

## Priority 1: Continue Q49 SCAV_CLAIM_NODE hypothesis testing

**Status post session 68**: Q49 remains FALSE. Two objective-type hypotheses empirically ruled out this session:
- **DROPTABLE_ITEM_TOTAL[1018] ≥ 15** — 109+ butts scavenged post-acceptance across sessions 66-68. Disproven.
- **ITEM_BURN[1018] ≥ 15** — burned 15 butts in two tx (1 + 14) this session. Q49 still FALSE. Disproven.

**Remaining lead**: `SCAV_CLAIM_NODE[15] ≥ N` (likely N=15). Currently at 3 separate claim transactions post-acceptance (sessions 66/67/68 each contributed 1). Need to accumulate more claim tx to test.

### Test plan
1. `check_quest_completable(49)` (free baseline).
2. `get_scavenge_points(15)` — if ≥100 (1+ tier), do `scavenge_claim_and_reveal(15)`. Re-check Q49. Each claim ~1.76M gas. **Cap at 3 small claims per session (~5.3M gas) to stay within budget.**
3. After 3 claims this session (cumulative 6 post-acceptance), if Q49 still FALSE: document the deadlock, write `memory/alerts.md` flag for human review (we may need someone to read the quest registry off-VM), and downshift to non-blocking work.

### Alternative path: harness-level objective reading

`component.id.parent` (hash `0xbca01f99…`) is in `integration/ids/components.json` but **does not resolve via `world.components()`** — `_resolve_component` raises "Component not found on-chain". `debug_traceCall` is also unavailable on this RPC. Direct objective-config reading is currently blocked.

Candidate next step (low priority unless Q49 blockade lasts ≥3 more sessions): explore alternative traversal paths to map quest entity → objective entities. Options to research:
- Indexer/explorer queries (off-chain GraphQL, if any) that pre-compute parent links.
- Reading `MudCompPushdownRegistry` or other component metadata to find which holder component links objectives.
- Parsing system code from open source MUD repos for the actual objective-creation pattern.

If a working path is found → build `get_quest_objectives(quest_index)` MCP tool and document.

## Priority 2: Auto_v2 health + level-up routine

- `get_all_strategies` + `get_strategy_status(43)` — confirm uptime/restarts (was 30h+ last session, 0 restarts).
- `get_kamis_progress_batch([all 20])` — by next session ~36h post-migration. With ~14h cycle cadence, expect 1-3 kamis with banked L34→L35 by now (10647 was closest at 60.1k/~80k needed).
- Level any RESTING kami with banked levels using `level_and_allocate_batch`. Skill plan: Guardian-leaning sustain (see CLAUDE.md). Skip HARVESTING kamis.

## Priority 3: Side-quest opportunistic check
- Q3007 (Move 500) — passive accumulator; check briefly.
- Other accepted quests in active list (76 total) — most are gates for future MSQ steps; ignore unless immediately completable.

## Inventory highlights (end of session 68)

- MUSU: **469,669** (basically unchanged from session 67 — auto_v2 mid-ramp post-flush, no new cycle stops)
- VIPP: 49,744 (unchanged)
- **Patinated Pipe: 184** (Q48 satisfied; durable buffer for any Pipe-tied recipes)
- **Cigarette Butt: 114** (was 120; -15 from burns, +9 from session 68 claim. Quest still demands 15 fresh — supply not the issue)
- Cheeseburger: 84 (+1)
- Sanguine Shroom: 29, Honeydew Scale: 61, Dried Stems: 367, Bone Chunk: 115
- Flash Talisman: 1
- Respec Potion: 1
- Node 15: **37 pts remainder** (post-claim)

## Active strategies

- **auto_v2 on node 15 (Temple Cave, Scrap)** — 20 kamis, REST regen, 5% safety, bountyCollectThreshold 10000. Strategy ID `48e08f68-4bd3-4d4b-8d27-f4ed5a5ca017`. Started 2026-04-29 03:14 UTC. ~31h uptime as of session 68.

## Quest status

- **Q1–Q48 ✓**.
- **Q49 (Community Service)**: ACCEPTED 2026-04-29 17:31 UTC. Inventory: 114 Butts. **Still FALSE despite 109 fresh scavenged + 15 burned**. Lead hypothesis: SCAV_CLAIM_NODE[15]≥15 (3 of 15 done).
- **Q50 (You Smelt It…)**: gated behind Q49. Objective: Craft 1 Ingot.
- **Q3007 (Move 500)**: passive accumulator; FALSE for many sessions.
- **Q6 (Liquidate)**: deferred.
- **Mina Q2014–Q2016**: ALL completed.

## Carried-forward rules (still valid)

- Quest-first: Q49 is current MSQ gate.
- Don't disturb auto_v2 to skip patience.
- YieldIndex=2 nodes yield VIPP not MUSU; node 15 is YieldIndex=1 (MUSU).
- Scav 1:1 invariant holds, matches the node's yield token.
- Inventory existing items DO NOT count for "Scavenge X" quest objectives (snapshot at acceptance).
- stop_harvest_batch: max ~5 per batch, silent-skip detection in harness.
- Travel `dry_run=True` first.
- `get_kami_state_slim` omits level/experience — use `get_kamis_progress_batch`.

## Lessons from session 68

- **"Scavenge X" wording is ambiguous in this game's quest schema.** Q48 cleared from a 12-tier flush yielding 6 pipes (DROPTABLE_ITEM_TOTAL[1017]). Q49's wording is structurally identical but objective type is NOT DROPTABLE_ITEM_TOTAL. Two more types ruled out empirically: ITEM_BURN, and (already known) DROPTABLE_ITEM_TOTAL. SCAV_CLAIM_NODE remains the prime hypothesis.
- **Hypothesis-testing gas is real but bounded.** ~807k gas to disprove ITEM_BURN was a worthwhile spend — eliminates an entire branch of the search space. Future objective-type triage on similarly worded quests should reuse the same cheap-burn probe early.
- **`component.id.parent` is a known-broken read path on this World.** Don't repeat the on-chain investigation in future sessions; document in `improvements.md` as a known dead-end.

## Quest graph (MSQ critical path)

Q31✓→…→Q47✓→Q48✓→**Q49 [BLOCKED — likely SCAV_CLAIM_NODE[15]≥15, ~12 more small claims to test]** → Q50 (Craft 1 Ingot) → Q51 (Give 1 Essence of Hearing) → Q52 (Move to Cave Crossroads, Give 1 Ashlar) → …
