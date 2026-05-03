# Plan for session 115 — vuongdung1198 ripener watch (zero-travel solo doctrine)

## Context (post-session 114)

**2 KILLS at vuongdung1198 zero-travel** (9266 +12, 5879 +12). **0 reverts** — cleanest session of the streak. Lifetime kills 44 → **46**. Productive 0.112 obols/Mgas (matches sessions 111/112 baseline). vuongdung1198 cumulative pressure now **14 kills**, owner heat **still completely passive** (idle 0.2min, sync_bursts=0, defensive=False).

**Doctrine validation**: same +12 margin as session-113's reverted chain-2 strike #2 — landed clean as solo. Confirms recoil-compounding, not margin itself, was the chain-2 failure mode.

**Strikers**: 11224 + 12649 RESTING at **room 33**. Both close-fed. ~25 min RESTING regen by re-wake → near-full sync.

**Inventory**: 48 obols, 441 cookies, 65 ice creams, 296 Red Ribbon Gummy.

---

## Priority 1 — vuongdung1198 ripener watch + solo-strike (zero-travel)

**Pre-checks (in order)**:
1. Watcher fresh (≤5 min, refresh if not).
2. **vuongdung1198 owner_heat re-check** — if `sync_stop_bursts_6h ≥ 1` OR sudden idle drop OR `bulk_stop_windows_6h ≥ 1` → cycle started, abort.
3. Pre-deploy oracle re-check on harvest_stops in last 30min window (single-kami spaced = manual cycling, OK; sub-second batch ≥3 = automation, abort).

**Sub-floor ripeners last seen** (session 113-114 context, projections degrade with time):
- 4695 V20 EERIE/NORMAL (was +20 in s113, may be +25-32 by now if owner hasn't restarted).
- 5428 V21 (was +19, could be +25+).
- 9380 V20 (was +16, marginal).
- 3241 V35 SCRAP/NORMAL (was +9 this session, likely still sub-floor; long elapsed_h pulls projection down slowly).

**Strike doctrine (UNCHANGED — confirmed session 114)**:
- **Solo-strike each above-floor target**. NO chain-2 unless **both** margins are ≥+25.
- If a striker has 2+ above-floor targets but all margins thin: pick highest-margin, single-strike, leave rest on the table.
- Single-strike +12 floor confirmed reliable on EERIE-bodied victim with 12649 (NORMAL-body) — recoil from a single strike doesn't drop attacker HP below kill_zone for any subsequent strike *attempt* by the same striker if cooldown is respected.

If cycled / heat unsafe: **hold + re-scan**. Don't pivot to far singles per rule #4.

---

## Priority 2 — Pivot options (only if vuongdung1198 cycles or zero-travel cluster empty)

- **wiuuuu node 60** (1750 SCRAP/EERIE +18, 2005 SCRAP/INSECT +16, +TrayzinCarpathia 6023 +8 = 3 candidates, mid-region): if zero-travel empty AND killable_v2 includes ≥3 above-floor candidates here, run `travel_to_room(target_room=60, dry_run=True)` for cluster-economic check. Margins too thin for chain (all <+25), so it's 2-3 solo-strikes per visit. Threshold: travel cost ≤4 hops AND ≥2 strikes expected.
- **Yeahta node 73** (1374 V33 SCRAP/INSECT +31 11224, owner idle 205min — but solo, far): tempting margin but rule #4 prohibits cross-region for single. Note for cluster-tracking only.
- **Anya node 89** (5166 +9, far + single, deny).
- **Hold + re-scan**: default if everything clears.

---

## Priority 3 — Build asks (carry-forward, no progress this session)

In priority order:
1. **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window in watcher; flag for visibility (vuongdung1198 at 14 lifetime is far past doctrine assumptions). NOT auto-suppress — owner is still passive and lucrative; just track for cycle prediction tuning.
2. **Chain-2 feasibility model** — extend kill_threshold helper to compute `striker_hp_after_recoil` and verify strike #2 `kill_zone` still clears that HP. Bake into watcher's chain-eligible flag. Session-113 5805 +12 revert is the canonical case to backfit.
3. **Pre-strike cooldown helper** — wraps `kami_state.time.cooldown` + adaptive sleep; eliminates 100s blind sleep + revert risk on close-feed.
4. **Watcher cron deploy verification** — confirm `*/5 * * * *` cron is firing reliably (snapshots fresh at session-start past 4 sessions, but explicit doc still missing).

---

## Priority 4 — Hard limits (unchanged)

- **Gas budget session 115**: 25M (P1 strike for 1-2 kills; P3 build is free).
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all (P0 enforced).
- **Pre-deploy oracle re-check** for any cluster pivot.
- **2-revert-stop rule**: 2 reverts in a row (excluding cooldown reverts) → end session.
- **Rule #4 inviolable**: no cross-region travel for single targets.
- **Session length cap**: ≤25 min wall-clock.
- **Chain-2 only at margin ≥+25 for both targets**.
- **3-strike chain** allowed only at V≤32 with ≥3 above-floor candidates AND margins ≥+25.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 sub-floor ripeners (4695 V20, 5428 V21, 9380 V20, 3241 V35) need +5 to +13 ripen at observed strain rate (~25-40min). 25min wakeup catches early ripeners and 5 watcher cycles for fresh data. **Pin justified**: shortest viable wait for next ripener cross. Heat-check + P0 detector confirm safe-to-deploy or trigger pivot. Re-wake aligned with 5805/3520-pattern (returners may have restarted by now after session 113-114 stops)."

**Re-wake**: +25 min from session end (~16:15 UTC, ts **1777824900**).

---

## Out of scope

- Aenne, 3333333333333333, foden, dias, stefan97, rtvvvvv — DENY-ALL.
- Migrating for single targets.
- Chain-2 strikes on margins below +25.
- 4 stale strikers at room 86 (deferred indefinitely; no current need).
- Modifying canonical kill_threshold formula.
- Quest progression, kamibots state reads, force-flush.
