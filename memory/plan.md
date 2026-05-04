# Plan for session 136 — node 60 outpost: ripen-watch + opportunistic strike

## Context (post-session 135)

**Session 135 = 3 KILLS TrayzinCarpathia cluster** (cross-region, lifetime 64→67):
- 11224 → 17177 (V13 H20 NORMAL/EERIE sb=0, kz=138 margin +53).
- 12649 → 16591 (V15 H24 NORMAL/SCRAP sb=0, kz=166 margin +74).
- 12649 → 991 (V13 H24 NORMAL/NORMAL sb=0 dts=160, kz=134 margin +67, chain-1 post-feed).

**Gas economics**: 38.99M gas / 3 obols = **0.077 obols/Mgas** — below 0.110 baseline.
- Travel 16 hops 73→60 = 14.16M gas (885k/hop, 6× the 50k/hop assumption).
- Strikes + stage + feeds + stop = 24.83M.
- Travel was 36% of session burn — biggest single line.

**End state**: operator at room 60, stamina 20. Strikers RESTING node 60.
- 11224 sync ~100/140 (full HP after rest cap).
- 12649 sync 100/170 (full HP after rest cap).
- Both kamis cooldown clear by session start (~30+ min idle).

**Arsenal**: 420 cookies (–3 close-feeds), 4 Apology, 1 Hostility, 69 Obols, 60901 VIPP (+844 from session 135 spoils — sit on this for now, sacrifice at room 64 only on a future trip there).

---

## Priority 1 — Node 60 sub-floor ripen-watch + opportunistic strike

**Stay at room 60.** Travel back to 73 requires 80 stamina; have 20, won't recover enough in one cron cycle.

### Remaining clean candidates at node 60 (post-session 135 watcher snapshot)
- **4273 wiuuuu V18 H16 sb=0 SCRAP/INSECT dts=0 elap 1.5h** — sub-floor margin +9. Ripens fast (low elapsed); may cross +25 by session 136.
- **2141 TrayzinCarpathia V12 H22 sb=0 dts=200 elap 6.9h** — sub-floor +7, dts=200 = high def_shift (lowers margin). Slow ripen.
- **2005 wiuuuu V14 H20 sb=0 SCRAP/INSECT dts=0 elap 2.1h** — sub-floor +3. Ripening.

### Off-limits (do not strike)
- 7531 sb=-125, 6032 sb=-125, 1339 sb=-125, 7304 sb=-50 — sustain off-limits per CLAUDE.md hard rule.

### STEP 1 — Verify watcher fresh (cron auto-refresh ×6 by 11:00)
- Read `predator/world_targets.json` for node 60. Confirm:
  - any of (4273, 2141, 2005) crossed +25 floor.
  - TrayzinCarpathia + wiuuuu heat (minutes_idle, k5, k60, sync_stop bursts, sync_feed bursts) — if owner ran defensive cycle after 3 kills, may bench cluster.
- Spot-check oracle: `SELECT MAX(block_timestamp) FROM kami_action JOIN kami_static USING(kami_id) WHERE LOWER(account_name)='trayzincarpathia' AND action_type IN ('harvest_stop','feed_kami')` — recent defensive activity.

### STEP 2 — Decision tree
- **≥1 candidate ≥+25 + heat clean**: solo strike with whichever striker has higher margin. Pre-stage that striker → 200s wait → strike → close-feed → stop. ~7.7M gas / 1 obol. EV at 0.13 obols/Mgas.
- **2 candidates ≥+30 + heat clean**: pair strike (different-striker, no chain). ~17M gas / 2 obols at 0.118 obols/Mgas.
- **No candidate above floor + heat clean**: HOLD. Re-wake +30 min for further ripen.
- **Heat shifted (defensive automation engaged)**: HOLD, await TrayzinCarpathia cool-down (60+ min).
- **Stamina recovered to 80+ AND no kills available**: travel back to 73 to monitor Yeahta cluster recovery. (Unlikely — stamina regen ~6 SP/h.)

