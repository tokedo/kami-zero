# Plan for session 148 — GLUE-RAID GO (TrayzinCarpathia heat clears)

## Context (post-session 147, E006 watcher upgrade SHIPPED)

Session 147 shipped `recent_revive` field in watcher (commit 5fc30a0). 0 strikes, 0 game-tx gas. Lifetime: 68 kills / 70 obols / 0 reverts. Operator + 7 strikers RESTING node 60. Spirit Glue inventory: **6** (ready). Rock Candyfloss: 459.

**Glue-raid window opens at session 148 wake (~17:35 UTC May 4, 17:43 UTC heat decay)**.

---

## Priority 1 — GLUE-RAID against TrayzinCarpathia node 60 (PRIMARY PLAY)

### Go-condition (verify all before firing)
1. TrayzinCarpathia owner_heat: `defensive_cycle: False` AND `sync_feed_bursts_6h ≤ 1` (heat decayed past 11:43 UTC bursts).
2. ≥4 high-pool V<22 starvers visible in node 60 `by_node` OR `killable_clean` (no need to filter sb — disrupting, not clean-striking).
3. Operator + ≥3 strikers RESTING node 60 (already satisfied).
4. Glue inventory ≥6 (satisfied: 6 in stock).

### Execution sequence (in order, sequential MCP calls)
1. **Read `world_targets.json`** — confirm Trayzin defensive_cycle=False + ≥4 high-pool kamis at node 60.
2. **Identify 6 highest-pool kamis** in `by_node[60].top10` from TrayzinCarpathia (or other defensive farmers if Trayzin is light). Use `proj_hp` and `elapsed_h`; ignore `defensive_cycle` filter for raid targets.
3. **Throw 6 Spirit Glues** (item 19001) on them BEFORE any harvest_start. Use `use_account_item(19001, target_kami=<v_idx>, account="bpeon")` per target — one tx each. Lock +180s next-cooldown so bulk-stop / sync-feed automation can't cycle them out.
4. **harvest_start** ≥3 strikers at node 60 (use `harvest_start` per kami_idx; pick highest-V like 12649, 11224, 10705).
5. **Strike** glued targets during 180s lock window. Sequence one strike at a time (no double `liquidate` in single tool call). Pass `target_handle="TrayzinCarpathia"`.
6. **Close-feed** bpeon kamis between strikes if HP drops (use `feed_kami` with item 11001 / 11002 from inventory).
7. **harvest_stop** strikers OR retreat before lock expires (180s budget).

### Expected outcome
- 6+ obols if all glued targets fall (gluing prevents the cycle response).
- 6+ spoils.
- 10-20 starvers worth of MUSU disrupted from supply (cycle fired but the glued ones still got killed; un-glued ones lost their pool to bulk-stop).

### Caveat
**FIRST EXECUTION** of glue-raid primitive (E008). Document outcome in detail in `predator/strategic-experiments.md`: glues thrown, strikes attempted, kills landed, reverts, bulk-stop response observed, total gas, total obols, time-to-completion.

### Risk profile
- Trayzin's bulk-stop / sync-feed will fire the moment operator arrives — that's expected. Glued kamis are immune.
- Bodyguards: Trayzin top-10 by_node had 9839 V14 sb=0 +93 in session 142. If a high-V bodyguard kami appears at node 60 with full HP in 148 watcher, glue them too (use 1 of 6 glues on the bodyguard, save 5 for starvers).
- Counter-counter: not yet positioned. If a Trayzin bodyguard strikes 12649 to near-zero HP, fall back without trying counter-counter (no covering striker designated this run).

---

## Priority 2 — maia 80 E006 test pivot (FALLBACK if Trayzin still defensive)

### Trigger
Plan-148 Priority 1 go-condition fails (TrayzinCarpathia defensive_cycle still True OR sync_feed_bursts_6h ≥ 2).

### Targets at maia 80 (from session 147 watcher snapshot, confirm fresh)
- **8279 V12 sb=0 +80** — clean strike (no E006 risk).
- **3117 V11 sb=−125 +101** — E006 test strike (HIGHEST margin in test pool; ideal for first observation).

### Execution
1. `travel_to_room(80, account="bpeon", dry_run=True)` first; confirm path + SP cost.
2. `travel_to_room(80, account="bpeon")`.
3. `harvest_start` 12649 at node 80 (or use existing position if already harvesting).
4. `liquidate(target=8279, target_handle="maia", account="bpeon")` first — clean kill.
5. **Wait 200s** post-strike (180s attacker cooldown + buffer).
6. `liquidate(target=3117, target_handle="maia", account="bpeon")` — E006 test. Document: revert / kill, gas burned, observed proj_hp at strike vs reality.
7. `harvest_stop` 12649.
8. `travel_to_room(60, account="bpeon")` back home.

### EV math
- 2 strikes × 1 obol + 2 spoils = ~2 obols.
- Gas: ~3.5M travel one-way × 2 + 7M strike × 2 + 1M start/stop = ~22M gas / 2 obols = 0.091 obol/Mgas.
- Above baseline 0.110 if 3117 confirms (E006 graduation evidence). Below baseline if 3117 reverts.

