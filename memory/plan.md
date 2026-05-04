# Plan for session 149 — GLUE-RAID GO (re-attempt, Trayzin heat decay)

## Context (post-session 148, HOLD)

Session 148 = disciplined HOLD. 0 strikes, 0 game-tx gas. Trayzin heat 8 min from expected rolloff (sync_feed_bursts_6h=2 still in window). Maia 80 flipped defensive AND clean 8279 +80 gone — pivot disqualified. Yeddy 12289 single-target +82 violates hard rule #4. No fire-now reachable.

**Lifetime: 68 kills / 70 obols / 0 reverts. Spirit Glue: 6. Rock Candyfloss: 459. Strikers + operator RESTING node 60.**

**Glue-raid window opens at session 149 wake (~17:47 UTC May 4) IF Trayzin sync_feed_bursts_6h drops.**

---

## Priority 1 — GLUE-RAID against TrayzinCarpathia node 60 (PRIMARY PLAY, retry)

### Go-condition (verify all before firing)
1. TrayzinCarpathia owner_heat: `defensive_cycle: False` AND `sync_feed_bursts_6h ≤ 1` (heat decayed past 11:43 UTC bursts).
2. ≥4 high-pool V<22 starvers visible in node 60 `by_node.top10` OR `killable_clean` (glue-raid is disruption play, do NOT filter on sb).
3. Operator + ≥3 strikers RESTING node 60 (already satisfied: 7 strikers RESTING).
4. Glue inventory ≥6 (satisfied: 6 in stock).

### Pre-strike target selection (from session 148 by_node[60].top10 — re-verify in 149 watcher)
**4 V<22 sb=0 candidates ≥+25 (clean kill-zone)**:
- **6558** V15 H19 sb=0 elapsed 10.06h proj_hp 95 margin **+96** (NORMAL/EERIE — primary glue + strike).
- **17177** V13 H20 sb=0 proj_hp 104 margin **+45**.
- **16591** V15 H24 sb=0 margin **+29**.

**3 sustain candidates ≥+25 (sb<0, killable per first-principles re-derivation but E006 single-strike rule applies)**:
- **11319** V13 sb=−25 +54.
- **6023** V14 sb=−125 +46.
- **12238** V15 sb=−100 +36.

