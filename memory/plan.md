# kami-zero session 87 prompt — STRUCTURAL RULE: oracle-only for world state, eliminate kamibots reads (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. Push to `~/kami-zero/memory/plan.md`, commit, fire.

---

## ⚠️ Foundational structural rule from founder (2026-05-02)

While you were running session 86, founder did an independent cross-check on the `compute_current_hp` utility against kami 16479. Result:

- The formula is **mathematically perfect**: given the right inputs, `220 − strain(1674) = 220 − 191 = 29` HP, which matches the in-game client exactly.
- But the cross-check input came from `get_kami_state` (kamibots playwright API) which returned `harvest.balance: 0`, `sync_hp: 220`, `rates: { all zeros }` — **stale by hours** for a kami the agent hadn't been actively polling.
- Real state (per the in-game client): **HP 29/220, bounty pool 1,674 MUSU, draining 16.81 HP/hr** — almost certainly killable (`projected HP 29` vs an 11224-class striker's `kill_zone ~35–45`).
- Sessions 81–86 walk-aways on long-runner candidates were over-conservative for exactly this class of target — kamibots' playwright cache was hiding the real pool, so the scanner could only see kamis the agent had recently touched.

**Founder mandate (verbatim):**

> "Can we please eliminate kamibots from these calculations completely? Let's only rely on oracle — something that we can control. Let's just use kamibots on other accounts like kami-agent to setup harvest strategies. I want my assassin to be pure and just rely on things that we can make reliable. […] Let's make this structural rule — no kamibots for info about the world, all info should come from oracle. If oracle misses anything — we modify it to add it."

**The new rule (hard, structural, applies forever):**

1. **All world-state reads come from oracle.** Stats, traits, skills, build, sync HP at last touch, current state, harvest pool, harvest start/last timestamps, bonuses, equipment, location, node affinity — all of it. Oracle is the single source of truth for "what is the world right now."
2. **Web3 direct chain reads are the staleness escape hatch.** When oracle has the schema but its snapshot lags chain (e.g., `kami_static.build_refreshed_ts` ≤ 24h, target leveled up since), refresh that specific kami's component values directly via web3. This was already in your toolkit (executor uses web3 for tx); use it for reads when oracle freshness isn't enough.
3. **Kamibots is forbidden for world-state reads in kami-zero.** No `get_kami_state`, no `get_account_kamis`, no `get_inventory` for predator targeting decisions, no playwright endpoints for live state. Anywhere in the predator hunting path.
4. **Kamibots remains in scope ONLY for kami-agent-side operations** — auto_v2 strategy lifecycle on harvester accounts, register_kamibots, etc. Those are control-plane configuration calls; not world-state reads.
5. **Oracle gaps get fixed by extending oracle.** If oracle doesn't have a field/table/view kami-zero needs, write a precise ask to `ideas_to_founder.md` (what's missing, why, where it would live, workaround if any). Founder routes oracle additions to kami-oracle. **Do NOT fall back to kamibots — accept reduced confidence or skip the candidate.**

The structural rule is the bright line. The rest of this prompt operationalizes it.

---

## Hard rules for this session

- **No `liquidate` tx until** the new oracle-only data path is in place AND has been re-validated against the same back-fit corpus that produced the 99.5% certificate.
- **No kamibots state reads** in any new code committed this session. If existing code paths use them for state, replace or deprecate them.
- All other doctrine still applies (guild gate, no force-flush in hunt mode, predator co-location, current-HP heuristic, validated kill threshold, heal-event guard, etc.).

---

## Priority 0 — Read the docs (orient before refactoring)

End-to-end:

1. **`~/kami-zero/integration/oracle.md`** — schemas, query patterns, auth.
2. **`~/kami-zero/systems/state-reading.md`** — canonical "project state from chain" patterns. The oracle is downstream of chain; the same projection logic applies.
3. **`~/kami-zero/systems/harvesting.md`** + **`systems/health.md`** — the formulas you already validated. Keep them in mind as you re-wire inputs.

Also re-read your own `executor/hp_projection.py` to confirm the input contract — what fields `compute_current_hp` expects and in what units. The contract doesn't change; only the source of those fields changes.

---

## Priority 1 — Audit `executor/server.py` for kamibots state reads

Grep for kamibots-API call sites. Likely candidates: `get_kami_state`, `get_kami_state_slim`, `get_account_kamis`, `get_inventory`, `get_account`, `get_tier`, anything that hits `KAMIBOTS_BASE/playwright/...` or uses `_api_get` / `_headers` for state info.

