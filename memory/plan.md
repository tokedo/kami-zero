# Plan for session 97 — fresh watcher scan, strike if any cluster ripens

## Context (post-session 96)

**Total kills: 10** (2 this session). Session 96 net: **2 obols + 2263 MUSU gross at 18.62M gas (0.107 obols/Mgas — NEW BEST, beat session 92's 0.103)**.

**Doctrine confirmed**:
- **Watcher-pivot rule**: when refresh shows 2nd target across +30 gate that wasn't there at plan time, dual-strike pays — marginal ~5M gas for +1 obol +636 MUSU.
- **+30 first-strike gate empirically validated** at margin +39 (9839 kill clean). Below this: chain-strike skipped.
- **TC profile 5-session lock (92→96)**: pure 7-9h auto-cycler, ~30 min between cycles, no defensive evolution. Trust the locked archetype.

**End state**: operator + 11224 + 12649 RESTING at room 60. Both fed cookie post-strike. Full HP at next session's perceive step (RESTING regen).

---

## Priority 0 — Read before acting

1. **Watcher snapshot** — `predator/world_targets.json` `generated_at` (cron */5). Scan for any cluster with margin ≥+30 candidate.
2. **Spot-check oracle** — TC activity past 60 min (cycle pattern detection); if stefan97 or Yeahta cluster appears in watcher, check their last-action timestamps for monitoring signature.
3. **Re-quote cooldowns**: 180s operator deploy, ~80s kami strike. Last 11224/12649 strike block 28317035/28317037 (02:51 UTC) — cooldowns long-cleared by ~03:08 UTC session start.

---

## Priority 1 — Strike scenarios by watcher state

### Scenario A: TC node 60 has fresh +30+ candidate
- 6032 was at +28 in session 96 watcher. Will ripen further over 15 min — could cross +30. Striker: 12649.
- New TC kamis cycle in (saw 11319 start 01:48, 17177 start 02:35, more pending) — start times mean their +30 gate crosses at 7-9h elapsed (so not for ~5h).
- **Action**: zero-travel single or dual strike with 11224/12649.

### Scenario B: stefan97 node 86 has fresh +30+ candidate
- Travel cost 60→86: ~16 hops ~10M gas. Net negative unless 2+ kills.
- stefan97 archetype: real-time room-arrival monitor, bulk-stops within 38s. Risky.
- **Action**: only if watcher shows ≥3 candidates +30+ with idle (≥10 min) farmer scan; otherwise skip.

### Scenario C: Yeahta node 73 ripens
- 6485 +42 (11224 striker), 1847 +38 (11224 striker) per session 95 close-out off-cluster scan.
- Travel 60→73: ~hops. Yeahta has not been observed defensive — session 92 dual-kill held.
- **Action**: dual-strike if both still listed. Need fresh watcher confirm.

### Scenario D: Cluster dry (most likely)
- All known +30+ candidates either cycled out or below gate.
- **Action**: stay at room 60, set re-wake +30-45 min for natural ripening.

---

## Priority 2 — Striker prep

- 12649 at session-96 close: just-fed cookie post-strike. Sync should regen to ~170 max during RESTING by session 97 (15 min).
- 11224 at session-96 close: fed cookie. Same regen profile.
- No pre-feed needed unless oracle shows sync <80% max_hp.

---

## Priority 3 — Hard limits

- **Total gas budget**: 20M (single-cluster zero-travel session).
- **No tx if striker HP <80% max_hp** unless 1 cookie feed first.
- **2 reverts in a row → end session**.
- **+5 HP margin revert → halt + post-mortem**.
- **TC/stefan97 bulk-stop signal during scan → halt** (defensive shift = invalidates archetype).

---

## Priority 4 — Post-session

- Append `predator/metrics.md`.
- If sessions 92-96 trend holds (5 clean sessions, 0.072–0.107 obols/Mgas), **write TC profile to `predator/learnings.md` § "Farmer profiles"** — defer this to session 97 if strike-busy.
- If 2 days of zero-travel single-cluster runs sustains 0.09+ ratio, propose to founder (`ideas_to_founder.md`) the doctrine: "stay parked at hot cluster until exhausted, only migrate on full depletion + watcher confirms next cluster has ≥3 in-margin candidates".

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Cluster largely depleted post-dual-strike. Watcher cron refreshes every 5 min — in 15 min the cron will have refreshed 3 times, showing whether 6032 crossed +30 (likely, was +28 at plan-96 watcher) or whether other clusters ripened. Strikers near-max HP via RESTING regen. Cooldowns long-cleared. +15 min balances ripening watch vs not over-waiting on a likely-quiet world."

**Re-wake**: +15 min (~03:08 UTC, timestamp 1777777656).

---

## Out of scope

- Migration off node 60 unless Priority 1 Scenario B/C fires AND target cluster has ≥3 in-margin candidates.
- Reviving 4 stale strikers on room 86. Dead-kami harvest_id check still pending design.
- Modifying canonical kill_threshold formula — production-validated 10/10 first-strikes.
- 11224 SP allocation (3 unspent SP). Wait for more data.
- Quest progression, kamibots state reads, force-flush.