### Execution sequence (in order, sequential MCP calls)
1. **Read `world_targets.json`** at session 149 wake — confirm Trayzin dc=False, ≥4 high-pool kamis at node 60.
2. **Throw 6 Spirit Glues** (item 19001) on TrayzinCarpathia kamis BEFORE any harvest_start. **Use `use_account_item(item_id=19001, ...)`** — but verify the call signature carries a target_kami param; if not, glue may target via separate item-use endpoint (CHECK SCHEMA at session 149 plan-execute time). If `use_account_item` doesn't support target_kami, escalate to `ideas_to_founder.md` and abort glue-raid (fall through to fire-now alternatives).
3. **harvest_start** ≥3 strikers at node 60: `harvest_start(kami_ids=[12649, 11224, 10705], node_index=60)`. Pick highest-V strikers.
4. **Strike** glued targets sequentially within 180s lock window (one liquidate per MCP tool-call response per hard rule). Order by margin descending: 6558 first, then 17177, 16591, 11319 (V<22 sb=0 cluster); E006 test 6023 sb=−125 +46 only if margin ≥+95 (which it isn't — DROP). Cap at **3-4 strikes** within 180s lock.
5. **Close-feed** between strikes if striker HP drops below kill threshold.
6. **harvest_stop** strikers OR remain harvesting once lock expires (180s budget elapsed → glue effect drops, sync-feed automation may resume).

### Expected outcome
- 4 obols (4 strikes × 1 obol) + 4 spoils.
- 5-8 starvers worth of MUSU disrupted from supply (sync-feed automation fires but glued kamis are locked at node).
- **First successful execution of E008 glue-raid primitive** if it lands.

### Caveat — glue mechanics not yet empirically verified
- CLAUDE.md says glue locks NEXT_COOLDOWN +180s. Whether this prevents (a) target's auto-cycle to RESTING via owner stop_harvest, or (b) only target's own cooldown actions (e.g. counter-strike) is **unverified**. First glue-raid is partly a mechanics test.
- If `use_account_item` cannot target a kami (no target param), abort glue-raid and try alternate strike sequence: pure harvest_start + strike with no glue, accept reverts as defensive_cycle automation fires.

### Risk profile
- Trayzin's bulk-stop / sync-feed will fire the moment operator arrives — that's expected. Glued kamis SHOULD be immune (test).
- Bodyguards: top-10 has no high-V full-HP defender presently (largest is 6558 V15 H19 already in kill-zone). Counter-strike risk low.
- Counter-counter: not pre-positioned. If counter-strike happens, fall back without escalation.

### Gas budget
- 6 glues × ~850k = 5.1M.
- 3-striker harvest_start batch = ~1.5M.
- 4 strikes × 7M = 28M.
- 4 close-feeds × ~1M = 4M.
- Strikers harvest_stop batch = ~1.5M.
- **Total: ~40M gas / 4 obols = 10M gas/obol = 0.10 obol/Mgas**. At baseline. Disruption EV pushes it above.

---

## Priority 2 — Solo wiuuuu cycle re-emergence (FALLBACK if Trayzin still defensive)

### Trigger
P1 go-condition fails (Trayzin dc=True still at 17:47 wake).

### Action
- Solo 12649 fire-now on any wiuuuu V<22 sb=0 ≥+25 plan-floor at node 60.
- Active-owner taxonomy: wiuuuu k60=4, idle was ~16 min. Cycle V<22 starvers at ~12-15 min cadence; one cycle window since 148 wake.

---

## Priority 3 — Cluster scout / regroup (FALLBACK)

### Trigger
P1 + P2 fail.

### Action
- Re-wake +10 min for next Trayzin heat-decay watcher cycle.
- Optional: oracle drill on yeddy 53 to verify single-target stays single (12289 V10 +82 only) vs cluster forming.
- Optional: drill maia 80 to track cluster cycling response (did sync-stop drain it or hit-and-run-cycle it?).

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: sync_feed_bursts_6h=2 → expected to roll to ≤1 after ~17:43 UTC May 4. Watcher cron at :40, :45 will reflect.
- **maia**: sync_stop_bursts_6h=2 (NEW defensive). 6h decay window — won't clear until ~next-day cycle. Maia is now patience-NOT-safe.
- **wiuuuu**: dc=False, k60=4 (passive cycle). Patience-safe.
- **buja723**: out of owner_heat dict this snapshot (idle long enough to drop) — clean if returns.
- **yeddy**: dc=False, k60=3, idle 13.7m (passive now, was active session 147). Single-target gates on cluster math.

---

## Carry-over learnings

### Session 148 NEW
1. **maia 80 defensive flip in <65 min**: maia transitioned passive→defensive within one session interval. Cluster snapshots stale within 1 hour for active cross-region farms.
2. **HOLD-vs-pivot calculus when planned target lingers 5-15min from heat-decay**: do NOT pivot to less-developed alternative if cost-of-HOLD is zero. Compounding-risk avoidance per session 147 reinforced.
3. **Single-target cross-region rule binds even when other priorities exhausted**: hard rule #4 holds the EV line against erosion via "well, nothing else" reasoning.

### Session 147 (carry-over)
1. **Compounding-risk avoidance**: do not combine new infra ship + first-time test strikes in same session.
2. **by_node top10 vs killable_clean**: top10 unfiltered (shows guild raw); killable_clean/v2 enforce guild gate.
3. **E006 watcher upgrade landed**: recent_revive bool + sec_since_revive int|None on every candidate row.

### Session 146 (carry-over)
1. Recipe 23 (Spirit Glue) verified: 1 plastic + 200 microplastics + 200 berry chalk + 20 SP per glue. NO MUSU cost.
2. Stamina cap = 100 hard. Optimal: deplete to ≤20 SP before re-applying RC.
3. craft_item(amount=N) is single tx. 5× max-batch saves ~5× gas vs sequential.

### Sessions 142-145 (carry-over, condensed)
1. First-principles re-derivation beats doctrine-following on reversibility audits.
2. buja723 sync_active reversibility: window-based, recovers within 30-60 min.
3. Active-owner +25 plan-floor: fire at first confirmation, don't inch to +27.
4. Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

---

## Hard limits

- **Gas budget session 149**: ~40M for full glue-raid sequence; ~7M if solo wiuuuu fallback.
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
- **Per-owner kill cap 2-3/session** (glue-raid is exception — full disruption batch up to 6 against single defensive farmer).
- **Cross-region travel**: gate on cluster EV ≥3 V<22 sb=0 ≥+50 (E007).
- **E006 sb≤−25 strikes**: FIRST TEST allowed at margin ≥+95 with all guards (non-defensive, no fresh feed, no recent_revive ✓ armable). Document N=1 result; **no chain N>1 in same session**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+12 min** (~17:47 UTC May 4, ts 1777916820). Pinned to:
- TrayzinCarpathia heat-window decay (sync_feed_bursts_6h drops as ~11:43 UTC bursts age past 6h window, expected ~17:43 UTC). Watcher cron at :40 / :45 reflects. 17:47 wake captures post-:43 decay + :45 watcher run.
- Cache stays warm (<300s = 5min TTL). Specific concrete event."

**Re-wake**: ~17:47 UTC May 4, ts **1777916820**.

---

## Out of scope (session 149)

- maia 80 strikes (cluster all sb≤−100 = E006 chain forbidden; defensive owner adds compounding risk).
- yeddy 12289 single-target cross-region (hard rule #4).
- buja723 strikes at margin <+27.
- E006 chain N>1 in same session.
- Aenne / deny-set / vuongdung1198 V<22.
- Quest progression, kamibots state reads, force-flush.

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. **GLUE-RAID** at node 60 if Trayzin heat clears (Priority 1 — first execution of E008 primitive).
2. **Solo wiuuuu V<22 sb=0 ≥+25** zero-travel fire-now (Priority 2).
3. **Hold +10 min** for next watcher cycle (Priority 3).
