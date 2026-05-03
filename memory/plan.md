# Plan for session 117 — vuongdung1198 zero-travel hunt continuation

## Context (post-session 116)

**2 KILLS clean (lifetime 46→48, obols 48→50, gas 17.989M, 0.111 obols/Mgas).** Doctrine corrected: vuongdung1198 is a passive-reviver, not a defensive-cycler. Item 11001 (Red Ribbon Gummy, `Type=Revive`) only fires on DEAD targets — the 15-feed burst at 16:10 UTC was post-kill recovery, NOT a defensive heal. Surviving 5 kamis on node 33 had `fresh_feed_since_start=False` — confirmed they're untouched. Session 116 manually overrode the watcher's `defensive_cycle=True` flag and struck (clean).

**Strikers**: 11224 + 12649 RESTING at **room 33**. Cooldown clear ~16:53 UTC (post-stop) → fully cool by re-wake +25min. Sync regen substantial.

**Inventory**: 50 obols, 439 cookies, 65 ice creams, 296 Red Ribbon Gummy, 527,442 MUSU. Lifetime kills 48.

**Cumulative on vuongdung1198**: 16 kills total (sessions 108-114, 116). Last revive batch at 16:10 UTC for 14 dead. Two more dead (11134, 6044) since. Owner's next revive batch likely after ~10-14 more kills accumulate.

---

## Priority 1 — vuongdung1198 zero-travel hunt continuation

**Pre-checks (in order)**:
1. Watcher fresh (≤5 min, refresh if not).
2. **vuongdung1198 heat re-check**: expected `sync_feed_bursts_6h ≥ 1` for next ~5h (16:10 burst's 6h SQL window persists). **Override doctrine**: per session-116 mechanics.md, manually verify the burst items via `oracle_sql` — if all item 11001/11002 (Type=Revive), the flag is REVIVE-only and does NOT contribute to actual defense. Continue hunting.
3. **Inspect vuongdung1198 candidates in `killable_clean` (NOT v2 — v2 still suppresses)** to see post-strain projections at node 33.
4. **Pre-deploy oracle re-check on vuongdung1198 last 30min**: confirm no sync-stop-burst (≥3 stops in 5s) and no sync-heal-burst (≥3 feeds with FOOD items, not 11001/11002). Stops/starts spaced over minutes are safe.

**Strike doctrine (UNCHANGED)**:
- Solo-strike each above-floor target. NO chain-2 unless **both** margins ≥+25.
- Single-strike floor +12 confirmed reliable (sessions 111-114, 116).

**Expected node 33 surviving candidates after +25min strain ripening**:
- 5100 V33 NORMAL/INSECT (12649) — was +14, projecting +18 by re-wake
- 5371 V35 SCRAP/SCRAP (11224) — was +12, projecting +16
- 9553 V30 EERIE/NORMAL (12649) — was +10, projecting +14

3 above-floor likely available zero-travel. 11224 has 1 (5371), 12649 has 2 (5100, 9553) → solo-strike highest-margin per striker.

**Pivot options if cluster unexpectedly empty**:
- node 60 wiuuuu region: 1451 +15 (11224), 4273 +8 (sub-floor) — only 1 reliable. Skip per "≥3-candidate cluster" rule.
- node 73 Yeahta: 1374 +52 single (cross-region). Rule #4 deny.
- node 89 Anya 3957 +11, node 9 tamagotcho 7311 +10/+18, node 62 buja723 +6 — all far singles. Deny.
- node 15 stefan96, Aenne, foden, dias, rtvvvvv, 3333333333333333 — DENY-ALL (P0 detector + manual deny).

**Default**: Hold + re-scan every 25-30min until a ≥3-candidate cluster surfaces zero/short-travel.

---

## Priority 2 — Build asks (carry-forward)

In priority order (no progress this session beyond doctrine note):

1. **Watcher detector refinement — REVIVE-burst vs HEAL-burst split** (NEW, doctrine action item from session 116):
   - Add `sync_revive_bursts_6h` (informational only): feed-bursts where ALL items in {11001, 11002}.
   - Add `sync_heal_bursts_6h` (genuine defense): feed-bursts using non-revive food items.
   - `anti_predator_automation` triggered ONLY by `sync_stop_bursts_6h ≥ 1 OR sync_heal_bursts_6h ≥ 1`. NOT revive-only.
   - Files: `predator/scripts/refresh_world_targets.py` `owner_heat_check()` — modify the existing `feed_burst_*` CTEs.
   - Validation: vuongdung1198 should drop from `defensive_cycle=True`. 3333333333333333/Aenne/foden unchanged (stop-bursts).
2. **Cumulative-burst owner tracker** — count kills per owner per 24h window in watcher; flag for visibility (vuongdung1198 16 lifetime kills = canonical "passive-reviver" case).
3. **Chain-2 feasibility model** — extend `kill_threshold` helper to compute `striker_hp_after_recoil` and verify strike #2's `kill_zone` clears. Session-113 5805 +12 chain-2 revert is the canonical backfit case.
4. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk on close-feed.
5. **Watcher cron deploy verification** — confirm `*/5 * * * *` cron firing reliably (snapshots fresh past 6 sessions); doc in `predator/infrastructure.md`.

---

## Priority 3 — Hard limits (unchanged)

- **Gas budget session 117**: 25M (P1 strike for 1-2 kills if cluster reopens; else build/hold).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced via detector).
- **vuongdung1198 hunting RE-OPENED** per session-116 doctrine correction (REVIVE-burst is not defensive). Continue until evidence of HEAL-burst or STOP-burst.
- **Pre-deploy oracle re-check** for any cluster pivot AND for vuongdung1198 (mandatory while watcher still misclassifies).
- **2-revert-stop rule**: 2 reverts in a row → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥+25 for both targets**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 cluster confirmed alive at node 33 — 3 above-floor candidates remaining (5100 +14, 5371 +12, 9553 +10) at strain-floor levels. **25min re-wake** captures: (a) 5 watcher cycles for fresh strain projections, (b) striker sync regen (~30min RESTING from full-sync close-feed), (c) early-evidence of any vuongdung1198 secondary defensive response (HEAL-burst or STOP-burst — none expected given REVIVE-only pattern). **Pin justified**: shortest viable wait that gives meaningful strain ripening on 3 candidates and full striker recovery. Same cadence as sessions 113-114 productive zero-travel runs."

**Re-wake**: +25 min from session end (~17:18 UTC, ts **1777828216**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL (P0).
- Migrating for single targets (rule #4).
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
