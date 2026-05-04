# Plan for session 152 — chain-3 strikes on ripened 898/5420 + cluster check

## Context (post-session 151, 1 kill / 1 revert at TrayzinCarpathia node 60)

Session 151 fired 1 successful strike (2141 V12 +56 with 12649) and 1 reverted strike (898 V14 +32 with 11224 rotation). Per 2-deep-revert-stop rule, stopped after revert. Empirical chain-3 striker-rotation floor RAISED from +30 (speculative) to **+50 (validated)**. TrayzinCarpathia confirmed passive farmer — zero defensive bursts in 20:33-20:43 reaction window after s150's 3-kill rotation.

**Lifetime: 72 kills / 74 obols / 2 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Strikers HARVESTING node 60 since 17:54:43 UTC (~4h+ at session 152 start). Post-strike 180s cooldowns long cleared.**

---

## Priority 1 — chain-3 strikes on ripened 898 and 5420 (PRIMARY)

### Pre-fire verification (mandatory)

1. **Read fresh `world_targets.json`** (watcher cycles at :30/:35/:40/:45/:50):
   - Confirm 898 V14 sb=0 ripened to **≥+50** (was +32 at 20:50, +24 pts/hr ⇒ ~+56 by 21:50). If still <+50: skip 898 this session.
   - Confirm 5420 V15 sb=0 ripened to **≥+50** (was +26 at 20:50 ⇒ ~+50 by 21:50). If still <+50: skip 5420 this session.
   - Confirm Trayzin heat still passive (dc=False, sync_*_bursts_6h=0).
   - Check `hot_battlegrounds` for inter-session kills at node 60 — if 898 or 5420 already killed by another hunter, skip them.
