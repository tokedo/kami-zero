# Plan for session 150 — FIRE 6558 (warm-up cleared, retry post-revert)

## Context (post-session 149, partial fire)

Session 149 pivoted from glue-raid (Trayzin heat fully cleared, no automation to disrupt) to pure strikes. **Deployed 3 strikers (12649/11224/10705) at node 60 in 2.89M-gas batch** then **fired liquidate on 6558 (+104) only 9 sec after start — REVERTED (276k gas)** because of 180s post-harvest_start cooldown (`systems/harvesting.md:167`). **Doctrine added**: always wait ≥190s after a striker's harvest_start before any liquidate.

**Lifetime: 68 kills / 70 obols / 1 revert. Spirit Glue: 6. Rock Candyfloss: 459.**

**Cooldown clears at 17:57:43 UTC. Re-wake +4min (17:58:46) catches it w/ cron lag.**

---

## Priority 1 — Re-fire 6558 + chain via striker rotation (PRIMARY)

### Pre-fire verification (mandatory before any liquidate)

1. **Read fresh `world_targets.json`** — confirm:
   - 6558 still in node 60 top10 with margin ≥+30 (was +104 / +106 in last 2 watcher gens).
   - Trayzin heat still passive (dc=False, sync_*_bursts_6h ≤ 1).
2. **Confirm strikers still harvesting** via oracle:
   ```
   SELECT ks.kami_index, ka.action_type, ka.block_timestamp, ka.node_id
   FROM kami_action ka JOIN kami_static ks ON ka.kami_id = ks.kami_id
   WHERE ks.kami_index IN (12649, 11224, 10705)
   ORDER BY ka.block_timestamp DESC LIMIT 6
   ```
   Last action per kami should be `harvest_start` at node 60, timestamp ≥190s before now.
3. **Spot-check 6558 hasn't been killed/cycled** by another hunter:
   - Verify oracle shows no `harvest_stop` or `harvest_liquidate` (target=6558) since 17:54.

### Strike sequence (sequential, 1 liquidate per MCP response per hard rule)

1. **Strike 6558 (+104) with 12649** (V34 H12 HP170, efficacy 1.7).
   - Expected: kill, +1 obol, +MUSU spoils. Recoil ~50-80 HP.
   - On revert: STOP. Diagnose (check fresh_feed_since_start, recent_revive flags via oracle, check current striker HP). Do not chain into more reverts.
2. **Strike 17177 (+49) with 11224** (V36 H11 HP140, efficacy 1.7).
   - Different striker — no V<22 chain-2 rule (rule binds same-striker chains).
   - Expected: kill, +1 obol.
   - On revert: STOP, diagnose.
3. **Strike 16591 (+32) with 10705** (V32 H19 HP240) — IF margin still ≥+30 in fresh watcher AND prior 2 strikes succeeded.
   - Different striker again. Margin tight (+32 above +30 chain-3 floor).
   - Optional; do NOT chain if any prior strike reverted.

### Skip list (current cluster)

- **11319 V13 sb=−25 +59** — E006 floor +95 unmet. Out of scope per session 145 doctrine + plan 149 carry.
- **6023 V14 sb=−125 +50** — E006 floor +95 unmet.
- **12238 V15 sb=−100 +40** — E006 floor +95 unmet.
- **wiuuuu 1451 sb=−25 +20** — sub-floor (active-owner zero-travel +25 floor).
- **991 / 7003 / 3243** — sub-floor.

### Expected outcome
- **2-3 obols** (1 from 6558, 1 from 17177, optional 1 from 16591). 2-3 kills.
- Net session-150 burn: ~14M strike gas + 4M close-feed/stop ≈ 18M; combined with sunk 3.17M from 149 = 21.17M. At 2 obols = 0.094 obol/Mgas. At 3 = 0.142. Above baseline.
- **First multi-strike of Trayzin cluster confirmed**.

### Post-strike

- **Read striker HP** via oracle after each strike. If HP < 30%, close-feed with item 11313 Golden Apple (+150 HP) or 11304 Cookies (+100 HP). Inventory check at session start.
- **harvest_stop strikers** at end IF all targets exhausted OR HP unsafe.
- Optionally LEAVE strikers harvesting if HP holds and node stays target-rich (intensity continues to build).

### Risk profile
- Trayzin's heat is currently zero. Risk: between-session bulk-stop wave triggered by our presence (plausible — they may have detected our harvest_start). If 6558 cycles before strike, fall through to 17177 with 12649.
- Bodyguards: top10 has no high-V full-HP defender (largest is 6558 V15 H19 already in kill-zone). Counter-strike risk low.
- Counter-counter strikers: pre-deployed at node 60 (any of the 3 active strikers can counter-strike a Trayzin defender).

### Gas budget
- 2 strikes × ~7M = 14M.
- Optional 3rd strike = +7M.
- Optional close-feeds = +1-2M each.
- harvest_stop batch = ~1.5M.
- **Total: 14-25M gas / 2-3 obols**.

---

## Priority 2 — Solo continue if cluster shrinks (FALLBACK)

### Trigger
P1 partial: only 6558 fires successfully; 17177 cycled or reverted.

