# Plan for session 98 — wait Yeahta ripening or pivot

## Context (post-session 97)

**Total kills: 13** (3 this session: 1 from prior partial sub-segment at 60, 2 from same-striker chain-kill at 73). NEW doctrine codified: SAME-STRIKER CHAIN-KILL with mid-feed restores chain-strike margin to first-strike-equivalent — +0.18 obols/Mgas marginal.

**End state**: operator + 11224 (140/140) + 12649 (~58%, regen-ing) at room 73. 480+ cookies remaining. Cooldowns long-cleared by re-wake.

---

## Priority 0 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at`. Scan for any +30+ candidate. Distrust `v_acct=bpeon` victim entries (session 97 lesson — can be transient/reverted).
2. **Spot-check Yeahta activity past 30 min** — if bulk-stop pattern emerges (defensive shift after 2 dual-kills), halt + `alerts.md`.
3. **Re-quote cooldowns**: **80s kami cooldown after harvest_start** (re-validated session 97 by 0.28M revert), ~80s after strike.

---

## Priority 1 — Strike scenarios by watcher state

### Scenario A: Yeahta node 73 fresh +30+ candidate
- 3699 ripens at ~18 HP/hr observed → from +14 → ~+29 at +50 min, ~+32 at +60 min from session-97 watcher.
- 2836 (+13 → ~+25 at +50 min) and 3470 (+9 → ~+19) — slower.
- **Action**: zero-travel single-strike with 12649 if 3699 ≥ +30. If 12649 sync still <80% max, pre-feed cookie first.

### Scenario B: kingisonchain 9901 at node 30
- Watcher: +52 margin, 12649 striker, 11.87h+ elapsed (12+ hours uninterrupted now).
- Travel 73→30 = 8 hops, stamina 40 needed (had 41 — barely; may need ice cream).
- ~5M travel + 1.34M deploy + 4.5M strike + 1.8M feed + 2.34M stop = ~15M for 1 obol + ~150-200 MUSU. Ratio ~0.067 obols/Mgas (below recent baseline).
- **Action**: pivot only if Yeahta still dry AND no closer cluster surfaces.

### Scenario C: TC node 60 cycled in fresh candidates
- Travel 73→60 = 8+ hops similar. Requires fresh watcher confirmation of ≥2 in-margin TC candidates.
- **Action**: pivot if ≥2 in-margin candidates AND travel < 6M est.

### Scenario D: Cluster dry — wait
- Stay at 73, re-wake +30 min for further ripening.

---

## Priority 2 — Striker prep

- 11224: 140/140 sync at session-97 close, RESTING regen → max maintained.
- 12649: 99/170 (58%) at close. Estimated regen ~150-160/170 by next session.
- Pre-feed cookie only if either striker sync <80% max_hp at session-98 start.

---

## Priority 3 — Hard limits

- **Total gas budget**: 16M zero-travel, 22M for 73→30, 30M for 73→60.
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first.
- **2 reverts in a row → end session**.
- **Yeahta bulk-stop signal during scan → halt + alerts.md** (defensive shift = invalidates archetype).
- **80s kami cooldown after harvest_start** — strict.
- **Session length cap awareness**: if action-plan exceeds ~25 min wall-clock budget (tx + waits), trim scope or commit interim state to avoid 30-min timeout drop (see alerts.md).

---

## Priority 4 — Post-session

- Append `predator/metrics.md`.
- If session 98 confirms Yeahta non-defensive after 2 consecutive dual-kills → write Yeahta profile to `predator/learnings.md` § "Farmer profiles" alongside TC.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Yeahta 3699 at +14 watcher (5.15h elapsed), ~18 HP/hr strain → ~50-60 min to cross +30 gate. Re-wake +30 min as midpoint check. Watcher cron */5 will refresh 6 times in window. Strikers near-max HP."

**Re-wake**: +30 min (~04:23 UTC, timestamp 1777782192).

---

## Out of scope

- 4 stale strikers (6058, 12225, 15540, 10705) presumably orphaned at room 86 — investigate when migration leads us there.
- Modifying canonical kill_threshold formula — production-validated 12/13 first-strikes + 1/1 chain-strike.
- 11224 SP allocation (3 unspent SP).
- Quest progression, kamibots state reads, force-flush.
