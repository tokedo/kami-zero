# kami-zero session 90 prompt — ship Cadence Discipline + agent's session-90 plan (founder-merged)

This is a complete replacement for `memory/plan.md` on the VM. Founder merged: kept the agent's session-90 plan content (cooldown rule, recon, world_targets.json infra) and prefixed it with the new Cadence Discipline doctrine + fired immediately (overriding the lazy +30 min default).

---

## ⚠️ Founder principle being shipped this session

Session 89 self-scheduled `next-run-at` = +30 min "for restart-and-rescan" — same lazy default that bit session 88. Founder framing 2026-05-02:

> "What is the justification for waiting? […] The only justification I see — there are no targets in the world that we can currently liquidate, and we take some break to see what happens in an hour or so."

**Right. From now on**: self-scheduled delays must be **pinned to a specific thing being waited for**. If you can't name it concretely, fire sooner. Build-phase mode (now): bias hard toward fire-now. Sub-10-min re-wakes are the norm if there's any meaningful next action. The metric absorbs the cost.

This session ships the discipline to CLAUDE.md (Priority 1) and applies it (the founder fired this session NOW, not at 23:48).

---

## Priority 0 — Read before acting

Before reading anything else, **re-read `predator/mechanics.md` § "Attacker cooldown"** (around line 504-507, codified session 83). The rule is **180s** post-`harvest_start`. Session 89's plan misquoted "80s" and cost 0.28M gas to a guaranteed-revert. The mechanics.md value is the authority; never trust a session-prompt restatement.

Then re-read `predator/mechanics.md` § "Canonical override — session 89" (just shipped). The canonical formula is now in production; the empirical formula is gone. The cert is 99.40% (492/495) — the 3 misses are floor edge cases on weak matchups with large def_shift. Treat the canonical's verdict as authoritative for any candidate with affinity_shift ≥ 0; for weak matchups, eyeball the kill_zone before strike — if floor-rounding pushed it negative, the candidate is unkillable.

Glance at `memory/decisions.md` last 3 entries (88/89/this-plan) for continuity.

---

## Priority 1 — Ship Cadence Discipline block to CLAUDE.md

Insert as a new top-of-file block, immediately after Block G "System Thinking":

> ## Cadence Discipline — fire now unless pinned wait
>
> When you set `next-run-at`, the delay must be **pinned to a specific thing you're waiting for**. If you can't name it concretely, fire sooner.
>
> ### Acceptable reasons to wait (with concrete pinning)
> - **Strain-wait**: re-wake at the precise time a target's projected HP crosses kill-zone — timestamp computable, ±5 min buffer.
> - **Strike cooldown**: after a successful strike, our kami's ~3 min game-mechanic cooldown.
> - **Counter-predator cooling**: a *named* threat just attacked our node; wait the named time, not "a while".
> - **Truly empty world**: thorough scan returned zero non-guild HARVESTING candidates within travel-economic range. Re-scan in 10–20 min.
> - **Owner restart wave**: e.g. stefan97 bulk-stopped 10 kamis; their pools start at 0 — wait 30–60 min for pool to accumulate, then re-scan.
>
> ### Unacceptable reasons (call these out and reject)
> - "+30 min, restart-and-rescan" with no concrete reason.
> - "Rescan in N min by default" — defaults should be short (5–10 min) when there's any next action.
> - "Might be more interesting later" — speculation.
> - "I built infrastructure, let it run a while" — infrastructure runs in background; sessions don't have to wait for it.
> - "Founder might want to review" — founder reads async.
>
> ### Build-phase mode (now, until further notice)
> Bias hard toward fire-now. Sub-10-min re-wakes are normal if there's any meaningful next action. The metric in `predator/metrics.md` absorbs the cost.
>
> ### End-of-session discipline check
> Before writing `next-run-at`, ask explicitly: *"My re-wake is X minutes from now. What specifically am I waiting for?"* If you can't name it in one concrete sentence, halve the delay or fire now.
>
> ### Forward direction (eventual, not now)
> Once formulas + infrastructure are stable and the system mostly executes patterns rather than discovers them, you may propose self-tiered model usage in `ideas_to_founder.md` — Sonnet for routine scans/watchers, Opus for strategic review of metrics + doctrine + infrastructure builds. Founder approves async.

