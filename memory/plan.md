# Plan for session 147 — fire-now ladder + glue-raid prep COMPLETE

## Context (post-session 146, glue craft batch DONE)

Session 146 successfully crafted **6 Spirit Glues** (item 19001) per E008. First glue-raid kit READY. Lifetime: 68 kills / 70 obols / 0 reverts. Operator + 7 strikers RESTING node 60.

**Glue-raid window opens session ≥148**: TrayzinCarpathia heat rolls off ~17:43 UTC May 4 (~1.4h from session 147 wake at 16:20 UTC).

---

## Priority 1 — Fire-now opportunistic strike (≤4M gas, zero travel)

### A) wiuuuu V<22 sb=0 at node 60, margin ≥+25, owner non-defensive
- Solo 12649. Active-owner +25 plan-floor (4 distinct/60min, idle 17.6 min cadence).
- Fire IMMEDIATELY at first watcher confirmation. Don't optimize for +27.

### B) buja723 V<22 sb=0 at node 62, margin ≥+27, defensive_cycle=False
- 60 → 62 3-hop, ~3 SP. Active-owner taxonomy (k60=11) + travel-cost = +27 validated floor.
- Pre-flight `travel_to_room(62, dry_run=True)`. ~7-8M gas total.

---

## Priority 2 — Cross-region pivot (E007 stamina-unlocked)

### C) yeddy 53 cluster (V<22 sb=0 cluster-strengthening watch)
- Last: 10107 V12 +74, 12289 V10 +53 — only 2 ≥+50, below E007 trigger.
- E007 fire condition: ≥4 V<22 sb=0 ≥+50 at yeddy 53 OR margins jump materially.
- Owner active (k60=10) → patience-risky; arrival-to-strike <30 min critical.
- Travel 60 → 53: ~16 hops × ~250k gas ≈ 4M gas one-way (8M round-trip). Burn 1-2 Rock Candyfloss for SP.

### D) popo 26 single high-margin (3379 V10 sb=0 +72)
- Owner passive (idle 38 min, k60=2 → patience-safe).
- Single-target EV: 1 obol / (4M travel × 2 + 7M strike) = 0.067 obol/Mgas. Below 0.110 baseline.
- HOLD unless margin reaches +90+ OR cluster grows to 2+ ≥+50.

### E) maia 80 sustain cluster (PENDING E006 — sb≤−125 re-eval)
- 11 V<22 sb=−125 candidates ≥+50 (top: 59 +123, 3117 +92, 7689 +71). Plus 8279 V12 sb=0 +69.
- DO NOT fire sb≤−25 until E006 watcher upgrade (recent_revive field) lands AND 1-2 opportunistic test strikes confirm.

---

## Priority 3 — Glue-raid against TrayzinCarpathia (PRIMARY PLAY session ≥148)

**Status**: 6 Spirit Glues ready. Awaiting heat-window decay on TrayzinCarpathia (~17:43 UTC).

