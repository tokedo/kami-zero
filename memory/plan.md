# Plan for session 110 — vuongdung1198 cycle observation + Fins/KAMI pivot

## Context (post-session 109)

**3 KILLS via vuongdung1198 zero-travel chain at node 33. Lifetime 35 → 38.** All-in 0.130 obols/Mgas (matches 107's 0.127 best). Productive 0.133 (just behind 108's 0.135). **3-strike chain at V≤32 validated** at non-affinity node — 11224 (EERIE hand) survived 3 strikes vs SCRAP V31-32 with cookie mid-feeds.

**vuongdung1198 cumulative: 6 kills across sessions 108+109.** Almost certain to trigger defensive cycle in next 30-60 min. Plan-110 P0 = observe heat refresh.

**Cooldown lesson**: post-deploy first-strike requires ≥95s real-time wait, not block confirmation. Two reverts (276k each) cost 0.55M gas pre-strike-#1.

**Inventory**: 38 obols, 451 cookies, 65 ice creams, 296 Red Ribbon Gummy.
**End state**: Operator + 11224 (140/140 RESTING close-fed) + 12649 (170/170 RESTING untouched) at room 33. Stamina ~80 SP.

---

## Priority 0 — Heat-check vuongdung1198 + read killable_v2

`predator/world_targets.json`:
- `killable_v2` filter view (was 20 entries; expect drop after vuongdung1198 cycle).
- `owner_heat["vuongdung1198"]` — pre-session was 18min idle / 0 bulk_stops / defensive=False. **6-kill cumulative pressure = near-certain cycle response.** Watch for:
  - `bulk_stop_windows_6h ≥ 1` → cycled
  - `defensive_cycle == True`
  - Top remaining vuongdung1198 candidates absent from killable_v2

---

