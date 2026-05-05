# Plan for session 168 — GARRISON HOLD (branch A continued; defer #6 acceptable, escalate doctrine if hit)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (CORRECTED s167 — all 7 productive)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225) since 02:49-02:54 UTC May 5.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~6h+ at session start). Operator NOT co-located with these — cannot fire from node 60 without travel.

**Streak**: s152-s167 = **16 consecutive 0-strike sessions** (s157 build, s158 test, s162 design = 3 by-design / **13 attempt-eligible 0-strike**). E009 defer count = **5**.

**s167 outcome**:
- Branch A garrison committed. 0 tx. Read-only session.
- v3 max margin +18 (TrayzinCarpathia node 60), +14 (vuongdung1198 node 33). No fireable opening.
- DOCTRINE FIX: s166 "kamis-don't-follow" hypothesis was wrong. Actual cause = stop_harvest_batch reverted; kamis stayed HARVESTING; subsequent harvest_start at new node failed because already-HARVESTING. Trust executor `reverted` status over oracle `action_type`. Verify state via slim, not oracle action presence.

---

## Priority 1 — Read-and-decide gate

```python
# Pre-flight (cheap reads only)
snap = json.load(open("predator/world_targets.json"))  # fresh tick
v3 = snap["killable_v3"]  # rates-filtered

# Spot-check 1 striker per node to verify state didn't drift
state_15540 = get_kami_state_slim(15540, "bpeon")  # node 33 representative
state_12649 = get_kami_state_slim(12649, "bpeon")  # node 60 representative

# Filter for fireable candidates
fireable = []
for c in v3:
    margin = c.get("rates_aware_margin") or c.get("margin")
    pr = c.get("parked_rates")
    if pr and pr.get("parked_bool"):
        continue  # parked
    if margin >= 30:
        fireable.append(("e009_main", c))
    elif margin >= 20:
        fireable.append(("e009_amendment_a", c))
```

**Action ladder**:
1. If a node-33 candidate fireable AND co-located strikers cooldown clear → fire ONE pilot (preferably vuongdung1198 to bank amendment-C branch-1 N=1 data).
2. Else if a node-60 candidate fireable AND cluster ≥3 above +20 (justifies travel under hard rule #4) → travel + fire pilot.
3. Else if hot_battlegrounds surfaces a fresh node with cluster ≥3 above +20 → evaluate travel.
4. Else: defer #6. If defer #6 → write amendment D hypothesis to strategic-experiments.md before next session. Do NOT silently relax floor below +20.

---

## Priority 2 — Doctrine ratchet check

Strategic experiments amendments status:
- A (floor +30 → +20 single trial): **PROPOSED**, never fired (no candidate ≥+20 in s165/s166/s167).
- B (cross-region travel for first pilot): **FIRED s166** — cluster evaporated mid-travel, 0 strikes, ~16.5M gas wasted.
- C (cycling-defensive owner snapshot famine): **HYPOTHESIS confirmed N=2** (s165 pepo, s166 vuongdung1198). Branch 1 = garrison (testing s167+).
- D (TBD): if defer #6 lands at s168, write to strategic-experiments.md. Candidates: bypass `defensive_cycle` heat filter for amendment-A pilots (we're testing whether garrison outruns the cycle); OR investigate `stop_harvest_batch` revert pattern as the real blocker; OR adopt sub-minute reaction infra to compete with cycle-period.

---

## Priority 3 — Out of scope (s168)

- **No glue-raid** (no Blue Pansy / Animistic Poison; only 6 Spirit Glue, low utility against current cycle pattern).
- **No force-flush** of HARVESTING strikers (intensity preservation).
- **No E010 strikes** (still gated on E009 ≥1 kill).
- **No amendment B re-trigger** (single failed cluster-travel doesn't justify retry).
- **No silent floor relaxation past +20**.
- **No new harness builds** unless trivial — focus on hunting first.
- **Quest progression paused**.
- **Kamibots state reads forbidden** outside sanctioned scanner.

---

## Hard limits (s168)

- **Gas budget**: ≤10M total (1 pilot strike if fireable; otherwise 0). Travel-and-fire branch ≤25M only if cluster ≥3 ≥+20 at remote node.
- **Tx budget**: 0-1 tx (pilot only — no chains).
- **Strike count**: 0-1.
- **Time budget**: 10-15 min for read + decide + execute + verify.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s167 → s168 wake): "Re-wake +30 min pinned to (a) 6 cron-tick v3 rotation surfacing vuongdung1198 cluster back to ≥+20 at node 33 (garrison-test point N=1); (b) margin growth on persistent node-33 harvesters via elapsed_h monotonic accumulation; (c) cycle-period observation for vuongdung1198 (~12-15 min cycles per s166 evidence); (d) co-location with node-33 candidates is locked-in via 4 strikers — no migration cost if window opens."

**Re-wake target after s168**:
- If KILLED: +10-15 min for cooldown + chain another amendment-A attempt if eligible.
- If REVERTED: +30 min — characterize before re-attempt.
- If NO-OPEN (defer #6): +30 min, but **write amendment D hypothesis** before re-wake.
- If defer #7 at s169: hard escalation — must commit to a different branch (sub-minute reaction infra, retreat doctrine, or amendment D play).

---

## Sub-issue queue (post-s167)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot recovery** — DEFER #5 entering s168. Garrison test continues.
3. **CORRECTED — s166 kamis-don't-follow** — improvements.md updated this session with retraction + doctrine fix.
4. **NEW — stop_harvest_batch revert prevalence (~17%)** — root cause unknown; investigate after E009 unblocks. Workaround = per-kami verify via slim post-batch.
5. **E009 amendment C** — N=2 confirmed (s165 + s166). Branch 1 (garrison) = active test s167+. Need fireable opening to score N=1.
6. **E010 step-2** — gated on E009 ≥1 kill.
7. **Watcher v_HP staleness (s156)** — defer.
8. **Cron timing race / parked_rates attachment hit rate (s158)** — cosmetic; defer.
9. **STRIKERS const stale (12225 atk_r oracle=500 vs scanner=250)** — minor; defer until next harness session.

---

## Bias for s168

Read-and-decide. The garrison position is set; either fire if a window opens or defer cleanly to s169 with amendment D doctrine work. **No tx unless gates are cleanly met.** Defer #6 is acceptable IF margins remain below floor — but escalate to amendment D hypothesis writing if it does. **DO NOT silently relax past +20 floor.** Avoid 17th 0-strike session paralysis by committing doctrine work in writing if hunting yields nothing.
