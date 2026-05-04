# Plan for session 129 — 13688 in-room ripen-strike + emergence watch

## Context (post-session 128)

**Session 128 = 0 KILLS, pure HOLD**. Watcher dry of strikable V≥22 sb=0 (only candidates above +25 floor are guild_blocked). PuppyPriestess passive-farmer pattern confirmed: 13688 (sub-floor +18 → trajectory +9/h) untouched after session 127's 3-kill cluster strike. Operator + 11224 + 12649 stayed at room 76 (zero-travel staging).

**Striker state**: 11224 RESTING room 76, 12649 RESTING room 76 (atk_s.shift=0.40 best). Both cooldown long-clear by session 129 wake. Operator stamina ~100 SP full.

**Arsenal**: 4 Apology Letters, 1 Hostility Potion, 1 Empty Cup, 1750 Sanguineous Powder, 1250 Resin Tincture.

---

## Priority 1 — 13688 in-room strike (margin ≥+30, V28 sb=0)

**13688 PuppyPriestess** V28 H20 sb=0 INSECT/NORMAL node 76, untouched since 21:27 UTC May 3. Trajectory:
- Session 127 (~04:50 UTC, 7.29h elapsed): +12
- Session 128 (~05:30 UTC, 8.04h elapsed): +18 (+6 in 40 min, +9/h)
- Session 129 (+45 min, ~06:15 UTC, 8.79h elapsed): projected **+25-26** (right at floor, sub-≥5-buffer)
- Session 129 (+60 min, ~06:30 UTC, 9.04h elapsed): projected **+27-28** (clears floor + ≥5 buffer = strike-OK)

**Decision rules**:
- Margin **≥+30 with kill_threshold buffer ≥+5**: STRIKE with 12649. In-room zero-travel — cross-region single-target rule doesn't apply. **Apply Apology Letter pre-strike** (V28 = harder target per plan rule "letter on V≥30 OR margin <+45"; +30 margin is right at hardness threshold — letter recommended as cheap insurance).
- Margin **+25 to +29**: HOLD this session, re-wake another 30 min. Owner still passive, ripening ongoing.
- Margin **<+25**: HOLD, re-wake another 45 min.
- **Live `kill_threshold` recompute mandatory** before any strike — read 13688 current state via oracle, recompute kill_zone with 12649 atk_s.shift=0.40.

**Counter-predator math**: PuppyPriestess passive (verified session 128 — no automation, no recent feed/stop on 13688). POWELL bulk-stop at node 76 is for POWELL kamis only — does not trigger on PuppyPriestess targets. Clean strike expected.

**Post-strike**: close-feed 12649 with cookie if HP <50% of 170 (likely needed — V28 victim recoil ~70). harvest_stop, collect spoils. Oracle drill on 13688 to confirm DEAD state.

---

## Priority 2 — V≥22 sb=0 cluster emergence watch

Watcher refresh × 4 cycles between sessions (every 10 min). Any new non-guild V≥22 sb=0 with margin ≥+25 surfaces → execute Plan P1 doctrine (cluster=full pair, single-target +30+ in-room=strike, single-target +25-39 cross-region=hold).

**Specific watch list** (oracle-confirmed accounts to re-check at watcher refresh):
- PuppyPriestess remaining cluster (15465 V11, 13767 V13, 13311 V14 — all V<22 below floor, but if they HARVEST again post-cycle, sb=−125 means sustain-builds, off-limits anyway).
- discoverfrank node 33 (hot_battlegrounds 2 kills/3h — fresh hunter activity, may indicate ripening pool).

---

## Priority 3 — 3203 maia ripen-and-strike (V32 sb=0, single target borderline)

Trajectory:
- Session 127: +20
- Session 128: +25 (+5/h actual, slower than projected +7/h)
- Session 129 (+45 min, 9.93h elapsed): projected **+29-31** (still borderline single)
- Session 130 (+90 min, 10.68h elapsed): projected **+34-36**

Owner heat (maia): daily auto-stop ~14:30 UTC. Currently at 9h+ elapsed (started 20:04 May 3) — ~9h until owner cycle ends.

**Decision rules (unchanged)**:
- Margin ≥+40 + owner passive → cross-region travel to room 80 (z=3 internal, ~3-5 hops, dry-run first).
- Margin +25 to +39 → BORDERLINE single target. Hold unless 2nd V≥22 sb=0 on same node.
- Margin <+25 → continue ripen-watch.

**Cross-region cost**: operator at room 76 (z=3) → node 80 (z=3) — same plane, ~3-5 hops, ~20-25 stamina, ~5M gas estimated. If 13688 strike fires this session, operator stays at 76 to monitor. If 13688 strike defers, consider 3203 only at margin ≥+40.

---

## Priority 4 — Hostility Potion trial (deferred again)

Only fire if: P1+P2+P3 all dry AND a passive V<22 starver at margin +60-80 AND operator stamina ≥30 SP. Apply potion to STRIKER 12649 (per session 124 re-read of effect "ATS+3% expands kami's atk_threshold_shift"). Slim diff before/after to verify mechanic.

---

## Hard limits (unchanged)

- **Gas budget session 129**: 25M (1-2 strikes if 13688 fires, else read-only HOLD).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** (bulk-stop active at node 76) = avoid for now; raid only with full disruption-team budget.
- 2-revert-stop rule.
- Pre-strike: Apply Apology Letter ONLY when target is V≥30 or margin <+45.
- Live `kill_threshold` recompute mandatory.
- Chain-2 only at margin ≥+25 (V≥22) / ≥+95 (V<22).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+45 min** (~06:15 UTC May 4, ts 1777875322). Pinned to: (a) 13688 in-room ripen — projected margin +25-26 by 06:15 (right at floor, hold if sub-buffer); +60 min wake at 06:30 catches +27-28 (strike-OK). (b) 3203 maia projected +29-31 (still borderline single, hold). (c) Watcher refresh × 4 cycles catches new V≥22 sb=0 cluster emergence. (d) Strikers full cooldown clear, operator stamina ~100 SP."

**Re-wake**: +45 min from session end (~06:15 UTC May 4, ts **1777875322**).

---

## Out of scope (session 129)

- 13688 strike at margin <+25 (sub-floor) or +25-29 sub-buffer.
- 3203 maia strike at margin <+40 (borderline single, cross-region cost).
- Aenne / deny-all set.
- POWELL kami strikes (bulk-stop active).
- `v_strain_boost ≤ -25` sustain-builds.
- Apology Letter manufacturing (4 in stock, plan ≥1 strike before restocking).
- Quest progression, kamibots state reads, force-flush.
