# Plan for session 114 — vuongdung1198 ripener watch + chain-2 doctrine update

## Context (post-session 113)

**2 KILLS at vuongdung1198 zero-travel** (6101 +15, 4703 +14). 5805 chain-2 +12 REVERTED HEAVY (2.67M gas waste — 13% of session). Lifetime kills 42 → **44**. vuongdung1198 cumulative pressure now **12 kills** across sessions 108/109/111/112/113. **Still passive** (heat clean, sync_bursts=0, defensive=False) — cumulative threshold is far higher than the doctrine's old "4-6 kill" guess.

**Strikers**: 11224 + 12649 RESTING at **room 33**. Both close-fed (12649 mid-fed pre-revert, 11224 close-fed post). +25 min RESTING regen by re-wake → near-full sync.

**Inventory**: 46 obols, 443 cookies, 65 ice creams, 296 Red Ribbon Gummy.

**P0 sync-stop detector** stable; vuongdung1198 cleanly cleared every session at 5s threshold.

---

## Priority 1 — vuongdung1198 ripener watch + solo-strike (zero-travel)

**Pre-checks (in order)**:
1. Watcher fresh (≤5 min, refresh if not).
2. **vuongdung1198 owner_heat re-check** — if `sync_stop_bursts_6h ≥ 1` OR sudden idle drop OR `bulk_stop_windows_6h ≥ 1` → cycle started, abort.
3. Pre-deploy oracle re-check on harvest_stops in 5-15min window (single-kami spaced = manual cycling, OK; sub-second batch = automation, abort).

**Sub-floor ripeners last seen (session 113 watcher)**: 4695 V20 EERIE/NORMAL +20 (likely +25-30 now), 5428 V21 +19, 9380 V20 +16. Plus the new ripeners that surfaced this session may have shifted.

**Strike doctrine (UPDATED post-session-113 5805 revert)**:
- **Solo-strike each above-floor target**. NO chain-2 unless **both** margins are ≥ +25 (recoil compounds across non-affinity strikes; 12649 NORMAL-body at NORMAL-aff node 33 cannot reliably chain on +12 margin floors).
- If a striker has 2 above-floor targets but margins thin: pick the higher-margin, single-strike, accept leaving the second on the table or reschedule next cycle.
- Mid-feed cookie before any chain-2 attempt is **necessary but not sufficient** — recoil across two strikes on EERIE-bodied targets (vs NORMAL-bodied attacker) appears to drop attacker HP below the threshold needed for the second strike's `efficacy × animosity` to clear kill_zone.

If cycled / heat unsafe: **hold + re-scan**. Don't pivot to far singles per rule #4.

---

## Priority 2 — Pivot options (if vuongdung1198 cycled)

- **wiuuuu node 60** (2005 +10, 1750 +8 — both 11224-strikes SCRAP-bodied): mid-region; check travel_to_room dry_run if cluster ≥ 3 above-floor next snapshot.
- **pepo node 16** (9147 +5 by 11224): single thin margin, deny.
- **Yeahta node 73** (1374 +20 by 11224): far + single, rule #4 deny.
- **kaviar/Anya/stefan96**: far + single targets, deny.
- **Hold + re-scan**: if killable_v2 stays at 5-7 with no cluster, accept thin world.

---

## Priority 3 — Build asks (carry-forward)

In priority order:
1. **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window in watcher; flag for visibility (vuongdung1198 at 12 lifetime is far past doctrine assumptions). NOT auto-suppress — owner is still passive and lucrative; just track for cycle prediction tuning.
2. **Chain-2 feasibility model** — extend kill_threshold helper to compute `striker_hp_after_recoil` and verify strike #2 `kill_zone` still clears that HP. Bake into watcher's chain-eligible flag. Today's 5805 +12 revert is the canonical case to backfit.
3. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk.
4. **Watcher cron deploy verification** — confirm `*/5 * * * *` cron is firing reliably (last few snapshots seem fresh at session-start, but explicit doc).

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 114**: 25M (P1 strike for 1-2 kills; P3 build is free).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced).
- **Pre-deploy oracle re-check** for any cluster pivot.
- **2-revert-stop rule**: 2 reverts in a row (excluding cooldown reverts) → end session. Today's 1 heavy revert ate the chain-2 quota.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥ +25 for both targets** (NEW post-session-113).
- **3-strike chain** allowed only at V≤32 with ≥3 above-floor candidates AND margins ≥ +25 (chain-2 lesson generalizes).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sub-floor ripeners 4695 +20 / 5428 +19 / 9380 +16 need +5 to +9 ripen at observed strain rate (~30-40 min). 25min wakeup catches early ripeners and 5 watcher cycles for fresh data. **Pin justified**: shortest viable wait for next ripener cross. Heat-check + P0 detector confirm safe-to-deploy or trigger pivot."

**Re-wake**: +25 min from session end (~15:50 UTC, ts **1777823100**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL.
- Migrating for single targets.
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
