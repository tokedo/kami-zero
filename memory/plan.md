# Plan for session 88

## Standing context

- **Data plane**: oracle-only (CLAUDE.md top-of-file rule, founder mandate 2026-05-02). Use `executor/oracle_state.py` (`oracle_kami_state`, `reconstruct_bounty_pool`, `resolve_target_owner`) for every state read in the predator path. Kamibots is forbidden for world-state reads.
- **HP-projection cert (re-validated session 87)**: N=495, M=493, **99.6%** on 7d window 2026-04-25→2026-05-02 via oracle-only inputs. Cert recorded in `predator/mechanics.md` § "Validated HP projection — Session 87 re-validation".
- **Cross-check passed**: kami 16479 oracle path → proj_HP=29 at ×1.4 calibration (matches founder client exactly), proj_HP=15 at ×1.5 default (conservative). Both verdicts STRIKE; 16479 itself is GUILD-BLOCKED via caw-caw on no-touch list, so it can't be the actual target.
- **No on-chain tx in session 87** — pure refactor + validation. Strike gate now structurally unblocked.

## Priority 1 — Live targeting via the new oracle-only path

The strike contemplated by session 87's plan is now structurally available. Run the oracle-only scanner on currently-HARVESTING non-guild kamis. For each candidate:

1. `oracle_kami_state(kami_index)` — full state read.
2. Reject if `n_feeds_since_start > 0` (heal-event guard, session 85 rule).
3. `compute_current_hp(...)` with the KamiState fields — projected_hp.
4. `kill_threshold(...)` for the chosen attacker — kill_zone.
5. Reject if `kill_zone − projected_hp < 5` (HP margin gate).
6. Counter-predator scan on the candidate's node: oracle SQL for recent `harvest_liquidate` events targeting your kamis on that node + check no other predator with V≥30 has a clear shot at your striker.
7. Co-location: if operator-room ≠ candidate's node room, compute travel cost; reject if cluster math doesn't justify (one distant target rarely does).

**Candidates carried over from session 87 prep** (still need fresh state-read at session 88 wake):

- **Node 9 cluster**: BandG, theplux, kaviar — ~14 kamis with `fed_since_start=null` (no feed events in oracle), elapsed ~9 days at session 87 prep time. Likely heavily strained. Watch for window-edge over-claim (oracle 28d retention cuts off the harvest_start anchor).
- **Kami 6661 (alivebatman, node 30)**: V=16, H=17, max_hp=90 — glass cannon. No feeds. Low margin but achievable.
- **Avoid**: kami 13071 Ironwrench at node 72 (atk_threshold_shift=260, counter-predator threat). Caw-caw cluster at node 82 (GUILD-BLOCKED).

If the scan returns no clean candidate, that's a finding — document and reschedule.

## Priority 2 — If first kill lands, chain on the cluster

After a successful strike, re-run the same scan on the node where the kill happened. Long-runner clusters tend to have multiple soft targets; the second strike costs less gas (same room, no travel, attacker still placed).

Single-attempt rule per the founder mandate: log everything (gas, obol delta, before/after pool, projected vs actual HP). Update `predator/metrics.md`.

## Priority 3 — Migrate the Class A call sites in `executor/server.py` (refactor)

13 kamibots `_api_get` call sites in the predator-decision path are still live (audit table in `memory/improvements.md` § "Kamibots state-read audit (session 87)"). Sequence:

1. Rewrite `liquidate()` pre-flight — replace `_api_get_kami` owner lookup with `oracle_state.resolve_target_owner`.
2. Rewrite `get_kami_state` → thin wrapper over `oracle_state.oracle_kami_state` for predator callers; keep raw kamibots version under `_legacy_get_kami_state_kamibots` for kami-agent control plane.
3. Add a server-level guard: any tool decorated `@predator_only` rejects internal `_api_get*` calls in its call graph (mypy / runtime assertion).

This is refactor-only; tests = the same back-fit cert plus a smoke test of `liquidate()` against a known-killable target on testnet (or zero-tx via `staticCall`).

If session 88 lands a kill in P1, do P3 *after*; do not delay the strike for refactor work.

## Priority 4 — Document next batch of oracle gaps if any surface

`ideas_to_founder.md` § 4 lists 5 known gaps from session 87. If P1's scan surfaces anything new (e.g., a bonus `oracle_kami_state` doesn't reflect that biases a verdict), add to that section.

## Active strategies / state

- bpeon: 6-kami predator roster (12649, 6058, 12225, 15540, 10705, 11224). 11224 has 3 unspent SP — allocation deferred until first observed kill.
- No active auto_v2 (predator mode; quest-paused).
- Operator location: last known room per session 86 was 86 (node 86 for stefan97 attempt). Re-check at session 88 wake.

## Stop conditions

- One kill landed → chain on cluster, then end session, +15 min re-wake.
- Migration partial / no candidate cleared → end, +20–30 min re-wake.
- Gas budget > 15M without a kill → post-mortem in decisions.md, +30–60 min re-wake.
- Genuinely quiet world (no soft targets after thorough scan) → +60–90 min re-wake.

## Out of scope for session 88

- Quest progression (paused).
- Cross-region travel for a single target.
- Auto_v2 launches on bpeon.
- Force-flush.
- 11224 SP allocation (still gated on first observed kill + per-kami learning entry).

## Communication back to founder (end-of-session 88)

In `decisions.md` session 88:
- First kill: Y/N. If Y: target, projected HP, actual HP, kill_zone, margin, obol delta, gas.
- New oracle gaps surfaced (count + headlines).
- Class A migration progress (count migrated).
- `next-run-at` and rationale.
