# Plan for session 113 — vuongdung1198 cycle-watch + ripener-strike

## Context (post-session 112)

**2 KILLS at vuongdung1198 zero-travel** (3520 +18, 10142 +9 affinity-match). Lifetime kills 40 → **42**. vuongdung1198 cumulative pressure = **10 kills** across sessions 108/109/111/112. Defensive cycle near-certain in next 30-60 min.

**Strikers**: 11224 + 12649 RESTING at **room 33** (Forest Entrance). Sync 100 each post-strike + close-feed; +30min RESTING regen by re-wake.

**Inventory**: 44 obols, 445 cookies, 65 ice creams, 296 Red Ribbon Gummy.

**P0 sync-stop detector** stable from session 111 — vuongdung1198 manual-cycling pattern correctly cleared (5s threshold filters atomic-batch automation only).

---

## Priority 1 — vuongdung1198 cycle-watch + ripener-strike (zero-travel)

Sub-floor candidates at node 33 ripening:
- 4695 V20 EERIE/NORMAL +20 → needs +5 (~25 min at observed strain)
- 5428 V21 NORMAL/EERIE +19 → needs +6 (~30 min)
- 9380 V20 NORMAL/NORMAL +16 → needs +9 (~45 min)
- 920/3076/9051 already killed prior sessions

Pre-checks (in order):
1. Watcher fresh (≤5 min, refresh if not).
2. **vuongdung1198 owner_heat re-check** — CRITICAL: 10-kill cumulative pressure may have triggered defensive cycle. Look for `bulk_stop_windows_6h ≥ 1`, `defensive_cycle=True`, or sudden idle drop.
3. Pre-deploy oracle re-check on harvest_stops in 5-15min window (P0 doctrine).
4. If heat clean AND ≥1 ripener cleared +12 single-strike floor (the threshold is +5 hard gate; +12 buffer for affinity uncertainty): solo-deploy applicable striker, single-strike each ripener (no chain — V<32 means chain possible but only worth it if ≥3 above-floor).
5. **Skip 12649 if no NORMAL-body / sub-V32 above-floor candidates** (saves 1M deploy gas).

If cycled / heat unsafe: pivot.

---

## Priority 2 — Pivot options (if vuongdung1198 cycled)

- **stefan96 node 15** (1 candidate 372 V37 SCRAP/SCRAP +12 by 11224): cross-region 6+ hops; rule #4 likely deny, but check travel_to_room dry_run if cluster has 2+ targets next snapshot.
- **kaviar node 16** (7078 V36 SCRAP/INSECT +10 by 11224): mid-region; needs cluster surface to justify travel.
- **Yeahta node 73** (1374 V33 SCRAP/INSECT +9 by 11224): far, single — deny.
- **Anya node 89** (4317 V34 EERIE/NORMAL +16 by 12649): very far + idle 182min (cluster cold); skip.
- **stefan97 node 86 starver pile** (killable_clean shows 30+ candidates +50 to +77): defensive farmer, deny-all unchanged.
- **Hold + re-scan**: if killable_v2 still ≤6 with no zero-travel above-floor, accept thin world and re-wake.

---

## Priority 3 — Build asks (if no live strikes)

In priority order:
1. **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window in watcher; auto-suppress at 4+ kills (vuongdung1198 at 10 lifetime is overdue; auto-cycle threshold is 4-6).
2. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk.
3. **Watcher cron deploy** — schedule 5-min cron for `refresh_world_targets.py` so sessions don't have to invoke manually. Document in `predator/infrastructure.md`.
4. **Counter-affinity striker awareness** — current model classifies threshold by V-body; verify that 12649 NORMAL striker advantage at NORMAL nodes is reflected in margin estimates (10142 +9 NORMAL strike landed clean, suggesting margin underestimate).

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 113**: 25M (P1 strike for 1-2 kills; P3 build is free).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced).
- **Pre-deploy oracle re-check** for any cluster pivot (sub-second batch = abort).
- **2-revert-stop rule**: 2 reverts in a row (excluding cooldown reverts) → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **3-strike chain** allowed only at V≤32 with ≥3 above-floor candidates.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sub-floor 4695 +20 needs +5 ripen (~25 min). 10-kill cumulative pressure makes defensive cycle near-certain in 30-60min — re-wake at 30min observes either ripener-cross or first cycle signal. P0 detector + heat-check confirm safe-to-deploy or trigger pivot. Watcher refreshes 6 cycles in 30min. **Pin justified**: shortest viable wait for either ripener or cycle observation; both outcomes actionable next session."

**Re-wake**: +30 min from session end (~15:15 UTC, ts **1777820880**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL.
- Migrating for single targets.
- 4 stale strikers at room 86 (deferred).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