For each call site found, classify:

| Class | Action |
|---|---|
| **A — World-state read used in predator decisions** | Migrate to oracle (Priority 2). Mark kamibots version DEPRECATED in code comment. |
| **B — Control-plane / kamibots-strategy-side** | Leave alone. These stay (auto_v2 management on kami-agent accounts is allowed). |
| **C — Used only by paused quest code** | Leave alone, mark as quest-paused; not predator's concern. |
| **D — Diagnostics / one-off debugging** | Acceptable but document as out-of-doctrine fallback; not for production hunt decisions. |

Output the audit table to `memory/improvements.md` § "Kamibots state-read audit (session 87)" so the founder can review.

---

## Priority 2 — Build the oracle-only state-read primitives

You design the API. Sketch (you decide names/signatures/return shapes):

- **`oracle_kami_state(kami_id) -> KamiState`** — replaces `get_kami_state`. Returns: `state`, `sync_hp_at_last_touch`, `last_touch_action`, `last_touch_ts`, `harvest_start_ts`, `harvest_last_ts`, `bounty_pool_now` (reconstructed), `node_id`, `node_affinity`, `power`, `violence`, `harmony`, `body_aff`, `hand_aff`, `bonuses{...}`, `build`, `freshness_warnings[]`. Confidence: high (≥0.95) if all fields fresh; lower if any field shows staleness.
- **`oracle_account_state(account) -> AccountState`** — list of kami_ids owned, each with summary state (state, last_touch_ts, current node).
- **`reconstruct_bounty_pool(kami_id) -> float`** — the load-bearing piece. Same logic as the back-fit's empirical mode: walk kami_action since `harvest_start`, accumulate Fert+Int per-second × Δt × multipliers, subtract `collect_event.amount` for each collect, return current pool. Validate against the same 200-kill back-fit corpus — should still hit ≥99.5% (the back-fit *already used this approach*, you're just packaging it as a live primitive).
- **`refresh_kami_build_onchain(kami_id) -> dict`** — web3-direct read for cases where `kami_static.build_refreshed_ts` is older than the latest `level_up` / `upgrade_skill` event for that kami. Use this *only when* the staleness check fires; otherwise oracle.

Implementation hints:

- The reconstruction function is **already inside `executor/scripts/backfit_liquidations.py`** (empirical mode). Extract the per-kami forward-simulation into `executor/oracle_state.py` (or wherever fits) and expose as a callable for live targeting. No new logic — just refactor.
- For `bonuses`, you need equipped items per kami → `kami_equipment` view + `items_catalog.effects` column. If a needed effect isn't parsed in oracle today, log to `ideas_to_founder.md` and skip-with-warning rather than read kamibots.
- For dual-affinity nodes, `nodes_catalog.affinity` may be a list or string — handle both.
- **No backward compat with kamibots structure.** New primitives return a clean shape that maps directly to `compute_current_hp` arguments. Kill the `harvest.bounty.balance` vs `harvest.balance` ambiguity in your new contract.

---

## Priority 3 — Re-validate back-fit on the new path

Run `executor/scripts/backfit_liquidations.py` (or your refactored equivalent) using the **new oracle-only primitives** as inputs, not the kamibots-fed ones. Same N=200 historical kills (or expand to N=500 if oracle has that much).

**Acceptance:** ≥99.5% accuracy. If you're below, the bounty pool reconstruction has a gap — likely a bonus you weren't parsing. Find it, fix it, document it. Update the calibration certificate in `predator/mechanics.md` to reference the oracle-only path.

If you genuinely cannot hit 99.5% because oracle is missing critical inputs (e.g., a specific bonus), document the missing field in `ideas_to_founder.md` and report the partial accuracy. Don't claim the certificate transfers without the validation.

---

## Priority 4 — Cross-check on kami 16479 (the founder's smoking gun)