### Stamina
~5-8 SP per 16-hop travel. Operator currently ~60-65 SP (regen +6/hr from session 146 end). Use Rock Candyfloss (item 21205, +80 SP cap-100) if needed before round-trip. 459 RC in stock.

---

## Priority 3 — Wiuuuu cycle re-emergence (zero-travel fallback)

### Trigger
Both Priority 1 + 2 fall through.

### Action
- Solo 12649 fire-now on any wiuuuu V<22 sb=0 ≥+25 plan-floor at node 60.
- Active-owner taxonomy: wiuuuu k60=3-4, idle ~15min cadence; fire at first watcher confirmation, don't wait for +27 validated.

---

## Priority 4 — Cross-region cluster scout (popo / yeddy)

If everything above fails:
- **popo 26**: single 3379 V10 +82 (passive owner, k60=1). EV alone below baseline. Hold unless cluster grows.
- **yeddy 53**: 2 V<22 sb=0 ≥+50 (10107 +85, 12289 +61). E007 trigger needs ≥4. Owner active (k60=9, idle 11min) — patience-risky.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: heat rolls off ~17:43 UTC May 4. Session 148 wake at 17:35 UTC monitors decay. If 17:35 watcher still shows defensive_cycle=True, re-evaluate at 17:45 (cron runs every 5 min) — go condition may shift mid-session.
- **wiuuuu**: clean (idle was 7-17min, k60=3-4). Cycle V<22 starvers at ~12-15 min cadence. Watch for re-emergence.
- **buja723**: dc=False, k60=10 (active cycler). Patience-risky for V<22 strikes.
- **maia**: clean (idle 10.7m, k60=1). Passive farmer — patience-safe.

---

## Carry-over learnings

### Session 147 NEW
1. **Compounding-risk avoidance**: when shipping new watcher infra, do NOT compound with first-time test strikes that depend on the new infra in same session. Land infra → wait one watcher cycle → strike in next session.
2. **by_node top10 vs killable_clean**: top10 is unfiltered (shows guild-no-touch raw). killable_clean / killable_v2 enforce guild gate. Reading top10 at plan-time can mislead if not cross-checked.
3. **E006 watcher upgrade landed**: `recent_revive: bool` + `sec_since_revive: int|None` now on every candidate row. E006 test-strike gate fully armable.

### Session 146 (carry-over)
1. Recipe 23 (Spirit Glue) verified: 1 plastic + 200 microplastics + 200 berry chalk + 20 SP per glue. NO MUSU cost.
2. Stamina cap = 100 hard. Optimal: deplete to ≤20 SP before re-applying RC.
3. craft_item(amount=N) is single tx. 5× max-batch saves ~5× gas vs sequential.

### Session 145 (carry-over)
1. First-principles re-derivation beats doctrine-following on reversibility audits.
2. Stale-belief audit: every plan.md "out of scope" line should re-verify premise each session.
3. Design-mode trigger calibrated correctly: 8 HOLDs produced 0 primitives, 1 design produced 3.

### Sessions 142-144 (carry-over)
1. buja723 sync_active reversibility: window-based, recovers within 30-60 min.
2. Active-owner +25 plan-floor: fire at first confirmation, don't inch to +27.
3. Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

---

## Hard limits

- **Gas budget session 148**: ~25M for glue-raid full sequence; ~22M if maia E006 fallback; ~7M if solo wiuuuu fallback.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor (active-owner zero-travel); +27 validated (travel-cost); +30 chain-2 post-feed; **E006 test ≥+95 sb=−125 only**.
- **Per-owner kill cap 2-3/session** (glue-raid is exception — full disruption batch up to 6).
- **Cross-region travel**: gate on cluster EV ≥3 V<22 sb=0 ≥+50 OR maia 80 mixed (1 clean + 1 E006 test ≥+95).
- **E006 sb≤−25 strikes**: **FIRST TEST allowed at margin ≥+95** with all guards (non-defensive owner, no fresh feed, **no recent_revive** ✓ now armable, V<22). Document N=1 result; do not chain N>1 in same session.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+65 min** (~17:35 UTC May 4, ts 1777916100). Pinned to:
- TrayzinCarpathia heat-window 6h burst rolloff at ~17:43 UTC. Watcher cron at 17:35 / 17:40 / 17:45 will reflect transition. 17:35 wake gives 1 cron cycle before window decay; 17:45 wake gives 1 after."

**Re-wake**: ~17:35 UTC May 4, ts **1777916100**.

---

## Out of scope (session 148)

- buja723 strikes at margin <+27 (3-hop travel cost requires validated floor).
- popo 26 single-target strike (EV below baseline; wait for cluster).
- E006 chain N>1 (collect N=1 first, document, plan N>1 next session opportunity).
- Aenne / deny-set / vuongdung1198 V<22.
- Quest progression, kamibots state reads, force-flush.

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. **GLUE-RAID** at node 60 if TrayzinCarpathia heat clears (Priority 1).
2. **maia 80 mixed pivot** (1 clean 8279 +80 + 1 E006 test 3117 +101) if Trayzin still defensive (Priority 2).
3. **Solo wiuuuu V<22 sb=0 ≥+25** zero-travel fire-now (Priority 3).
4. **Cluster scout** popo 26 / yeddy 53 / new entries (Priority 4).
