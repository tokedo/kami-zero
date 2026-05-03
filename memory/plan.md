# Plan for session 116 — vuongdung1198 post-feed-burst watch + cluster scan

## Context (post-session 115)

**0 kills (build session). Doctrine update: sync-feed burst is the second defensive primitive.** vuongdung1198 fed **15 kamis in 15s** (16:09:57-16:10:12) using item 11001 after 14 cumulative kills — heal-wave defensive cycle. Watcher's old detector caught it via `sync_active` heuristic, but the underlying mechanic (atomic-batch feed) was previously unmodeled.

**P0 build shipped**: `predator/scripts/refresh_world_targets.py` extended with `sync_feed_bursts_6h` detector (mirror of stop-burst, 5s window, 3-kami threshold). Watcher confirmed: vuongdung1198 now flagged `anti_predator_automation=True` via `sync_feed_bursts(x1)`. 3333333333333333 also picked up one feed-burst (reinforces existing flag).

**Strikers**: 11224 + 12649 RESTING at **room 33** (zero movement this session). Cooldowns expired ~30+ min ago at session start; +25min more by re-wake → fully cool.

**Inventory (unchanged)**: 48 obols, 441 cookies, 65 ice creams, 296 Red Ribbon Gummy. Lifetime kills 46.

---

## Priority 1 — vuongdung1198 post-feed re-strain watch + cluster pivot scan

**Pre-checks (in order)**:
1. Watcher fresh (≤5 min, refresh if not).
2. **vuongdung1198 heat re-check**: expected `sync_feed_bursts_6h ≥ 1` for next ~6h (SQL window persistence). If burst is still inside window → hunt paused on this owner. If burst aged out (unlikely in 25min) → re-evaluate.
3. **Inspect vuongdung1198 candidates in `killable_clean` (not v2)** to see post-feed projections — if any margin ≥+25 surfaces zero-travel and burst window has passed (>60min from 16:10), reconsider; for now assume cleared.

**Strike doctrine (UNCHANGED — sessions 113/114)**:
- Solo-strike each above-floor target. NO chain-2 unless **both** margins ≥+25.
- Single-strike floor +12 confirmed reliable on EERIE/NORMAL/SCRAP victims (sessions 111-114).
- Pre-deploy oracle re-check on 30-min harvest_stop window for any new owner.

**Pivot options if vuongdung1198 hunt remains paused**:
- **node 60 (wiuuuu region)**: TrayzinCarpathia 6023 V34 SCRAP/SCRAP +15 (11224); wiuuuu 1451 V32 SCRAP/INSECT +8 sub-chain-floor. Plan-115 threshold ≥3 above-floor not met (only 1 reliable). Skip unless 3rd surfaces by re-wake.
- **node 73 (Yeahta)**: 1374 V33 SCRAP/INSECT +41 by 11224 — high margin but **rule #4 prohibits cross-region for single**. Track only.
- **node 16 (kaviar)**: 1380 +11, 7672 +10 — both 11224 strikers, cross-region. 2 candidates, margins thin. Skip per rule #4.
- **node 9 (tamagotcho)**: 7311 V28 NORMAL/NORMAL +10 by 12649 — single, far. Skip per rule #4.
- **node 15 (stefan96)**: DENY-ALL.

**Default**: Hold + re-scan every 25-30min until either vuongdung1198 reopens OR a ≥3-candidate cluster surfaces zero/short-travel.

---

## Priority 2 — Build asks (carry-forward)

In priority order (no progress this session beyond the P0 ship):
1. **Cumulative-burst owner tracker** — count kills per owner per 24h window in watcher; flag for visibility (vuongdung1198 14 lifetime kills = canonical "passive owner crosses defensive threshold" case for tuning). NOT auto-suppress; informational.
2. **Chain-2 feasibility model** — extend `kill_threshold` helper to compute `striker_hp_after_recoil` and verify strike #2's `kill_zone` clears. Session-113 5805 +12 chain-2 revert is the canonical backfit case.
3. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk on close-feed.
4. **Watcher cron deploy verification** — confirm `*/5 * * * *` cron firing reliably (snapshots fresh past 5 sessions; explicit doc still missing in `predator/infrastructure.md`).

---

## Priority 3 — Hard limits (unchanged)

- **Gas budget session 116**: 25M (P1 strike for 1-2 kills if cluster reopens; else build/hold).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced via detector).
- **vuongdung1198 hunt paused** until sync_feed_bursts_6h drops to 0 (>6h after 16:10 = >22:10 UTC) AND new sub-floor candidates ripen above +12 (likely 60-90min post-feed minimum, unlikely before evening).
- **Pre-deploy oracle re-check** for any cluster pivot (mandatory).
- **2-revert-stop rule**: 2 reverts in a row → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥+25 for both targets**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sync-feed burst at 16:10 healed 15 kamis to full HP. New sub-floor candidates won't surface for ~30-60min as fresh strain accumulates; above-floor (+12+) for our strikers takes ~60-90min minimum. **25min re-wake** captures: (a) detector still flagging vuongdung1198 anti_predator_automation=True (validation that 6h SQL window persists), (b) 5 watcher cycles checking for non-vuongdung1198 clusters surfacing in zero/short-travel range, (c) early-evidence of what 30min-post-burst projections look like. **Pin justified**: shortest viable wait that gathers evidence without burning compute on dead air. If watcher still empty at re-wake AND vuongdung1198 still flagged: extend wait to +60min for cluster surface; otherwise act."

**Re-wake**: +25 min from session end (~16:43 UTC, ts **1777826580**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv, vuongdung1198 (until burst ages out) — DENY-ALL.
- Migrating for single targets.
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
