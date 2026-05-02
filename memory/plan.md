# kami-zero session 80 prompt — doctrine correction (founder-authored)

This is a complete replacement for `memory/plan.md` on the VM. After founder review, push to `~/kami-zero/memory/plan.md` and commit.

---

## ⚠️ Three corrections from the founder, in order of priority

Founder reviewed sessions 76–79 (26.1M gas, 0 kills, 5 strikes all reverted, 1 of our kamis killed by a counter-predator). Three things were wrong, all course-correctable:

### Correction 1 — STOP DERIVING MECHANICS EMPIRICALLY. Read the docs.

The kami-zero repo inherits `kamigotchi-context`'s full `systems/` distillation. The kill threshold formula, the Skills 323 + 341 Armor defense ratio, the affinity bonus magnitude, the "kami lacks violence (weak)" error string, the gas limit (7.5M) — **all of it is already documented** in your own working directory:

- **`~/kami-zero/systems/liquidation.md`** — the agent decision guide for liquidation. Kill condition (`threshold > currentHealth`, with **current** health), animosity formula (Gaussian CDF over Violence/Harmony ratio), threshold efficacy (affinity matchup), shift modifier (Predator/Guardian skill bonuses), recoil math, loot distribution, defensive vs offensive decision rules, gas requirement (7,500,000), entity ID derivation. **READ THIS FILE END-TO-END BEFORE PLANNING ANY STRIKE.**
- **`~/kami-zero/systems/harvesting.md`** — strain rate, HP decay over harvest time, affinity-on-node mechanics. Critical for projecting current HP from harvest start time.
- **`~/kami-zero/systems/state-reading.md`** — how to read live kami state (current HP, strain, harvest start time, etc.) and project future HP.
- **`~/kami-zero/systems/leveling.md`** — Predator tree (122/142/162 = ATS, 121/151 = ATR), Guardian tree (323 Armor + 341 = DEF_THRESHOLD_RATIO contributors).
- **`~/kami-zero/integration/system-ids.md`** + **`~/kami-zero/integration/abi/`** — system addresses, ABIs.
- **`~/kami-zero/strategies/`** if it exists (contains predator-threat-assessment if inherited from upstream) — strategy patterns.

**Operating rule going forward:** if a question can be answered by reading a `systems/*.md` file, **read that file first**. Do not run an on-chain experiment that costs gas to discover what's already documented. `predator/mechanics.md` should be cross-references back to the canonical `systems/*` docs, not a parallel record. Move agent-empirical observations into `predator/learnings.md` (per-session experience).

### Correction 2 — TARGETING REFRAMED: hunt by CURRENT HP, not base stats

The session 79 "soft-filter v2" (`def_shift = 0 AND def_ratio = 0`) was wrong-headed. Founder direct quote (2026-05-02):

> "we should look for any kamis (outside of guild) that have low HP left — ideally below liquidation threshold so we pop on the node and take them down. People often leave their kamis to harvest for longer (more musu / less tx) and as a result they often go to 'dangerous zone' in their HPs. But because now there are no predators in the game, this often works and leads to huge musu inflation. Kami-zero should be scanning for such kamis that have low current hp, not low base stats."

This matches `systems/liquidation.md` § "Estimating If Target Is Killable":
> 1. Estimate target's projected HP (from strain over time)
> 2. Calculate your kill threshold (Violence vs their Harmony)
> 3. If projected HP < threshold → killable

**The hunting heuristic is now:**

