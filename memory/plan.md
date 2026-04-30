# Plan for session 70

## Priority 0a — Ship Tier-1 harness mods (founder-authorized, no gas)

Three small additions, one bug fix, two CLAUDE.md edits. Commit under prefix `harness:` separately from any session-action commit. All work in `executor/server.py` unless noted.

### Mod 1 — `quest_state(quest_index, account="main")` MCP tool

Discriminated read replacing the broken `get_quest_status` and disambiguating `check_quest_completable`. Returns:

```python
{
  "quest_index": int,
  "entity_id": str,            # 0x-prefixed hex
  "owned": bool,                # qid in component.id.quest.owns for account
  "completed": bool,            # component.is.complete.has(qid)
  "completable_now": bool,      # complete() staticCall succeeds
  "revert_kind": str,           # "none" | "objs_not_met" | "not_active" | "other"
  "revert_reason": str | None,  # raw revert string if revert_kind != "none"
  "state": str,                 # "not_accepted" | "active_blocked" | "active_ready" | "completed"
}
```

State derivation:
- `completed=True` → `"completed"`
- `owned=False` and `completed=False` → `"not_accepted"`
- `owned=True` and `completable_now=True` → `"active_ready"`
- `owned=True` and `completable_now=False` → `"active_blocked"`

`revert_kind` parsing: substring match on revert reason — `"objs not met"` → `"objs_not_met"`, `"not active"` → `"not_active"`, else `"other"`.

### Mod 2 — Fix `get_active_quests`

Currently returns all owned quests including completed ones (so e.g. Q48 still shows in the list weeks after completion). Fix:

- Keep returning all owned entity IDs (preserves diagnostic value), but
- For each quest, also call `component.is.complete.has(qid)` and include `completed: bool` per quest
- Add summary fields: `owned_count`, `completed_count`, `truly_active_count`
- Rename misleading `active_quest_count` → keep as alias if other code reads it, but ensure documentation reflects that it's owned, not truly-active.

### Mod 3 — `get_expected_objective(quest_index)` MCP tool

Reads the quest catalog files at `~/kami-zero/catalogs/quests/quests.csv` and `objectives.csv` (founder-provisioned). Returns:

```python
{
  "quest_index": int,
  "title": str,
  "objectives": [
    {
      "description": str,
      "type": str,         # e.g. "DROPTABLE_ITEM_TOTAL"
      "delta_type": str,   # "INC" | "CURRENT" | "BOOLEAN" | "DECREASE"
      "operator": str,     # "MIN" | etc
      "index": int | None,
      "value": int,
    },
    ...
  ],
  "rewards": str,          # raw text, leave parsing for later
}
```

Implementation notes:
- Load both CSVs once at module import (small, ~few KB).
- Match by `Index` column in `quests.csv`. Pull `Objectives` text.
- Split `Objectives` text on lines / clear delimiters if multiple; lookup each in `objectives.csv` by `Description` exact match.
- If a quest has no row in `quests.csv` or no objective match in `objectives.csv`, return `objectives: []` and a `note` field rather than erroring — the catalog may not always be in sync with chain.
- This tool reads the catalog as documentation, NOT as ground truth. Treat output as "what the catalog says to expect" — chain may differ.

### Mod 4 — Tests

Add minimal smoke tests in `executor/tests/`:
- `test_quest_state.py`: assertions against bpeon's known state — Q48 state="completed", Q49 state="active_blocked" with revert_kind="objs_not_met", Q50 state="not_accepted" with revert_kind="not_active".
- `test_expected_objective.py`: Q49 returns objective with `type="DROPTABLE_ITEM_TOTAL"`, `index=1018`, `value=15`. Q48 returns `index=1017, value=5`.

### Mod 5 — CLAUDE.md additions

Append two short sections to `CLAUDE.md` (at the kami-zero repo root, not blocklife-ai):

**Section: "Quest debugging discipline"** (place after existing Movement/Quests section if present, else at end):

> When a quest's `complete()` staticCall reverts and you suspect the objective type, before spending gas on hypothesis tests:
>
> 1. Call `get_expected_objective(idx)` — see what the catalog says the objective is.
> 2. Call `quest_state(idx)` — confirm `state == "active_blocked"` and `revert_kind == "objs_not_met"`.
> 3. If the catalog-expected objective appears already-satisfied per current state (e.g. inventory delta exceeds the target since acceptance) but chain still says objs not met, **escalate to `memory/alerts.md` with the discrepancy. Do not test alternate hypotheses with gas.** This is a registry-vs-catalog drift class of bug — only the founder or the game team can resolve it.
> 4. Only proceed with empirical hypothesis testing when the catalog is silent or the catalog-expected objective is genuinely unverifiable from local state.

**Section: "Force-flush gas budgeting"**:

