# kami-zero session 81 prompt — revive + co-location doctrine + continued hunt (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. After founder review, push to `~/kami-zero/memory/plan.md` and commit.

---

## ⚠️ Two additions from founder, on top of your own session 80 plan

Your session 81 plan was good (live-gate, low-Harmony long-runners, owner blacklist, pre-flight checklist). It's preserved below as Priorities 2–5. Founder added two corrections that should go ahead of the hunt:

### Addition A — Revive 12649 with Red Ribbon Gummy. ONE FREE TX.

You said in session 79 that revive was blocked because "no Onyx Shards." Wrong — that's only the heavyweight `system.kami.onyx.revive` path. The catalog has TWO additional revive items already in your inventory:

| Item | Index | Cost | Effect |
|---|---|---|---|
| Red Ribbon Gummy | 11001 | 1 ribbon (you have **99**) | RESTING, **+10 HP** — via `feed_kami` / `system.item.use` |
| Melkarth's Heroic Awakening Spell Card | 11002 | 1 card (you have **1**) | RESTING, **+50 HP** — via `feed_kami` / `system.item.use` |

The use mechanism is **the same primitive you already used** for Cheeseburger (heal in session 80) and Hostility Potion (in session 77): `feed_kami(item_index, target_kami_id)`. There's nothing to "verify" — the catalog row IS the spec (`Type=Revive`, `effect=STATE-RESTING,HP+10`).

Operating rule going forward: if `catalogs/items.csv` has the effect string for an item, that's authoritative. Don't defer with "mechanism unverified." The catalog *is* the documentation.

### Addition B — Predator co-location with operator (doctrine, not a hard rule)

The liquidation system requires `attacker.account.room == target.node.room`. There is essentially no scenario where leaving a predator on a node and moving the operator elsewhere is correct — predators aren't deploy-and-forget like harvesters or guardians. They need the operator co-located to act.

This may already be why session 80 burned 17.9M gas on the 30→86 travel: at some point the operator drifted from room 86 while predators stayed at node 86, and you had to pay to reunite them.

Going forward: when the operator moves, **all predators move with it** — `harvest_stop` everyone first, travel together, `harvest_start` together at destination. If a session ends with the operator-room ≠ kami-node for any predator, log it to `alerts.md` and reunite next session before any strike attempt.

---

## Priority 0 — Revive 12649 (1 tx, ~1.5M gas)

`feed_kami(item_index=11001, target_kami_id=12649)` — Red Ribbon Gummy → 12649 RESTING at 10 HP.

Optional follow-ups same session if you want 12649 in fighting shape:
- `feed_kami(11002, 12649)` (Melkarth Spell Card) → +50 HP → ~60 HP total. Spell card is rare (you have 1) — use it for the spearhead.
- A few more Cheeseburgers / ribbons as needed to hit ~80% of max HP (270) before next active deploy.

After: snapshot inventory and roster state to `decisions.md`. Roster is now 6/6 again (if you used Melkarth, mention the inventory delta).

---

## Priority 1 — CLAUDE.md doctrine updates

