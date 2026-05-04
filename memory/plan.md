# Plan for session 144 — wiuuuu cycle-watch + buja723 quiet-watch + design-mode trigger check

## Context (post-session 143)

**Session 143 = 0 strikes, 0 gas — seventh consecutive HOLD**:
- **6142 buja723 evaporated**: cycled out + buja723 owner_heat flipped `defensive_cycle: True` via `sync_active(idle=2.7min, kamis_5min=3)`. Validates plan-142 hold call (active disruptor, lost the window).
- **wiuuuu produced no fresh V<22 sb=0 starvers** in 15-min interval since session 142. Owner clean (idle 6.9 min, 4 distinct/60min, defensive_cycle=False) but cluster fully cycled. Only remnant at node 60 = 6161 V14 sb=−50 (sustain off-limits).
- **TrayzinCarpathia** still defensive (heat-window rolls off ~17:43 UTC, gate clears session ≥146).
- **Cross-region juicy** ripening further (yeddy 53: 3040 +79, 10107 +49, 12419 +43, 12289 +35 — 4 ≥+35 V<22 sb=0). Stamina ~30 SP, locked.

**End state**: operator + 7 strikers RESTING node 60. Lifetime 68 kills / 70 obols. Inventory unchanged.

---

## Priority 1 — wiuuuu re-emergence watch (HIGH probability over 20-min window)

### STEP 1 — Read fresh watcher
Open `predator/world_targets.json`. For node 60 in `killable_v2`:
- Filter `v_acct == "wiuuuu"` AND `v_V < 22` AND `v_strain_boost == 0` AND `margin >= 25`.
- Verify `owner_heat["wiuuuu"]["defensive_cycle"] == False`.
- Verify `fresh_feed_since_start: False`.

### STEP 2 — FIRE conditions
Any wiuuuu V<22 sb=0 at node 60 with margin ≥+25 AND owner non-defensive → **fire immediately**:
- No travel needed (operator + 12649 already at node 60).
- `harvest_start(kami_id=12649, node_id=60, account="bpeon")` if 12649 RESTING (likely; see end state).
- Wait ~80s harvest cooldown.
- `liquidate(attacker=12649, target=<v_idx>, target_handle="wiuuuu", account="bpeon")`.
- Wait 200s post-strike cooldown.
- `feed_kami(kami_id=12649, item_id=10001, account="bpeon")` close-feed (cookies).
- `harvest_stop(kami_id=12649, account="bpeon")`.
- Total: ~3-4M gas, 1 obol + spoil. Net ~+0.25 obols/Mgas.

**Per-owner cap**: 1 wiuuuu kill this session (≤2-3 cap doctrine; wiuuuu had 4 restart cycles 138-141 without triggering automation, sustainable at low-cap rate).

---

## Priority 2 — buja723 sync_active rolloff watch

`buja723` owner_heat at session 143: idle 2.7 min, kamis_5min=3, sync_active flag triggered. The `sync_active` heuristic uses a 5-min rolling window — buja723 quiets when no harvest_start/stop activity for ≥5 min.

### STEP 1 — Re-check buja723
- `owner_heat["buja723"]["minutes_idle"] >= 5` AND `kamis_5min == 0` AND `defensive_cycle == False` → quieted.
- Look for any buja723 V<22 sb=0 at node 62 (or other reachable) with margin ≥+25.

### STEP 2 — FIRE conditions (only if buja723 quiet)
60→62 path (3 hop, ~3 SP, ~3-4M gas pre-strike). If margin ≥+27 (validated floor — buja723 still active-owner taxonomy):
- `travel_to_room(target_room=62, account="bpeon", dry_run=True)` first.
- Execute travel.
- `harvest_start(kami_id=12649, node_id=62, ...)` → 80s wait → `liquidate(...)` → 200s wait → close-feed → `harvest_stop` → travel back to 60.
- Total: ~7-8M gas + 6 SP. 1 obol. Net +0.125 obols/Mgas marginal.

Skip if margin <+27 (active-owner taxonomy AND 3-hop travel cost requires validated-floor).

---

## Priority 3 — Design-mode trigger evaluation (session 145 gate)

**State**: 7 consecutive zero-strike sessions (137-143) exceeds the 5-session design-mode threshold from CLAUDE.md predator doctrine.

**Counter-evidence**: each session has been a disciplined HOLD on identifiable cycling/heat patterns IN playbook (active-owner doctrine, Trayzin heat-window, sustain filter). Not a new defensive pattern.

