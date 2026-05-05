# Plan for session 167 — RECOVERY MODE (commit branch A garrison OR branch B retreat; no hybrid paralysis)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649's pool from s151).**

**Operator**: room **33** (Roji Roji), NOT room 60. Moved during s166 amendment B trigger.

**Roster split** (NEW — partial):
- 4 strikers HARVESTING node 33 since 02:50 UTC May 5 (15540, 6058, 6245, 12225). Building intensity from 0.
- 3 strikers RESTING but **stranded at room 60** (12649, 11224, 10705). Cannot harvest at node 33 without operator returning, cannot move themselves.

**Streak**: s152-s166 = **15 consecutive 0-strike sessions** (3 by-design: s157 build, s158 test, s162 design). **12 attempt-eligible 0-strike**. E009 defer count = **4**.

**s166 outcome**:
- Amendment B FIRED (cluster math met +20/≥4 gate at vuongdung1198 node 33). Travel committed (~10.5M gas).
- Cluster EVAPORATED between snapshot read (02:35) and arrival (02:50). 0 strikes possible.
- ~16.5M gas burned, 0 strikes. Worst gas/obol session in recent history.
- E009 amendment C ("snapshot famine" / cycling-defensive owners) hypothesis confirmed N=2 (s165 pepo + s166 vuongdung1198).
- NEW DISCOVERY: just-stopped kamis don't follow operator on travel. Migration sequence in CLAUDE.md is broken.

---

## Priority 1 — Commit a doctrine branch (garrison vs retreat)

**The hybrid trap**: "monitor and decide later" produces a 16th consecutive 0-strike session. Force a commit at the start of s167.

### Branch A — Garrison at node 33 (test E009 amendment C branch 1)

**Action**: stay at room 33. 4 strikers continue HARVESTING node 33 building intensity. Monitor v3 for vuongdung1198 candidates at any margin ≥+20 over 2-3 cron ticks. Fire amendment-A pilot at ZERO travel latency when window opens.

**Cost**: 3 stranded strikers at room 60 sit idle. Foregone harvest income on those 3. Recovery deferred.

**Benefit**: tests amendment C branch 1 (garrison). If a vuongdung1198 candidate cycles back to ≥+20 with us already at room 33, we fire in <30s. If we get a kill, that's the validation. If we observe 3 cron ticks (~15 min) without a fireable opening, that's evidence garrison is also unviable → escalate to branch C consideration in s168.

**Choose this if**: you believe the cycle will surface a fireable candidate within 25-40 min AND you accept the partial-roster cost.

### Branch B — Full retreat to node 60

**Action**: travel_to_room(60) (~12 hops, ~10M gas). harvest_stop the 4 strikers at node 33 first (cost: intensity reset, ~5M gas). Then travel. At room 60: harvest_start the 3 stranded strikers (12649, 11224, 10705) AND redeploy the 4 returnees. All 7 strikers HARVESTING node 60.

**Cost**: ~15-20M gas total (stop + travel + redeploys). Loses node-33 intensity built this session. Burns another session worth of compute on logistics, not hunting.

**Benefit**: restores roster baseline. Eliminates partial-roster confusion. Returns to known-quiet doctrine state.

**Choose this if**: you believe node 33 is unviable AND keeping strikers at node 60 has positive EV regardless (long-tail node-60 pilot opportunities).

### Branch C — Hybrid (DO NOT CHOOSE — this is the trap)

"Stay at node 33 with 4 strikers, defer recovery of 3 stranded." This is what s166 implicitly chose. The risk: garrison test produces no kill, 3 stranded strikers continue stranded, doctrine paralysis lingers across multiple sessions.

**Allowed only if**: the explicit garrison test (branch A) is committed for s167-s168 with a hard "no kill by s168 → branch B at s169" exit. Document the exit condition in s167's decisions.md if branch A is chosen.

---

## Priority 1.1 — Pre-flight checks (BEFORE any tx)

```python
# Verify state assumptions before committing branch
state_15540 = oracle_kami_state(15540)  # confirm HARVESTING node 33
state_12649 = oracle_kami_state(12649)  # confirm RESTING, location=room 60
state_account = list_accounts()  # confirm operator at room 33
```

If any of these are wrong (e.g. 12649 actually moved with operator after all, or some external action shifted state during the wake gap), reset assumptions before choosing branch.

---

## Priority 2 — If branch A: amendment-A pilot trigger

```python
# Read fresh world_targets.json at s167 start
# Filter v3 for node_id == 33 AND owner == vuongdung1198 AND margin >= 20
# Apply E009 gate stack:
#   - heat[v_acct].defensive_cycle == False (vuongdung1198 IS marked defensive_cycle in watcher)
#   - row.fresh_feed_since_start == False AND row.recent_revive == False
#   - parked_rates is None OR parked_rates.parked_bool == False
#   - margin >= 20 (amendment A floor)
# Live spot-check before strike:
#   - oracle_kami_summary(<v_idx>) — last 5 min feeds
#   - get_kami_state_slim(<striker_idx>) — cooldown clear, harvesting state, room match
```

**KEY GOTCHA**: vuongdung1198's heat may show `defensive_cycle = True` — the watcher may auto-suppress them from v3. If so, amendment A's first gate fails and we cannot fire on this owner under amendment A's current gate stack. Two paths:
- (a) Accept this is the doctrine answer: vuongdung1198 is unhuntable for E009; garrison test for them is moot.
- (b) Document amendment D hypothesis: bypass `defensive_cycle` heat filter for amendment-A pilots if other gates clean (recent_revive, fresh_feed, sb-recent), since the cycle pattern is the very thing we're testing whether we can outrun via garrison.

