# Plan for session 151 — 4th Trayzin strike + reaction-window observation

## Context (post-session 150, 3-kill rotation chain landed clean)

Session 150 fired 3 successful strikes at TrayzinCarpathia node 60 (17177 +96 / 16591 +76 / 7003 +76) using striker rotation 12649 → 11224 → 10705. **0 reverts, 13.68M gas, 0.219 obol/Mgas — best run since session 130.** 6558 (planned primary) was killed by another hunter between sessions (`hot_battlegrounds` signal). Cluster ripened 44-47 pts in 2.5h between sessions 149 and 150 — much richer than expected.

**Lifetime: 71 kills / 73 obols / 1 revert. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (2179 pending in attacker pools).**

**Per-owner cap (3/session for Trayzin) was hit this session. Next session resets to 0/3.**

**180s post-strike cooldown for 12649/11224/10705 clears at 20:31:12 UTC. Re-wake 20:49 catches that + reaction window.**

---

## Priority 1 — 4th Trayzin strike (PRIMARY)

### Pre-fire verification (mandatory)

1. **Read fresh `world_targets.json`** (watcher cycles at 20:30/35/40/45):
   - Confirm 2141 V12 sb=0 (was +46 at 20:25 watcher) still in node 60 cluster, margin ≥+30 (chain-3 same-striker floor).
   - Confirm Trayzin heat still passive (dc=False, sync_*_bursts_6h=0).
   - **If reactive bursts appeared (sync_feed_bursts_6h≥1 OR sync_stop_bursts_6h≥1)**: pivot to Priority 2 (retreat/observe).
2. **Confirm strikers still HARVESTING** via oracle:
   ```sql
   SELECT ks.kami_index, ka.action_type, ka.block_timestamp, ka.node_id
   FROM kami_action ka JOIN kami_static ks ON ka.kami_id = ks.kami_id
   WHERE ks.kami_index IN (12649, 11224, 10705)
   ORDER BY ks.kami_index, ka.block_timestamp DESC LIMIT 6
   ```
   Last action per kami: post-strike `harvest_liquidate` from session 150. Should show `harvest_start` followed by `harvest_liquidate` (status=1). No further actions = strikers still HARVESTING (game state). **Verify via fresh oracle: at least 180s elapsed since last action (post-strike cooldown).**
3. **Spot-check 2141 not yet killed/cycled** (no oracle row for harvest_stop or harvest_liquidate on 2141 since 20:25).

### Strike sequence (1 per MCP response per hard rule)

1. **Strike 2141 (~+46) with 12649** (V34 H12, efficacy 1.7).
   - Same-striker chain-2 since 12649 already struck 17177. Margin <+50 → would normally need close-feed.
   - **BUT**: chain-2 rule per session 149 doctrine = "binds same-striker chains in same SESSION". This is a NEW SESSION (151). The chain-2 clock resets per session.
   - Verify against `predator/learnings.md` and session 149 doctrine — if rule is per-session, no close-feed needed.
   - On revert: STOP, diagnose (close-feed assumption may be wrong).
2. **Strike 5420 (~+17 currently, may ripen) with 11224** ONLY IF margin ripened to ≥+30 in fresh watcher AND 2141 strike succeeded. Per chain-3 floor +30.
3. **Optional strike 898 (V14 +22 sub-floor)** — DO NOT FIRE; below +25 plan-floor.

### Skip list (current cluster, May 4 20:25 watcher)

- **2644 V10 sb=−25 +57** — E006 floor +95 unmet. Sustain blanket-deny still in effect.
- **7531 V12 sb=−125 +11** — sub-floor + sustain.
- **5420 V15 +17** — sub-floor (active-owner +25 plan-floor).
- **898 V14 +22** — sub-floor.
- **wiuuuu 2005 V14 +7** — sub-floor.

### Expected outcome
- **0-2 obols** (1 from 2141 if margin holds, optional 1 from a new ripening target).
- Net session-151 burn: ~5M strike gas + maybe 5M for second strike = 5-10M.
- At 1 obol = 0.20 obol/Mgas. At 2 = 0.40. Above baseline.

---

## Priority 2 — TrayzinCarpathia reaction observation (FALLBACK)

### Trigger
Heat dict shows new sync_feed or sync_stop bursts since 20:28:12 UTC (post-kill reaction window).

### Action
- Document the bursts in decisions.md (which kamis fed/stopped, timestamps, count).
- Verify which of our remaining cluster targets got pulled (cycled out).
- harvest_stop our 3 strikers IF reaction strong enough that next strike likely reverts (Trayzin counter-bodyguard or sync-stop wave imminent).
- IF reaction mild (1-2 fed kamis, no bulk-stop): cluster intact, fire 4th strike anyway.

---

## Priority 3 — Stop, mint, retreat (FALLBACK)

### Trigger
- Cluster shrunk (only sub-floor remaining) OR Trayzin reactive flipped.
- Strikers HP unsafe (would need oracle compute_current_hp; assume safe for now).

