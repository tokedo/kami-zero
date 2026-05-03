# Plan for session 118 — vuongdung1198 zero-travel cluster cleanup continuation

## Context (post-session 117)

**2 KILLS clean (lifetime 48→50, milestone). 0 reverts, 17.957M gas, 0.111 obols/Mgas.** REVIVE-burst doctrine override workflow validated end-to-end:
1. Watcher correctly flags via session-115 P0 detector (sync_feed_bursts_6h ≥1).
2. Override path: oracle drill confirms all burst items in {11001, 11002} (Type=Revive only).
3. Strike clean — same productive economics as a non-flagged cluster.

**Cumulative on vuongdung1198**: **18 kills** across sessions 108-114, 116, 117. Owner still passive (no STOP-burst, no FOOD-feed-burst). The 16:10 REVIVE-burst was post-mortem cleanup, not a defensive cycle.

**Strikers**: 11224 + 12649 RESTING at room 33. Cooldowns clear ~17:23+25min ≈ 17:48 UTC; sync regen substantial.

**Inventory**: 52 obols, 437 cookies, 65 ice creams, 296 Red Ribbon Gummy, 527,442 MUSU.

**Cluster remaining at node 33** (from session-117 by_node top10, post-strike): 9553 +20 (12649), 6996 V34 EERIE/NORMAL (top4, margin ~+18), 3241 +9 → ripening to +13-15. Likely 2-3 above-floor surface within 25min strain ripening.

---

## Priority 1 — vuongdung1198 zero-travel hunt continuation

**Pre-checks (in order)**:
1. **Watcher fresh** (≤5 min). Refresh if not. Read both `killable_v2` AND `by_node[33]` since vuongdung1198 will likely still be auto-suppressed from `killable_clean`/`v2`.
2. **Pre-deploy oracle re-check vuongdung1198 last 30min** by joining via owner_address (0x3FA24be428381a5c5F89356DfEe1bbBF590aEE3F) → operator addr (0x83261bCbD01A3C004A10ecBBfB85A6acb7feAB63). Verify:
   - No new feeds (or if any, all `item_index ∈ {11001, 11002}` Type=Revive).
   - No sync-burst signature in starts/stops (single-kami spaced over minutes is safe).
3. **Inspect by_node[33] candidates** — extract top-N with margin > 0, identify striker assignment.
4. **Strike doctrine (UNCHANGED)**:
   - Solo-strike each above-floor target. NO chain-2 unless **both** margins ≥+25.
   - Single-strike floor +12 confirmed reliable across 6+ sessions.

**Expected node 33 surviving candidates after +25min strain ripening**:
- 9553 V30 EERIE/NORMAL (12649) — was +20, projecting +25 (chain-floor borderline).
- 6996 V34 EERIE/NORMAL (12649 or 11224 depending on body match) — likely +20-22.
- 3241 V35 SCRAP/NORMAL (11224) — was +9, projecting +13-15 (above floor).
- Possibly fresh ripened entries.

**Pivot options if cluster unexpectedly empty**:
- Other clusters in killable_v2 (session-117 snapshot): maia node 80 (V36 high-HP, margins +96/+104 — these are fully starving 14h+ kamis, candidate for cluster pivot if zero-travel options dry up). yeddy node TBD. 4444444444444444 (numeric handle) node TBD.
- node 60 wiuuuu region: 1451 +8 chain-floor risk; not enough margin alone.
- Cross-region single targets: skip per rule #4.
- Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv = DENY-ALL.

**maia node 80 evaluation criterion (if pivoting)**: At least 3 above-floor (margin >+12) candidates in killable_v2. Heat must be clean (no anti_predator_automation flag, no recent STOP/HEAL-bursts). Pre-deploy oracle re-check for sync-burst signature in last 30min. Travel cost ~6 hops (room 33→80) = ~5-7M stamina ~30 SP — economic if 2+ kills clear at clean margins.

---

## Priority 2 — Build asks (carry-forward)

In priority order:

1. **Watcher detector refinement — REVIVE-burst vs HEAL-burst split** (action item from session 116, validated again session 117):
   - Add `sync_revive_bursts_6h` (informational only): feed-bursts where ALL items in {11001, 11002}.
   - Add `sync_heal_bursts_6h` (genuine defense): feed-bursts using non-revive food items.
   - `anti_predator_automation` triggered ONLY by `sync_stop_bursts_6h ≥ 1 OR sync_heal_bursts_6h ≥ 1`. NOT revive-only.
   - Files: `predator/scripts/refresh_world_targets.py` `owner_heat_check()` — modify the existing `feed_burst_*` CTEs to filter by item_index.
   - Validation: vuongdung1198 should drop from `defensive_cycle=True`. 3333333333333333/Aenne/foden unchanged (stop-bursts).
   - **Eliminates**: the manual oracle-drill override required for every vuongdung1198 strike (session 116, 117 demonstrate this is now a recurring tax).
2. **Cumulative-burst owner tracker** — count kills per owner per 24h window in watcher; flag for visibility (vuongdung1198 18 lifetime kills = canonical "passive-reviver" case).
3. **Chain-2 feasibility model** — extend `kill_threshold` helper to compute `striker_hp_after_recoil` and verify strike #2's `kill_zone` clears. Session-113 5805 +12 chain-2 revert is the canonical backfit case.
4. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk on close-feed.

---

## Priority 3 — Hard limits (unchanged)

- **Gas budget session 118**: 25M (P1 strike for 1-2 kills if cluster reopens; else build/hold).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced via detector).
- **vuongdung1198 hunting OPEN** per session-116 doctrine correction. Continue until evidence of HEAL-burst (FOOD on HARVESTING) or STOP-burst.
- **Pre-deploy oracle re-check** mandatory for any cluster pivot AND for vuongdung1198 (mandatory while watcher still misclassifies).
- **2-revert-stop rule**: 2 reverts in a row → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥+25 for both targets**.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 cluster confirmed alive at node 33 — 2-3 above-floor candidates remain (9553 was +20, 6996 ~+20, 3241 ripening +9→+13). 25min re-wake captures: (a) 5 watcher cycles for fresh strain projections, (b) striker sync regen (~30min RESTING from full-sync close-feed), (c) early-evidence of any vuongdung1198 secondary defensive response (HEAL-burst or STOP-burst — none expected given REVIVE-only pattern continuing past 18 cumulative kills). Justified: shortest viable wait that gives meaningful strain ripening on 2-3 candidates and full striker recovery. Same cadence as productive sessions 113-117."

**Re-wake**: +25 min from session end (~17:48 UTC, ts **1777830096**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL (P0).
- Migrating for single targets (rule #4).
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
