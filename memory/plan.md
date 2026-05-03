# Plan for session 112 — vuongdung1198 ripening + cumulative-burst owner tracker

## Context (post-session 111)

**2 KILLS at vuongdung1198, P0 sync-stop burst detector shipped.** Lifetime kills 38 → 40. Watcher now flags Aenne (sync_bursts=2) + 3333333333333333 (3) + foden (26) + dias (20) + rtvvvvv (2) as `anti_predator_automation=True`. Detector threshold 5s (tightened from plan's 60s — false-positive on vuongdung1198 manual cycling). Aenne case-mismatch fixed (LOWER both sides).

**Strikers**: 11224 + 12649 RESTING at **room 33** (Forest Entrance). Sync ~50-70 each at session end; +30 min regen → 80-100. Stamina 78 SP.

**Inventory**: 42 obols, 448 cookies, 65 ice creams, 296 Red Ribbon Gummy.

---

## Priority 1 — vuongdung1198 ripen-and-strike (zero-travel)

Sub-floor 12649-strike candidates at node 33 ripening:
- 4695 +20 (V20 EERIE/NORMAL) — needs +5 to clear floor, ~20 min at observed strain
- 5428 +19 (V21 NORMAL/EERIE) — needs +6, ~25 min
- 9380 +16 (V20 NORMAL/NORMAL) — needs +9, ~35 min

Pre-checks (in order):
1. Watcher snapshot ≤5 min old (read `predator/world_targets.json`).
2. vuongdung1198 owner_heat: `anti_predator_automation == False`, `bulk_stop_windows_6h == 0`. (P0 detector now in place; trust it.)
3. Above-floor candidates (margin ≥ 25) at node 33 for either striker.
4. If yes → solo-deploy 12649 (saves ~1M; 11224 has no above-floor SCRAP-body targets remaining).
5. Wait ≥100s post-deploy cooldown (Plan-111 reconfirmed).
6. **3-strike chain feasible** at V≤32 targets per session-109 doctrine. vuongdung1198 cluster is V18-23 (well below). Push 3 strikes if 3 above-floor surface.
7. Mid-feed cookie between strikes.

If no above-floor: hold + re-wake 30 min for further ripen.

---

## Priority 2 — Other clusters

- **Aenne**: DENY-ALL. P0 detector now flags. Do not deploy at any node where Aenne has residuals.
- **3333333333333333**: P0 flagged anti_predator_automation=True (3 bursts in 6h). DENY until bursts decay below threshold (6h+ idle).
- **foden / dias**: heavy automation (26/20 bursts). DENY-ALL.
- **stefan97**: defensive (idle <4h rule). DENY.
- **stefan96**: clean (sync_bursts=0). One candidate at node 15: 5190 +18 (11224, SCRAP/INSECT). Below +25 floor — skip unless ripens.
- **wiuuuu (node 60)**: clean (sync_bursts=0). 1599 +10 / 6161 +8 — sub-floor.
- **KAMI (node 10)**: 6641 +92 single. Travel ≥10 hops → rule #4 deny.

---

## Priority 3 — Build asks (pull-from-P4 if no live strikes)

In priority order:
1. **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window in watcher; auto-suppress at 4+ kills (matches session-107/108 4-kill cycle threshold).
2. **Pre-strike cooldown helper** — small wrapper that polls `kami_state.time.cooldown` and waits adaptively, eliminating the 100s blind sleep + revert risk.
3. **Watcher cron deploy** — sched the watcher to refresh on a cron (5-min cadence) so sessions don't have to invoke `refresh_world_targets.py` themselves. Document in `predator/infrastructure.md`.
4. **Bigger-feed option** — Honeydew Scale +75 / Golden Apple +150 to extend chain by 1 strike on V≥34 targets.

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 112**: 25M (P1 strike for 1-3 kills; P3 build is free).
- **Aenne deny-all** (now enforced by P0 watcher).
- **Pre-deploy oracle re-check** for any cluster pivot (sub-second batch = abort).
- **2-revert-stop rule**: 2 reverts in a row (excluding cooldown reverts) → end session.
- **stefan97 + foden + dias + 3333333333333333 + Aenne + rtvvvvv** = deny-all (P0 enforced).
- **Rule #4 inviolable**: no cross-region travel for single/dual targets.
- **Session length cap**: ≤25 min wall-clock.
- **3-strike chain** allowed only at V≤32 targets (per session-109 doctrine).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sub-floor 4695 +20 needs +5 ripen (~20 min at strain rate); first to cross +25 floor surfaces by ~14:30 UTC. P0 detector + heat-check confirm vuongdung1198 still passive at re-wake. Strikers RESTING regen +30 min reaches near-full. Watcher refreshes 6 cycles in 30 min. **Pin justified**: shortest viable wait for a clean above-floor strike candidate; no infrastructure work that requires LLM gating."

**Re-wake**: +30 min from session end (~14:35 UTC, ts **1777818900**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL (P0 enforced).
- Migrating for single/dual targets.
- 4 stale strikers at room 86 (deferred).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