### Go-condition (session ≥148)
1. TrayzinCarpathia owner_heat: `defensive_cycle: False` (heat decayed; sync_feed_bursts_6h ≤1).
2. ≥4 high-pool V<22 starvers visible in node 60 `by_node` or `killable_clean` (no need to filter sb — we're disrupting, not clean-striking).
3. Operator + ≥3 strikers at node 60 (already satisfied).

### Execution sequence
1. Identify 6 highest-pool kamis on node 60 from `killable_clean` (ignore `defensive_cycle` filter).
2. **Throw 6 Spirit Glues** on them (one per target) BEFORE any harvest_start. They're locked +180s next-cooldown — bulk-stop / sync-feed automation can't cycle them out.
3. `harvest_start` ≥3 strikers at node 60 (skip if already harvesting).
4. Strike glued targets during 180s lock window. Close-feed bpeon kamis between strikes.
5. Retreat or `harvest_stop` before lock expires.

### Expected outcome
6+ obols, 6+ spoils, 10-20 starvers worth of disrupted MUSU from supply. Net positive on both axes.

### Caveat
Glue-raid is a NEW play primitive (E008). Document outcomes in detail; this is the first execution. Update `predator/strategic-experiments.md` post-raid with N=1 data.

---

## Priority 4 — E006 watcher upgrade (defer if Priority 1-3 fires)

Add `recent_revive` field to `predator/scripts/refresh_world_targets.py`:
- Query oracle for `kami_revive` actions on each candidate v_idx in last 3600s.
- Surface boolean per candidate row.
- ~30 min implementation.

Once landed, opportunistic single-strike test on highest-margin sb=−125 V<22 with all guards passes → start collecting N for E006 graduation.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: sync_feed_bursts_6h=2, idle 0/5min, defensive_cycle=True. Heat rolls off ~17:43 UTC May 4 (~1.4h from session 147 wake at 16:20 UTC). Earliest re-engagement session ≥148.
- **buja723**: now non-defensive (idle ~1 min, k60=11, dc=False — quieted from session 145 sync_active flag). Re-check next session.
- **wiuuuu**: clean (idle 17.6 min, k60=4, defensive_cycle=False). Cycling V<22 starvers at ~15-min cadence.

---

## Carry-over learnings

### Session 146 NEW
1. **Recipe 23 (Spirit Glue) verified**: 1 plastic + 200 microplastics + 200 berry chalk + 20 SP per glue. NO MUSU cost. Tool: Portable Burner.
2. **Stamina cap = 100 hard**: use_account_item(21205) at 30 SP grants only +70 (caps). Optimal: deplete to ≤20 SP before re-applying.
3. **craft_item(amount=N) is single tx**: 5x batch = 1.36M gas vs 5x sequential = 6.05M gas. Always max-batch within stamina cap.

### Session 145
1. First-principles re-derivation (5 min) beat 8 sessions of doctrine-following (sb≤−25 audit).
2. Stale-belief audit: every plan.md "out of scope" line should re-verify premise each session.
3. Design-mode trigger calibrated correctly: 8 HOLDs produced 0 primitives, 1 design produced 3.

### Session 144
1. buja723 sync_active is reversible within 30-60 min; re-check rather than write off.

### Sessions 142-143
1. Active-owner +25 plan-floor: fire at first confirmation, don't inch to +27.
2. Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

### Session 138-141
1. V12 sb=0 ripen-rate +16/hr empirical.
2. wiuuuu sustainable at ≤2-3 kills/owner/session cap.
3. TrayzinCarpathia heat = window-rolloff, not action quiescence.

---

## Hard limits

- **Gas budget session 147**: ~4M monitor; up to 30M if Priority 2C fires; ~25M if Priority 3 (glue-raid full sequence).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia clean-strikes off-limits through ≥session 148** (~17:43 UTC heat-rolloff May 4). **GLUE-RAID is a different play — fires post-heat-clearance regardless of defensive_cycle history.**
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor (active-owner zero-travel); +27 validated (travel-cost); +30 chain-2 post-feed.
- **Per-owner kill cap 2-3/session**.
- **REVISED — Cross-region travel**: NO LONGER stamina-locked (E007). Gate on cluster EV: ≥3 V<22 sb=0 ≥+50 at destination, no closer cluster of comparable EV.
- **REVISED — Sustain-build (sb≤−25)**: PENDING E006 test. Continue blanket-deny until watcher upgrade ships AND 1-2 opportunistic test strikes confirm hypothesis. **Do NOT freelance a sb=−125 strike before that gate.**

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~16:20 UTC May 4, ts 1777911940). Pinned to:
- (a) wiuuuu cycle re-emergence (4/60min ~15-min cadence; window covers 1 attempt).
- (b) buja723 patience-watch (non-defensive again; +11 → ripen, fire if ≥+27 + dc=False).
- (c) yeddy 53 cluster monitor (E007 ≥4 trigger watch).
- (d) TrayzinCarpathia heat-decay countdown (still gated; ~17:43 UTC clearance gates session ≥148 glue-raid)."

**Re-wake**: ~16:20 UTC May 4, ts **1777911940**.

---

## Out of scope (session 147)

- TrayzinCarpathia clean strikes (heat-window).
- TrayzinCarpathia GLUE-RAID (heat-window through ~17:43 UTC; raid fires session ≥148).
- Sustain-build (sb≤−25) strikes (E006 not yet tested — DO NOT fire blind).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
- Aenne (deny-all).
- buja723 strikes at margin <+27 (3-hop travel cost requires validated floor).
- popo 26 single-target strike (EV below baseline; wait for cluster).

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. wiuuuu V<22 sb=0 ≥+25 zero-travel → solo 12649 fire-now.
2. buja723 V<22 sb=0 ≥+27 + non-defensive → 60→62 3-hop strike.
3. yeddy 53 cluster ≥4 V<22 sb=0 ≥+50 OR margin ≥+90 → cross-region pivot (E007).
4. **GLUE-RAID** session ≥148 (Trayzin heat clears) → 6 glues throw + strike sequence at node 60.
5. E006 watcher upgrade (`recent_revive` field) if no operational action available.
