# Alerts

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