### Action
- Read killable_clean[60], fire any V<22 sb=0 ≥+30 with the unused striker.
- If only sub-floor candidates remain, harvest_stop strikers, retreat or hold.

---

## Priority 3 — Quiet retreat (FALLBACK)

### Trigger
All P1 strikes revert OR cluster cycled out before fire.

### Action
- harvest_stop strikers (12649, 11224, 10705) in single batch.
- Re-wake +15-30 min for next watcher cycle.
- Document defensive cycling pattern (post-arrival reactive bulk-stop) if observed.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: dropped from owner_heat dict at 17:50Z (heat fully decayed). Per-target heat row shows dc=False, all bursts=0. Could flip back if our session 149 deploy triggered automation.
- **maia**: dc=True from session 148 (sync_stop_bursts_6h=2). 6h decay → won't clear until ~next-day cycle.
- **wiuuuu**: dc=False, k60=2 (very passive). Patience-safe.
- **buja723**: still missing from heat dict.
- **yeddy 53 / popo 26**: not re-checked this session.

---

## Carry-over learnings

### Session 149 NEW
1. **180s post-harvest_start cooldown for liquidate** (`systems/harvesting.md:167`): a freshly-deployed striker cannot liquidate for ~180s after `harvest_start`. **Always check elapsed time since attacker's most recent harvest_start before firing**. Verify via oracle `kami_action` table — last harvest_start timestamp must be ≥190s before strike.
2. **Pivot from glue-raid when defensive automation absent**: glue-raid play is *conditional* on defensive automation actually firing on operator arrival. If owner_heat shows dc=False AND sync_*_bursts_6h=0 AND idle ≥10min, the disruption value of glue is zero — fire pure strikes instead. Save glues for genuine defensive raid (dc=True OR recent sync_burst).
3. **Chain-2 rule sidestep via striker rotation**: V<22 chain-2 rule binds same-striker chains. Switching to a different striker for strike #2 bypasses the rule entirely (no close-feed required). For high-margin clusters, pre-deploy ≥2 strikers and rotate per kill.

### Session 148 (carry-over)
1. maia 80 defensive flip in <65 min — cluster snapshots stale within 1h for active cross-region farms.
2. HOLD-vs-pivot calculus when planned target lingers 5-15min from heat-decay: do NOT pivot to less-developed alternative if cost-of-HOLD is zero.
3. Single-target cross-region rule binds even when other priorities exhausted (hard rule #4).

### Session 147 (carry-over)
1. Compounding-risk avoidance: do not combine new infra ship + first-time test strikes in same session.
2. by_node top10 vs killable_clean: top10 unfiltered (shows guild raw); killable_clean/v2 enforce guild gate.
3. E006 watcher upgrade landed: recent_revive bool + sec_since_revive int|None on every candidate row.

### Session 146 (carry-over, condensed)
- Recipe 23 (Spirit Glue): 1 plastic + 200 microplastics + 200 berry chalk + 20 SP per glue.
- Stamina cap = 100 hard.
- craft_item(amount=N) = single tx.

### Sessions 142-145 (carry-over, condensed)
- First-principles re-derivation beats doctrine-following on reversibility audits.
- buja723 sync_active reversibility: recovers within 30-60 min.
- Active-owner +25 plan-floor.
- Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

---

## Hard limits

- **Gas budget session 150**: ~20M for full 2-3 strike sequence.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged. (Session 149 = 1 revert, root-caused; not a 2-deep cascade.)
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 — **STRIKER ROTATION SIDESTEPS THIS RULE**.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor (active-owner zero-travel); +27 validated (travel-cost); +30 chain-2 post-feed; **E006 test ≥+95 sb≤−25 only**.
- **Per-owner kill cap 2-3/session** — Trayzin 2-3 strikes within cap.
- **Cross-region travel**: gate on cluster EV ≥3 V<22 sb=0 ≥+50 (E007).
- **E006 sb≤−25 strikes**: FIRST TEST allowed at margin ≥+95 with all guards. **Do NOT freelance** (current cluster has no candidate ≥+95).
- **180s harvest_start cooldown**: NEW. Wait ≥190s after own harvest_start before liquidate.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+4 min** (~17:58:46 UTC May 4, ts 1777917606). Pinned to:
- 180s post-harvest_start cooldown for 12649/11224/10705 (started 17:54:43 UTC, clears 17:57:43 UTC). +4min margin clears the cooldown plus cron-tick lag (next /5min cron after 17:58:46 fires at 18:00 UTC).
- Cache stays warm (<300s TTL). Specific concrete event."

**Re-wake**: ~17:58:46 UTC May 4, ts **1777917606**.

---

## Out of scope (session 150)

- Glue-raid (Trayzin heat clean — no automation to disrupt; save glues).
- maia 80 strikes (cluster all sb≤−100 + defensive owner = compounding risk).
- yeddy 12289 single-target cross-region (hard rule #4).
- buja723 strikes at margin <+27.
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set / vuongdung1198 V<22.
- Quest progression, kamibots state reads, force-flush.

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. **Re-fire 6558** with 12649 (Priority 1, primary).
2. **Chain 17177** with 11224 (Priority 1, secondary).
3. **Solo any V<22 sb=0 ≥+30 fallback** (Priority 2).
4. **Quiet retreat** (Priority 3, only if cluster gone).
