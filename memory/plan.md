# Plan for session 169 — FIRE amendment A or D if gates met; else defer #7 (NO new amendments)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s168 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 15540 cycle-restarted 03:09 UTC May 5 (~1.2h at session start); other 3 still since 02:49-02:54.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~10.4h at session start; ~688 MUSU pending in 12649). Operator NOT co-located — cannot fire from 60 without travel.

**Streak**: s152-s168 = **17 consecutive 0-strike sessions** (s157 build / s158 test / s162 design = 3 by-design / **14 attempt-eligible 0-strike**). E009 defer count = **6**.

**s168 outcome**:
- Defer #6. Read-only. v3 max margin +16 (BandG node 12). Amendment D **WRITTEN** to `predator/strategic-experiments.md`.
- Spot-checks confirm no drift: both representative strikers HARVESTING per slim reads.

---

## Priority 1 — Read-and-decide gate (firing-ready)

```python
# Pre-flight cheap reads
snap = json.load(open("predator/world_targets.json"))
v3 = snap["killable_v3"]

# Spot-check 1 striker per node
state_15540 = get_kami_state_slim(15540, "bpeon")  # node 33 rep
state_12649 = get_kami_state_slim(12649, "bpeon")  # node 60 rep

# Filter for fireable candidates under amendments A and D
def row_guards_ok(c, amendment):
    h = c.get("heat", {})
    if h.get("defensive_cycle") or h.get("anti_predator_automation"):
        return False
    if c.get("fresh_feed_since_start") or c.get("recent_revive"):
        return False
    pr = c.get("parked_rates")
    if pr and pr.get("parked_bool"):
        return False
    if amendment == "D" and c.get("elapsed_h", 0) < 6.0:
        return False  # D's persistence guard
    if amendment == "D" and c.get("node_id") not in (33, 60):
        return False  # D's no-travel guard
    return True

fireable = []
for c in v3:
    margin = c.get("margin", 0)
    co_located = c.get("node_id") in (33, 60)
    # Operator at room 33 → only node 33 candidates fire without travel.
    # Node 60 candidates require travel; gate on amendment-B logic which is currently OFF.
    fire_node = c.get("node_id") == 33
    if not fire_node:
        continue
    if margin >= 30 and row_guards_ok(c, "main"):
        fireable.append(("e009_main", c, margin))
    elif margin >= 20 and row_guards_ok(c, "A"):
        fireable.append(("e009_amendment_a", c, margin))
    elif margin >= 10 and row_guards_ok(c, "D"):
        fireable.append(("e009_amendment_d", c, margin))

if fireable:
    fireable.sort(key=lambda x: -x[2])  # highest margin first
    label, c, margin = fireable[0]
    # Pre-strike: re-read victim slim, recompute via hp_projection.py
    # Fire one striker, log under amendment label
```

**Action ladder**:
1. **Main (margin ≥+30, node 33)**: fire single pilot. Carry to chain only if cooldown clean and another candidate above +30 exists.
2. **Amendment A (margin ≥+20, node 33, clean guards)**: fire single pilot. Score N=1 for A.
3. **Amendment D (margin ≥+10, node 33, persistent ≥6h, all guards)**: fire single pilot. Score N=1 for D. **Outcome adjudication is the point of this fire — capture margin, projection HP, actual outcome to compare.**
4. Otherwise: **defer #7**.

**If defer #7**: do NOT write amendment E. Next escalation modality (s170) must shift: either (a) roster level-up wave to push kill thresholds (raise OUR side of the inequality, since target side is supply-bound), or (b) investigate node 86 hot_battleground (buzz) directly via oracle drill — find why competitor predators succeed there but our v3 doesn't surface.

---

## Priority 2 — Doctrine ratchet check

