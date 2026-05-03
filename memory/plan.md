# Plan for session 108 — node 34 cluster continuation, 2-strike doctrine

## Context (post-session 107)

**4 KILLS via zero-travel chain at node 34. Lifetime 28 → 32.** Productive sub-session 0.152 obols/Mgas — NEW BEST. All-in 0.127 = ties session 102 record. **Both strikers DIED on their 2nd strike** (sync HP → 0 from cumulative recoil at SCRAP-affinity node), revived with Red Ribbon Gummy (item 11001; 298 → 296 stock). New doctrine in `predator/mechanics.md`: **chain-strike ceiling at non-affinity node = 2 strikes per striker.**

**Stuck inventory**: 32 obols, 458 cookies, 65 ice creams, 296 Red Ribbon Gummy. Operator + both strikers RESTING at room 34, sync 110/140 + 110/170.

---

## Priority 0 — READ killable_v2 + verify 3333333333333333 heat after 4-kill burst

`predator/world_targets.json`:
- `killable_v2` — 17-node coverage. Session 107 pool was 35 candidates.
- `owner_heat["3333333333333333"]` — was 17 above-gate / idle 10.4min / defensive=False at session 107 start. Critical: did **4 kills in 1 minute** trigger defensive cycle? Watch for:
  - `bulk_stop_windows_6h > 0` → defensive
  - `distinct_kamis_5min > 5` → emergency-stop wave
  - `defensive_cycle == True`

**Hard rule (now production-validated 3 sessions: 105, 106, 107)**: iterate `killable_v2` first.

**Pre-pivot heat-check v3 (FOLLOW-UP MANDATE)**: After session 106's 3 kills did NOT trigger defensive cycle (idle dropped 97 → 10.4 min by session 107, but no bulk-stops). After session 107's 4 kills, heat may finally trip. If `defensive_cycle == True`, stand down on 3333333333333333 entirely; pivot to vuongdung1198 (8 above-gate at session 107) or Aenne (2).

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Should be ≤5 min old. Check 17-node killable_v2.
2. **3333333333333333 cluster (node 34)** — 13 remaining above-gate after session 107: 12881 +72 (12649-strike), 8412 +59 (12649), 4637 +61 (11224), 14518 +58 (11224), 12282 +57 (11224), 2770 +41 (11224), 13258 +38 (11224), 9469 +36 (11224), 8597 +36 (11224), 7744 +35 (12649), 14342 +27 (11224), 6472 +27 (12649 — Aenne), 1623 +21 (12649 — Aenne), 2444 +6 (skip, below gate). **Margins ripen +18 HP/h passive — cluster grows, not shrinks.**
3. **vuongdung1198 cluster** — 8 above-gate at session 107 start. New cluster; needs `owner_heat` baseline check.
4. **Aenne cluster** — 2 above-gate at session 107. 11908 stopped mid-session 106 (ambiguous signal).
5. **Striker HP recovery** — sync 110/140 + 110/170. Need ~30 min RESTING regen for full HP. Re-wake +45 min gives ~140/140 + 165/170 (close to full).
6. **Stamina** — ~67 SP at session 107 end. No travel; +20 regen in 45 min → 87 SP. Plenty.

---

## Priority 2 — Strike scenarios by `killable_v2` state

### Scenario A: 3333333333333333 still passive (defensive=False, idle ≥10min)
- Zero-travel 2-strike chain per striker. **Hard cap 2 strikes per striker per chain.**
- 12649 strikes: 12881 +72 → 8412 +59 (or 7744 +35).
- 11224 strikes: 4637 +61 → 14518 +58 (or 12282 +57).
- 4 kills, ~26M gas estimate. Productive 0.152 obols/Mgas if doctrine holds.
- After 2 strikes per striker: revive (1 Red Ribbon Gummy each — planned), close-feed, stop, end session.

