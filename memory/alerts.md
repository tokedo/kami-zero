# Alerts

### 2026-05-03 04:35 UTC (session 98) — Mid-session pivot bypassed pre-deploy heat-check; stefan97 cycle defense re-engaged

Plan-98 was Yeahta @ node 73 (wait or zero-travel strike). Watcher snapshot (gen 04:25Z) showed 16 stefan97 candidates +6 to +49 at node 86 — pivoted plan to that cluster mid-session. **Skipped the pre-pivot heat-check** (session-93 doctrine: dominant farmer last-action <5 min + ≥10 active kamis = monitored). Travel 73→86 (9.94M) + deploy (2.02M) + 2 cookie feeds (3.77M) = 15.7M committed before live spot-check.

stefan97 bulk-stopped + bulk-started ~3 min after my deploy (04:31:37 stop / 04:31:46 start; 143 stops + 116 starts past 12h via oracle). 7 prime watcher candidates spot-checked all RESTING/INACTIVE. Single strike fired before diagnosis: REVERTED 0.29M (target not HARVESTING). Stopped batch (3.70M cleanup), capped loss.

**Doctrine fix (now MANDATORY)**: any mid-session plan pivot to a new target node must run an activity-heat oracle query on the dominant farmer BEFORE travel. If `MAX(block_timestamp) > NOW() - INTERVAL '5 minutes'` AND that farmer has ≥10 active kamis at the node, abort the pivot. Plan-99 carries this as a hard precondition.

**Watcher fix (deferred — build task)**: stefan97 should be on an owner-blacklist in the watcher cron, suppressed from `killable_clean` unless their account has been idle ≥4h. See ideas_to_founder.md for the ask.

**Action**: no harness bug, just plan-discipline failure. Documented in predator/learnings.md § "Session 98 (2026-05-03) — stefan97 cycling pattern reconfirmed".

# Alerts

### 2026-05-03 03:55 UTC (session 97) — 30-min `timeout` cap dropped a partial session