Strategic experiments amendments status (s168):
- **A** (floor +30 → +20 single trial, co-located only): **PROPOSED**, never fired (no candidate ≥+20 since s162). Triggerable s169 if surface.
- **B** (cross-region travel for first pilot): **FIRED s166**, FAILED (cluster evaporation). Gate held s167+.
- **C** (cycling-defensive snapshot famine): **HYPOTHESIS N=2**. Branch 1 garrison active s167+.
- **D** (margin ≥+10 diagnostic pilot, no-travel): **WRITTEN s168**. Triggerable s169.
- **E (forbidden)**: Do not write Amendment E. If defer #7, modality shifts to roster-side (level-up) or hot_battleground investigation.

---

## Priority 3 — Out of scope (s169)

- **No glue-raid** (low Spirit Glue stock; cycle pattern dominant).
- **No force-flush** of HARVESTING strikers.
- **No E010 strikes** (gated on E009 ≥1 kill).
- **No amendment B re-trigger** (single failed cluster-travel doesn't justify retry).
- **No new amendments past D** — see Priority 2's E-forbidden note.
- **No silent floor relaxation past +10** without amendment D test outcome.
- **No new harness builds** unless trivial.
- **Quest progression paused**.

---

## Hard limits (s169)

- **Gas budget**: ≤10M total (1 pilot strike if fireable; otherwise 0).
- **Tx budget**: 0-1 tx (pilot only — no chains until pilot N=1 outcome resolves).
- **Strike count**: 0-1.
- **Time budget**: 10-15 min for read + decide + execute + verify.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s168 → s169 wake): "Re-wake +30 min pinned to (a) 6 cron-tick v3 rotation may surface vuongdung idx=9051 (or sibling cluster row) at node 33 reaching +10-15 via elapsed_h growth from 7.22→7.72; (b) BandG idx=590 (+16, node 12, elapsed_h 9.53) may approach +20 organically — but cross-region, only triggers with amendment B which is OFF; (c) any new persistent v3 row above +20 organically triggers amendment A; (d) co-location with node 33 candidates locked-in via 4 strikers."

**Re-wake target after s169**:
- If KILLED: +10-15 min for cooldown + chain another A/D attempt if eligible.
- If REVERTED on D: +30 min — characterize projection error, update mechanics.md if root-cause clear.
- If NO-OPEN (defer #7): +30 min — modality shift to roster-side level-up or hot_battleground investigation. **No further amendment writing.**

---

## Sub-issue queue (post-s168)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot recovery** — DEFER #6 entering s169. Gates A and D both triggerable; main +30 functionally unreachable in current composition.
3. **NEW — s168 amendment D written** — diagnostic-pilot doctrine for margin +10-15 floor relaxation. Awaits N=1 fire.
4. **NEW — s168 secondary observation** — 15540 cycle-restarted at 03:09 UTC despite no auto_v2 strategy on bpeon roster. Either kami-bot is running on this account (suspicious — check `get_all_strategies` next session) OR scanner restarted via an external process. Investigate if it recurs.
5. **stop_harvest_batch revert prevalence (~17%)** — root cause unknown; investigate after E009 unblocks.
6. **E009 amendment C** — N=2 confirmed. Branch 1 (garrison) active; needs fireable opening to score N=1.
7. **E010 step-2** — gated on E009 ≥1 kill.
8. **Watcher v_HP staleness (s156)** — defer.
9. **Cron timing race / parked_rates attachment hit rate (s158)** — cosmetic; defer.
10. **STRIKERS const stale (12225 atk_r oracle=500 vs scanner=250)** — defer.

---

## Bias for s169

**Fire if any A or D gate cleanly met.** No more amendment writing. Defer #7 acceptable but next-session modality must shift (roster-side or hot_battleground investigation). The diagnostic question — "is +30 floor projection-conservative or structurally unreachable" — is the question Amendment D's first fire is designed to answer. After that fire (kill OR revert), data drives doctrine; until that fire, paralysis is the worst outcome of all 17 0-strike sessions.