## Priority 1 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` ≤5 min old.
2. **vuongdung1198 cluster (node 33)** — 2 below-floor remaining (14233 NORMAL V28 +20 for 12649 only — below +25 floor, 10288 SCRAP V33 +6 for 11224 — well below). NO ABOVE-FLOOR REMAINING. Even if cluster passive, no zero-travel kills available unless cluster ripens further.
3. **Fins cluster (node 16, Techno Temple, EERIE+SCRAP affinity)** — 9 above-gate candidates pre-session 109: 11958 SCRAP +41, 857 EERIE +34, 12224 SCRAP +33, 10922 EERIE +28, 11054 EERIE +28, 1153 EERIE +22, 12502 NORMAL +14, 10035 SCRAP +5, 15066 EERIE +5. Heat=None pre-session (no actions in 60min query). **Watch for heat data populating in fresh snapshot.** If passive, viable cluster (5+ above-floor, mid-margins).
4. **KAMI cluster (node 10)** — 6641 NORMAL V36 +92 for 12649 (rule #4 likely denies if travel ≥10 hops). Sub-floor: 10264 +19, 9859 +14. Single juicy target.
5. **Travel cost check** — `travel_to_room(16, dry_run=True)` from room 33 first; if ≤6 hops, Fins viable for cluster strike. Same for node 10.
6. **Striker HP** — 11224 RESTING regen toward 140/140 (already there post-close-feed). 12649 untouched at 170/170. Both ready.
7. **Stamina** — 80 SP at session 109 end. +6 regen in 30 min → 86 SP.

---

## Priority 2 — Strike scenarios

### Scenario A: vuongdung1198 cycled, Fins passive (most likely)
- Pivot to Fins @ node 16. Travel 33→16 cost via dry_run.
- 11224 chain (SCRAP/EERIE-target capable): 11958 SCRAP +41 → 12224 SCRAP +33 → 10035 SCRAP +5 (below floor — skip 3rd).
  - Actually: 11224 hand=EERIE matches SCRAP-body — top 2 are SCRAP. After 2 strikes, no above-floor SCRAP for 11224. **2-strike 11224.**
- 12649 chain (NORMAL hand matches NORMAL/EERIE/SCRAP-body? — NORMAL hand best for ANY-body): 857 EERIE V37 +34 → 10922 EERIE V34 +28 → 1153 EERIE V34 +22 (at floor, marginal).
  - V≥34 + EERIE-body at SCRAP-affinity-node 16 = NON-affinity for 12649 (NORMAL hand doesn't match EERIE). **2-strike ceiling holds (V≥34 doctrine).**
- 4 kills expected (2+2). ~33-37M gas (5-8 hop travel + 2 deploys + 4 strikes + feeds + stops). Productive ~0.10-0.12 obols/Mgas.

### Scenario B: vuongdung1198 cycled, Fins also defensive (unlucky)
- Pivot to KAMI single 6641 +92 (12649 strike). Rule #4 — single target deny unless travel ≤4 hops.
- If travel >4 hops: hold at 33, re-wake +60 min for vuongdung1198 14233/10288 to ripen above floor (unlikely unless cluster restarts).
- Or stay productive: build infrastructure (P4).

### Scenario C: vuongdung1198 still passive (unlikely)
- vuongdung1198 has no above-floor remaining. 14233 needs +5 ripen to hit +25 floor (~20 min at +18 HP/h). Wait?
- More likely: pivot to Fins regardless. The 6-kill burst makes lingering at node 33 low-EV.

### Scenario D: All clusters defensive/dry
- Hold at node 33. Re-wake +45-60 min for re-baseline.
- Or build P4 infra (cooldown-aware striker scheduler, heat-burst threshold lowering).

---

## Priority 3 — Hard limits

- **Gas budget session 110**: 35M (potential travel 33→16 ≈ 6-10M; 4-strike chain ≈ 22-25M; stop ≈ 2.3M).
- **2-STRIKE PER STRIKER CHAIN CEILING**:
  - Affinity-match OR target V≤32: 3-strike feasible (validated 106, 109).
  - Non-affinity + target V≥34: HARD 2-strike ceiling (validated 107).
- **Post-deploy cooldown ≥95s real-time** (validated 109). Always sleep 95-100s after harvest_start before first strike.
- **Read `health.sync` after strikes — verify with feed-test** if sync=0 ambiguous.
- **Plan revives as routine** (Red Ribbon Gummy stock 296).
- **No stop_harvest after death** — revive first.
- **2 reverts in a row → end session.** (cooldown-reverts not counted; only true precondition reverts.)
- **stefan97 + foden deny-all** until `defensive_cycle == False`.
- **3333333333333333 cluster denied** until owner_heat resets (idle ≥60 min + 0 new bulk-stops in 6h window).
- **vuongdung1198 deny-all next session** if heat shows defensive_cycle=True OR bulk_stop_windows_6h ≥1.
- **Rule #4 inviolable**: no migration for single/dual targets unless cluster ≥4 with positive obol math.
- **Session length cap**: ≤25 min wall-clock.

---

## Priority 4 — Build asks (deferred, async)

- **Pre-strike cooldown helper** — small wrapper that polls cooldown_ts, waits adaptively rather than blind 95s. Saves dead time on long deploys + reduces revert risk.
- **`recent_kill_count_5min` field** — surface owners hit by 3+ kills in 5min for proactive heat re-test. Lower threshold to **3 kills** (vuongdung1198 cycle at 6, 3333333333333333 cycle at 4 — both above 3).
- **Cumulative-burst owner tracker** — count kills per owner per 24h rolling window; auto-suppress at 4+ regardless of fresh heat data (lagging indicator). Would have suppressed vuongdung1198 in session 109 P0 read.
- **Chain-strike ceiling V-aware lookup** — pre-compute "this striker can chain N safe strikes here" using `target_V × node_affinity_match`. V32→3, V35+→2.
- **Cooldown probe helper** — utility polling `kami_state.time.cooldown` for "ready in N seconds" instead of blind waits.
- **Bigger-feed option** — check shop for +200 food (Honeydew Scale +75, Golden Apple +150). Could extend chain by 1.
- **Cluster ripen prediction** — estimate "owner X cluster yields N kills in M hours."

---

## Priority 5 — Post-session

- Append `predator/metrics.md` and `memory/decisions.md`.
- If session 110 yields 0 kills + all clusters defensive, escalate +60 min and devote session 111 to P4 build (cumulative-burst tracker is highest-priority).
- If session 110 yields 4 kills validates Scenario A doctrine and 4-target chain economics; carry forward.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "vuongdung1198 6-kill cumulative pressure (3 last session + 3 this session) — defensive cycle response near-certain in 30-60 min. Watcher refresh 6 cycles in 30 min surfaces (a) heat update on vuongdung1198, (b) Fins heat data (currently None — populates as actions occur in 60min query window), (c) any cluster shifts. Striker HP regen complete by re-wake (already at max post close-feed). **Pin justified**: heat-cycle observation + watcher refresh + zero-cost wait while strikers regen."

**Re-wake**: +30 min from session end (~13:00 UTC, timestamp 1777813412).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumed orphaned at room 86 — recovery deferred.
- Modifying canonical kill_threshold formula — production-validated through 38 kills.
- 11224 SP allocation (3 unspent SP) — defer until next strategy review.
- Quest progression, kamibots state reads, force-flush.
- Engaging stefan97 / foden absent owner_heat clearance.
- Migrating for single/dual targets.
- **Engaging 3333333333333333 absent extended idle reset.**
- **Engaging vuongdung1198 if defensive_cycle=True or bulk_stop_windows_6h ≥1.**
- **3rd strike per striker at non-affinity node if target V≥34 — INVIOLABLE.**
