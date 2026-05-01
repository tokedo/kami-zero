# Plan for session 76 — execute first hunt (or revise)

Read at session start: `predator/learnings.md` "First Hunt Plan — session 76 candidate" section. That spec defines targets, attacker pick, trigger condition, bail-outs, item usage. **Apply it; do not freelance.**

## Priority 1 — Build the liquidate MCP tool (gating step)

`liquidate` is NOT yet in `executor/server.py`. Strike cannot happen without it. Build first, strike second.

1. Add `_ABI_HARVEST_LIQUIDATE` next to `_ABI_HARVEST_STOP` in `executor/server.py`:
   ```python
   _ABI_HARVEST_LIQUIDATE = json.loads(
       '[{"type":"function","name":"executeTyped",'
       '"inputs":[{"name":"victimHarvestID","type":"uint256"},'
       '{"name":"killerKamiID","type":"uint256"}],'
       '"outputs":[{"type":"bytes"}],"stateMutability":"nonpayable"}]'
   )
   ```
2. Add `liquidate(target_kami_id, attacker_kami_id, account)` MCP tool. Use `_harvest_entity_id(target_kami_id)` for victimHarvestID, `_kami_entity_id(attacker_kami_id)` for killerKamiID. Gas limit **7,500,000** (GDD requirement).
3. Wire in the **guild-no-touch gate**: load `predator/guild-no-touch.csv`, check `Updated:` line ≤ 7 days old (else hard-fail "deny all"), match target by account_id then handle. Block tx if matched. This is hard rule #1 — encode in code, not memory.
4. Document in `memory/improvements.md` (separate `harness:` commit).
5. Restart MCP server: tool surfaces only after restart. Command per past sessions: `pkill -f 'server.py' && nohup ... &` — find the pattern in past `improvements.md` entries.

Optional but useful: build a `scan_node_for_targets(node_index)` read-only helper composing `get_all_kamis` + `get_kami_state_slim` + guild gate. Gap 2 in session 73 audit.

## Priority 2 — Live perception of node 86

After tool restart:
1. `get_account_kamis("bpeon")` — confirm 6 kamis still RESTING (or HARVESTING after auto-cycle? new owner means no auto_v2 — they're idle). Confirm cooldown expired (post 2026-05-02 00:08 UTC).
2. `get_all_kamis()` (full population) — filter `nodeIndex == 86 && state == "HARVESTING"`. Cross-reference with the top-15 7d-liquidators (oracle query in learnings.md "Counter-predator scan") to flag dangerous occupants.
3. For top 5 non-guild candidates by HP%-low + bounty-high, `get_kami_state_slim` to get exact HP, harmony, body-affinity.
4. Compute kill threshold per `predator/mechanics.md` formula for our spearhead vs each candidate.

## Priority 3 — Execute first hunt (if trigger condition met)

Trigger from learnings.md:
- ≥ 5 non-guild HARVESTING kamis on node 86, AND
- ≥ 3 of those with V:H ratio ≤ 2, AND
- No top-15 7d-liquidator currently HARVESTING on node 86.

If met:
1. Pop **Hostility Potion** (item 11410) on chosen attacker via `use_account_item`. Read attacker stats pre/post.
2. `liquidate(target_kami_id, attacker_kami_id, account="bpeon")` — first strike with 12649 unless target H ≥ 18 (then 11224).
3. Verify: `get_inventory("bpeon")` for obol delta (item 1015 should appear/+1) and MUSU delta. `get_kami_state_slim(attacker)` for HP/strain post-recoil.
4. Decide whether to chain a second strike based on attacker HP, cooldown, and whether new candidates qualify.

If trigger NOT met:
1. Document the recon to `predator/learnings.md` (what was on the node, why it didn't qualify).
2. Bump `predator/metrics.md` row with 0 kills + notes.
3. Schedule next wake +3–6h to let prey accumulate.
4. **Do not freelance a strike.** Doctrine: data work, not movement.

## Priority 4 — Allocate 11224's 3 SP only IF observed

Founder rule: allocate only after observing 11224 in real hunts. If session 76 produces no kill, leave the 3 SP unspent. Write the rationale either way to `predator/learnings.md`.

If we DO see 11224 strike: note the recoil HP cost and whether the V36 broke through where 12649's V34 wouldn't. Initial allocation idea (refined per observation):
- 113 Mercenary 4→5 (max tier 1, +1)
- 132 Vampire 1 OR 133 Bandit 1 (tier 3 entry — exclusive with Warmonger 131; pick based on recoil cost observed). Reason for Vampire/Bandit over Warmonger: 11224 is glass-cannon (HP 230, lowest harmony 11), so heal-on-kill (Vampire) or extra spoils (Bandit) > +threshold (Warmonger).

## Priority 5 — Metrics + commit

End of session, append a row to `predator/metrics.md` with:
- gas_spent (sum of all liquidate tx + tool-build tx if any)
- musu_spent (Hostility/Grace/etc)
- musu_balance_end
- obols_earned (count of successful liquidations = obol delta)
- musu_earned (spoils MUSU credited via harvest bounty pickup)
- kamis_liquidated count
- items_consumed (e.g. `Hostility:1;Grace:0`)

Commit discipline:
- `harness: liquidate tool + guild-no-touch gate` (separate commit)
- `predator: session 76 hunt result` (mechanics/learnings/metrics)
- `session: 76 — first hunt`

## Priority 6 — Next session schedule

Set `next-run-at` based on:
- If 1+ kill: short re-wake (60–90 min) — the cluster is live and we want to repeat-strike before the prey scatters.
- If 0 kills with valid recon (nothing qualified): 3–6h to let prey re-populate.
- If something blew up (tool reverted, guild-roster stale, etc.): write to `alerts.md`, longer wake (12h) for founder visibility.

## Read at start

- `memory/alerts.md` — founder may have replied
- `ideas_to_founder.md` — async items
- `predator/README.md` — doctrine refresher
- `predator/mechanics.md` — kill formula reference (esp. recoil)
- `predator/learnings.md` — Roster brief + First Hunt Plan (the spec for this session)
- `predator/guild-no-touch.csv` — verify `Updated:` line ≤ 7 days old before any strike
