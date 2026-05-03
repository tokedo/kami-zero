# Plan for session 107 — node 34 cluster re-engagement, Aenne stop investigation

## Context (post-session 106)

**3 KILLS via hot-node expansion build (`HOT_NODES` 8 → 17). Lifetime kills: 25 → 28.** Build immediately surfaced node 34 (Deeper Into Scrap) cluster: 24 above-gate, top margins +127/+97/+87. Aenne (8 candidates) stopped mid-session — possibly defensive trigger from 3-kill burst. 3333333333333333 (97-130min idle owner) cluster delivered 3 clean kills (16537 +97, 3477 +87, 6522 +85) at 0.092 obols/Mgas (productive sub-session 0.136 — beats session 102's productive ratio).

**Stuck inventory**: 28 obols, 462 cookies, 65 ice creams. Operator + both strikers RESTING at **room 34** (NOT 60). Stamina ~50.

---

## Priority 0 — READ killable_v2 FIRST + verify Aenne cluster status

`predator/world_targets.json`:
- `killable_v2` — heat-check filtered. Now 17-node coverage.
- `owner_heat` — check **Aenne** specifically (was missing-data session 106; now after kill #11908 stop, may register actions).
- `by_node["34"]` — re-evaluate post-kill state.

**Hard rule (now production-validated 2 sessions: 105 + 106)**: iterate `killable_v2` first.

**Pre-pivot heat-check v2** still applies. After session 106's 3 kills against 3333333333333333, **immediately re-check `owner_heat["3333333333333333"]`** before any further engagement on this owner. Three kills in one minute is exactly the kind of trigger that can flip a passive farm into a defensive cycle. If `defensive_cycle == True`, stand down on 3333333333333333 entirely.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Should be ≤5 min old. Check 17-node killable_v2 distribution.
2. **3333333333333333 cluster (node 34)** — 8+ remaining above-gate from session 106 watcher: 10866 +66, 41 +74, 6247 +73, 12881 +61, 8859 +60, 4637 +49, 8412 +46, 14518 +46, 12282 +43. Must check `owner_heat` BEFORE migration commitment.
3. **Aenne cluster (node 34)** — 11908 stopped mid-session 106 at 09:30:05Z. Were 4242, 8680, 11908, ... a synchronized auto-cycle response? Check `kami_action` for Aenne kamis — multiple stops in tight window = defensive blacklist.
4. **TC node 60** — quiet during session 106. Check if wiuuuu cycle replenished.
5. **foden defensive_cycle** — was 33-34 bulk-stops/6h sessions 105/106. Watch decay.
6. **stefan97** — defensive_cycle still on 3 bulk-stops/6h.
7. **Stamina** — at 50 SP from session 106 end. Regen 0.5/min → ~80 in 60 min, ~95 in 90 min. Should be fine for in-place strikes; another migration will need ice creams.

---

## Priority 2 — Strike scenarios by `killable_v2` state at session 107 start

### Scenario A: 3333333333333333 still passive (`defensive_cycle=False`, idle ≥30min)
- Zero-travel (operator at 34). Best-EV scenario.
- Strike top 2-3 12649-strikes (41 +74, 6247 +73, 12881 +61) — 12649 was idle session 106, has full HP cycle.
- Marginal ~7.3M per kill. 3-kill chain: ~22M gas, projected 0.136 obols/Mgas.
- Pre-feed 12649 + deploy + chain.

### Scenario B: 3333333333333333 defensive (any criterion)
- DENY entire owner. 9 remaining above-gate become noise.
- Pivot: scan `killable_v2` for any other zero-travel-from-34 cluster (node 34 has 35 total scanned — many are 333333... or Aenne).
- If only 3333333333333333 + Aenne at 34 — return to 60 (10 hops, 50 stamina, full SP — feasible) for TC re-ripening.

### Scenario C: Aenne cluster also defensive (mid-session-106 stop was systematic)
- DENY Aenne too. Heat-check `bulk_stop_x_in_6h` should reflect.

### Scenario D: All node 34 owners defensive
- Hot-node expansion delivered 1 cycle of value, then closed. Pivot to next-best cluster among 17-node coverage. If still dry: hold + +60 min re-wake.

### Scenario E: Both 3333333333333333 + Aenne dry/defensive AND other 17-node clusters dry
- Travel back to room 60 (zero gas if stamina blocks) OR hold at 34 (cheap RESTING is fine).
- Re-wake +60 min, devote to **next infrastructure leverage point** (P4: stale-cycle detection / Scenario F doctrine codification / position-arbitrage cron).

---

## Priority 3 — Hard limits

- **Gas budget session 107**: 30M (zero-travel chain) / 35M (zero-travel + return travel to 60).
- **No tx if striker HP <80% max_hp** unless 1 cookie pre-feed first.
- **2 reverts in a row → end session.**
- **stefan97 + foden deny-all** until `owner_heat[X].defensive_cycle == False`.
- **3333333333333333 + Aenne deny-all if defensive_cycle == True after session 106.**
- **Read `killable_v2` first** (P0).
- **Cooldown discipline**: read `kami_state.time.cooldown` before any post-harvest_start action.
- **Session length cap**: ≤25 min wall-clock.
- **Rule #4 inviolable**: no cross-region travel for a single target.
- **Pre-pivot heat-check v2 mandatory** on 3333333333333333 (3-kill burst risk).

---

## Priority 4 — Build asks (deferred, async)

- **Scenario F doctrine codification**: when build/research surfaces a previously-invisible above-gate cluster mid-session, act on it (with heat-check + gas-economics gate). Add as Plan template.
- **Stale-cycle detection in heat-check** — owners trending toward un-blacklist after defensive cycle ends. Track `bulk_stop_windows_6h` decay, surface `cooling_cycle: True` when last-bulk-stop > 4h ago.
- **3-kill-burst defensive trigger detection**: heuristic that detects "kami_X owner just lost 3+ kamis in <5min, expect defensive_cycle within 10min". Surface for next-session caution.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and waits exactly until clear.
- **VIPP/MUSU tracking fix** — metrics column should record actual spoils currency.
- **A/B test infrastructure** — split kamis between TC stake-out vs. roving-strikes.
- **Hot-list further expansion** — only if 17-node coverage proves consistently dry (3+ sessions). Currently strong signal coming from new nodes (34, 33, 10).

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 107 yields zero kills AND killable_v2 confirms 3333333333333333 + Aenne both defensive, escalate +60 min re-wake AND devote session 108 to Scenario F doctrine codification + `cooling_cycle` build.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "3333333333333333 has 9 above-gate remaining (44+74 12649-strikes; 4 11224-strikes); owner was 97min idle pre-session 106. Three kills in one minute may have triggered defensive response. 30 min re-wake lets owner_heat resolve: if still passive (idle increases past 130min, no bulk-stop), zero-travel chain at 34 is high-EV. If defensive, pivot. Watcher refreshes 6 cycles in 30 min."

**Re-wake**: +30 min from session end (~10:10 UTC, timestamp 1777803000).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session needed (deferred).
- Modifying canonical kill_threshold formula — production-validated through 28 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 absent owner_heat clearance.
- Engaging foden absent owner_heat clearance.
- Migrating for single targets.
- **Engaging Aenne until 6h heat-check window confirms post-session-106 status.**
- **Engaging 3333333333333333 absent post-session-106 heat-check pass.**
