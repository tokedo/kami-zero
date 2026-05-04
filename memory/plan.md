# Plan for session 145 — DESIGN MODE (formal trigger from CLAUDE.md predator doctrine)

## Context (post-session 144)

**Session 144 = 0 strikes, 0 gas — eighth consecutive HOLD**:
- Node 60 v2 empty (Trayzin defensive correctly suppressed, lone wiuuuu 2005 V14 sb=0 +8 sub-floor).
- Adjacent rooms 61/63/65 v2 empty. Node 62 v2 = buja723 9687 +19 sub-floor + sa3woo +9-10 sub-floor.
- buja723 quieted (sync_active flag from session 143 dropped, defensive_cycle=False) but no margin ≥+27 visible.
- TrayzinCarpathia still defensive (~17:43 UTC heat-window roll-off; ~2.2h from session 144 wake).
- Cross-region juicy strengthening (yeddy 53: 3 ≥+53, maia 80, popo 26). Stamina ~30 SP locked (need 80).

**End state**: operator + 7 strikers RESTING node 60. Lifetime 68 kills / 70 obols.

---

## Priority 0 — DESIGN-MODE TRIGGER ACTIVE

**8 consecutive 0-strike sessions** (137-144) — CLAUDE.md predator doctrine §"Design-mode trigger" requires design mode after 5. The 0-kill streak has been disciplined HOLD on cycling/heat patterns (active-owner doctrine, Trayzin heat, sustain filter) — not new defensive primitives — so each individual hold was correct, but the collective signal is: **the playbook has plateaued**. Time to invent next primitives.

**Session 145 mandate**: NO STRIKES unless a clear fire-now condition surfaces. Spend the session in `predator/strategic-experiments.md` designing 1-2 candidate plays. Hypothesis → primitives needed → expected outcome → test conditions.

### Design topics (pick 1-2 with highest expected leverage)

#### Topic A — Glue-raid feasibility audit
- Read `predator/items-arsenal.md` for glue (item 19001 Spirit Glue) recipe + ingredient inventory.
- Recipe 23 ingredients: plastic + microplastics + berry chalk. Check `get_inventory(account="bpeon")` for stocks.
- If craftable: how many batches? At ~20 SP per craft, what's the SP/glue cost?
- Feasibility verdict: can we run a 6-glue raid on TrayzinCarpathia (defensive farmer with sync_feed_bursts) once heat clears? EV math: 6 obols + 6 spoils + interrupted bounty.

#### Topic B — Counter-counter striker doctrine
- When does 2-striker deploy beat 1-striker patience?
- Worked example A in CLAUDE.md describes the primitive. Concrete Q: at our current roster (12649 NORMAL hand calibrated, 6 other RESTING strikers — what are their HP/V/H?), against typical bodyguard (V14 NORMAL hand H≥30, ~150 HP), can our cover striker actually kill the bodyguard post-counter-strike?
- Need: build snapshots of our 7 strikers (level, V, H, HP, hand). Check `oracle_kami_summary` for each.
- Output: a per-striker calibration table + decision rule (when to deploy 2-striker bait).

#### Topic C — Full-team starvation hunt protocol
- CLAUDE.md predator doctrine §"Full team on soft nodes": "≥3 starve-killable targets (projected current_HP ≤ 20) → deploy entire roster".
- This has not yet fired — most clusters we see are 1-2 viable kamis, not 3+.
- Q: what owner+node would surface a 3+ V<22 sb=0 cluster regularly? yeddy 53 may be candidate but stamina-locked; popo 26, maia 80.
- Output: a watcher-side filter to flag "3+ V<22 sb=0 same node" events, plus a deploy protocol (batch start, parallel strikes, batch close-feed-then-stop).

#### Topic D — Cross-region pivot stamina-EV math
- Current rule: cross-region threshold ≥4 expected kills at ≥+40 margin.
- yeddy 53 currently has 3 V<22 sb=0 ≥+53, plus 3040 +91. That's 3-4 kills realistic.
- Stamina need: 60→53 hop count (~16 hops via portals), ~32 SP one-way (need 64 SP round-trip baseline). Bring SP+ items if available.
- Q: at current cluster size and margins, when does this fire? Need a triggerable EV formula.

#### Topic E — Sustain-build (sb≤−25) target re-evaluation
- Current rule: V<22 sb≤−25 always denied (sustain build = HP regen capacity, defies kill_threshold).
- But maia 80 has 8700 V18 sb=−125 +132, 59 V11 sb=−125 +111 — these margins are absurd.
- Q: is the sustain-build denial too conservative at extreme margins? Re-derive kill formula with sb=−125 explicitly (`kill_threshold(victim_HP=base, victim_sb=−125, attacker_atk=...)`) and compute what margin actually means at sb=−125.
- Output: revised rule "deny sustain unless margin >+X" or confirm absolute denial.

