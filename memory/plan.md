# Plan for session 172 — FIRE A/D if gates met; else 12649 migration EV write-up

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s171 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 15540 since 03:09 UTC May 5; 6058/6245/12225 since 02:49-02:54.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~14.7h projected at s172 start).

**Streak**: s152-s171 = **20 consecutive 0-strike sessions** (5 by-design / **15 attempt-eligible**). E009 defer count = **9**.

**Banked SP audit (s171)**: Only 11224 has banked SP (3). All others 0. Allocation plan: 11224 → 1 SP `162 Lethality` (T6, +0.10 ATS, +24 kill_zone vs 240HP). Gated on natural-RESTING OR operator-at-room-60 (currently neither met; allocation deferred — see learnings.md s171).

**Per-striker calibration vs vuongdung1198 idx=16268 (top node-33 candidate)**:
- 12649 (node 60): kill_zone=178, margin=+15 — clears D, fails A. Watcher's signature.
- 15540/6058 (node 33): kill_zone=129, margin=-34. Negative.
- 6245 (node 33): kill_zone=137, margin=-26.
- 12225 (node 33): kill_zone=141, margin=-22.

→ Co-located node-33 fire IMPOSSIBLE without either (a) victim margin growing +20 above what 12225/15540 can hit OR (b) migrating 12649 to node 33.

---

## Priority 1 — Read-and-decide gate (firing-ready)

```python
import json
snap = json.load(open("predator/world_targets.json"))
v3 = snap["killable_v3"]
# Gates A=+20 co-located clean; D=+10 co-located ≥6h clean no-travel.
# Operator at 33. Co-located strikers: 15540/6058/6245/12225 (V=30-31).
# Watcher striker_idx may be 12649 (node 60) → recompute margin per-striker via
# executor.hp_projection.kill_threshold for the actual co-located striker pool.
# Fire only if recomputed margin meets gate; do NOT trust watcher margin alone for
# co-located fire decisions.
```

**Action ladder**:
1. Co-located main +30 (recomputed) → fire.
2. Amendment A +20 co-located clean (recomputed) → fire (N=1).
3. Amendment D +10 co-located ≥6h all guards (recomputed) → fire (N=1, diagnostic).
4. Else: **defer #10 + execute Priority 2 (migration EV write-up)**.

---

## Priority 2 — 12649 migration cost-benefit write-up (mandatory if defer #10)

**Goal**: structured EV analysis for migrating 12649 (node 60 → node 33) to convert the persistent vuongdung1198 cluster from "watcher-only signal" to "fireable from co-located striker".

**Inputs**:
- **Cost (gas)**:
  - Travel operator room 33 → room 60: BFS path via `travel_to_room` dry_run. ~3-12 rooms historically; 5-10M gas band.
  - `harvest_stop_batch [12649, 11224, 10705]` at room 60: ~1-9M gas (depends on harvest age — 12649/11224/10705 at ~14.7h elapsed → high band, budget 8-9M gas per CLAUDE.md force-flush rule).
  - Travel room 60 → room 33: another 5-10M gas.
  - `harvest_start_batch [12649]` at node 33: ~250k-1M gas. (Optional: also start 11224/10705 at node 33 if we keep ALL strikers at 33 going forward.)
  - Total budget: **15-30M gas** (single migration).

- **Benefit (ongoing)**:
  - Watcher s171 surfaced 5 vuongdung1198 candidates at node 33 with margins +5/+7/+9/+10/+15 (calibrated on 12649). Of these, +10 and +15 clear D-gate immediately; +9 is borderline.
  - Persistent vuongdung1198 cluster has been watcher-visible for several sessions (parked-rate cycling).
  - Single kill = 9-12 obols + spoils + 11224's Lethality unlock pathway (operator already at 60 during stop, allocate 11224 in same trip).

- **Decision matrix**:
  - If migration cost ≤ 20M gas AND ≥3 watcher-D-clear candidates persist: GO.
  - If migration cost > 25M gas OR <2 D-clear candidates persist: NO-GO + write Amendment E.
  - Otherwise: HOLD (watch one more cycle; re-evaluate s173).

**Output**:
- Append cost-benefit math to `predator/strategic-experiments.md` as new experiment entry.
- If GO decided: stage execution for s173 (DO NOT execute s172 — write-up first, sleep on it).
- Combine with 11224 Lethality allocation (operator already at room 60 during stop → free allocation opportunity).

### Out of scope for Priority 2

- **No quest progression** (PAUSED).
- **No glue-raid** (low Spirit Glue, no clean cluster).
- **No E010** (gated on E009 ≥1 kill).
- **No Amendment E unless migration NO-GO confirmed** — Lane B has actionable output (defer-not-null).

---

## Priority 3 — Hard limits (s172)

- **Gas budget**: ≤2M total (only if A/D pilot fires; no migration this session).
- **Tx budget**: 0-1 tx (single pilot strike if gate met; no chains).
- **Time budget**: 15-30 min — migration EV write-up is math + strategic-experiments.md append.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s171 → s172 wake): "Re-wake +30 min pinned to (a) 6 cron-tick rotation may surface persistent vuongdung1198 candidate at +20 (currently +15 watcher / -22 to -34 co-located); (b) 12649 migration cost-benefit produces durable decision document compounding into s173 execution if GO; (c) co-location with node 33 locked-in via 4 strikers (no migration cost yet); (d) world remains sparse for kami-zero (node 86 closed; onlinelink at node 12 cross-region irrelevant)."

**Re-wake target after s172**:
- If KILLED (A or D fire): +10-15 min for cooldown + chain another A/D attempt if eligible.
- If REVERTED on D: +30 min — characterize projection error, update mechanics.md.
- If NO-OPEN AND migration EV write-up completed: +30-45 min; durable decision doc.
- If NO-OPEN AND no write-up: doctrine failure; +10 min.

---

## Sub-issue queue (post-s171)

1. **E009 pilot recovery** — DEFER #9; entering s172 with A/D gates.
2. **NEW PRIORITY (s172) — 12649 migration EV** — write cost-benefit to strategic-experiments.md.
3. **11224 Lethality allocation** — gated on natural-RESTING OR operator-at-room-60. Combine with 12649 migration for free allocation opportunity.
4. **Lane A node 86** — RESOLVED (closed s170).
5. **Lane B per-striker SP audit** — COMPLETE (s171, learnings.md).
6. **Amendment D** — WRITTEN, UNFIRED.
7. **stop_harvest_batch revert prevalence (~17%)** — defer.
8. **E009 amendment C** — N=2 garrison test active.
9. **E010** — gated on E009 ≥1 kill.
10. **Watcher v_HP staleness** — defer.
11. **STRIKERS const stale (12225 atk_r)** — defer.
12. **Long-term**: roster leveling wave (multi-week, all strikers need 1-2M XP next, current banks 18-127k).

---

## Bias for s172

**Fire if any A or D gate cleanly met** (after per-striker margin recompute — DO NOT trust watcher margin for co-located fire). **Otherwise, EXECUTE migration EV write-up — do NOT close as another pure-defer session.** 20-session streak; Lane A closed, Lane B audited — migration is the next path to break it. If migration NO-GO, that's the trigger to write Amendment E hypothesis (Lane A + Lane B both exhausted).
