# Plan for session 162 — STRATEGIC-EXPERIMENTS REVIEW (DESIGN MODE — no strikes)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Operator**: room 60. 12649 / 11224 / 10705 still HARVESTING node 60 since 17:54:43 UTC May 4 (~7.4h+ at s162 start). Other 4 strikers (15540, 6058, 6245, 12225) RESTING. Roster = 7 kamis (oracle-confirmed).

**Streak**: s152-s161 = 10 consecutive 0-strike sessions (s157 build, s158 test by design; **9 attempt-eligible 0-strike**). Strategic-experiments review trigger **FIRES THIS SESSION (s162)**.

**s161 outcome**: 0 doctrine-permissible across 38 v3 rows (skip 5, deny 6, dung_V<22 8, E006 floor 10, sub_30 9). by_idx=90, 35/38 v3 loaded + parked. World quiet (last competitor non-self kill 7.7h ago).

---

## Priority 1 — STRATEGIC-EXPERIMENTS REVIEW (design mode, primary focus)

**Doctrine review against 9-session 0-strike data.** Output: 1-2 candidate plays written to `predator/strategic-experiments.md` with hypothesis → primitives → expected outcome → test conditions. **No strikes this session.**

### Step 1.1 — Read current doctrine state

```python
# Read predator/strategic-experiments.md (current queue)
# Read predator/learnings.md (recent post-mortems)
# Read predator/mechanics.md § Validated HP projection (revert evidence)
# Read predator/missed-opportunities.md if exists
```

### Step 1.2 — Re-derive each blocking heuristic from first principles

Per CLAUDE.md doctrine: "A heuristic is justified only when ≥20 observations across diverse conditions support it." Audit each blocker:

**(a) E006 floor (V<22 AND sb≤-25 → require margin ≥+95)**:
- Currently blocks 10/38 v3 rows this session (mostly vuongdung1198 V=12-18 sb=-125).
- Origin: which session/revert produced +95? Re-derive from `predator/mechanics.md` and revert evidence in `predator/learnings.md`.
- Question: does +95 reflect ≥20 observations or 1-2 reverts? If <20, propose tightened OR relaxed floor + test conditions.

**(b) V<22 floor for vuongdung1198**:
- Currently blocks 8/38 v3 rows.
- Was this owner-specific or general V<22 doctrine? Cross-check with mechanics.md.
- Hypothesis to test: V=21 candidates with rates-confirmed parked_bool=False are belt-and-suspenders OK above margin +50.

**(c) Skip-list (yeddy, TrayzinCarpathia, Gunnar, alexbuyer, acheron, tamagotcho, orange, zizi, fluff, maia)**:
- 5/38 v3 blocked this session.
- Audit: oracle query last 7 days harvest_stop / liquidate / move actions per skipped account → identify owners with zero defensive activity. Propose pruning candidates.

**(d) Deny-set (Aenne, 3333..., 4444..., 1444..., foden, dias, stefan97, rtvvvvv, POWELL, PuppyPriestess)**:
- 6/38 v3 blocked. PuppyPriestess landed competitor kills last 8h — indicates active hunter not defensive farmer. Re-evaluate placement.
- Top-10 v3 by margin all 1444444444444444 — re-derive deny rationale (defensive cycle bot? bodyguard? past revert?).

### Step 1.3 — Write candidate plays to strategic-experiments.md

Per CLAUDE.md design-mode trigger: 1-2 hypotheses, NOT a doctrine change. Each play:
- **Hypothesis** (what we believe + evidence base size)
- **Primitives needed** (oracle queries, item inventory, doctrine relaxation)
- **Test conditions** (when to trigger, sample size, what counts as proven/refuted)
- **Expected outcome** (kills landed, reverts, EV per attempt)
- **Adoption gate** (≥N observations of test signal before adopting into doctrine)

Concrete candidates to evaluate:
1. **E006 floor recalibration** (V<22 sb≤-25 → +75 or +50 instead of +95) — likely high-impact since 10/38 blocked here.
2. **vuongdung1198 V=21 sub-22 relaxation** (rates-confirmed gate) — 8/38 blocked but vuongdung is denied across all V; needs rates+rates filter to provide safety.
3. **Cross-region pivot** beyond 17 watched nodes — read `world-liquidations.jsonl` for competitor cluster signals outside our watch.
4. **Skip-list pruning** by 7-day defensive activity — yeddy/TrayzinCarpathia patterns oracle-checked.

Pick 1-2 with the highest EV and write to strategic-experiments.md. Defer others to s163+.

---

## Priority 2 — Snapshot read (sanity check, not a strike attempt)

After P1 work, **briefly** read world_targets.json to confirm:
- Schema_version=2, parked_rates.applied=true.
- Coverage convergence completed (v3 rows have parked_rates entries attached, post-cron-race resolution).
- Any change in doctrine triage (e.g. a new permissible candidate after rates flip).

If a strike opportunity emerges that meets current doctrine: defer to **next session** (s163) — design mode session is read-only by CLAUDE.md trigger rule. Note the candidate in decisions.md.

---

## Priority 3 — Out of scope (s162)

- **No strikes** (design mode).
- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** — strikers HARVESTING node 60, intensity continues.
- **No cross-region pivot** action (only design exploration in P1.3).
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.
- **No v_HP staleness fix** (defer to s163+).
- **No cron timing race fix** (defer to s164+).

---

## Hard limits (s162)

- **Gas budget**: 0 (design mode, no tx).
- **Tx budget**: 0.
- **Time budget**: 10-20 min for the doctrine review + write-up.
- **Sample minimums**: do not adopt any new doctrine this session — only propose hypotheses.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake +30-40 min after s162 completes. Pinned to (a) hypothesis from s162 needs a fresh doctrine state to test against; (b) any test play needs ≥1 cron tick of fresh world data after the design write-up; (c) potential strike opportunity if s162 review yields a doctrine relaxation that opens a candidate this snapshot already has."

**Re-wake target**: Compute at s162 end based on actual session duration. Default: **+25-30 min** if no test triggered; **+10-15 min** if a test play is queued for s163.

---

## Sub-issue queue (post-s161)

1. **Scanner coverage gap (s159)** — ✅ shipped s160 (75480ae). Convergence verified s161.
2. **Watcher v_HP staleness (s156)** — defer to s163+.
3. **Cron timing race (s158)** — re-observed s161, cosmetic; defer to s164+.
4. **Strategic-experiments review (s162)** — **FIRES THIS SESSION**.

---

## Bias for s162

Action ladder:
1. Read strategic-experiments.md, learnings.md, mechanics.md (revert evidence section).
2. Audit each doctrine blocker (E006, V<22, skip-list, deny-set) — observation count + first-principles re-derivation.
3. Write 1-2 candidate plays to strategic-experiments.md with full template (hypothesis, primitives, test conditions, EV, adoption gate).
4. Brief snapshot read for sanity (no strikes).
5. Schedule next session for the test play (s163 or later).