---

## Priority 2 — Watcher cluster scan (rest of world)

After node 60 decision, scan `killable_v2` globally for any other emergence:
- Cross-region travel from room 60 unlikely justified now (stamina constraint + travel-cost lesson).
- Adjacent nodes from room 60 (single-hop) — worth a sniff. Rooms 60↔65↔63↔57 etc.
  - Node 65 / 63 / 57 status: scan top10 if any clean candidates.
- Note nodes 53 (yeddy 6 feeds 6h = sync-feed risk) and 26 (popo cycling) for **next-next session** if node 60 cools and stamina recovers.

---

## Priority 3 — Carry-over learnings

**Doctrine update from session 135**:
1. **Travel cost ≈ 885k gas/hop**, not 50k. **Cross-region threshold revised**: ≥4 expected kills at ≥+40 margin to break even on 10+ hop travel.
2. **NORMAL hand striker has eff 1.2 base affinity_shift** (special rule). With atk_ratio=0.5, NORMAL → any-body = eff 1.7. **12649 is a universal strong striker** — prioritize for first-pick on non-SCRAP body clusters.
3. **VIPP spoils on SCRAP-affinity nodes** (node 60 Scrap Trees produces VIPP not MUSU). Track separately. Sacrifice at room 64 if visiting; otherwise hold.
4. **Sequential `liquidate` calls** (no parallel-tool dispatch) — session 134's nonce collision did not recur this session because both strikes ran in separate response blocks. Keep this pattern.

---

## Priority 4 — Striker affinity-aware planning (ongoing carry-over)

Watcher's `striker_idx` always picks 12649 due to higher atk_s. **Manually compute alternate striker margins** with `executor.hp_projection.kill_threshold` for chain/pair opportunities. Today's pair benefited from 11224 having +53 margin on 17177 (still above floor) — no chain-2 same-striker needed.

---

## Hard limits (unchanged)

- **Gas budget session 136**: ~5M monitor OR ~7-17M if 1-2 strikes fire (no travel).
- **NO `harvest_start` if any strike planned same session** unless accepting 200s mid-session wait.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444 / 1444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **`v_strain_boost ≤ −25` sustain-builds** off-limits.
- **POWELL** (bulk-stop active node 76) avoid.
- **PuppyPriestess re-visits within 24h** avoid.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50.
- **Pre-strike Apology Letter** ONLY when target V≥30 OR margin <+45.
- **Always pass `target_handle`** to `liquidate` (resolver flake).
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response** — sequence them serially to avoid nonce collisions.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~11:02 UTC May 4, ts 1777892541). Pinned to:
- (a) Node 60 sub-floor ripening — 4273 V18 sb=0 +9 → ~+15-20 by re-wake (1.5h elapsed → 2h, may not cross +25 yet). 2005 V14 sb=0 +3 → ~+10. Likely sub-floor still; one more cycle for ripening.
- (b) TrayzinCarpathia defensive heat — 3 kills/session may trigger automation; +30 min lets the heat counter signal stabilize before plan revision.
- (c) Operator stamina regen — 20 → ~25 (still well below 80 travel threshold; not a primary timer).
- (d) Watcher refresh ×6 cycles catches new emergence.
**Bias fire-now**: at-room cluster, no travel needed. If anything crosses +25, fire."

**Re-wake**: ~11:02 UTC May 4, ts **1777892541**.

---

## Out of scope (session 136)

- Cross-region travel (stamina 20, justified by lesson learned).
- Chain-2 with V<22 victim same-striker without margin ≥+50 + close-feed.
- Sub-floor strikes (margins <+25 forbidden absent target V≥22 sb=0).
- Sustain-build strikes (sb ≤ −25 hard rule).
- Quest progression, kamibots state reads, force-flush.
- POWELL / deny-set strikes.
- VIPP sacrifice trip (room 64 — out of stamina range, not worth dedicated trip).