Two small additions to the existing CLAUDE.md (these were carried from session 80 P2 — fold them in this time, don't defer further):

### 1a. Block F (Knowledge Sources) — top of file, above Standing Authorizations

Per session 80 plan. Add the canonical-doc pointer block exactly as session 80 prompt described, with one extra entry: **`catalogs/items.csv` — authoritative for item effects. The Type column and the effect string are the spec. No "mechanism unverified" defers.**

### 1b. Predator Doctrine — add a "Predator deployment" thought-block

Append to the existing Predator Doctrine section:

> **Predator deployment.** Predators are not deploy-and-forget. Liquidation requires `operator.room == target.node.room` — a predator HARVESTING on node X while the operator is at room Y can never fire `liquidate`. When the operator moves, **all predators move with it**. Standard sequence: `harvest_stop` every predator → travel → `harvest_start` at destination. If a session ends with operator-room ≠ any predator's node, that's an anomaly — log to `alerts.md` and reunite next session before any strike. There are no realistic scenarios where partial-team moves are correct.

### 1c. Update targeting heuristic and cadence per session 80 plan

Same as session 80 P2 carryover — current-HP doctrine, cadence norms 10–30 min active. Lock these in if not already done.

---

## Priority 2 — Continue the hunt (your session 80 plan, lightly amended)

Hunt low-Harmony long-runners with the live-gate per your session 80 plan. Pre-flight checklist, owner blacklist, threshold compute — all unchanged.

**Two small amendments based on session 80 findings:**

- **Strain rate is empirically ≤ 0.072 HP/min on H≥25 skill-boosted farmers**. Use this in projection. Update `predator/mechanics.md` "Empirical layer" section with the H-tier strain rate table.
- **Listing has no oracle action-row.** Live `state==HARVESTING AND balance>0` is mandatory. This is now in `predator/learnings.md`; keep it operational.
- **Target churn ~10 min on auto-managed farms.** Inline pre-strike re-read is cheaper (~0.28M for early-revert) than blind strike (2.68M for deep revert). For a target that passed the pre-flight scanner ≥3 min ago, do the slim re-read in the same MCP round-trip as the liquidate call.

**Owner blacklist update:** rtvvvvv (3 reverts: 3764, 13253, 15538). If founder later confirms that rtvvvvv farms have *un*usually high Guardian SP investment as a known build, blacklist might extend to other farms with similar shape.

**Where to hunt:** since operator is now at room 86 (post session 80) and 11224 + the rest of the predator team are at node 86, default to scanning node 86 first. Don't move the operator unless cluster math at a different node decisively justifies the travel cost (session 80's 17.9M-gas reminder).

---

## Priority 3 — Reconcile predator/mechanics.md (carried from session 80 P1)

Same as before — replace empirical-derived sections with cross-references to `systems/liquidation.md`. Add the new H-tier strain rate empirical row. Do this only after Priority 0–2 attempts.

---

## Priority 4 — Roster state-of-the-team check

After revive, take stock of the 6-kami roster:
- 12649 (Spearhead-A, V34/H20/HP270) — revived, healing
- 11224 (V36, EERIE-hand, 3 SP unspent) — currently RESTING node 86 ~140 HP
- 6058 (SCRAP-hand)
- 10705 (INSECT-hand)
- 12225, 15540

For 11224's 3 unspent SP: still deferred until you've seen the kami in a successful strike. After your first kill — and only after — write a rationale in `predator/learnings.md` and allocate.

For team composition: note which affinity matchups each kami is best for. The targeting heuristic should pair the right striker to each candidate.

---

## Priority 5 — Self-schedule

Cadence per CLAUDE.md norms. After a kill: 15 min re-wake (chain on the same cluster). After a no-kill but live targets identified for next session: 20–30 min. Genuinely quiet (no soft targets after a thorough scan): 45–60 min, not more.

If you find yourself wanting > 60 min, write the reasoning in `decisions.md` first.

---

## Stop conditions

- First kill → scan and chain on same node. Don't leave a hot zone.
- 3 consecutive deep-reverts despite passing pre-flight → stop, re-read `systems/harvesting.md` strain section, log post-mortem.
- Roster ≤3 healthy strikers → defensive mode (you should be at 6 after Priority 0).
- Total gas > 50M without a kill → end session, post-mortem.

---

## Out of scope

- 11224 SP allocation (still gated on first kill).
- Quest progression (paused).
- Cluster moves to nodes 60/62 (cancelled session 80, do not revisit unless you've re-scanned and the math now decisively justifies travel).
- Any operator move > 1 hop without `harvest_stop` on every predator first (per Predator deployment doctrine).

---

## Communication back to founder

End-of-session in `decisions.md`:
- Did first kill land? Y/N.
- 12649 revive status (Y, +HP delta, used items).
- Total gas, total tx.
- Cadence chosen, why.
- Roster co-location at session end (operator-room and each predator's node — they should match).
