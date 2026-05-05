# Plan for session 170 — FIRE A/D if gates met; else MODALITY SHIFT (no more deferring-only sessions)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s169 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 15540 since 03:09 UTC May 5; others since 02:49-02:54.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~10.9h at s169 start).

**Streak**: s152-s169 = **18 consecutive 0-strike sessions** (3 by-design / **15 attempt-eligible**). E009 defer count = **7**.

**s169 outcome**:
- Defer #7. Read-only. v3 max +19 yeddy node 53 (cross-region, fails D no-travel guard). Co-located: node 33 max +7, node 60 max +12 (fails D persistence).
- World-wide kill rate last 6h = 9 kills, all node 86, by Assassins+aitcoin chaining 2 victims. World is sparse.

---

## Priority 1 — Read-and-decide gate (firing-ready, unchanged from s169)

```python
snap = json.load(open("predator/world_targets.json"))
v3 = snap["killable_v3"]
# Gates A=+20 co-located clean; D=+10 co-located ≥6h clean no-travel.
# Operator at 33 → only node 33 fires without travel. Node 60 = travel ~10M gas (amendment B OFF).
# Fire single pilot if gate met; else proceed to Priority 2 (modality shift WORK).
```

**Action ladder**:
1. Main +30 node 33 → fire.
2. Amendment A +20 node 33 clean → fire (N=1 for A).
3. Amendment D +10 node 33 ≥6h all guards → fire (N=1 for D — diagnostic).
4. Else: **defer #8 + execute Priority 2 work**. Do NOT just close session.

---

## Priority 2 — MODALITY SHIFT WORK (mandatory if defer #8)

**The 18-session 0-strike streak is a doctrine cost. The way out is changing what we look at, not waiting for v3 floor to surface organically.** Two parallel work lanes — pick whichever has higher EV based on session-start data; do at least one if defer #8 lands.

### Lane A — Node 86 hot_battleground oracle drill (PRIMARY)

**Question**: why do Assassins + aitcoin land 9 kills/6h on 2 victims at node 86 while our v3 surfaces zero candidates there?

