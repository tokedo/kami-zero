# kami-zero session 74 prompt — transfer prep: force-stop in-flight harvests (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. After founder review, push to `~/kami-zero/memory/plan.md` and commit.

---

## ⚠️ Single-purpose session

Session 73 halted the auto_v2 strategy but left 17 kamis HARVESTING (per the prompt's "no force-flush" rule, which was wrong for this context). Founder is now ready to transfer kamis between accounts, and **transfer requires the kami to be RESTING** — not in-flight on a node. So this session does one thing: force-stop the 17 HARVESTING kamis so all 20 are at the operator and transferable.

**Predator doctrine and hard rules from CLAUDE.md still apply** — but this session's gas spend is a one-time transfer-prep cost authorized by the founder, NOT a violation of "no force-flush in predator mode" (that rule is about hunt-loop discipline, not transfer logistics).

After this session: report back to founder via `decisions.md` with the post-state. Schedule a long delay; founder will wake kami-zero when the transfer is complete and predators are loaded.

---

## Priority 0 — Force-stop in-flight harvests, batched

Target kamis (17 HARVESTING per session 73 baseline):

```
43, 1064, 2553, 6096, 7803,
8745, 10011, 10647, 11716, 12459,
13235, 13390, 13702, 13857, 13947,
14286, 14306
```

Already RESTING (do NOT touch): `3874, 3983, 7722`.

**Batching**: per session 69's empirical lesson, gas scales with batch size and harvest age. Use **batches of 5** (final batch of 2). Four batches total:

| Batch | Kami IDs |
|-------|---------|
| 1 | 43, 1064, 2553, 6096, 7803 |
| 2 | 8745, 10011, 10647, 11716, 12459 |
| 3 | 13235, 13390, 13702, 13857, 13947 |
| 4 | 14286, 14306 |

Procedure:

1. Pre-state read: `get_account_kamis("bpeon")` once. Confirm 17 H / 3 R matches expectation. If a kami already moved to RESTING since session 73 (HP-decay cycling), drop it from the batch list.
2. For each batch in order: `stop_harvest_batch([kami_ids], "bpeon")`. Log return value, gas used, and any silent-skips to `decisions.md` immediately after the batch.
3. After all four batches, run `get_account_kamis("bpeon")` once more. Expected: 0 HARVESTING / 20 RESTING. If any kami is still HARVESTING (silent-skip per session 69's kami 2553 anomaly), retry that kami solo: `stop_harvest_batch([id], "bpeon")`.
4. If a solo retry also silent-skips, log the kami ID + symptoms to `memory/alerts.md` and continue. Do NOT block the session on a single stuck kami — founder will handle.

**Gas expectation** (sanity bounds, not budget caps):
- Best case (most harvests <2h old after the 60h auto_v2 cycle): ~5–7M gas total.
- Worst case (some kamis untouched by auto_v2 for >6h): up to ~25–35M gas total.
- Anything north of 40M is anomalous — pause batches, log to alerts.md, escalate to founder.

---

## Priority 1 — Update predator/metrics.md row

Append a row reflecting this session even though no obols/musu earned. The metrics file is the long-term feedback loop; transfer-prep gas counts.

```
session, started_at, ended_at, gas_spent_gwei, obols_earned, musu_earned,
kamis_liquidated, items_consumed, nodes_visited, claude_tokens_used,
notes
```

For session 74, fill values; leave `claude_tokens_used` blank if harness doesn't expose it. Note column: `transfer-prep stop_harvest_batch ×N kamis; one-time cost authorized by founder, not a doctrine violation`.

---

## Priority 2 — Update decisions.md and ideas_to_founder.md

`decisions.md`: standard session entry. Pre-state, per-batch gas, post-state, silent-skip count, total gas.

`ideas_to_founder.md`: mark item 2 (predator team transfer) as **READY** — all 20 kamis at operator, awaiting founder action. Move item 2 from "Pending" to "Standing" with a status line: `READY for founder action — all 20 kamis at operator and transferable as of <timestamp>`.

---

## Stop conditions

- All 20 kamis RESTING → end session.
- Any silent-skip after a solo retry → log to alerts.md, continue. End session anyway.
- Total gas >40M → pause and log; founder will decide whether to continue.
- **No other actions this session.** No leveling, no oracle queries, no doctrine refinement, no Q49 probes. Pure transfer prep.

---

## Reschedule

`+72h` (3 days). Founder will manually wake kami-zero when the transfer is complete and predators are loaded. If kami-zero wakes naturally before that, the next session reads `ideas_to_founder.md` first to check if transfer status changed.

---

## Commit discipline

Single commit, prefix `session:`, message:
```
session: 74 — force-stop in-flight harvests for transfer prep

All 17 HARVESTING kamis stopped via stop_harvest_batch (batches of 5).
Total gas: <X> M. Final state: 20/20 RESTING. Predator team transfer
unblocked; ideas_to_founder.md item 2 marked READY.
```

---

## What is NOT in scope this session

- Any movement, leveling, quest action, oracle deep-dive, doctrine refinement.
- `force_harvest_start` or any node-side action — transfer requires kamis at the operator, NOT at a node.
- Item feeding to recover HP — kamis can transfer at any HP level. Healing happens post-transfer or pre-hunt.