A prior session-97 attempt fired ~03:13 UTC (cron after plan-96's next-run-at 03:08), did substantial on-chain work, and **failed to commit** before the `timeout 30m` cap in `scripts/run-session.sh` killed it. Sequence reconstructed from chain + oracle action stream + git status (no commit = no state snapshot):

- 03:13:55 — 12649 `harvest_start` at node 60.
- 03:17:30 — successful `liquidate` on node 60 (+843 MUSU spoils + 1 obol). Target unknown without `target_kami_id` resolve in oracle.
- 03:18:52 / 03:20:12 — feed + `harvest_stop` (+410 MUSU pool collected).
- ~03:20–03:35 — operator traveled 60→9 (cluster misread; node 9 had only +13 below-gate target), batch start at 9 reverted, per-kami starts succeeded, then both stopped at 9 with no productive harvest (+4/+4 MUSU). Estimated ~20M gas wasted.
- 03:35:45 — `harvest_start_batch([11224,12649], 73)` REVERTED (kami harvest entities still showed node 9 reset_ts).
- Process killed by `timeout 30m`. No `decisions.md` append, no commit, no `next-run-at` update.

A new cron tick at ~03:43 entered the recovery sub-session, observed the strange chain state (operator at 73, kamis RESTING after partial 60→9→73 thrash, plan-96 next-run already past), and recovered by reading current state directly. Recovery succeeded: 2 chain-strike kills on Yeahta@73 with 11224 (kills #12 + #13), netting +2 obols + 2025 MUSU on 16.36M gas (best sub-segment ratio 0.122 obols/Mgas, new doctrine: same-striker chain-kill via mid-feed).

**Lesson — session length budgeting**: Multi-hop travel (60→9 = 6+ hops, 9→73 = 7+ hops) plus harvest-cycle waits (80–195s × multiple) plus strike+stop flows can collectively exceed the 30-min cap. If a planned action sequence is likely to exceed ~25 min wall-clock from cron tick, **trim scope or commit interim state** between phases. Plan-98 carries this forward as a "Hard limit" entry: budget aware of timeout, pivot before exceeding.

**Action**: no harness change yet (the timeout cap exists for runaway-loop safety and shouldn't simply be raised). The fix is plan-side discipline. If this recurs across sessions 98–101, escalate to founder via `ideas_to_founder.md` to consider raising cap or adding mid-session checkpointing.

### 2026-05-02 17:15 UTC (session 83) — Oracle service down two consecutive sessions

`oracle_health` and `oracle_sql("SELECT 1 AS ok")` both errored this session.
Session 82 also saw oracle errors (logged inline in decisions.md). Two
consecutive outages — escalating per session-83 plan rule "If oracle stays
down through session 83, escalate to alerts.md".

Impact: P2 broader cluster scan blocked. Strain-wait on node 86 rtvvvvv
candidates remains the only available filter, and that pool just shrank
(7884 cycled RESTING between sessions 82 and 83). Without oracle, cannot
identify fresh non-guild non-rtvvvvv softs.

Action this session: skipped P2, executed P3 (rtvvvvv stop rule into
predator/targeting.md), no strike. Schedule +90 min and retry oracle.
If still down at session 84, demote to working-around-it (continue live
spot-checks of known candidates) and stop logging the outage every cycle.

### 2026-05-01 15:31 UTC update (session 72) — Q49 still blocked after 7th cumulative claim (cheap probe)

Plan-endorsed cheap probe this session: scav points had naturally accumulated to **14,302 = 143 tiers** since session 71 (no force-flush, ~12h elapsed). Did ONE `scavenge_claim_and_reveal(15)` per the discipline rule — 1.87M gas, +58 Pipes, +69 Butts, +16 Burgers (143 items total, correct).

- `quest_state(49, "bpeon")` post-claim → still `state="active_blocked"`, `revert_kind="objs_not_met"`, raw revert: `quest objs not met: Reverted`.
- Inventory now: **Cigarette Butt 266** (catalog target: ≥15). Drift now ~17.7× over target.
- 7 cumulative post-acceptance claims at node 15 still hasn't moved the needle.
- Natural scav rate confirmed stable: ~1,192 pts/hr/account at node 15 across sessions 70→71→72.

Discipline rule still in force: no more force-flush, no more hypothesis testing. Awaiting founder off-chain Q49 inspection. Schedule: +12h.

### 2026-05-01 03:18 UTC update (session 71) — Q49 still blocked after 6th cumulative claim (cheap probe)

Plan-endorsed cheap probe this session: scav points had naturally accumulated to **14,599 = 145 tiers** since session 70 (no force-flush). Did ONE `scavenge_claim_and_reveal(15)` per the discipline rule — 1.87M gas, +70 Pipes, +63 Butts, +12 Burgers (145 items total, correct).

- `quest_state(49, "bpeon")` post-claim → still `state="active_blocked"`, `revert_kind="objs_not_met"`, raw revert: `quest objs not met: Reverted`.
- Inventory now: **Cigarette Butt 197** (catalog target: ≥15). Drift now ~13× over target.
- 6 cumulative post-acceptance claims at node 15 still hasn't moved the needle. Reinforces the structural drift conclusion.

Discipline rule still in force: no more force-flush, no more hypothesis testing. Awaiting founder off-chain Q49 inspection. Schedule: +12h.

### 2026-04-30 15:25 UTC update (session 70) — drift now confirmed structurally, no gas spent

Tier-1 harness mods shipped this session (commit `b22935c`). Used the new tools to confirm the Q49 mystery is exactly the catalog-vs-chain drift class:

- `quest_state(49, "bpeon")` → `state="active_blocked"`, `revert_kind="objs_not_met"`, raw revert: `quest objs not met: Reverted`
- `get_expected_objective(49)` → catalog says **DROPTABLE_ITEM_TOTAL[1018] ≥ 15**
- Inventory: **134 Cigarette Butts (1018)** — catalog target met ~9× over.
- Chain disagrees → registry-vs-catalog drift, not an empirical-testing problem.

Per the new CLAUDE.md "Quest debugging discipline" rule (added this session), this is escalation territory. **No more gas testing.** Awaiting founder / Kami-team off-chain inspection of the Q49 objective component(s) on-chain.

Cheap probe NOT done this session: node 15 scav at 45/100 pts (0 claimable tiers); plan threshold for cheap claim was ≥1 tier.

### 2026-04-30 ~14:35 UTC — Q49 BLOCKADE persistent, multi-session gas drain (ACTIVE)

Quest 49 ("Community Service") **cannot be cleared empirically** after 5 cumulative `scavenge_claim` transactions at node 15 since acceptance. Three objective-type hypotheses ruled out:

| Hypothesis                          | Disproven via                                                    |
|-------------------------------------|------------------------------------------------------------------|
| `DROPTABLE_ITEM_TOTAL[1018] ≥ 15`   | 129 fresh butts scavenged across sessions 66–69, Q49 stayed FALSE |
| `ITEM_BURN[1018] ≥ 15`              | 15 butts burned in session 68 (1 + 14), Q49 stayed FALSE         |
| `SCAV_CLAIM_NODE[15] ≥ 5` (best fit so far) | 5 separate post-acceptance claim tx now executed, still FALSE |

Live hypothesis: `SCAV_CLAIM_NODE[15] ≥ N` for N ≥ 6 (possibly N=15). Testing N=15 needs ~10 more claim tx. Cost per claim+force-flush cycle this session was MUCH higher than budgeted: `stop_harvest_batch` of long-accumulated harvests cost **~8.5M gas per 5-kami batch** vs ~1.5M originally budgeted. Session 69 hit the 18M gas ceiling after only 2 new claims.

#### Cumulative claim timeline (post-Q49 acceptance 2026-04-29 17:31 UTC)

| # | Session | UTC                  | Tier count consumed | Q49 after |
|---|---------|----------------------|---------------------|-----------|
| 1 | 66      | 2026-04-29 17:30     | 12                  | FALSE     |
| 2 | 67      | 2026-04-30 03:45     | 244                 | FALSE     |
| 3 | 68      | 2026-04-30 10:15     | 11                  | FALSE     |
| 4 | 69      | 2026-04-30 ~14:30    | ~26                 | FALSE     |
| 5 | 69      | 2026-04-30 ~14:35    | ~32                 | FALSE     |

#### What I need from the founder

1. **Off-chain inspection of Q49's objective component(s).** With `component.id.parent` not registered on this World contract, on-chain traversal from quest entity to objectives is blocked from agent side (see `memory/improvements.md` 2026-04-30 KNOWN-BROKEN entry). Even just *the objective type* (DROPTABLE / ITEM_BURN / SCAV_CLAIM_NODE / ITEM_TOTAL / ROOM / etc.) and *its target value/index* would unblock me.
2. **Or**: confirmation that Q49 is structurally broken / mis-deployed and should be skipped via direct registry edit / quest-drop tooling.

#### Side-effect observed this session: reveal-revert regression at node 15

`scavenge_claim_and_reveal` REVEAL step **reverted on both session-69 claims** at node 15. Sessions 66/67/68 had no reveal reverts at this node. The harness handled it gracefully (`reveal_skipped` flag) and items materialized in inventory at approximately expected counts (52 items vs ~58 expected — RNG-consistent, possibly minor loss). Worth investigating if this becomes systematic.

#### Bot autonomy decision while blocked

Continuing to do single-claim tx every 6–12h would still burn significant gas to test N=15 with the unexpectedly high force-flush cost. Without founder input, the next session will:

- Not perform new claims at node 15 unless natural scav points ≥1 tier accumulate without force-flushing (cheap probe).
- Continue auto_v2 grind for MUSU income.
- Wait for founder off-chain investigation before committing more gas to this hypothesis.

Schedule for next session: +12h (give founder time to inspect).

---

## Resolved

### 2026-04-09 ~17:24 UTC — Kamibots platform-wide infra reset (RESOLVED — strategy relaunched session 2)
Platform reset removed all running strategies. auto_v2 relaunched and stable since.

### 2026-04-09 14:17 UTC — Kamibots strategy containers broken (RESOLVED session 2)
Supabase key error. Fixed server-side by Kami team. auto_v2 working as of 2026-04-09 17:14 UTC.
