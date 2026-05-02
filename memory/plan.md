# kami-zero session 90 plan — re-scan post-stefan97-bulk-stop, honor 180s cooldown, consider world_targets.json infra build

Session 89 outcome: canonical `kill_threshold()` shipped (6/6 calibration PASS, cert 99.40%), System Thinking doctrine added to CLAUDE.md. Strike attempt on stefan97/4795 reverted at 0.28M gas — cooldown timing misread (waited 60s, needed ≥180s); during the 130s recovery wait, stefan97 bulk-stopped all 10 top-margin candidates. Net session: 4.01M gas (1.32M deploy + 0.28M revert + 2.41M cleanup), 0 kills.

---

## Priority 0 — Read before acting

Before reading anything else, **re-read `predator/mechanics.md` § "Attacker cooldown"** (around line 504-507, codified session 83). The rule is **180s** post-`harvest_start` on node 86. Session 89's plan misquoted "80s" and cost 0.28M gas to a guaranteed-revert. The mechanics.md value is the authority; never trust a session-prompt restatement.

Then re-read `predator/mechanics.md` § "Canonical override — session 89" (just shipped). The canonical formula is now in production; the empirical formula is gone. The cert is 99.40% (492/495) — the 3 misses are floor edge cases on weak matchups with large def_shift. Treat the canonical's verdict as authoritative for any candidate with affinity_shift ≥ 0; for weak matchups, eyeball the kill_zone before strike — if floor-rounding pushed it negative, the candidate is unkillable.

Glance at `memory/decisions.md` last 3 entries (88/89/this-plan) for continuity.

---

## Priority 1 — Cooldown-timing rule, codified per-session

**Codify the rule directly here every session until it stops biting**:

```
After harvest_start(striker, node), the attacker cooldown is ~180 seconds.
Wait at minimum 185 seconds (5s buffer) before any liquidate call.
DO NOT trust prompt-quoted shorter intervals; mechanics.md is authoritative.
```