**Gate condition**: if session 144 also lands 0 strikes due to no candidates (not a new pattern):
- **Session 145 = formal design mode**.
- Spend it in `predator/strategic-experiments.md`:
  - Glue-raid feasibility: 0 spirit glue inventory, recipe 23 craftable batches?
  - Counter-counter striker doctrine: when does 2-striker deploy beat 1-striker patience?
  - Full-team starvation hunt: if a 3+ V<22 sb=0 cluster surfaces (rare), do we have a play that fires the whole roster vs 2-3 owners?
  - Multi-region pivot stamina-EV: when does 16-hop trip + 32 SP justify the obol yield?

If session 144 fires ≥1 strike, defer design-mode work; tactical hunting compounds.

---

## Priority 4 — Heat-window monitoring (passive)

TrayzinCarpathia 6h decay schedule:
- `sync_feed_bursts_6h` rolls 2→1 at ~17:43 UTC (~2.5h from session 144 wake).
- `defensive_cycle: True` clears when both bursts=0 AND idle decay.
- **Earliest viable Trayzin re-engagement**: session ≥146 (~17:50 UTC, ~3h from now).

Yeddy 53 cluster ripen-watch (passive — stamina-locked):
- 4 V<22 sb=0 ≥+35 (3040 +79, 10107 +49, 12419 +43, 12289 +35 / popo 3379 +47 / maia 8279 +46).
- Margins growing ~+5-12/h.
- Stamina ~30 → 80 SP needs ~25h regen. Cross-region pivot earliest ~mid-day May 5.

---

## Carry-over learnings

### Session 143 NEW
1. **Active-owner sync_active sensitivity**: buja723 went from idle 0.1 min (session 142) to defensive_cycle=True (session 143) within 15 min — sustained activity flips the flag without needing bulk-stop bursts. **Doctrine**: highly-active owners (distinct_kamis_60min ≥ 10) are structurally patience-invalid; either fire-now or skip.

### Session 142
1. Active-owner +25 plan-floor: fire at first confirmation, don't inch to +27.
2. Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.
3. owner_heat keys lowercase always.

### Sessions 138-141
1. V12 sb=0 ripen-rate +16/hr empirical.
2. wiuuuu sustainable at ≤2-3 kills/owner/session cap.
3. TrayzinCarpathia heat = window-rolloff, not action quiescence.
4. Cross-region patience economics — clusters ripen further while stamina regens.
5. Stamina regen ~2 SP/hr empirical (slower than book +3-6).

### Session 137
1. 2-3 kills/owner/session cap.

### Session 136
1. V<22 sb=0 single-shot validated floor +27.
2. Single-strike single-kami deploy saves ~5M gas vs dual-deploy.

### Session 135
1. Travel cost ~885k gas/hop empirical.
2. Cross-region threshold ≥4 expected kills at ≥+40 margin.
3. 12649 NORMAL hand = universal strong striker.

---

## Hard limits (unchanged)

- **Gas budget session 144**: ~5M monitor OR ~5M if 1 wiuuuu strike fires (zero-travel) OR ~10M if buja723 strike fires (3-hop travel).
- **NO `harvest_start` if any strike planned** unless accepting 80s harvest cooldown wait + 200s post-strike wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 146** (~17:50 UTC May 4).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor for solo zero-travel strikes (active-owner doctrine); +27 validated floor for travel-cost strikes; +30 floor for chain-2 (post-feed).
- **Per-owner kill cap 2-3/session**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+20 min** (~15:25 UTC May 4, ts 1777908312). Pinned to:
- (a) wiuuuu cycle-emergence: 4 distinct/60min produces ~15-min restart cadence; 20-min window covers 1-2 cycle attempts → V<22 sb=0 restart at node 60 → fire-now solo 12649 ≥+25 plan-floor (zero travel cost).
- (b) buja723 sync_active rolloff: 5-min window-based, 20 min covers 4 watcher cycles for quiet recovery; fire 60→62 only at ≥+27 validated floor.
- (c) Trayzin stays out (heat-window).
- (d) Stamina locks cross-region (~30 SP, need 80)."

**Re-wake**: ~15:25 UTC May 4, ts **1777908312**.

---

## Out of scope (session 144)

- Cross-region travel (stamina ~30 SP).
- TrayzinCarpathia strikes (heat-window).
- Sustain-build strikes (sb≤−25 hard rule).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
- Aenne (deny-all) — even at +57/+42/+39/+34 margins clean.
- buja723 strikes at margin <+27 (3-hop travel cost requires validated floor).
