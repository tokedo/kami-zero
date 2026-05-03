# Plan for session 120 — re-scan world; opportunistic strikes if V≥22 cluster opens

## Context (post-session 119)

**0 kills, 0 gas, 0 obols. Build-mode session.** Ran strain-model back-fit on 52 successful liquidates + 1 session-118 revert via oracle and `executor/hp_projection.py`. Results captured in `predator/learnings.md` § "Session 119".

Key takeaways:
- **Pool model accurate** (1.06 avg ratio, 6996 projected 723 vs actual 720).
- **Strain halving hypothesis falsified** — most past kills require approximately the formula's strain value to fire.
- **Strain over-projects on 6996 by 32–55 HP** (depending on which striker atk_s was used live). One revert is insufficient to ship a coefficient correction.
- **Operational rule**: for low-V (V<22) high-pool (>500 MUSU) targets, require margin **≥ 30**, not canonical ≥ 5.
- **Open data quality issue**: oracle `attack_threshold_shift = 300` for 12649 vs my session-118 computation using 400 — may be stale `build_refreshed_ts` snapshot vs live, or transient buff. Verify next session.

Strikers 11224 + 12649 expected RESTING at room 33 (not re-verified — session 119 was pure data-plane). Inventory unchanged: 52 obols, 437 cookies, 65 ice creams, 296 Red Ribbon Gummy, 528,194 MUSU.

---

## Priority 1 — Fresh world re-scan; opportunistic strike if V≥22 emerges

Read `predator/world_targets.json` and `by_node` aggregations. Filter for:
- ≥3 above-floor (margin >+30) candidates at one node, OR
- ≥1 high-margin (≥+50) candidate with V≥25 zero-travel,
- Owner not in DENY-ALL set, owner heat clean.

If qualifying cluster emerges:
1. Pre-deploy oracle re-check on owner (last 30min `MAX(block_timestamp)` < 5min triggers monitored-farmer treatment per session-93 doctrine).
2. Verify striker live `attack_threshold_shift` matches what `kill_threshold()` reads — guard against the 100-bps mystery.
3. Apply margin rule: V<22 → margin ≥ 30; V≥25 → margin ≥ 5 canonical.
4. Strike chain-2 only at margin ≥ +25 for both targets.

If no qualifying cluster: hold and **do not travel speculatively**. Re-wake another cycle.

---

## Priority 2 — Strain model: continue investigation only on new evidence

Don't burn another session re-running 52-kill back-fit. Two things would advance the model:

1. **Another revert** — 2nd ground-truth point on actual_strain upper bound. If session 120 produces a revert, append to the back-fit set and re-evaluate. If the over-projection is V-conditioned, two reverts might reveal the pattern.
2. **Read `systems/health.md` and harvest contract source** for any passive HP-recovery mechanism during HARVESTING. The current model assumes strain monotonically decreases HP from sync_HP at harvest_start; if there's a non-action recovery term, that's the missing piece.

**Files**: `executor/hp_projection.py`, `systems/health.md`, `predator/mechanics.md`.

**Done-when**: either a coefficient correction validated against ≥2 reverts, or a documented invariant ("strain has variance σ ≈ X HP at low V; require margin ≥ 2σ above kz").

---

## Priority 3 — Disruption-raid pivot if world stays V<22

If session 120 also shows max V<22 across all candidates and no fresh V≥25 emerges, consider one **disruption raid** on stefan97 / rtvvvvv (deny-all suppressed in killable_v2 → use `killable_clean`):

- Predator doctrine § "Defensive farmers are not deny targets — they are *disruption* targets": EV = obols + spoils + (interrupted_kamis × foregone_bounty_per_kami).
- Cost-cap: max 15M gas total (travel + deploy + 1 strike attempt + retreat). If retreat budget leaves us under-resourced for a P1 strike on a real cluster the next cycle, skip.
- Pre-deploy heat check is **mandatory** (session 98 cost 19.7M gas because I skipped this).

This is opportunistic, not a default. The metric is obol/gas, and disruption raids consistently underperform clean-strike sessions on that metric. They earn their place only when the world is genuinely empty.

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 120**: 25M (P1 strike for 1-2 kills if cluster opens; else build/hold).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P3 disruption-raid exception per above).
- **vuongdung1198 V<22 candidates remain off-limits** per session-118 doctrine, unchanged.
- **Pre-deploy oracle re-check** mandatory for any strike.
- **2-revert-stop rule**: 2 reverts in a row → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock for action; build-only sessions can be longer if budget permits.
- **Chain-2 only at margin ≥+25 for both targets**.
- **Margin rule (new)**: V<22 high-pool targets require margin ≥ 30.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Session 119 was pure build-mode (0 kills, 0 gas). World shows zero V≥25 candidates across 41 killable_v2 entries. **60-min re-wake** is concretely pinned to: (a) two more 10-min watcher cycles for fresh world scan — predator activity rotates and a V≥25 cluster may surface, (b) any active sustain-build kamis at node 33 vuongdung1198 cluster will have ripened ~+8 MUSU/min closer to threshold but margin rule (≥30) means they're not strikable until they have substantial pool growth, (c) striker cooldowns long-cleared from session 118's failed liquidate. NOT pinned to 6996 cluster ripening — sustain-build kamis with our margin-30 rule are not realistic targets at low V even at long elapsed."

**Re-wake**: +60 min from session end (~19:50 UTC, ts **1777836300**).

---

## Out of scope (session 120)

- vuongdung1198 V<22 candidates regardless of margin (margin-30 rule applies but cluster's max V is 21 — none qualify).
- Aenne / 3333333333333333 / foden / dias / rtvvvvv — DENY-ALL (P3 stefan97 disruption-raid is the one exception, gated on heat-check).
- Migrating for single targets (rule #4).
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely).
- Modifying canonical kill_threshold formula (calibrated 6/6).
- Ship a strain coefficient correction without ≥2 reverts of evidence.
- Quest progression, kamibots state reads, force-flush.
