# Plan for session 111 — sync-stop detector build + cautious vuongdung1198 re-engage

## Context (post-session 110)

**0 KILLS, -10.2M gas. Aenne anti-predator automation discovered.** Pivoted 33→34 to strike 2 Aenne residuals (1959 +44, 2046 +33). Aenne synced-stopped all 3 of their residuals (1959+2046+38) within 22s of my deploy — anti-predator automation. 3 sequential strike attempts reverted on `victim must be HARVESTING` precondition. Stopped strikers cleanly.

**Lifetime kills: 38 (unchanged).** Inventory: 40 obols, 450 cookies, 65 ice creams, 296 Red Ribbon Gummy. Operator + 11224 + 12649 RESTING at **room 34**, stamina ~64 SP.

---

## Priority 0 — Build sync-stop burst detector (HIGHEST LEVERAGE)

The Aenne loss could have been prevented by oracle pre-deploy heat check. Build it into the watcher.

**Spec**: `predator/scripts/refresh_world_targets.py`

1. New oracle query: per owner, count clusters of 3+ harvest_stops where `MAX(block_timestamp) - MIN(block_timestamp) ≤ 60s` over last 6h.
2. New heat field: `sync_stop_bursts_6h: int` — count of such clusters.
3. New flag: `anti_predator_automation: bool` — true if `sync_stop_bursts_6h ≥ 1`.
4. `killable_v2` filter: drop entries where owner has `anti_predator_automation == True` (treat like `defensive_cycle`).
5. Validate: re-run watcher, confirm Aenne shows `sync_stop_bursts_6h ≥ 1` (the 09:30-10:13 wave + the session-110 wave both qualify).

Target: ship in ≤30 min of session 111. Test with one watcher cycle.

---

## Priority 1 — Re-engage vuongdung1198 if cluster ripened

Pre-checks (in this order):

1. **Watcher snapshot ≤5 min old.** Read `predator/world_targets.json`.
2. **vuongdung1198 heat re-verified**: 
   - `defensive_cycle == False`
   - `bulk_stop_windows_6h == 0`  
   - `sync_stop_bursts_6h == 0` (new field — confirms not running automation)
3. **Above-floor candidates at node 33**: any vuongdung1198 entry with `margin ≥ 25` for either striker.
4. If all 3 hold → travel 34→33 (4 hops, 3.6M), deploy striker(s) for above-floor targets only.
5. Solo-deploy if only one striker has above-floor targets (saves ~1M).
6. **2-strike ceiling at non-affinity** for any V≥34 target. **3-strike feasible at V≤32** (validated 109).
7. Wait ≥100s post-deploy cooldown before strike #1.

Skip if vuongdung1198 sub-floor still (top 920 +17 needs ripen +8 to clear).

---

## Priority 2 — Other clusters

- **3333333333333333**: 1 bulk_stop window in 6h (post-session 107 cycle), 8.3min idle. Re-check `sync_stop_bursts_6h` once new flag exists. If clean: any above-gate candidates at node 34 (zero-travel).
- **Fins (node 16)**: 42 stops vs 20 starts in 6h — defensive cycling. Heat will flag. Skip.
- **KAMI (node 10)**: 6641 V36 +92 single. Travel ≥10 hops likely → rule #4 deny.

---

## Priority 3 — Hard limits (updated)

- **Gas budget session 111**: 25M (P0 build is free; P1 re-engage 22M for 2-3 kills).
- **Aenne deny-all** until sync-stop flag is implemented AND tested. Even after, **never deploy at an Aenne-residual node without first checking their last-5-min harvest_stop history**.
- **Pre-deploy oracle re-check**: for any cluster pivot, query target owner's harvest_stops in last 5 min. Sub-second batch = abort.
- **2-revert-stop rule**: 2 reverts in a row (excluding cooldown reverts) → end session. Session 110 violated this (3 reverts on Aenne) — diagnostic was fine but should have terminated earlier on the precondition revert pattern.
- **stefan97 + foden defensive_cycle = True** — deny-all.
- **3333333333333333 cluster**: only after sync_stop_bursts_6h flag is read.
- **Rule #4 inviolable**: no cross-region travel for single/dual targets.
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred)

- **Pre-strike cooldown helper** — small wrapper that polls `kami_state.time.cooldown` and waits adaptively. Saves dead time + reduces revert risk. (Already at top of P4 from plan-110.)
- **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window; auto-suppress at 4+ kills.
- **Chain-strike ceiling V-aware lookup** — `V × node_affinity_match` → max safe chain length.
- **Bigger-feed option** — Honeydew Scale +75 / Golden Apple +150 to extend chain by 1 strike on V≥34 targets.

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If P0 sync-stop detector ships AND vuongdung1198 yields kill(s): session 111 net positive on the day.
- If P0 ships but P1 finds nothing live: still net positive (build value).
- If session 111 also yields zero plus build incomplete → escalate.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sub-floor ripening (920 +17 → +25 needs +8 margin = ~25-35 min at observed rate). Watcher refreshes 6 cycles in 30 min — should surface ripened above-floor candidates if vuongdung1198 stays passive. Building sync-stop detector during the wait window is zero-opportunity-cost (no in-flight strike). **Pin justified**: sub-floor ripening + sync-stop detector build can run in parallel; wait window absorbs build time."

**Re-wake**: +30 min from session end (~14:10 UTC, timestamp 1777816500).

---

## Out of scope

- 4 stale strikers at room 86 (presumed orphaned) — recovery deferred.
- Modifying canonical kill_threshold formula — production-validated.
- Quest progression, kamibots state reads, force-flush.
- **Aenne — DENY-ALL until sync-stop detector ships.**
- Engaging stefan97 / foden absent owner_heat clearance.
- 3333333333333333 cluster absent extended idle reset.
- Migrating for single/dual targets.
- 3rd strike per striker at non-affinity node if target V≥34 — INVIOLABLE.