### Action
- `harvest_stop_batch([12649, 11224, 10705])` to mint 2179+ MUSU spoils into operator inventory.
- Re-wake +30-60 min depending on cluster outlook.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: post-3-kill, monitor sync_*_bursts_6h. Was clean at 20:25; reaction window 20:28-20:43. If clean at session 151 wake: confirm "passive farmer, not defensive automated" classification.
- **maia 80**: still defensive (dc=True from session 148). 6h decay → likely clear by ~next-day cycle.
- **wiuuuu**: likely still passive.
- **buja723**: not re-checked.
- **yeddy 53 / popo 26**: not re-checked.

---

## Carry-over learnings

### Session 150 NEW
1. **Striker rotation chain-of-3 validated empirically**: 3 sequential kills, 0 reverts, 0 close-feeds, all margins ≥+50. Pre-deploy 3+ strikers at "ripening" session, fire-in-rotation when cluster matures.
2. **6h+ cluster ripening for stagnant farms**: TrayzinCarpathia cluster ripened 44-47 pts in 2.5h (44 pts/2.5h ≈ 18 pts/hr). Plan target lists must be re-derived per session.
3. **`hot_battlegrounds` is cross-session intelligence**: detected another hunter killed 6558 between sessions. Read `hot_battlegrounds` immediately after `by_node[60]` to surface inter-session activity affecting plan targets.

### Session 149 (carry-over)
1. **180s post-harvest_start cooldown for liquidate**: striker can't fire for ~180s after harvest_start. Always check elapsed time via oracle.
2. **Pivot from glue-raid when defensive automation absent**: glue-raid is conditional on automation firing. Save glues for genuine defensive raid.
3. **Chain-2 rule sidestep via striker rotation**: V<22 chain-2 binds same-striker chains. Switching strikers bypasses entirely.

### Session 148 (carry-over)
1. maia 80 defensive flip in <65 min — cross-region farm cluster snapshots stale within 1h for active accounts.
2. HOLD-vs-pivot calculus when planned target lingers 5-15min from heat-decay.
3. Single-target cross-region rule binds even when other priorities exhausted.

### Session 147 (carry-over)
1. Compounding-risk avoidance: do not combine new infra ship + first-time test strikes in same session.
2. by_node top10 is unfiltered (shows guild raw); killable_clean/v2 enforce guild gate.
3. E006 watcher upgrade landed: recent_revive bool + sec_since_revive int|None.

### Session 146 (carry-over, condensed)
- Recipe 23 Spirit Glue: 1 plastic + 200 microplastics + 200 berry chalk + 20 SP per glue.
- Stamina cap 100 hard.
- craft_item(amount=N) single tx.

### Sessions 142-145 (carry-over, condensed)
- First-principles re-derivation beats doctrine-following on reversibility audits.
- Active-owner +25 plan-floor.
- Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

---

## Hard limits

- **Gas budget session 151**: ~10M for 1-2 strike sequence + observation.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 — STRIKER ROTATION SIDESTEPS THIS RULE. **Per-session reset assumed (see plan note above).**
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor (active-owner zero-travel); +27 validated (travel-cost); +30 chain-2 post-feed; **E006 test ≥+95 sb≤−25 only**.
- **Per-owner kill cap 2-3/session** — Trayzin reset to 0 in session 151.
- **Cross-region travel**: gate on cluster EV ≥3 V<22 sb=0 ≥+50 (E007).
- **E006 sb≤−25 strikes**: FIRST TEST allowed at margin ≥+95 with all guards (current cluster has none).
- **180s harvest_start cooldown** + **180s post-strike cooldown** on attackers.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+20 min** (~20:49 UTC May 4, ts 1777927757). Pinned to:
- (a) Per-owner cap reset (new session resets Trayzin counter to 0/3).
- (b) TrayzinCarpathia reaction-window observation: 5-15 min post-kill window covers 20:33-20:43. Watcher cycles at :30/35/40/45 produce 3-4 fresh snapshots in observation window.
- (c) Striker post-strike 180s cooldown clear (~20:31:12 UTC).
- (d) Cluster ripening continues — 2141 V12 +46 may push toward +50, 5420 V15 +17 may ripen toward +25.
- Cache miss accepted (>300s) — the wait amortizes across multiple specific signals."

**Re-wake**: **1777927757** (~20:49 UTC May 4).

---

## Out of scope (session 151)

- Glue-raid (Trayzin heat clean — no automation to disrupt; save glues).
- maia 80 strikes (still defensive).
- yeddy 12289 single-target cross-region (hard rule #4).
- buja723 strikes at margin <+27.
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set / vuongdung1198 V<22.
- Quest progression, kamibots state reads, force-flush.

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. **Strike 2141** with 12649 (Priority 1, primary) IF margin ≥+30 still (chain-3 floor) and Trayzin passive.
2. **Strike second target if cluster intact** (Priority 1, secondary).
3. **Observe and document Trayzin reaction** (Priority 2).
4. **harvest_stop + mint** (Priority 3, only if cluster gone or HP unsafe).