> `stop_harvest_batch` cost scales with how long the affected harvests have been accumulating. Empirical (session 69 lesson):
>
> - Harvests <2h old: ~1–1.5M gas per 5-kami batch
> - Harvests >6h old: ~8–9M gas per 5-kami batch (5–6× the naive estimate)
>
> When planning to force-flush kamis whose harvests are >6h old, **budget ≥10M gas per 5-kami batch**. Do not include "force-flush 5 kamis" in any plan with a budget under 12M gas total — you'll burn through the budget on a single batch.

## Priority 0b — Q49 status check (no gas hypothesis testing)

Once Tier-1 mods are shipped (or in parallel during reads):

1. Read `memory/alerts.md` — Q49 BLOCKADE flag is ACTIVE awaiting founder/Kami-team off-chain investigation.
2. `quest_state(49)` — should return `state="active_blocked"`, `revert_kind="objs_not_met"`. Record in decisions.md.
3. `get_expected_objective(49)` — should return `DROPTABLE_ITEM_TOTAL[1018]≥15`. Confirms the new tool works AND surfaces the catalog-vs-chain discrepancy structurally.
4. `get_scavenge_points(15)` — if ≥100 (1+ tier from natural cycling, NO force-flush), do ONE `scavenge_claim_and_reveal(15)` (~1.76M gas) as a low-cost data point. Re-check Q49 via `quest_state(49)`. Stop after one claim regardless.
5. **Do NOT force-flush. Do NOT test alternate hypotheses.** The discipline rule from CLAUDE.md applies: catalog-expected objective is already-satisfied per inventory but chain disagrees → escalation territory, not gas territory.

## Priority 1 — Level-up routine (standard, no special handling)

`get_account_kamis` + `get_kamis_progress_batch([all 20])`. With session-69's force-flush of 9 kamis having added ~579 XP each on top of pre-existing residue, expect multiple kamis with banked +1 levels.

`level_and_allocate_batch` for any RESTING kami with ≥1 banked level. Default skill plan: Guardian-leaning sustain (see CLAUDE.md). Priority for current L33–38 roster: finish 313 Patience to 5 SP for any kami below; then 321/322/323 (T2 Guardian) once T1 sums to 5.

## Priority 2 — Auto_v2 health

`get_all_strategies` + `get_strategy_status(43)`. Verify still ACTIVE. If kami 2553 (silent-skipped on session 69's stop_harvest_batch) has been ACTIVE >24h with no progress, optional single-kami `stop_harvest_batch([2553])` to cycle it. Otherwise leave alone.

## Priority 3 — Side-quest passive checks (free reads only)

Q3007 (Move 500) — passive accumulator; check briefly. Nothing else accept-able without Q49 cleared.

## Stop conditions

- Tier-1 mods shipped + tested + committed (priority 0a complete) → proceed to 0b/1/2/3.
- If Tier-1 mod implementation hits an unexpected blocker (e.g., `is.complete.has` ABI shape doesn't match what server.py uses), document the blocker in `decisions.md` and `improvements.md` and ship whatever subset works. Do NOT block the rest of the session on full Tier-1 completion.
- Cheap claim done (priority 0b step 4) — at most one. No force-flush regardless of gas headroom.

## Commit discipline

- Harness changes (Mod 1–4 and the CSV-loading): one commit, prefix `harness:`, message describing the three new tools + the get_active_quests fix.
- CLAUDE.md additions (Mod 5): can go in the same harness commit, or a separate commit prefixed `docs:`. Either is fine.
- Session memory (decisions.md, plan.md, alerts.md, next-run-at): standard `session:` commit at end.

## Reschedule

- If Q49 cleared via cheap claim (unlikely): +6h.
- Otherwise: +12h. Continue waiting on founder/Kami-team off-chain Q49 investigation.

## Inventory snapshot (end of session 69, for context)

- MUSU: 474,877. VIPP: 49,744.
- Patinated Pipe: 212. Cigarette Butt: 134. Cheeseburger: 88.
- Sanguine Shroom 29, Honeydew Scale 61, Dried Stems 367, Bone Chunk 115, Scrap Metal 71.
- Essence of Hearing × 2, Ashlar × 1 (pre-stocked for Q51, Q52 once Q49 unblocks).
- Node 15: 12 pts remainder.

## Quest status

- Q1–Q48 ✓.
- Q49: ACCEPTED 2026-04-29 17:31 UTC, state="active_blocked", catalog-expected `DROPTABLE_ITEM_TOTAL[1018]≥15`, 5 cumulative claims post-acceptance + ~129 fresh butts in inventory + 15 burned, all hypothesis tests inconclusive. **AWAITING FOUNDER / KAMI-TEAM OFF-CHAIN INVESTIGATION.**
- Q50 (You Smelt It…): not accepted, gated behind Q49.
- Mina Q2014–Q2016: complete.

## Quest graph

Q47✓ → Q48✓ → **Q49 [BLOCKED, awaiting external investigation]** → Q50 → Q51 (Essence of Hearing × 1, have 2) → Q52 (Ashlar × 1, have 1) → …
