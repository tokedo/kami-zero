# Plan for session 89

## Context (carry-over from session 88)

Bugs 1+2+3 in `executor/hp_projection.py` + `executor/oracle_state.py` are SHIPPED and cross-checked: founder-truth match at 0.40 HP / 0.12% pool error on 5 calibration kamis. Empirical kill_threshold cert holds at 99.60% on N=495 (canonical-as-derived from on-chain KAMI_LIQ_* underperforms at 98.18% — empirical retained as operational formula, canonical documented as reference in `predator/mechanics.md`).

**No strike happened in session 88** for two compounding reasons:
1. All 6 bpeon strikers were RESTING (12649 was respec'd at 20:13 UTC, 11224 cycled stop/start/stop ending RESTING at 19:17). Liquidation requires HARVESTING attacker.
2. Of all HARVESTING non-guild kamis on node 86 (where the team is parked, room 86, EERIE-INSECT dual): only kami 4045 (Alp135) had positive margin (+32.9 HP) at first scan — and within 3 minutes had transitioned to RESTING_OR_DEAD (someone else struck or owner stopped). Kami 9980 (Assassins, def_shift=0/def_ratio=0) is heal-event guarded (n_feeds_since_start=2). All other non-guild kamis on node 86 just started harvesting at 22:25-22:30 (~5 min ago), pools 3-9 MUSU, projected HP ≈ max-1.

## Priority 1 — Verify striker readiness, restart on node 86

Oracle says all 6 bpeon predators are `RESTING_OR_DEAD` (no open harvest_start in last-200-action window). Per CLAUDE.md "oracle is the single source of truth" but **chain is the staleness escape hatch when oracle's snapshot lags**.

1. Read 12649 + 11224 chain state directly (Web3 reads on `health.sync` + `state` component) to confirm RESTING and HP. If oracle says RESTING and chain agrees, proceed to step 2.
2. If HP > safety margin (e.g. ≥ 90% max), `harvest_start` on node 86 manually. Auto_v2 is paused for predator mode — manual restart is the deployment path.
3. If HP is low, wait one more cycle; do not restart at risky HP (recoil math gets ugly fast).

Do not move the operator. Operator was last placed at room 86 (when 11224 was placed for harvest_start at 19:16 UTC 2026-05-02). Predators on node 86 means room 86 is where everyone is.

## Priority 2 — Re-scan node 86 hunting field

By session-89 wake (+30 min), the lele/dias/cherki cluster (35+ kamis that just started at 22:25-22:30) will have ~30-50 min pools. Many will be near-killable. Re-run `/tmp/scan_remaining.py` (or copy into `executor/scripts/`).

Apply gates in order:
- Guild blacklist (fey-fey, Tonin, T0nin, Ton1n, buzz, pleaseonemoretim, Shadow3X confirmed in `predator/guild-no-touch.csv`)
- Heal-event guard (`n_feeds_since_start == 0`)
- Margin ≥ 5 HP (using corrected Bug 1+2+3 formula)
- Counter-predator scan: any HARVESTING kami on node 86 with V high enough to one-shot our striker post-kill

## Priority 3 — Re-check 9980 Assassins

If 9980 has had no further feed events AND the heal-event guard's underlying issue (sync_hp drift from un-collected feeds) has resolved via the target's next harvest_collect, 9980 becomes a high-EV candidate (V=28/H=24/HP=170 with def_shift=0/def_ratio=0 — fully unprotected glass cannon, 14h+ harvest, big pool). Verify feeds count is still 2 (not increased) and that there's been a collect event SINCE the latest feed — if so, sync_hp re-anchored and projection is reliable again.

## Priority 4 — Single strike if margin ≥ 5 HP

Pick the highest-margin clean candidate. Fire one strike. Document predicted vs realized outcome. If revert: pull target's full state and post-mortem (the corrected formula failed; investigate before next strike).

## Priority 5 — Self-schedule

- Strike landed → 15 min re-wake, chain.
- Restart-only, no kill → 30 min re-wake (pools accumulate).
- All 6 strikers genuinely starving (HP < safety) → 60 min re-wake (rest recovery).

## Hard rules carry-over

- Oracle-only data plane for predator decisions (kamibots forbidden).
- Guild blacklist enforced via `predator/guild-no-touch.csv`.
- Bug 1+2+3 corrected formula in `compute_current_hp` + `harvest_efficacy` is now the source of truth — no `×1.4-1.5` calibration multiplier.
- Empirical kill_threshold (`(animosity + atk_shift − def_shift) × (1 − def_ratio) × max_hp`) is the operational formula; canonical documented for reference only.
- Heal-event guard (no `feed` since `harvest.time.last`) is mandatory pre-flight.
- ≥ 5 HP margin required before strike fires.

## Active strategies

- None. Auto_v2 paused since 2026-05-01 (predator mode). Strikers manually managed.

## Roster brief

- **12649** (V=34/H=12/HP=170, atk_shift=300, atk_ratio=500, spoils=200, cooldown=-150, hand=NORMAL, Level 56) — primary striker post-respec.
- **11224** (V=36/H=11/HP=140, atk_shift=280, atk_ratio=500, spoils=80, cooldown=-100, hand=EERIE) — secondary striker, glass cannon.
- 10705, 15540, 6058, 12225 — back-up strikers (V=30-32, lower atk_shift). Currently RESTING.

## Open questions for founder (async, non-blocking)

- The canonical kill_threshold derived from KAMI_LIQ_ANIMOSITY=[_,400,_,3] and KAMI_LIQ_THRESHOLD=[_,1000,_,3] underperforms empirical by 1.4 percentage points on N=495. Possible explanations: (a) precision exponent interpretation off (we used `/ 10^3`, maybe `/ 10^(18+3-6) = /1e15` of WAD CDF), (b) missing affinity_shift term not yet pulled from chain, (c) `KAMI_LIQ_THRESHOLD[2]` (the index-2 slot) is the affinity bonus and we're plugging the wrong slot. Empirical cert remains operational. Worth a 10-line founder note when convenient.
