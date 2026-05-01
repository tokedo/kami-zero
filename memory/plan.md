# kami-zero session 75 prompt — learning window: characterize the new roster, deepen mechanics, write first hunt plan (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. After founder review, push to `~/kami-zero/memory/plan.md` and commit.

---

## ⚠️ Single-purpose session: LEARN before hunting

Founder transferred the elite predator team to bpeon at ~2026-05-01 23:30 UTC, plus a starting pack of items, ~500k MUSU starting capital, and abundant stamina recovery items. **Per-kami transfer cooldown is ~1h** — the new predators can't act yet. This is exactly the window doctrine wants: *data work, not movement*.

Use this session to characterize the new roster, deepen liquidation mechanics, and produce a written first hunt plan in `predator/learnings.md`. Do **not** move or strike this session. The next session (75 or 76 depending on agent's call) executes the first hunt **autonomously, without waiting for founder approval**.

---

## Standing authorizations from founder (read carefully — these widen what you may do without asking)

The founder will not approve session-by-session decisions. These standing authorizations apply going forward:

1. **MUSU spending** at shop and marketplace is at your discretion. Use the 500k starting capital however your judgment says best serves obol-per-tx growth — predator-class consumables, recovery items, gear, etc. Log every purchase to `predator/metrics.md` (`musu_spent` column you'll add) and brief rationale in `decisions.md`. There is no per-session cap. If a single purchase exceeds 100k MUSU, mention it in `ideas_to_founder.md` for visibility — **not for approval**, just so the founder sees it on their next read.

2. **Stamina recovery items** are abundant — use them freely so a roaming assassin is never blocked from reaching a cluster because the operator is low on stamina. *But:* these took kami-agent real effort to farm; don't waste them. Heuristic: use one when stamina is genuinely the gating factor on a worth-it move; don't pre-emptively top up at 99/100.

3. **Kami 11224 has 3 unspent skill points.** You do NOT allocate them this session. Allocate only after you (a) understand liquidation mechanics deeply, (b) observe 11224 in real hunts to see its actual role / affinity, and (c) write the rationale to `predator/learnings.md` first. Respec is possible but costs a rare "mint" item plus many tx — get it right on the first allocation.

4. **Tool builds (the 4 gaps from session 73)** — build them when *you* judge them needed, in the order *you* judge useful. The founder authorizes the build envelope as a whole; you don't need per-build approval. Prefer building only what's blocking your next concrete action; don't build all four upfront.

5. **`ideas_to_founder.md` items are non-blocking.** The founder reviews periodically and asynchronously. Never wait on a `ideas_to_founder.md` item to act. If something would otherwise block action, fix it on your side or work around it.

6. **Self-paced cadence** — set `next-run-at` based on what *you* observe (live targets / live cooldowns / quiet world). Founder does not gate the schedule.

These authorizations are **standing** — they apply to every session from this one onward. Add a "Standing authorizations" section to CLAUDE.md (Block E below) so future-you sees them on every session start.

---

## Priority 0 — Read the transfer landing

`get_account_kamis("bpeon")` — confirm the new predator roster. Compare to session 74's pre-transfer baseline (the 20-kami list now mostly different). Capture:

- Full new roster: kami IDs, names, current state (RESTING/HARVESTING — should all be RESTING from cooldown).
- For each kami: level, body, hand, traits — note especially attack-relevant traits.
- Note kami 11224 specifically: 3 unspent SP, current allocation tally, body+hand affinity.
- Whether any expected kami is missing or any unexpected kami present (signals partial-transfer or other anomaly).

`get_inventory("bpeon")` — confirm:
- ~500k MUSU.
- New items received (predator consumables, gear, etc.).
- Stamina recovery items: count by type (Ice Cream, Better Ice Cream, Rock Candyfloss, etc. — call out any abundance unusually high).

`get_account("bpeon")` — current operator stamina (100/100 expected).

Snapshot all three reads to `decisions.md`.

---

## Priority 1 — Update CLAUDE.md and ideas_to_founder.md to reflect autonomy

### CLAUDE.md — add Block E (Standing authorizations)

Insert above Block A (Operational Mode banner) so it's the very first thing future-you reads:

> ## Standing Authorizations (founder, 2026-05-01)
>
> The founder will not approve session-by-session decisions. These authorizations apply to every kami-zero session going forward:
>
> 1. **MUSU spending** at shop / marketplace is at your discretion. Log purchases in `predator/metrics.md` + rationale in `decisions.md`. No per-session cap. Single purchases > 100k MUSU: mention in `ideas_to_founder.md` *for visibility, not approval*.
> 2. **Stamina recovery items** are abundant — use freely when stamina genuinely gates a worth-it move; don't waste them.
> 3. **Skill points / build decisions** — your call after understanding mechanics. Write rationale to `predator/learnings.md` before allocating. Respec is expensive (rare "mint" + many tx); get it right the first time.
> 4. **Tool builds** — judge needed-ness yourself; build only what unblocks the next concrete action.
> 5. **`ideas_to_founder.md` is async / non-blocking.** Never wait on it. If something would block action, fix it locally or work around it.
> 6. **Self-paced cadence** — set `next-run-at` from observation, not from a fixed schedule.
>
> Default: act. Ask founder only via `ideas_to_founder.md` (async visibility). The metrics trend in `predator/metrics.md` is the feedback loop, not session-by-session approval.

### ideas_to_founder.md — restructure as async-only

Move the "BLOCKER" framing out. Items are visibility / FYI / strategic asks the founder *might* address when they review. Add this preamble at the top of the file:

> **This file is async and non-blocking.** kami-zero writes here when something would benefit from founder attention but never to gate kami-zero's action. Founder reviews periodically. If kami-zero needs to act and a `ideas_to_founder.md` item touches the action, kami-zero acts anyway with whatever workaround it judges best.

Also: rewrite item 2 (predator team transfer) — that's now DONE; move to "Resolved" with a note.

### `predator/metrics.md` — add columns

Update the column header to include `musu_spent` and `musu_balance_end`:

```
session, started_at, ended_at, gas_spent_gwei, musu_spent, musu_balance_end,
obols_earned, musu_earned, kamis_liquidated, items_consumed, nodes_visited,
claude_tokens_used, notes
```

Backfill blank `musu_spent` / `musu_balance_end` columns for existing session rows (just commas, since prior sessions didn't track this).

---

## Priority 2 — Deepen liquidation mechanics (the session 73 carryover)

You logged "known unknowns" to `predator/mechanics.md` in session 73. Resolve as many as you can this session. **Use kamigotchi-context, GDD, and on-chain reads — figure it out from primary sources.** Specific carryovers:

1. **`system.harvest.liquidate` ABI.** Read `executor/server.py` to find how systems are resolved and which one(s) liquidate uses. Document the function signature, params, gas cost (estimate from past on-chain calls if you can sample any).
2. **`harvest_id → kami_id → node_id` traversal.** Pick a recent `harvest_liquidate` row from oracle (within last 7d), then resolve target_kami_id and node_id via on-chain component reads. Document the traversal path so future tools can use it.
3. **What does `amount` represent in `harvest_liquidate` rows?** Hypotheses to test: obol payout, MUSU bounty stolen, harvest tier consumed. Compare a known liquidator's recent `amount` sum vs their on-chain obol balance change over the same window if observable. If unobservable from current data, document as an open question and move on.
4. **Liquidatable threshold.** What HP threshold makes a kami liquidatable? Read GDD `mechanics/liquidation.md` (or equivalent) — should give the formula. Cross-check against a few real liquidations from oracle (target HP at time of strike, if recoverable).
5. **Attacker stat → obol payout relationship.** GDD again — does attacker level / body / hand affect payout? If unclear from docs, note it as a hypothesis to test once you start hunting.

Update `predator/mechanics.md` with concrete answers (and clearly-marked open questions where you couldn't answer). Cite sources (GDD path, oracle row, on-chain call).

Time-box this priority to ~30 minutes of recon. Quality over completeness.

---

## Priority 3 — Roster characterization

For each new predator kami:

- Base stats (HP max, attack-relevant stats — figure out from harness which stats are which).
- Skill point allocation — which trees, which tier, what role does the build optimize for?
- Body + hand traits and any affinity bonuses.
- **One-line "best target archetype"** based on stats + traits (e.g. "fast-moving low-HP target", "high-HP slow target", "specific node type").

Append to `predator/learnings.md` as a **Roster brief — session 75** section. Include 11224 with explicit "3 unspent SP — pending allocation" and your *initial* read on what the build would benefit from (don't allocate yet).

Identify the 1–2 strongest predators in the roster — "the spearhead." Future hunt plans likely lead with these.

---

## Priority 4 — Write the first hunt plan (do NOT execute)

Using everything above plus oracle data, produce a **First Hunt Plan** section in `predator/learnings.md`:

1. Target node candidates — top 3, with rationale (target density, recent liquidation activity, distance from current operator location, presence of counter-predators).
2. For each candidate node, expected liquidatable targets (kamis with HP below threshold per the formula you derived in P2). Apply the guild-no-touch gate: filter out any target whose `account_id` or `handle` matches `predator/guild-no-touch.csv`. Note unresolved-handle entries and treat them as no-touch.
3. Counter-predator scan per candidate node — who else is sitting there, what's their archetype, do mutual-kill math hold up?
4. The pick — single node + rationale + which kamis travel + estimated gas + estimated obol return.
5. **Trigger condition**: under what circumstances do you execute the plan vs revise it? (e.g. "execute if cluster ≥N targets confirmed at wake; revise if cluster <N").
6. Bail-out rules: if anything looks off when you wake, what falls through to the next session.

This plan does NOT execute this session. The next session reads it and either executes or revises it based on the wake-time state.

---

## Priority 5 — Schedule next session

Your call. Suggested reasoning:

- New predators have ~1h cooldown from transfer time (~23:30 UTC). They can act ~24:30 UTC = 2026-05-02 00:30 UTC.
- If your hunt plan in P4 is concrete and the cluster looked live in oracle data → schedule re-wake shortly after cooldown ends (60–90 min from now).
- If the plan needs more recon (e.g. mechanics still unclear, target picture fuzzy) → schedule longer (4–6h) and use the next session for more learning before first strike.

You decide. Write `next-run-at` and a brief rationale to `decisions.md`.

---

## Stop conditions

- All five priorities done → end session.
- If the new roster is missing or unexpected (e.g. fewer than expected predators present, or guardians still on bpeon) → log to `alerts.md`, finish whatever priorities don't depend on the missing roster, end session, schedule short re-wake (1–2h) for founder visibility on next read.
- **No movement, no strike, no liquidation this session.** Cooldown gates it anyway, but the doctrine is the harder constraint: first-strike requires a written plan that's been on the page for at least one session.

---

## Commit discipline

- One commit per file family:
  - `pivot:` for CLAUDE.md (Block E addition)
  - `pivot:` for `predator/metrics.md` (column update + ideas_to_founder.md preamble)
  - `predator:` for `predator/mechanics.md` and `predator/learnings.md` updates
  - `session:` for `memory/decisions.md`, `memory/improvements.md`, `next-run-at`
- Mention "session 75 — learning window, no on-chain action" in the session commit body.

---

## Communication back to founder

End-of-session, in `decisions.md`:
- New roster summary (count + the 1–2 spearhead picks).
- Mechanics resolved (count out of 5 carryovers from P2).
- First-hunt plan: which node, expected return, trigger condition.
- `next-run-at` and rationale.
- Any anomalies in `alerts.md` (should be empty unless transfer was incomplete).

Founder reviews when they get to it. **Do not wait on review** — the next session executes per your written plan.
