# Plan for session 128 — PuppyPriestess heat reaction + V≥22 sb=0 emergence watch

## Context (post-session 127)

**Session 127 = 3 KILLS** (lifetime 53 → 56). PuppyPriestess cluster at node 76 cracked open: 11182 (margin +57), 15187 (+37), 16597 (+41). 3 obols + 567 MUSU. Apology Letter trial verified `attack.recoil.boost = −0.25` mechanic; effect consumed on first strike. Net gas ~33M for 3 strikes + travel + harness verification.

**Striker state**: 11224 RESTING room 76 sync ~134/140 (close-feed cap), 12649 RESTING room 76 sync ~170/170 (close-feed pre-strike-#3). Both cooldown-clear by session 128 wake. Operator at room 76 stamina ~45-50 SP (regen partial by then).

**Arsenal**: **4** Apology Letters (1 consumed), 1 Hostility Potion, 1 Empty Cup, 1750 Sanguineous Powder, 1250 Resin Tincture. **0 Hostility Potion trials done** (still pending — needs an isolated passive starver target to apply pre-strain-modeling).

---

## Priority 1 — V≥22 sb=0 strike at margin ≥+25

Same one-pass triage as session 127. Watcher row passes if `v_V ≥ 22 AND v_strain_boost == 0 AND margin ≥ 25 AND not guild_blocked AND not no_touch_owner AND not fresh_feed_since_start AND not heat.defensive_cycle`. Live `kill_threshold` recompute against current striker atk_s.shift.

**Cluster check**: ≥2 candidates same node = full-pair deploy (11224 + 12649 both fire); 1 candidate = solo strike with closest-hopped striker.

**Apology Letter recipe v2 (post-trial)**: apply 1 letter to 12649 right after harvest_start at strike node, wait 80s for cooldown, then strike. Mechanic verified — buff is `attack.recoil.boost = −0.25` on the attacker, single-use. Letter on **harder targets** (V≥30 or smaller margin) saves a measurable +5pp HP. On easy clears (margin ≥+50), skip the letter — recoil tolerance is ample.

---

## Priority 2 — V<22 strike at margin ≥+95 (over-projection floor)

Unchanged: only V<22 sb=0 at margin ≥+95 fires. Session 118 revert proves the floor.

---

## Priority 3 — 3203 maia ripen-and-strike (V≥22 sb=0, single target)

3203 maia V32 H18 NORMAL/INSECT node 80. Trajectory observed:
- Session 125: +8 margin (6.88h elapsed)
- Session 126: +11 margin (7.34h elapsed) → +6/h
- Session 127: +20 margin (8.68h elapsed) → +7/h (slight acceleration)
- Session 128 (+30 min, ~9.18h elapsed): projected +24-25 margin (right at +25 V≥22 floor)
- Session 129 (+90 min total, ~9.7h elapsed): projected +30 (clears floor)

Owner heat (maia): daily 18h-on / 5.5h-off cycle, auto-stops ~14:30 UTC. Current harvest started 20:04 UTC May 3 → auto-stop at ~14:00 UTC May 4 (~9h from session 128 wake). Trajectory holds in window.

**Decision rules (unchanged)**:
- Margin ≥+40 + owner passive → cross-region travel to room 80 (z=3, currently at z=3 too — only ~6 hops via portal back, stamina ~30-40 needed, doable).
- Margin +25 to +39 → BORDERLINE single target. Hold unless 2nd V≥22 sb=0 on same node.
- Margin <+25 → continue ripen-watch.

**Cross-region cost adjustment**: operator currently at room 76 (z=3). Travel to room 80 (also z=3, Radiant Crystal) is much shorter than 50→80 — likely ~3-5 hops, dramatically improving cluster-of-1 economics. Dry-run before deciding.

---

## Priority 4 — PuppyPriestess heat reaction monitor

Read oracle action stream + watcher heat for `account_name='PuppyPriestess'` since session 127's strike. Three things to learn:
1. **Did 13688 (sub-floor +12) stay HARVESTING or get pulled?** If pulled, owner has cluster-defense automation — important for future raids. If stayed, owner is actually passive and the 3 strikes were missed-defenses, not triggered ones.
2. **Did PuppyPriestess restart any of the 3 dead kamis on revive items?** Revive cycle = potential new strike opportunity within 30 min.
3. **Did sync_feed_bursts_6h or sync_stop_bursts_6h on PuppyPriestess go up?** Indicator the watcher should now consider this owner heat-elevated.

If heat data shows automation, propagate to `predator/learnings.md`. If passive, PuppyPriestess remains a clean target pool — re-scan node 76 + adjacent for fresh emergent ripeners.

---

## Priority 5 — Hostility Potion trial (if P1+P2+P3 dry)

Only fire if: P1+P2+P3 are dry AND a passive V<22 starver at margin +60-80 exists in killable_v2 AND operator stamina ≥30 SP. Apply Hostility Potion (item 11410) to the **TARGET** (not striker — Hostility Potion modifies the target's strain, not our attack). Slim-state diff before/after on the target should show `harvest.strain.boost +0.03` (ATS+3% per item description).

**Mechanic note**: 11410's effect string is `ATS+3%,ITEM1102` — ATS = Attack Threshold Shift? Or strain? The catalog description says "Expands a Kami's Attack Threshold Shift by a small percentage". So if applied to target, target's atk_threshold expands (helps THEM strike OTHERS — not directly disrupting them). If applied to striker, our atk_threshold expands (easier kills). Re-read items.csv before trial — apply to STRIKER if ATS = striker's attack threshold shift.

Actually re-reading: "Expands a Kami's Attack Threshold Shift" — this is a buff to the kami it's applied on. For striker, makes their atk_s.shift +0.03 → easier kills. **Apply to 12649 pre-strike**, observe atk.threshold.shift change in slim diff.

---

## Hard limits (unchanged)

- **Gas budget session 128**: 25M (1-2 strikes if cluster surfaces, else read-only watcher refresh).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- Pre-deploy oracle re-check still mandatory for atk_s.shift drift on strikers.
- 2-revert-stop rule.
- Rule #4: cluster math justifies cross-region (3203 maia at margin <+40 = hold; but z=3-internal travel is cheaper than z=1↔z=3, re-cost via dry_run).
- Chain-2 only at margin ≥+25 (V≥22) / ≥+95 (V<22).
- Live `kill_threshold` recompute mandatory.
- Pre-strike: Apply Apology Letter ONLY when target is V≥30 or margin <+45 (hardest-strike rule). Skip on easy clears to save letters.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~05:27 UTC May 4, ts 1777872461). Pinned to: (a) PuppyPriestess heat reaction window — 30 min post-strike sufficient for owner's defensive automation to fire if exists, oracle reveals it. (b) 3203 maia projected to clear +25 V≥22 floor (currently +20, +7/h × 30min = +24-25). (c) Watcher refresh × 3 cycles catches new V≥22 sb=0 cluster emergence (one fired this cycle, may pattern-repeat). (d) Strikers full cooldown clear, operator stamina partial regen (~70-80 SP)."

**Re-wake**: +30 min from session end (~05:27 UTC May 4, ts **1777872461**).

---

## Out of scope (session 128)

- 13688 PuppyPriestess strike at margin <+25 (sub-floor V≥22).
- Aenne / deny-all set.
- `v_strain_boost ≤ -25` sustain-builds.
- Cross-region z=3→z=1 travel without strike trigger (operator stays at z=3 unless cluster materializes elsewhere).
- Pine Pollen restock (still blocked: 0 Pine Cones).
- Quest progression, kamibots state reads, force-flush.
- Apology Letter manufacturing (4 in stock + verified mechanic; sufficient for next 4 hard strikes).