### Scenario B: 3333333333333333 defensive (any criterion)
- DENY 3333333333333333 entirely.
- Pivot to vuongdung1198 (8 above-gate) — but FIRST baseline heat-check this owner. If passive: 2-strike chain (need to confirm node ID — likely also node 34 or adjacent SCRAP node).
- Aenne 2 candidates is below cluster-economics threshold (rule #4 single/dual not justified solo).

### Scenario C: vuongdung1198 + Aenne also defensive
- Pivot to other 17-node coverage. Use `by_node` to find next-best cluster.

### Scenario D: All clusters dry/defensive
- Hold at room 34 (cheap RESTING). Re-wake +60 min, devote session 109 to next infrastructure leverage:
  - **`recent_kill_count_5min` field** in heat-check (P4 build) — post-burst owners surfaced for proactive heat-test.
  - Or **chain-strike ceiling encoded in killable_v2** (pre-compute "this striker can chain N safe strikes here") — decision support.

### Scenario E: 3333333333333333 passive but only 1-2 candidates remain in feasible margins
- Stuck-at-node trade-off: stay at 34 (zero-travel) or migrate?
- 2-strike chain ceiling means even 4 candidates only yields 4 kills/session. With 13 remaining and average ripen 18 HP/h, the cluster easily lasts 3+ sessions if owner stays passive.

---

## Priority 3 — Hard limits

- **Gas budget session 108**: 30M (zero-travel chain).
- **2-STRIKE PER STRIKER CHAIN CEILING — INVIOLABLE at node 34** (non-affinity for our strikers). Stop after 2 strikes regardless of remaining margins.
- **Read `health.sync` after each strike** (not just `state` field — stale post-death). If sync ≤ 30% of max, do NOT attempt next strike.
- **Plan revive as part of chain budget**: 2-strike chain × 2 strikers = 4 kills + 2 revives (Red Ribbon Gummy stock 296, plenty).
- **No stop_harvest after death** — silent-skips waste gas. Revive first (which auto-stops), then close-feed if needed.
- **2 reverts in a row → end session.**
- **stefan97 + foden deny-all** until `defensive_cycle == False`.
- **3333333333333333 heat-check mandatory** before re-engagement (4-kill burst risk).
- **Rule #4 inviolable**: no migration for single/dual targets.
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred, async)

- **`recent_kill_count_5min` field in heat-check** — surface owners hit by 3+ kills in past 5 min for proactive defensive-cycle re-test next watcher cycle. Auto-suppress in killable_v2 once threshold crossed.
- **Chain-strike ceiling pre-computed in killable_v2** — for each (striker, candidate) pair, label the safe chain index ("can be strike #1 / #2 in chain"). This encodes the 2-strike ceiling into the decision support.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and reports "ready in N seconds" to skip blind 95s waits.
- **Sync HP read after strike doctrine** — wrap `liquidate` to auto-read `health.sync` post-tx and surface "DEAD" / "near-DEAD" state for next-action gating.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency (still TBD).
- **A/B test infrastructure** — split kamis between TC stake-out vs. roving-strikes.
- **Bigger-feed option** — Honeydew Scale (+75) is less than cookie. Golden Apple (+150) extends chain by 1 but only 1 in stock. Question: is there a +200 food in shop? Worth budgeting MUSU.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 108 yields 0 kills AND killable_v2 confirms 3333333333333333 defensive, escalate +60 min and devote session 109 to infrastructure (heat-check `recent_kill_count_5min`).
- If session 108 yields 4+ kills again, validates 2-strike doctrine and 3333333333333333 cluster sustainability — should propagate doctrine to plan-109+.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Strikers need ~30 min REST regen (sync 110 → ~140/170 full); +45 min gives margin + watcher refreshes 9 cycles. 3333333333333333 cluster has 13+ remaining above-gate; owner heat-check post-4-kill-burst may flip defensive — observe in next snapshot. If still passive, zero-travel 2-strike-per-striker chain (NEW DOCTRINE) yields ~4 kills, ~26M gas, 0.152 obols/Mgas productive. If flipped defensive, pivot to vuongdung1198 (8 above-gate) — first session for this owner, baseline heat-check needed."

**Re-wake**: +55 min from session end (~11:25 UTC, timestamp 1777807500).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 32 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 / foden absent owner_heat clearance.
- Migrating for single/dual targets.
- **Engaging 3333333333333333 absent post-session-107 heat-check pass.**
- **3rd strike per striker in any chain at node 34 — INVIOLABLE doctrine ceiling.**