This is the second time the 180s rule has been misread (session 80, session 89). Cost so far: ~0.6M gas across the two reverts. If session 90 has any strike attempt, the deployment loop is:
1. Read mechanics.md cooldown rule (literally — check it's still 180s).
2. `harvest_start(striker, node)` — record timestamp T0.
3. While `now() − T0 < 185s`, do nothing on the strike side. Use the wait window for: (a) re-reading target state mid-wait, (b) writing scratch notes, (c) checking other roster members.
4. At T0+185s, **re-scan target**: still HARVESTING, no `feed` since `harvest_start`, no `harvest_stop`. If any of those flip, abort and `harvest_stop(striker)`.
5. `liquidate(target, striker)` — only after the above gate passes.

---

## Priority 2 — Re-scan node 86 + assess stefan97 bulk-restart timing

Stefan97 bulk-stopped 10 kamis between 23:13:23 and 23:14:55 UTC on 2026-05-02. Prior session 86 prep notes recorded stefan97 as a synchronized-cycle archetype (full restart waves on a multi-hour rhythm). At +30min from session 89 (re-wake target), the restart wave is unlikely to have begun — pools will still be tiny on whatever stefan97 has restarted.

**Process**:
1. Run `/tmp/scan89.py` (renamed/reused from session 89 — it has the canonical formula path baked in already; if it's gone from `/tmp/`, regenerate it from session 89 decision-log description).
2. Filter results: non-guild, no-feed-since-start, elapsed ≥ 60s, margin ≥ +5 HP across any of our 6 strikers.
3. **Owner-aware filter**: drop rtvvvvv (no-touch, session 80 rule). Eye stefan97 candidates with caution — if all top results are stefan97, that's the bulk-restart wave and they'll just bulk-stop again before strike. Wait one more cycle.

If the scan returns **a clean non-stefan97 non-rtvvvvv candidate ≥ +5 HP margin**: deploy striker per Priority 1 rules, single attempt.

If the scan returns **only stefan97**: defer (re-wake +90 min) and write a short note in `predator/learnings.md` about stefan97's cycle — refine the timer estimate.

If the scan returns **0 candidates**: this is the longer-cycle quiet window. See Priority 3.

---

## Priority 3 — Reconnaissance scan of alternative nodes (no movement, no tx)

When node 86 is quiet, the next leverage is **knowing where the targets live**, not migrating speculatively. Spend ≤10 minutes on an oracle scan of:
- Node 25 (Iron Pier, last session 78/79 read = ~49 zero-def EERIE-body kamis, but 100% jun-guild)
- Node 60 (last session 79 read = wiuuuu cluster, 7 SCRAP-soft)
- Node 62 (last session 79 read = buja723 cluster, 8 INSECT-soft)
- Node 73 (last session 79 = oracle build_refreshed_ts staleness — POWELL has full Guardian build now)

For each: count current HARVESTING population, count non-guild population, count def_shift=0/def_ratio=0 population, scan for top-margin candidates that would be killable by our roster's best striker.

**Output**: a short table in `predator/learnings.md` § "Roster brief" → new sub-section "Cluster intel snapshot 2026-05-02 23:48 UTC". This is reading-only, no movement, no tx. Cluster math gates any actual migration: **single-node target counts must justify the gas to migrate**, and migration cost on bpeon's roster is ~10–20M gas (full team move sequence per CLAUDE.md "Predator deployment").

---

## Priority 4 — Consider building `predator/world_targets.json` background watcher

Per System Thinking doctrine (just shipped to CLAUDE.md), the highest-leverage infrastructure-build identified this session is a **background world-targets refresher**. Spec:

```
Cron: */5 * * * *  (every 5 min)
Script: predator/scripts/refresh_world_targets.py
Output: predator/world_targets.json (atomic write)
Schema:
  {
    "generated_at": "2026-05-02T23:48:00Z",
    "candidates": [
      {
        "v_idx": 4795, "owner": "stefan97", "node": 86,
        "elapsed_h": 1.4, "proj_hp": 85.2,
        "best_striker": 12649, "kill_zone": 109, "margin": 23.8,
        "guild_blocked": false, "no_touch_owner": false,
        "fresh_feed_since_start": false
      },
      ...
    ]
  }
```

Then sessions read `predator/world_targets.json` at the top of the perception phase instead of running a fresh oracle scan — saves ~30–60s of session time and lets the agent see *trends* (which candidates have been killable across multiple snapshots, vs flash-killable that just-restarted).

**Decision gate for session 90**: build it iff (a) Priority 1+2 finish in under 30 minutes, (b) the canonical formula doesn't surface any structural issue, (c) you have ≥45 minutes of remaining session budget. Otherwise, document the design in `predator/infrastructure.md` (create the file) and ship in session 91.

**If you build it**:
- Use `urllib.request` (httpx not available system-wide — confirmed session 89).
- Reuse `executor/oracle_state.py` patterns where possible.
- Read guild blacklist, no-touch owner list, current striker stats from the same canonical sources sessions use.
- Atomic write (write to `.tmp`, rename) so partial reads never see truncated JSON.
- Document the cron entry in `predator/infrastructure.md` with the exact crontab line, the script path, and the failure mode (e.g., what happens if oracle is down — the watcher must not corrupt the JSON).
- Test by running it manually once before adding the cron entry. Verify the JSON is well-formed and contains expected fields.
- Add an entry to `memory/improvements.md` with title "world_targets.json background refresher" and the cron line.

---

## Priority 5 — Strike if all gates clear

If Priority 2 surfaced a clean candidate and 180s cooldown has been honored, single strike. Hard rules unchanged: heal-event guard, counter-predator scan, predator co-location, ≥+5 HP margin, no rtvvvvv, no guild.

**On revert**: post-mortem before re-attempting. The canonical formula is now ground-truth; any deep-revert with margin ≥ +5 HP is a structural surprise (oracle staleness, on-chain state divergence, target-feed event between scan and strike, etc.). Document and stop hunting that target until root cause identified.

**On kill**: log the predicted vs actual margin, gas (success cost, ~3M for first kill on node 86 expected), obol earned, recoil HP. Then re-scan immediately for next candidate same node — chain on cluster.

---

## Stop conditions

- First kill on canonical formula → end session, write post-mortem on predicted vs actual margin.
- 2 reverts in a row despite passing all gates → stop, log, post-mortem.
- Total gas > 12M without a kill → end session, post-mortem (high gas + 0 kills means we're either timing-misreading again or the target population is too churning).
- Built `world_targets.json` watcher → ship it, document, end session (don't also try to hunt the same session — keep that work clean).

---

## Out of scope

- Force-flush, quest progression, kamibots state reads (forbidden).
- Cross-region travel for a single-target opportunity (cluster math gates moves > 1 hop).
- Modifying the canonical kill_threshold formula or the calibration test (session 89 just shipped — let it bake before any change).
- Respec or skill-point allocation (still gated on first kill per founder rule).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Cooldown rule honored (Y/N).
- Re-scan candidate count (non-guild, non-no-touch, ≥+5 HP margin).
- Reconnaissance: which nodes scanned, what was found (one-liner per node).
- World-targets watcher: built (Y/N), commit sha, cron entry recorded.
- First kill: Y/N. If Y, predicted margin vs actual.
- `next-run-at` and rationale.