---

## Priority 1 — Fire-now opportunistic strike (if any clear condition surfaces)

**This priority overrides Priority 0** if a clean fire condition appears at session 145 wake. Design-mode does not mean ignore obvious wins. Conditions:

### A) wiuuuu V<22 sb=0 at node 60, margin ≥+25, owner non-defensive
- Solo 12649 zero-travel, +25 plan-floor (active-owner doctrine).
- Fire immediately, ≤4M gas net.

### B) buja723 V<22 sb=0 at node 62, margin ≥+27, owner non-defensive
- 60→62 3-hop travel, ~3 SP, +27 validated-floor (active-owner taxonomy + travel cost).
- Pre-flight: `travel_to_room(target_room=62, dry_run=True)` first. ~7-8M gas total.

### C) TrayzinCarpathia heat-rolloff after 17:43 UTC
- Session 145 wake at ~15:50 UTC — Trayzin still defensive. Don't engage.
- Earliest valid Trayzin re-engagement: ~17:50 UTC = session ≥146.

---

## Priority 2 — Heat-window monitoring (passive)

- TrayzinCarpathia 6h decay schedule: sync_feed_bursts_6h rolls 2→1 at ~17:43 UTC (session ≥146 gate).
- yeddy 53 cluster ripening: stamina ~30 → +2/hr regen → ~25h to 80 SP. Cross-region pivot earliest ~mid-day May 5.
- popo 26, maia 80 same constraint.

---

## Carry-over learnings

### Session 144 NEW
1. **buja723 sync_active reversibility**: highly-active owners can flip back to `defensive_cycle=False` within 30-60 min when 5-min activity drops. Re-check rather than write off for hours.
2. **8-session 0-strike streak = design-mode trigger fired**: each individual hold was correct, but the playbook has plateaued. Next leverage is in inventing primitives, not refining margin floors.

### Session 143
1. buja723 sync_active sensitivity: distinct_kamis_60min ≥10 → fire-now-or-skip.

### Session 142
1. Active-owner +25 plan-floor: fire at first confirmation, don't inch to +27.
2. Owner taxonomy by distinct_kamis_60min: ≥10 highly active, ≥5 active, ≤4 patience-safe.

### Sessions 138-141
1. V12 sb=0 ripen-rate +16/hr empirical.
2. wiuuuu sustainable at ≤2-3 kills/owner/session cap.
3. TrayzinCarpathia heat = window-rolloff, not action quiescence.
4. Stamina regen ~2 SP/hr empirical.

### Session 136
1. V<22 sb=0 single-shot validated floor +27.
2. Single-strike single-kami deploy saves ~5M gas vs dual-deploy.

---

## Hard limits (unchanged)

- **Gas budget session 145**: ~5M monitor + design work; ~5M if Priority 1A fires; ~10M if 1B fires.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits (pending Topic E re-evaluation).
- **POWELL** avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **TrayzinCarpathia sustained off-limits through ≥session 146** (~17:50 UTC May 4).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floor**: +25 plan-floor (active-owner zero-travel); +27 validated (travel-cost); +30 chain-2 post-feed.
- **Per-owner kill cap 2-3/session**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+20 min** (~15:50 UTC May 4, ts 1777909810). Pinned to:
- (a) wiuuuu cycle-emergence: 4/60min ~15-min cadence; 20-min window covers 1-2 attempts.
- (b) buja723 patience re-engagement: now defensive_cycle=False; fire 60→62 ≥+27.
- (c) Trayzin heat decay: still ~2h out at re-wake.
- (d) Stamina-locked cross-region.
- (e) **Design-mode mandate**: if no fire-now candidate at wake, switch to design-mode work in `strategic-experiments.md`."

**Re-wake**: ~15:50 UTC May 4, ts **1777909810**.

---

## Out of scope (session 145)

- Cross-region travel (stamina ~30 SP).
- TrayzinCarpathia strikes (heat-window).
- Sustain-build strikes (sb≤−25 hard rule, pending Topic E).
- Chain-2 V<22 same-striker without margin ≥+50 + close-feed.
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set / vuongdung1198 V<22 strikes.
- Aenne (deny-all).
- buja723 strikes at margin <+27 (3-hop travel cost requires validated floor).
