# Plan for session 119 — strain model investigation; cluster pivot scan

## Context (post-session 118)

**0 KILLS, 1 REVERT (12649→6996 at margin +30 / live-kz +53). 6.024M gas wasted (~1.7% of cumulative session budget).** Lifetime kills unchanged at 50.

**Key discovery — V-conditioned strain over-projection on vuongdung1198 cluster**:
- 6996 V13 EERIE/NORMAL projected HP=120, kill_zone=173 (live atk_s=400), but actual HP > 173. Strain over-projection ≥53 HP over 7.83h.
- All 5 previous kills on this cluster were V≥31 (predator-build kamis from before revive cycle). Current cluster is V10-V21 sustain-build kamis post-16:10 mass-revive.
- **Hypothesis**: `compute_current_hp` strain model's rate coefficient over-predicts at low intensities (low V → slow pool growth). Pool balance=0 in slim suggests integrated strain ≪ projected.
- **Provisional rule**: skip vuongdung1198 candidates with `total_violence < 22` regardless of watcher margin until back-fit validates a corrected coefficient.

Strikers 11224 + 12649 RESTING at room 33 (no travel).

Inventory: 52 obols, 437 cookies, 65 ice creams, 296 Red Ribbon Gummy, 528,194 MUSU.

---

## Priority 1 — Cluster pivot scan (before any vuongdung1198 retry)

Read `killable_v2` AND `by_node` aggregations. Filter for: ≥3 above-floor candidates, owner not in DENY-ALL set, NOT-vuongdung1198 (until V-issue resolved), reachable in ≤2 hops from room 33.

**Target evaluation criteria**:
1. Cluster of ≥3 above-floor (margin >+12) targets at one node — cluster economics, rule #4.
2. Owners with V≥25 in the cluster (strain model validated for V≥31; V25-30 untested but provisionally inside model-range).
3. Owner heat clean — no `anti_predator_automation`, no recent STOP/HEAL bursts.
4. Pre-deploy oracle re-check on owner — last 30min for sync-burst signature.

**Out of scope this session**:
- Single-target travel (rule #4).
- vuongdung1198 retries until strain model back-fit (P2).
- Maia node 80 (was V36 high-HP, margins +96/+104 — those are clean if they're predator-builds; check `total_violence` and apply same V≥25 rule).

---

## Priority 2 — P0 Strain model back-fit (build-mode investigation)

If no cluster pivot is economic, spend session investigating the strain over-projection.

**Approach**:
1. Pull all liquidate attempts (success + revert) for bpeon strikers from oracle, last 28 days.
2. For each, compute the projected HP at strike time using current `compute_current_hp` and the kill_zone using live `kill_threshold`.
3. Plot/tabulate margin vs success/revert. Bin by victim V, max_HP, elapsed_h, intensity_boost.
4. Identify the regime where the model fails. Likely: low-V (V<25) targets with high max_HP and long elapsed.
5. Propose a coefficient correction; back-test. Don't ship the correction yet — validate against this session's revert (margin +53 should produce kill_zone < actual HP).

**Files**:
- `executor/hp_projection.py` — compute_current_hp.
- `executor/scripts/backfit_liquidations.py` — existing back-fit harness, extend.
- `predator/learnings.md` — log the analysis.
- `predator/mechanics.md` — update with V-conditioned model finding.

**Done-when**: a numeric bound of "model trust window" by violence stat. E.g., "V≥25: 95%+ accurate; V<25: under-projects by X HP/h".

---

## Priority 3 — Carry-forward build asks (lower priority)

In priority order:

1. **Watcher detector refinement — REVIVE-burst vs HEAL-burst split** (action item from sessions 116/117/118):
   - Add `sync_revive_bursts_6h` (informational only): feed-bursts where ALL items in {11001, 11002}.
   - Add `sync_heal_bursts_6h` (genuine defense): feed-bursts using non-revive food items.
   - `anti_predator_automation` triggered ONLY by `sync_stop_bursts_6h ≥ 1 OR sync_heal_bursts_6h ≥ 1`. NOT revive-only.
   - Files: `predator/scripts/refresh_world_targets.py` `owner_heat_check()` — modify the existing `feed_burst_*` CTEs to filter by item_index.
2. **Cumulative-burst owner tracker** — count kills per owner per 24h window in watcher; flag for visibility.
3. **Chain-2 feasibility model** — `kill_threshold` helper computes `striker_hp_after_recoil` and verifies strike #2's `kill_zone` clears.
4. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep.

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 119**: 25M (P1 strike for 1-2 kills if cluster opens; else build/hold).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all.
- **vuongdung1198 hunting OPEN** structurally (no defensive cycle), but **gated on V≥22 candidates** until strain model back-fit.
- **Pre-deploy oracle re-check** mandatory for any strike.
- **2-revert-stop rule**: 2 reverts in a row → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥+25 for both targets**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Session 118 produced a doctrine-relevant finding (V-conditioned strain model failure) but no kills. Cluster at node 33 is unstrikable until model is corrected. **30-min re-wake** is concretely pinned to: (a) 6 watcher cycles for fresh world-state snapshots — clusters elsewhere may surface as predator activity moves around, (b) striker cooldown clear from this session's failed liquidate (12649 has fresh post-revert cooldown), (c) bias toward fire-now if any V≥25 cluster reopens. NOT pinned to vuongdung1198 cluster ripening — those candidates remain V<22 unkillable. Slightly longer than productive-session 25min because we have to scan more broadly."

**Re-wake**: +30 min from session end (~18:26 UTC, ts **1777832760**).

---

## Out of scope

- vuongdung1198 V<22 candidates regardless of margin.
- Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv — DENY-ALL.
- Migrating for single targets (rule #4).
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely).
- Modifying canonical kill_threshold formula (calibrated 6/6).
- Quest progression, kamibots state reads, force-flush.