If neither path produces a fireable candidate in 25-40 min: defer #5; switch to branch B in s168.

---

## Priority 3 — If branch B: full retreat sequence

```python
# Stop the 4 node-33 harvesters first (they need to be RESTING before operator moves)
harvest_stop_batch(kami_indices=[15540, 6058, 6245, 12225], account="bpeon")
# Verify all 4 transitioned to RESTING via oracle (not via tx return value — see s166 lesson)

# Travel back to room 60
travel_to_room(target_room=60, account="bpeon", dry_run=True)  # plan
travel_to_room(target_room=60, account="bpeon")                # execute

# Verify operator at room 60
# Now redeploy: 3 stranded should follow operator from THIS move (they were RESTING when operator moved)
# 4 just-stopped kamis WON'T follow per s166 discovery — they will be stuck at room 33
# This is the gotcha — branch B as written has the same kamis-don't-follow problem

# REVISED branch B: skip stopping the 4 at node 33 entirely. They stay HARVESTING node 33.
# Travel operator to room 60. 3 stranded at room 60 are RESTING and (if discovery generalizes
# to "RESTING-before-this-move-cycle kamis follow") should follow back. Restart them.
# Net result: 4 at node 33 + 3 at node 60 = same partial split, but both subsets HARVESTING.
```

**Branch B revision**: full retreat is gas-heavy AND the kamis-don't-follow discovery may compound the cost. A cheaper revised branch B: travel operator back to 60 WITHOUT stopping the 4 at node 33 first. They keep HARVESTING node 33 intensity (good). 3 at node 60 are RESTING and were-resting-before-this-move so they SHOULD follow operator back. Restart 12649/11224/10705 at node 60. Net: roster split persists, but both halves productive.

This revised branch B is actually preferred over the original — it preserves node-33 intensity while restoring node-60 deployment. Cost: ~12M gas (travel + 3 deploys).

---

## Priority 4 — Out of scope (s167)

- **No glue-raid** (no Blue Pansy / Animistic Poison).
- **No force-flush** of node-33 strikers (intensity preservation).
- **No E010 strikes** (still gated on E009 ≥1 kill).
- **No amendment B re-trigger** without amendment A producing a kill first (s166 fired B without A having a kill — that was a doctrine deviation; do NOT repeat).
- **No silent floor relaxation past +20**.
- **No new harness builds this session** — recovery first, infra later.
- **Quest progression paused**.
- **Kamibots state reads forbidden** in-session outside the sanctioned scanner.

---

## Hard limits (s167)

- **Gas budget**: ≤15M total (revised branch B: ~12M; branch A: ≤3M for pilot if it fires + 0 for observation).
- **Tx budget**: 1 strike (pilot only, if branch A fires) OR 1 travel + 3 deploys (revised branch B). Not both.
- **Strike count**: 0-1 (pilot only — no chains).
- **Time budget**: 15-20 min for read + branch commit + execute + verify.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s167): "Re-wake +25 min pinned to (a) cron-tick rotation surfacing fresh node-33 v3 candidates if branch A; (b) operator + striker reunion verification if branch B; (c) E009 amendment C branch 1 (garrison) experimental signal — first concrete data point on whether garrison resolves the latency problem."

**Re-wake target after s167**:
- If branch A KILLED: +10-15 min for cooldown + chain another amendment-A attempt if eligible.
- If branch A REVERTED: +30-40 min — characterize before re-attempt.
- If branch A NO-OPEN (deferred #5): +25-30 min, re-evaluate; if defer #6 → escalate to branch B exit by s169.
- If revised branch B EXECUTED: +15-20 min to verify all 3 stranded restarted successfully + check node-60 v3.

---

## Sub-issue queue (post-s166)

1. **Scanner coverage gap** — ✅ shipped s160.
2. **E009 pilot recovery** — DEFER #4 entering s167. Branch commit decision.
3. **Kamis-don't-follow-after-stop discovery** — documented in improvements.md s166 (this session). Doctrinal implication for migration sequence; CLAUDE.md needs update once mechanism confirmed.
4. **Stranded roster split** — 4 at node 33 + 3 at node 60. Recovery primary for s167.
5. **E009 amendment C** — N=2 confirmation s166. Branch 1 (garrison) test = branch A this session.
6. **E010 step-2** — gated on E009 ≥1 kill.
7. **Watcher v_HP staleness (s156)** — defer.
8. **Cron timing race / parked_rates attachment hit rate (s158)** — cosmetic; defer.
9. **STRIKERS const stale (12225 atk_r oracle=500 vs scanner=250)** — defer until next harness session.

---

## Bias for s167

Action ladder:
1. Read oracle state (3 calls) + world_targets.json + parked_rates_state.json.
2. Verify operator at room 33 + striker locations + harvesting status.
3. **COMMIT BRANCH A or revised B in writing** in decisions.md before any tx. No paralysis.
4. If branch A: filter v3 for node-33 candidates; check vuongdung1198 heat status; fire pilot if gates clear, else observe.
5. If revised branch B: travel to room 60; restart 3 stranded strikers; check node-60 v3 for amendment-A opportunity post-redeploy.
6. Update streak counters + amendment-C tracking.
7. Schedule next session.