Commit with prefix `pivot:` and a one-liner: `pivot: cadence discipline — fire now unless pinned wait (founder principle)`.

---

## Priority 2 — Cooldown-timing rule, codified per-session

**Codify the rule directly here every session until it stops biting**:

```
After harvest_start(striker, node), the attacker cooldown is ~180 seconds.
Wait at minimum 185 seconds (5s buffer) before any liquidate call.
DO NOT trust prompt-quoted shorter intervals; mechanics.md is authoritative.
```

This is the second time the 180s rule has been misread (sessions 80, 89). Cost so far: ~0.6M gas across two reverts. If session 90 has any strike attempt, the deployment loop is:
1. Read mechanics.md cooldown rule (literally — check it's still 180s).
2. `harvest_start(striker, node)` — record timestamp T0.
3. While `now() − T0 < 185s`, do nothing on the strike side. Use the wait window for: re-reading target state mid-wait, scratch notes, checking other roster members.
4. At T0+185s, **re-scan target**: still HARVESTING, no `feed` since `harvest_start`, no `harvest_stop`. If any flip, abort and `harvest_stop(striker)`.
5. `liquidate(target, striker)` — only after the above gate passes.

---

## Priority 3 — Re-scan node 86 + assess stefan97 bulk-restart timing

Stefan97 bulk-stopped 10 kamis between 23:13:23 and 23:14:55 UTC on 2026-05-02. Prior session 86 prep notes recorded stefan97 as a synchronized-cycle archetype (full restart waves on a multi-hour rhythm). At fire-now from session 89 (~23:25 UTC), the restart wave is unlikely to have begun — pools will still be tiny on whatever stefan97 has restarted.

**Process**:
1. Run `/tmp/scan89.py` (renamed/reused from session 89 — it has the canonical formula path baked in already; if it's gone from `/tmp/`, regenerate from the session 89 decision-log description).
2. Filter results: non-guild, no-feed-since-start, elapsed ≥ 60s, margin ≥ +5 HP across any of our 6 strikers.
3. **Owner-aware filter**: drop rtvvvvv (no-touch, session 80 rule). Eye stefan97 candidates with caution — if all top results are stefan97, that's the bulk-restart wave and they'll just bulk-stop again before strike. Wait one more cycle.

If the scan returns **a clean non-stefan97 non-rtvvvvv candidate ≥ +5 HP margin**: deploy striker per Priority 2 rules, single attempt.

If the scan returns **only stefan97**: defer briefly (re-wake 30–60 min, named pinning: "stefan97 cycle restart") and write a short note in `predator/learnings.md` about stefan97's cycle.

If the scan returns **0 candidates**: see Priority 4.

---

## Priority 4 — Reconnaissance scan of alternative nodes (no movement, no tx)

When node 86 is quiet, the next leverage is **knowing where the targets live**, not migrating speculatively. Spend ≤10 minutes on an oracle scan of:
- Node 25 (Iron Pier, last session 78/79 read = ~49 zero-def EERIE-body kamis, but 100% jun-guild)
- Node 60 (last session 79 = wiuuuu cluster, 7 SCRAP-soft)
- Node 62 (last session 79 = buja723 cluster, 8 INSECT-soft)
- Node 73 (last session 79 = oracle build_refreshed_ts staleness — POWELL has full Guardian build now)

For each: count current HARVESTING population, count non-guild population, count def_shift=0/def_ratio=0 population, scan for top-margin candidates killable by our best striker.

**Output**: a short table in `predator/learnings.md` § "Roster brief" → new sub-section "Cluster intel snapshot 2026-05-02 23:25 UTC". Reading-only, no movement, no tx. Cluster math gates any actual migration: single-node target counts must justify gas to migrate; migration cost on bpeon's roster is ~10–20M gas (full team move sequence per CLAUDE.md "Predator deployment").

---

## Priority 5 — Build `predator/world_targets.json` background watcher (System Thinking unlock)

Per System Thinking doctrine in CLAUDE.md (just shipped session 89), the highest-leverage infrastructure-build identified is a **background world-targets refresher**. Spec:

```
Cron: */5 * * * *  (every 5 min)
Script: predator/scripts/refresh_world_targets.py
Output: predator/world_targets.json (atomic write)
Schema:
  {
    "generated_at": "2026-05-02T23:25:00Z",
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

Sessions read `predator/world_targets.json` at the top of perception phase instead of running a fresh scan — saves ~30–60s and lets the agent see **trends** (candidates killable across multiple snapshots vs. flash-killable just-restarted).

**Decision gate for session 90**: build it iff (a) Priorities 1+2+3 finish in under 30 minutes, (b) the canonical formula doesn't surface a structural issue, (c) you have ≥45 minutes of remaining session budget. Otherwise, document the design in `predator/infrastructure.md` (create the file) and ship in session 91.

**If you build it**:
- Use `urllib.request` (httpx not available system-wide — confirmed session 89).
- Reuse `executor/oracle_state.py` patterns where possible.
- Read guild blacklist, no-touch owner list, current striker stats from canonical sources.
- Atomic write (`.tmp` → rename) so partial reads never see truncated JSON.
- Document the cron entry in `predator/infrastructure.md` with the exact crontab line, script path, failure mode (oracle-down → must not corrupt JSON).
- Test manually once before adding cron. Verify well-formed JSON + expected fields.
- Add entry to `memory/improvements.md` titled "world_targets.json background refresher" with the cron line.

This is the first concrete System Thinking build. **Do it if you have time.**

---

## Priority 6 — Strike if all gates clear

If Priority 3 surfaced a clean candidate and 180s cooldown has been honored, single strike. Hard rules unchanged: heal-event guard, counter-predator scan, predator co-location, ≥+5 HP margin, no rtvvvvv, no guild.

**On revert**: post-mortem before re-attempting. Canonical is now ground-truth; deep-revert with margin ≥+5 HP is a structural surprise (oracle staleness, on-chain divergence, target-feed between scan and strike, etc.). Document and stop hunting that target until root cause identified.

**On kill**: log predicted vs actual margin, gas (success cost ~3M for first kill on node 86 expected), obol earned, recoil HP. Then re-scan immediately on same node — chain on cluster.

---

## Stop conditions

- First kill on canonical formula → log post-mortem on predicted vs actual margin. Re-wake 5–15 min, named pinning: "chain on cluster after first kill".
- 2 reverts in a row despite passing all gates → stop, log, post-mortem.
- Total gas > 12M without a kill → end session, post-mortem.
- World targets watcher built and tested → log to improvements.md, re-wake 10 min to verify the JSON is being refreshed by cron.

---

## Self-schedule (apply Cadence Discipline)

End-of-session: write `next-run-at` with named pinning. If your candidate pin is fuzzy, fire sooner. Examples:
- *"Stefan97 bulk-restart wave — pools begin growing at ~24:30 UTC, I'll wake at 24:45 to catch the first margin-positive candidates."* ✓
- *"world_targets.json watcher just deployed — wake in 10 min to verify refresh."* ✓
- *"+30 min default for rescan."* ✗ — halve to 10 min, or wake immediately if any concrete next action exists.

If you genuinely need > 30 min: name the pin in one sentence in `decisions.md`. Founder will see it and either accept or correct.

---

## Out of scope

- Force-flush, quest progression, kamibots state reads (forbidden).
- 11224 SP allocation (still gated on first kill).
- Modifying kami-oracle code (route oracle gaps via `ideas_to_founder.md`).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Cadence Discipline block landed in CLAUDE.md: Y/N.
- Cooldown rule re-codified: Y/N.
- Re-scan outcome (candidate / stefan97-only / 0 candidates).
- Recon scan of alternative nodes: brief table.
- world_targets.json watcher built: Y/N (if N, design doc in `infrastructure.md`).
- First kill: Y/N. If Y, predicted margin vs actual.
- `next-run-at` and the **named pin** (one concrete sentence).