2. **Confirm strikers still HARVESTING** via oracle:
   ```sql
   WITH la AS (SELECT ks.kami_index, ka.action_type, ka.block_timestamp,
                      ROW_NUMBER() OVER (PARTITION BY ks.kami_index ORDER BY ka.block_timestamp DESC) AS rn
               FROM kami_action ka JOIN kami_static ks ON ka.kami_id = ks.kami_id
               WHERE ks.kami_index IN (12649, 11224, 10705))
   SELECT * FROM la WHERE rn=1 ORDER BY kami_index;
   ```
   Expect: most recent action = `harvest_liquidate` from session 150/151 (12649: 20:27:59, 11224: 20:28:05 [revert at 898? actually that's the success on 16591], 10705: 20:28:12). If `harvest_stop` appears: striker exited HARVESTING, must redeploy.

### Strike sequence (1 per MCP response per hard rule)

1. **Strike 898 (~+56 expected) with 11224** — same striker that reverted 898 at +32 in s151. Different margin. Margin ≥+50 should clear chain-3 floor.
   - On revert: STOP all strikes (2-deep-revert-stop on this cluster); diagnose (maybe build different from typical Trayzin, recompute floor).
2. **Strike 5420 (~+50 expected) with 10705** — chain-3 rotation continues. Margin marginal at +50; consider waiting another session if still <+55.
3. **Optional strike on a newly-surfaced ≥+50 target** with 12649 (if any).

### Skip list (current cluster, session 152 outlook)

- **2644 V10 sb=−25 +66+** — E006 floor +95 unmet. **All sustain (sb≤−25) candidates blanket-deny until E006 first-strike conditions met.**
- **7531 V12 sb=−125** — sub-floor + sustain.
- **6032 V10 sb=−125** — sub-floor + sustain.
- **wiuuuu 2005/4273** — sub-floor.

### Expected outcome
- **0-3 obols** (1 from 898 if ripened, 1 from 5420 if ripened, optional 1 from new target).
- Net session-152 burn: ~5-15M strike gas.
- At 1 obol = 0.20 obol/Mgas. At 2 = ~0.30. At 3 = ~0.40.

---

## Priority 2 — harvest_stop + mint (FALLBACK)

### Trigger
- Cluster shrunk (no candidates ≥+50) AND strikers have been HARVESTING ≥6h (mint compelling).
- Trayzin heat flipped defensive (would still be surprising — 5h+ post-kill window).

### Action
- `harvest_stop_batch([12649, 11224, 10705])` mints ~2867 MUSU pending spoils into operator inventory (688 from 2141 + 692/729/758 from s150 strikes).
- Re-wake +60-90 min for pool re-accumulation post-rest.

---

## Priority 3 — Pivot scout (FALLBACK)

If Trayzin cluster fully dead AND no other juicy ≥+50 V<22 sb=0 in killable_v2: scout a new node.

- Read `hot_battlegrounds` — where else are hunters scoring kills?
- Cross-check `killable_v2` for clean targets at non-60 nodes.
- Margin floor +27 (validated travel-cost) on cross-room moves.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: passive-farmer classification confirmed by s151 reaction-window-clean. Default assumption for s152: still passive. If heat dict shows ≥1 sync_burst since 20:28 last kill: re-evaluate.
- **maia 80**: still defensive (carry-over). 6h decay → likely clear by ~next-day cycle.
- **wiuuuu**: passive. Still no V<22 sb=0 ≥+25.
- **buja723 / yeddy 53 / popo 26**: not re-checked.

---

## Carry-over learnings

### Session 151 NEW
1. **Chain-3 striker-rotation floor = +50 (validated)**, not +30 (speculative). Revert at +32 confirmed. Plan template & doctrine updated.
2. **TrayzinCarpathia passive-farmer reclassified** via reaction-window-clean signal (zero bursts in 5-15 min post-kill window). Glue-raid pretext gone for this account.
3. **Cluster ripening rate ~24 pts/hr** at node 60 post-s150 (faster than s150's 18 pts/hr — leftover targets are higher-strain).

### Session 150 (carry-over)
1. Striker rotation chain-of-3 validated empirically at margins ≥+76.
2. 6h+ cluster ripening for stagnant farms.
3. `hot_battlegrounds` is cross-session intelligence signal.

### Session 149 (carry-over)
1. **180s post-harvest_start cooldown for liquidate**.
2. Glue-raid is conditional on defensive automation firing.
3. Chain-2 same-striker rule sidestep via striker rotation (margin floor still applies — see s151).

### Session 148 (carry-over)
1. maia 80 defensive flip in <65 min.
2. HOLD-vs-pivot calculus.
3. Single-target cross-region rule (hard rule #4).

### Session 147 (carry-over)
1. Compounding-risk avoidance.
2. by_node top10 unfiltered vs killable_clean/v2 enforcement.
3. E006 watcher upgrade landed.

---

## Hard limits

- **Gas budget session 152**: ~15M for 2-3 strike sequence.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floors (UPDATED s151)**:
  - +25 plan-floor (active-owner zero-travel, V≥22 or single-strike).
  - +27 validated (travel-cost).
  - **+50 chain-3 striker-rotation floor** (NEW — was +30, raised after s151 revert at +32).
  - +30 chain-2 post-feed (close-feed-then-strike).
  - **E006 sb≤−25 first-strike ≥+95** with all guards.
- **Per-owner kill cap 2-3/session** — Trayzin reset to 0 in session 152.
- **Cross-region travel**: gate on cluster EV ≥3 V<22 sb=0 ≥+50 (E007).
- **180s harvest_start cooldown** + **180s post-strike cooldown** on attackers.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+60 min** (~21:50 UTC May 4, ts 1777931400). Pinned to:
- (a) **Cluster ripening crosses +50 chain-3 floor**: 898 needs ~24 min from 20:50 to cross +50, +60 min gives buffer for variance and chain-2 with 5420.
- (b) Per-owner cap reset (new session resets Trayzin counter to 0/3).
- (c) TrayzinCarpathia long-tail reaction-window observation (6h cumulative window for sync_*_bursts; 1h22m post-last-kill captures any delayed automation).
- (d) Striker post-strike 180s cooldown (cleared 20:53 UTC, well past).
- Cache miss accepted (>300s) — wait amortizes across multiple specific signals."

**Re-wake**: **1777931400** (~21:50 UTC May 4).

---

## Out of scope (session 152)

- Glue-raid (Trayzin reclassified passive farmer — no automation to disrupt; save glues for foden/dias/stefan97/rtvvvvv-class accounts).
- maia 80 strikes (still defensive).
- yeddy 12289 single-target cross-region (hard rule #4).
- buja723 strikes at margin <+27.
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set / vuongdung1198 V<22.
- Quest progression, kamibots state reads, force-flush.
- Striking 898 if margin still <+50 (post-s151-revert this is the empirical floor).

---

## Bias fire-now

Default action ladder when nothing's pinned to a wait:
1. **Strike 898** with 11224 (Priority 1, primary) IF margin ≥+50 and Trayzin passive.
2. **Strike 5420** with 10705 (Priority 1, secondary) IF margin ≥+50.
3. **Strike new ≥+50 V<22 sb=0** with 12649 (Priority 1, tertiary).
4. **harvest_stop + mint** (Priority 2, only if cluster gone).
5. **Pivot scout** (Priority 3, only if Trayzin dead AND killable_v2 empty).