**Hypotheses to test (one SQL query each)**:
1. **Filter suppression** — node-86 candidates are filtered out by `defensive_cycle` / `anti_predator_automation` / `parked` heuristics. Test: query oracle for harvesters at node 86 with their elapsed time + likely projection HP, compare to v3 raw scan list (pre-filter). If they exist in raw but not v3, doctrine error in heat filters.
2. **Sub-+30 strikes** — competitors are firing at margin <+30 (lower kill thresholds via better stats, or higher recoil tolerance). Test: query attacker kami stats (kami_static for Assassins + aitcoin's attacker kami) — what's their V/H, def_thresh, attack_thresh? Compute their kill_threshold formula with our hp_projection.py for node-86 victims; reverse-engineer what margins they're firing at.
3. **Glue/revive cycle exploitation** — they glue victim → kill → wait revive → re-kill. Test: order liquidations chronologically per victim_kami, look for ~3min gaps consistent with revive cooldown.

**Suggested queries** (copy-adapt):
```sql
-- Attacker stats
SELECT kami_id, name, level, base_violence, base_harmony, total_violence, total_harmony,
  attack_threshold_shift, attack_threshold_ratio, defense_threshold_shift, defense_threshold_ratio,
  account_name
FROM kami_static
WHERE account_name IN ('Assassins', 'aitcoin')
ORDER BY total_violence DESC LIMIT 20;

-- Victim node-86 harvesters last 6h
SELECT a.kami_id, ks.name, ks.account_name, ks.total_health, ks.total_violence, ks.total_harmony,
  a.block_timestamp, a.harvest_id
FROM kami_action a JOIN kami_static ks ON ks.kami_id = a.kami_id
WHERE a.action_type = 'harvest_start' AND a.node_id IS NOT NULL
  AND a.block_timestamp >= NOW() - INTERVAL '6 hours'
  AND a.kami_id IN (SELECT DISTINCT target_kami_id FROM kami_action WHERE action_type='harvest_liquidate' AND status=1 AND block_timestamp >= NOW() - INTERVAL '6 hours')
LIMIT 20;
```

Document findings in `predator/strategic-experiments.md` as a NEW section "Node 86 doctrine investigation s170" — this is RESEARCH not an amendment.

### Lane B — Roster level-up wave (SECONDARY)

**Question**: can we raise OUR side of the kill inequality enough to make current +5/+10/+15 candidates into +20/+25/+30 candidates?

**Steps**:
1. Read each striker's `level` and `experience` (slim reads — we have 7 strikers; 7 reads).
2. Compute banked levels per striker via `levelCost = floor(40 * 1.259^(level-1))` (per CLAUDE.md leveling guidance).
3. Per striker, project: at level+N, what's the new kill_threshold formula output? How much does our margin against current node-33/60 v3 candidates shift?
4. Decision: if +N levels per striker shifts node-33 candidates from margin +7 to margin ≥+20, level them up at next RESTING window.
5. Constraint: kamis must be RESTING for level_up. Currently all HARVESTING. So action is **measurement only this session**; trigger level-up at the next natural RESTING transition (or trigger one with a stop_harvest_batch — costs gas, evaluate EV).

Document outcome in `predator/learnings.md` as a level-up audit (input → projected output); decide whether to commit at s171.

### Out of scope for Lane A & B

- **No new amendments** (E remains explicitly forbidden until D fires N=1).
- **No floor relaxation past +10**.
- **No quest progression** (PAUSED).
- **No glue-raid** (low Spirit Glue stock, single-node hot battleground).
- **No E010** (gated on E009 ≥1 kill).
- **No force-flush** of HARVESTING strikers (esp. node-60 at ~10.9h elapsed — pool would be huge to discard).

---

## Priority 3 — Hard limits (s170)

- **Gas budget**: ≤10M total (1 pilot strike if A/D gate met; otherwise 0).
- **Tx budget**: 0-1 tx (pilot only — no chains until N=1 outcome resolves).
- **Time budget**: 15-25 min — modality shift work is research/SQL, not action; OK to spend session bandwidth on it.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s169 → s170 wake): "Re-wake +30 min pinned to (a) 6 cron-tick rotation may surface persistent +20 candidate; (b) modality shift work has concrete outputs (oracle drill writeup, level-up audit) that justify session bandwidth; (c) co-location with node 33 locked-in via 4 strikers; (d) world is sparse (9 kills/6h) so no urgency to wake sooner."

**Re-wake target after s170**:
- If KILLED: +10-15 min for cooldown + chain another A/D attempt if eligible.
- If REVERTED on D: +30 min — characterize projection error, update mechanics.md.
- If NO-OPEN AND modality-shift work landed: +30-45 min (gives time for v3 rotation; modality work is durable knowledge, no need to refresh fast).
- If NO-OPEN AND modality-shift work NOT executed: this is a doctrine failure; +10 min and re-attempt the modality work.

---

## Sub-issue queue (post-s169)

1. **E009 pilot recovery** — DEFER #7; entering s170 with same A/D gates active.
2. **NEW priority** — Lane A node-86 oracle drill (the highest-EV "where the action is" investigation).
3. **NEW priority** — Lane B level-up wave audit (raise OUR side of the inequality).
4. **Amendment D** — WRITTEN but UNFIRED. Trigger remains.
5. **Sub-issue #4** (15540 cycle-restart) — still open but de-prioritized.
6. **stop_harvest_batch revert prevalence (~17%)** — defer.
7. **E009 amendment C** — N=2 garrison test active.
8. **E010** — gated on E009 ≥1 kill.
9. **Watcher v_HP staleness** — defer.
10. **STRIKERS const stale** — defer.

---

## Bias for s170

**Fire if any A or D gate cleanly met. Otherwise, EXECUTE modality shift work — do NOT close as another pure-defer session.** 18-session streak is the cost; modality investigation is the path out. Lane A (node-86 oracle drill) is the higher-EV bet because it uses oracle-only reads (free, fast) and its output (doctrine update on what we've been filtering out) compounds across all future sessions. Lane B is durable but needs a stop-and-level execution window which gas-spends; defer to s171 unless audit shows clear net-positive EV.