1. Find HARVESTING kamis (any base stats — don't pre-filter by build).
2. Filter out guild members (`predator/guild-no-touch.csv`, account_id or handle match).
3. **Project each candidate's CURRENT HP** from `harvest_start_ts` + strain rate. The longer the harvest, the lower the HP — kamis left running for hours are the prime targets.
4. Compare projected current HP vs your kill threshold for that target (animosity × efficacy × maxHP, per the formula in `systems/liquidation.md`).
5. Strike when projected HP < threshold. Distance / cluster economics are secondary — single juicy targets justify a move if the obol math works after travel cost.

**The cluster move plans to nodes 60/62 from session 79 are CANCELLED.** Those were targeting full-HP kamis with low base stats — wrong-headed. Restart from the new heuristic on whichever node has the most candidates with low projected HP.

### Correction 3 — CADENCE AGGRESSIVE

Founder is fine spending compute. Multi-hour gaps between sessions are wrong when the world is active. Norms:

- **Active hunting** (live targets identified, cooldowns short): re-wake **10–30 min**.
- **Strain-wait or recon** (waiting for a specific kami's HP to cross threshold): re-wake at the projected crossing time, +/- 5 min buffer.
- **Genuinely quiet world** (zero candidates after a thorough scan): up to 1–2 hours, not more.

Cron tick has been bumped to **`*/5`** (was `*/15`) so your chosen `next-run-at` is honored to within 5 minutes. If you ever feel constrained by cron, propose a finer tick in `improvements.md` — but `*/5` should be plenty.

---

## Priority 0 — Read the docs (before any tool calls beyond `get_account_kamis`)

Open and read in full:

1. `~/kami-zero/systems/liquidation.md`
2. `~/kami-zero/systems/harvesting.md` — focus on strain rate and HP-over-time projection
3. `~/kami-zero/systems/state-reading.md` — focus on how to read current HP and harvest start time

Skim:
4. `~/kami-zero/systems/leveling.md` — Predator and Guardian skill trees (so you know what `bonuses.attack.threshold.shift`, `defense.threshold.ratio`, etc. mean and where they come from).
5. `~/kami-zero/strategies/` if it exists — particularly any predator-threat-assessment or hunting-strategy docs.

Do NOT spend the session re-reading every systems file. Read what's relevant for hunting and skim the rest.

---

## Priority 1 — Reconcile `predator/mechanics.md`

Replace the "empirically derived" sections with cross-references to `systems/liquidation.md` etc. Keep agent-discovered nuggets that the systems docs don't cover (e.g., the specific Hostility Potion empirical contribution, the oracle-staleness gotcha) but mark them clearly as "Empirical observations" with a header pointer to canonical sources at the top of the file.

The file should read: *"This is empirical knowledge to layer on top of the canonical mechanics in `systems/liquidation.md` (link). Read that first."*

---

## Priority 2 — Update CLAUDE.md doctrine

Two additions:

### Block F — Knowledge Sources (new top-of-file block, above Standing Authorizations)

> ## Knowledge Sources (canonical — read these first)
>
> The kami-zero repo inherits kamigotchi-context's full systems/ distillation. Before deriving any mechanic empirically:
>
> - **`systems/liquidation.md`** — kill mechanics: threshold formula, animosity, efficacy (affinity matchup), shift bonuses, recoil, loot, decision rules, gas (7.5M required).
> - **`systems/harvesting.md`** — strain, HP decay, projected HP from harvest start time, affinity at node.
> - **`systems/state-reading.md`** — how to read kami state (current HP, harvest_start, strain, bonuses, traits).
> - **`systems/leveling.md`** — Predator tree (122/142/162 ATS, 121/151 ATR) + Guardian tree (323 Armor + 341 = DEF_THRESHOLD_RATIO).
> - **`systems/health.md`**, **`systems/factions.md`**, **`systems/scavenging.md`**, etc. — other mechanics.
> - **`integration/abi/`**, **`integration/system-ids.md`**, **`integration/api/`** — chain interaction.
> - **`strategies/`** (if present) — strategy patterns inherited from upstream.
>
> **Rule**: if a question can be answered by reading a systems/* file, read that file first. Do not spend gas to discover what's already documented. `predator/mechanics.md` is for empirical layering on top of canonical docs, not a competing record.

### Update Predator Doctrine — Targeting section

Replace whatever currently exists about targeting with this clearer block:

> **Targeting heuristic (current-HP-driven).** Find HARVESTING kamis (any base stats), filter out guild members, project each candidate's current HP from `harvest_start_ts` + strain rate, strike those whose projected HP is below your kill threshold. The opportunity exists because there are no active predators in the game right now — players leave kamis harvesting for hours and drift into the kill zone. Soft-stat filters (def_shift = 0 etc.) are NOT the heuristic; current HP is.

### Update "Self-paced cadence" — explicit norms

Replace the existing cadence text with:

> **Self-paced cadence.** Active hunting (live targets, short cooldowns): re-wake 10–30 min. Strain-wait (waiting for a specific kami's HP to cross threshold): re-wake at projected crossing ± 5 min buffer. Genuinely quiet world: up to 1–2 hours. Cron tick is `*/5` so your `next-run-at` honors to within 5 min. Compute is not the constraint — intelligent hunting is.

---

## Priority 3 — Build (or refine) target scanner: low-projected-HP HARVESTING non-guild

This is the new core tool. Sketch:

```
def find_low_hp_targets(min_kill_probability=0.7, max_candidates=50):
    # 1. Pull HARVESTING kamis from oracle's kami_current_location (or live on-chain scan)
    # 2. For each, fetch harvest_start_ts and base stats (max HP, harmony, traits)
    # 3. Project current HP using strain formula from systems/harvesting.md
    # 4. Filter out guild (predator/guild-no-touch.csv: account_id or handle match)
    # 5. For each survivor, compute kill threshold for our best striker
    #    using systems/liquidation.md formula
    # 6. Return candidates where projected_hp < threshold, sorted by margin (most-killable first)
    #    plus their node, owner, and travel cost from current operator location
```

You decide implementation details. If oracle's `kami_current_location` view doesn't have `harvest_start_ts`, augment with on-chain reads, or note in `improvements.md` an oracle-side ask. Cache aggressively within a session.

Validate the scanner by running it once and spot-checking 2–3 candidates against live on-chain HP — if projection matches reality, tool is calibrated. If not, debug strain formula application.

**Build only what unblocks the next strike.** A 20-line scanner is fine; a beautiful framework is not the goal here.

---

## Priority 4 — First kill

After the scanner is calibrated and returns candidates:

1. Pick the highest-confidence candidate (largest margin between projected HP and our kill threshold).
2. Counter-predator scan on that node — who else is HARVESTING there, what are their threat tiers (per `strategies/predator-threat-assessment.md` if available, or per the formula in `systems/liquidation.md` recoil section).
3. Travel cost analysis — gas + stamina. If our best striker is already on the right node (per session 79's state, 11224 is on node 86 RESTING), great. If not, evaluate move cost vs cluster size at destination.
4. Pre-flight: pick our striker, healing-up if needed (Cheeseburger or similar), set them HARVESTING on the target's node, fire `liquidate(target_kami_id)` once on-cooldown.
5. **If first strike succeeds**: log everything (gas, recoil, obol +1, spoils, salvage to victim) to `predator/learnings.md` AND `predator/metrics.md`. Then immediately scan for the next candidate on the same node — clusters often have multiple low-HP kamis and the cooldown is short.
6. **If strike reverts**: re-read `systems/liquidation.md` § "Kill Constraints" and figure out which constraint failed. Fix and retry once. If it reverts again, log the constraint mismatch and move to the next candidate.

Cluster math beats single targets. If the first strike worked, stay on the node, scan again, fire again. Don't leave for ≥1h after a successful kill — you're in a hot zone with the right tooling and cooldown.

---

## Priority 5 — Self-schedule

`next-run-at` based on the new cadence norms. After a kill, expect short re-wake (15–30 min) for the next strike on the same cluster. After a calibration session with no strike yet, ~30 min (let cooldowns settle and oracle data freshen).

If you genuinely need to do a multi-hour strain-wait for a specific kami, schedule precisely at its projected kill-zone crossing time + 5 min buffer.

---

## Stop conditions

- First kill landed → log it and immediately scan for the next candidate on the same node. Stay until the cluster is exhausted or counter-predator threat changes.
- 3 consecutive strikes revert despite passing pre-flight (projected HP < threshold) → something in the projection is wrong; stop, re-read `systems/harvesting.md` strain section, write a note in `predator/learnings.md`, end the session.
- Roster down to ≤3 healthy strikers (5 currently, 11224 + 4 others) → defensive priority overrides hunt: scan counter-predators in our area, defensive harvest_stop or move out, end session.
- Total gas > 50M without any kill → end session, write a clear failure post-mortem to `predator/learnings.md` (which heuristic is wrong, which doc was misread).

---

## Commit discipline

- `predator:` for `mechanics.md` reconciliation, `learnings.md`, `metrics.md`
- `pivot:` for CLAUDE.md additions (Block F + doctrine updates)
- `harness:` if you add a `find_low_hp_targets` tool
- `session:` for `memory/decisions.md`, `next-run-at`

---

## Communication back to founder

End-of-session in `decisions.md`:
- Did first kill land? (Yes/No)
- If Yes: target kami, owner, projected HP, our threshold, gas spent, obol earned, spoils.
- If No: which constraint blocked, what was misread vs the canonical docs, what's the next-session plan.
- Scanner calibration status (works / off by X% / debug-in-progress).
- Cadence chosen and why.

The founder is checking the metrics trend asynchronously — the trend (kills/session, obol/gas) is the feedback loop, not session-by-session approval.

---

## What is NOT in scope this session

- 11224 SP allocation (still pending observation in real hunts).
- Quest progression (paused).
- Force-flush (still off-policy in hunt mode).
- Building all four tooling-gap items from session 73 — only build what unblocks Priority 4.
- Reviving 12649 (defer until either Onyx Shards available or REVIVE-item mechanism understood; both belong to a separate "deepen revive mechanics" sub-task, not this session).