To prove the migration works, run your new `oracle_kami_state(16479)` and pipe the result into `compute_current_hp`. You should get **projected HP ≈ 29** (within ±2 HP — strain rate may have advanced a few HP since founder's check). Compare against:

- The kamibots stale read (220 HP — the bug you're fixing).
- The expected ground truth from founder's client snapshot (29 HP, pool 1674).

Document the comparison in `predator/learnings.md` § "Session 87 oracle migration cross-check" — this is the falsification-test that the rule shipped is real, not just theoretical.

---

## Priority 5 — Update CLAUDE.md doctrine

Add a new top-of-file block, **above** Block F (Knowledge Sources), so it's the very first thing future-you reads:

> ## Data Plane: Oracle-Only (founder, 2026-05-02)
>
> **All world-state reads come from kami-oracle.** Stats, traits, skills, build, sync HP at last touch, current state, harvest pool, harvest timestamps, bonuses, equipment, location, node affinity — every datum that feeds a predator decision. Oracle is the single source of truth for "what is the world."
>
> Web3 direct chain reads are the **staleness escape hatch only** — use when oracle has the schema but its snapshot lags (e.g., `kami_static.build_refreshed_ts` older than the latest level_up event for the target). Web3 reads are not first-line; oracle is.
>
> **Kamibots is forbidden for world-state reads in kami-zero.** No `get_kami_state`, `get_account_kamis`, `get_inventory`, no playwright endpoints in any predator-decision path. Kamibots remains in scope only for control-plane operations (e.g., kami-agent strategy management on harvester accounts) — not for kami-zero's world-state reads.
>
> If oracle is missing a field kami-zero needs, write the ask to `ideas_to_founder.md` and either skip the candidate or accept reduced confidence. Do **not** fall back to kamibots.

Also: append to the Predator Hard Rules a one-liner: *"Hard rule: kamibots-API state reads are forbidden in any predator-decision path. Oracle is the data plane."*

Demote the existing "no strike unless certificate is current" line if it conflicts; the new doctrine is more specific.

---

## Priority 6 — Live targeting via the new path (only if Priority 3 ≥ 99.5%)

Run the new oracle-only scanner over all currently HARVESTING non-guild kamis. Apply:
- HP-projection cert (≥99.5% on new path)
- ≥5 HP margin
- No recent `feed_kami` event (heal-event guard)
- Co-location feasible (or current operator-room is the target's room — minimize travel gas)
- Counter-predator scan clear

The candidate that should now show up cleanly: **kami 16479 at node 82** (Geometric Cliffs, SCRAP affinity, ~29 HP, no def_ratio per founder's client snapshot — only +6% def_threshold_shift while equipped).

If 16479 (or a peer in similar shape) is killable per your new pre-flight, **fire one strike**. Single attempt, log everything. If it lands, scan for the next candidate on the same node and chain.

If your scanner returns no killable candidates after the migration, that's a finding — document in `predator/learnings.md` and reschedule.

---

## Priority 7 — `ideas_to_founder.md` — oracle additions if any

If you discovered missing fields/tables/views in oracle while building the new primitives, write each as a concrete ask:

- **Field name** + **why kami-zero needs it** + **where it would live** (table/view) + **suggested derivation logic** + **what kami-zero does meanwhile** (skip / reduced confidence).

Founder routes these to kami-oracle's roadmap.

---

## Priority 8 — Self-schedule

After this session:
- If first kill landed → 15 min re-wake, chain on the cluster (16479's node 82 likely has more long-runners in similar state).
- If migration done but no kill yet (e.g., 16479 cycled) → 20–30 min re-wake to re-scan.
- If migration partial (still validating) → 30–60 min, continue.

---

## Stop conditions

- Migration complete + back-fit ≥99.5% on new path + first kill landed → end session, log, schedule short re-wake.
- Migration complete + cross-check on 16479 confirms ≈29 HP projection (matches client) but no live strike fired (e.g., 16479 cycled, no other candidates yet) → end session, schedule short re-wake.
- Back-fit on new path < 99.5% → end session, document gap, schedule re-wake to continue.
- Total gas > 15M without a kill → end session, post-mortem (this is mostly refactor + validation, very little tx expected).

---

## Out of scope

- Quest progression (paused).
- 11224 SP allocation (still gated on first kill).
- Force-flush.
- Cluster moves to nodes 60/62 (still cancelled).
- Modifying kami-oracle code (that's a kami-oracle session — kami-zero only proposes).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Audit table summary (count by class A/B/C/D).
- New oracle primitives shipped (file paths, line counts).
- Back-fit re-run accuracy on new path (N, M, %).
- Cross-check on kami 16479: projected HP from new path vs founder's client value (29 HP, 1674 pool).
- Any oracle additions added to `ideas_to_founder.md` (count + headlines).
- First kill: Y/N. If Y, target / margin / outcome.
- `next-run-at` and rationale.
