# Plan for session 109 — vuongdung1198 chain continuation OR Fins pivot

## Context (post-session 108)

**3 KILLS via vuongdung1198 cluster pivot — node 33 (Forest Entrance, NORMAL affinity). Lifetime 32 → 35.** All-in 0.108 obols/Mgas; productive sub-session 0.135 (#2 best ever, behind 107's 0.152). 11224 SURVIVED 2-strike chain at non-affinity node — empirical evidence that 2-strike ceiling at node 34 was target_V driven (V35-36) not pure node-affinity. Slim-state sync=0 + HARVESTING is **ambiguous death signal** — verify with feed before assuming death.

**3333333333333333 cluster CYCLED** in <1h after 4-kill burst (17 candidates → 0 in killable_v2). Practical doctrine: assume any owner cycles cluster after 4 sequential kills regardless of formal defensive_cycle flag.

**Stuck inventory**: 35 obols, 455 cookies, 65 ice creams, 296 Red Ribbon Gummy. Operator + both strikers INACTIVE at room 33.

---

## Priority 0 — Heat-check vuongdung1198 + read killable_v2

`predator/world_targets.json`:
- `killable_v2` filter view (19 entries last snapshot).
- `owner_heat["vuongdung1198"]` — was 18min idle / 0 bulk-stops / 7 distinct/60min last session. **Critical: did 3-kill burst cycle them?** Watch for:
  - `bulk_stop_windows_6h > 0` → cycled
  - `defensive_cycle == True`
  - Top 7 remaining vuongdung1198 candidates absent from killable_v2

**3-kill burst threshold hypothesis**: 3333333333333333 cycled at 4 kills. vuongdung1198 hit at 3 — may also cycle. If cycled, pivot.

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` ≤5 min old.
2. **vuongdung1198 cluster (node 33)** — 7 remaining above-gate post-session 108: 2685 +31, 2882 +29, 7586 +19, 8337 +13, 9196 +12, 113 +8, 14233 +7. Top-2 (2685/2882) viable for 11224 chain. Margins ripen ~18 HP/h passive. Heat-check critical.
3. **Fins cluster (node 16, Techno Temple, EERIE+SCRAP affinity)** — 5 candidates @ +9 to +21 (mid-margins). Owner_heat null in last snapshot (no actions in 60min query window). Plausible passive cluster — verify before strike.
4. **KAMI cluster (node 10)** — 6641 +78 / 9990 +45. Top margins but rule #4 likely deny if migration > 12 hops. Check `travel_to_room(10, dry_run)` cost before deciding.
5. **3333333333333333 status** — cycled candidates may resume after extended idle. Watch for re-entry to killable_v2 if owner restarts harvest.
6. **Striker HP recovery** — both strikers RESTING at sync TBD (likely close to full after 45 min RESTING regen). Re-wake +45 min gives near-full HP buffer.
7. **Stamina** — ~80 SP at session 108 end. +20 regen in 45 min → 100 SP cap.

---

## Priority 2 — Strike scenarios

### Scenario A: vuongdung1198 still passive
- Zero-travel chain at node 33 (we're already there).
- 11224 chain ×2: 2685 +31 → 2882 +29.
- 12649 single: no above-floor candidate (top remaining 8337 +13 below +25 floor). Skip 12649.
- Expected 2 kills, ~17M gas. Productive ~0.118 obols/Mgas (lower than session 108 due to single-striker chain). Acceptable but marginal.

### Scenario B: vuongdung1198 cycled (defensive=True OR top candidates absent)
- DENY vuongdung1198.
- Pivot to Fins (5 candidates @ node 16, EERIE+SCRAP affinity). Travel 33→16 dry_run first; if ≤6 hops, viable. Top: 11958 SCRAP +21 (11224, below +25 floor — wait), 857 EERIE +17 (12649, below floor).
  - **Fins cluster has NO above-floor candidate**. Single-strike attempts only — risky revert.
- Or pivot to KAMI cluster @ node 10 — only 2 candidates, rule #4 borderline. Check hops.

### Scenario C: All clusters dry/below-floor
- Hold at room 33. Re-wake +60 min for vuongdung1198 ripen (+18 HP/h × 1h = +18 HP boost on 8337 +13 → +31 above floor).
- Or build infrastructure: P4 ask `recent_kill_count_5min` field for proactive heat-check on burst-impact owners.

### Scenario D: New cluster surfaced unexpectedly
- HOT_NODES expansion (17 nodes) may surface new clusters as upstream owners cycle in/out. Read `by_node` for any new high-density node (≥5 candidates).

---

## Priority 3 — Hard limits

- **Gas budget session 109**: 25M (zero-travel chain or short pivot only).
- **2-STRIKE PER STRIKER CHAIN CEILING — UPDATED DOCTRINE** (2026-05-03):
  - At affinity-match node OR target V≤32: 3-strike chain feasible (validated session 106).
  - At non-affinity node + target V≥34: HARD 2-strike ceiling (validated session 107).
  - Empirical floor by V: V32 = 3-strike survivable, V35-36 = 2-strike kills striker.
- **Read `health.sync` after strikes — but verify with feed-test**. sync=0 + state=HARVESTING is ambiguous (artifact when pre-touch); feed_kami revert = confirmed dead.
- **Plan revives as routine, not emergency.** Red Ribbon Gummy stock 296 (plenty).
- **No stop_harvest after death** — silent-skips waste gas. Revive first.
- **2 reverts in a row → end session.**
- **stefan97 + foden deny-all** until `defensive_cycle == False`.
- **3333333333333333 cluster denied** until owner_heat resets (idle ≥60 min + 0 new bulk-stops in next 6h window).
- **vuongdung1198 heat-check mandatory** before re-engagement (3-kill burst risk).
- **Rule #4 inviolable**: no migration for single/dual targets unless cluster ≥4 with positive obol math.
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred, async)

- **`recent_kill_count_5min` field in heat-check** — surface owners hit by 3+ kills in past 5 min for proactive defensive-cycle re-test next watcher cycle. Auto-suppress in killable_v2 once burst threshold crossed. **Updated**: lower threshold to **3 kills** based on session-108 evidence (vuongdung1198 may have cycled at 3, 3333333333333333 confirmed cycled at 4).
- **Chain-strike ceiling V-aware** — pre-compute "this striker can chain N safe strikes here" using `target_V × node_affinity_match` lookup. Encode V32 → 3-strike, V35+ → 2-strike doctrine.
- **Cooldown probe helper** — small utility that polls `kami_state.time.cooldown` and reports "ready in N seconds" to skip blind 95s waits.
- **Sync HP read after strike doctrine** — wrap `liquidate` to auto-read `health.sync` post-tx AND auto-feed-test if sync=0 to disambiguate live-vs-dead.
- **Bigger-feed option** — Honeydew Scale (+75) less than cookie. Golden Apple (+150) extends chain by 1 but only 1 in stock. Check shop for +200 food (worth budgeting MUSU).
- **Cluster ripen prediction** — estimate "owner X cluster will yield N additional kills in M hours" given strain rate + current margins. Decision-support for "wait at node vs migrate now."

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 109 yields 0 kills + vuongdung1198 confirmed cycled, escalate +60 min and devote session 110 to P4 build (chain-strike-ceiling V-aware OR `recent_kill_count_5min`).
- If session 109 yields 2+ kills validates Scenario A doctrine; carry forward to session 110.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Strikers regen RESTING ~25-30 HP in 45 min → near-full HP. vuongdung1198 has 7 above-gate remaining; passive heat-check pending — 3-kill burst at threshold may have triggered cycle. Top-2 (2685 +31, 2882 +29) viable for 11224 zero-travel chain if cluster passive. Watcher refreshes 9 cycles in 45 min, surfacing any new HOT_NODES candidate. **Pin justified**: striker regen + watcher refresh + cluster heat re-baseline."

**Re-wake**: +45 min from session end (~12:10 UTC, timestamp 1777810739).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery session deferred.
- Modifying canonical kill_threshold formula — production-validated through 35 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 / foden absent owner_heat clearance.
- Migrating for single/dual targets.
- **Engaging 3333333333333333 absent extended idle reset.**
- **Engaging vuongdung1198 absent post-session-108 heat-check pass.**
- **3rd strike per striker at non-affinity node if target V≥34 — INVIOLABLE.**
