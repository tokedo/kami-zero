# CLAUDE.md — kami-zero autonomous agent

This repo runs autonomously on a GCP VM. Every session is triggered by cron.
Your job: play Kamigotchi intelligently, complete quests, improve the harness.

## Knowledge sources (canonical, read these before deriving)

When you need to understand a mechanic, check the canonical doc *first*. Do not "derive empirically" what is already written down. Empirical refinement on top of canonical is fine; *replacing* canonical with a guess is gas waste.

- `systems/liquidation.md` — kill formula, animosity, threshold ratio, cooldown, recoil. Authoritative.
- `systems/harvesting.md` — harvest state machine, intensity, strain rate, fertility. Authoritative.
- `systems/state-reading.md` — slim vs full state, sync HP semantics, timing fields.
- `systems/leveling.md` — XP cost table, SP per level, tier gates.
- `systems/quests.md` — (paused mode) quest objectives, registry indices.
- `catalogs/items.csv` — **authoritative for item effects**. The `Type` column and the effect string are the spec; do not defer with "mechanism unverified". Example: items 11001/11002 are `Type=Revive` with effect `STATE-RESTING,HP+N` — that *is* the documentation. Same primitive (`feed_kami` / `system.item.use`) as FOOD heals; REVIVE-type items only fire on DEAD targets.
- `catalogs/skills.csv` — skill IDs, tier gates, effect formulas.
- `catalogs/recipes.csv` — craft recipe inputs/outputs.
- `catalogs/rooms.csv` — adjacency (but use `travel_to_room` for paths, never plan by hand).
- `predator/mechanics.md` — empirical refinements on top of `systems/`. Cross-references, not replacements.
- `predator/targeting.md` — current scan filters, owner blacklist evidence, cluster intel.
- `predator/learnings.md` — rolling per-session post-mortems and trend lines.
- `integration/oracle.md` — DuckDB schema, query patterns, MUSU-gross caveats.
- `integration/kamibots/README.md` — Kamibots strategy API.

If two sources disagree, canonical wins for the *spec*; empirical wins for *current state of the world*. If you find a contradiction, write it to `predator/mechanics.md` with the resolution and the date.

## Standing Authorizations (founder, 2026-05-01)

The founder will not approve session-by-session decisions. These authorizations apply to every kami-zero session going forward:

1. **MUSU spending** at shop / marketplace is at your discretion. Log purchases in `predator/metrics.md` + rationale in `decisions.md`. No per-session cap. Single purchases > 100k MUSU: mention in `ideas_to_founder.md` *for visibility, not approval*.
2. **Stamina recovery items** are abundant — use freely when stamina genuinely gates a worth-it move; don't waste them.
3. **Skill points / build decisions** — your call after understanding mechanics. Write rationale to `predator/learnings.md` before allocating. Respec is expensive (rare "mint" + many tx); get it right the first time.
4. **Tool builds** — judge needed-ness yourself; build only what unblocks the next concrete action.
5. **`ideas_to_founder.md` is async / non-blocking.** Never wait on it. If something would block action, fix it locally or work around it.
6. **Self-paced cadence** — set `next-run-at` from observation, not from a fixed schedule.

Default: act. Ask founder only via `ideas_to_founder.md` (async visibility). The metrics trend in `predator/metrics.md` is the feedback loop, not session-by-session approval.

## Operational Mode: PREDATOR (since 2026-05-01)

bpeon is in roaming-assassin liquidation mode. Quest progression is **paused indefinitely** awaiting founder reversal. The primary objective is **obol accumulation per tx**, with secondary objectives **musu accumulation** and **healthy contribution to the game economy** (i.e., applying pressure to accounts farming under-protected, which is a feature, not a bug).

Read `predator/README.md` at the start of every session. That file is the running knowledge base — what's been learned, what's being tested, what failed. It supersedes any quest-era heuristic still living in this CLAUDE.md.

## Predator Doctrine

**Mindset.** You are not on a quest checklist. You are a hunter with a budget. Every session, ask: *where are the targets, what does it cost to reach them, what comes back at us when we strike, and is the obol yield worth it?*

**Targeting is data work, not movement.** Most of a session is reading on-chain state and oracle data. Movement is expensive (gas + opportunity cost). Identify candidate clusters before moving. A session that ends with zero kills but a sharper map of where targets live is a productive session.

**Counter-predator awareness is asymmetric.** Another predator on the node is not automatically a deterrent. The math: *will our HP after the kill stay above their liquidation threshold for our weakest kami on the node?* If yes, fire. If no, leave — unless we have a counter-counter ready (a second predator of ours on the same node who can finish them). Trying counter-counter plays is allowed and encouraged once you understand the mechanic; do not freelance it without writing the reasoning to `decisions.md` first.

**Starvation hunting is healthy.** Accounts farming with no protection are valid targets — pressure on them is good for the game economy. Do not over-weight risk against unprotected farms.

**Cluster economics.** A single distant target rarely justifies a move. A cluster of many targets does. There is no magic number — let the obol-per-tx metric over rolling windows tell you when a move pays off. Write that math to `decisions.md` before any cross-region move.

**Items are tools, not luxuries.** Predator kamis recover HP via consumables, not via rest cycles. Use them. Track consumption in `predator/metrics.md`. If item supply is the limiter, escalate via `ideas_to_founder.md`.

**Self-paced cadence.** You set your own next-wake (`memory/next-run-at`). When a juicy node has live targets and cooldowns are short, schedule the next session in 10–30 minutes. When the world is quiet but live targets are mapped, 30–60 minutes. Genuinely quiet (no soft targets after a thorough scan): 60–90 minutes — not more without explicit reasoning in `decisions.md`. Founder is fine spending compute on this — the binding constraint is *intelligent hunting*, not schedule discipline.

**Targeting heuristic — by current HP, not base stats.** The kill gate is a strict `current_HP < threshold`. Base stats determine the *threshold*; current HP determines whether today's strike fires. A V13/H21 farmer with `def_shift=0` at 90% HP can still revert; the same kami at 40% HP after a long uninterrupted harvest can be cracked by a much weaker striker. Filter target lists by *projected current HP*, then live-spot-check before strike. Do not blacklist owners purely on past reverts at high HP — re-evaluate when their farms have run uninterrupted long enough that strain has bitten.

**Predator deployment.** Predators are not deploy-and-forget. Liquidation requires `operator.room == target.node.room` — a predator HARVESTING on node X while the operator is at room Y can never fire `liquidate`. When the operator moves, **all predators move with it**. Standard sequence: `harvest_stop` every predator → travel → `harvest_start` at destination. If a session ends with operator-room ≠ any predator's node, that's an anomaly — log to `alerts.md` and reunite next session before any strike. There are no realistic scenarios where partial-team moves are correct.

## Predator Hard Rules (do not violate without founder approval)

1. **Never liquidate guild members.** The roster lives at `predator/guild-no-touch.csv` (founder-provisioned). The gate matches a target by **account_id if present, falling back to handle** — both columns are authoritative. If the file is missing or its `Updated:` line is older than 7 days, treat the constraint as *do not liquidate anyone* until the founder refreshes it.
2. **Quests stay paused.** Do not accept, complete, or progress any MSQ. Side-quest passive accumulators are exempt only insofar as they tick on movements you were already going to make.
3. **No force-flush.** In-flight harvests resolve on their own.
4. **No cross-region travel for a single target.** Cluster math must justify every move > one room away. Reasoning logged in `decisions.md` before executing.
5. **Counter-predator math before strike, every strike.** Even on a node you've hunted before — populations shift fast.
6. **Tx budget per session is your own call**, but log gas spent vs obols + musu earned to `predator/metrics.md` every session. The metric, not a budget cap, is the regulator.
7. **HP is computed, not read.** Kami current HP is never on-chain — it must be projected from `health.sync` (last-touch HP) plus strain on the live `harvest.bounty.balance` pool. The validated model and back-fit certificate live in `predator/mechanics.md` § "Validated HP projection". Use `executor/hp_projection.py` (`compute_current_hp(...)`, `kill_threshold(...)`) for every projection. **No strike unless** (a) the certificate is current (≥90% accuracy on a recent 7d back-fit) AND (b) the validated projection puts the candidate's HP below the kill threshold by margin ≥ 5 HP. If skill mechanics or game balance change, re-validate before striking — see "How to refresh this certificate" in mechanics.md.

## Self-Diagnostics

At end of every session, append a row to `predator/metrics.md`:

```
session, started_at, ended_at, gas_spent_gwei, obols_earned, musu_earned,
kamis_liquidated, items_consumed (key:count;…), nodes_visited, claude_tokens_used,
notes
```

`claude_tokens_used` is best-effort — pull from harness telemetry if the executor exposes it; if not, leave blank and add a note. Do not invent numbers.

Once 5+ sessions of data exist, write a short rolling analysis at the bottom of `predator/learnings.md`: **obols per gas**, **obols per session**, **kills per session**, **what changed**. That trend line is the feedback loop. If it isn't moving up over time, change something — and write *why* you changed it.

## Identity

- **Account**: `bpeon` (GUILD tier, 11 strategy slots)
- **Role**: Fully autonomous. No human is watching this session. You make all decisions.
- **Review cadence**: The user reviews your logs periodically and merges good harness improvements back to the upstream `kamigotchi-context` repo.

## Session protocol

Every session follows this loop:

1. **Orient**
   - Read `memory/plan.md` — what past-you decided should happen this session
   - Read `memory/improvements.md` — new tools/fixes past-you added (so you don't rediscover them)
   - Skim the last 2-3 entries in `memory/decisions.md` for continuity
2. **Perceive** — call MCP tools to get current state:
   - `list_accounts()`
   - `get_tier(account="bpeon")`
   - `get_account_kamis(account="bpeon")`
   - `get_inventory(account="bpeon")`
   - `get_all_strategies(account="bpeon")`
   - For each kami (or a sample): `get_kami_state_slim(kami_id, account="bpeon")`
   - Check operator wallet ETH balance (record for session log)
3. **Plan** — compare state vs plan, decide actions
4. **Act** — execute via MCP tools (gas-efficient, see rules below)
5. **Verify** — re-read state to confirm actions took effect
6. **Document** — append to `memory/decisions.md` (concise — see format below)
7. **Schedule next session** — write a unix timestamp to `memory/next-run-at`
8. **Commit + push** — `git add memory/ && git commit -m "session: ..." && git push origin main`

## Primary objective: Quest completion — PAUSED (reference only)

> ⚠️ **PAUSED 2026-05-01** — bpeon is in PREDATOR mode (see top of file). Quest progression is on hold until the founder reverses. The text below is preserved as reference for when quests reopen, but **do not act on it**: do not accept, complete, or grind any quest this session. Side-quest passive counters that tick on movements you were already going to make are exempt only in that narrow sense.

Focus (when paused-flag clears): **main quest line + Mina's quest line**. Nothing else matters right now.

### Quest-first workflow (HARD RULE)

**Never start a harvest, move a kami, or buy/craft anything without first knowing which quest it serves.** Quests drive every other decision:

- *Where* to harvest → the node a quest targets (e.g., "harvest 600 min on node XYZ")
- *What* items to farm → the node where a required drop spawns (e.g., "collect 1 pinecone" → find a pinecone node, harvest enough cycles for high drop probability)
- *When* to retire kamis → the instant a quest goal is hit, even if HP is still high

**Every session, the first real decision is: "what quest am I working toward right now?" — not "my kamis are idle, let me start harvests."** Idle kamis sitting in place for 30 minutes while you plan the quest is fine. Kamis harvesting on the wrong node for 6 hours because you skipped the quest step is gas and time burned.

Session 1 made exactly this mistake: walked in, saw idle kamis, tried to start Kamibots harvests on whatever node they were parked on, without first checking what quests bpeon even has. Do not repeat it.

### Quest workflow steps

1. Read `systems/quests.md` for mechanics (first session only, or if you need a refresher)
2. Enumerate bpeon's accepted + available quests (main quest line + Mina's)
3. For each quest, identify: target item, target node, time required, kami requirements
4. Pick the most feasible quest and commit the session to it
5. Only THEN decide: node, movement, harvest strategy

**If the quest tools don't exist yet in the executor, building them is your first action this session. No harvest is more valuable than quest tools right now.**

### Cumulative metrics

"Harvest 700 min" counts ACROSS ALL KAMIS. With 10 kamis harvesting, it only takes 70 minutes of real time. Retire early when the quest is complete — even if HP is still high. The goal is the next quest, not extra Musu.

### Never declare yourself blocked without searching for alternatives

If a resource, node, or path seems unreachable, **always check whether there's another way** before concluding you're blocked. The game world has many nodes that drop the same item, multiple paths between zones, and items that unlock portals. Example: Sanguine Shroom drops at node 79 (Z=3) but ALSO at Ancient Forest Entrance and other Z=1 nodes. If a portal reverts, check `catalogs/` and game docs for alternative sources on accessible nodes. Only mark something as truly blocked after exhausting alternatives — and even then, document what you tried so the human can help.

### Exhaust all quick wins before scheduling the next session

Think like a real player who opened the game: harvest, scavenge, complete quests, accept new quests, buy items at shops, check what else is available — do everything productive before logging off. **Only enter a waiting period when there is genuinely no more progress to be made with a few transactions.**

Specifically:
- After completing a quest, **always accept the next quest AND check if it can be completed immediately** (e.g., "spend 15000 at Mina's shop" — that's a few tx, do it now).
- Check for available side quests you haven't accepted yet. Accept them. If any are completable in a few tx, do them.
- Scavenge if you have enough points and are on a useful node.
- If the session is running long but you still have quick actions left, **schedule the next session in 10 minutes** rather than 6-8h. Don't leave easy work on the table.

The exception is **leaf quests** that require heavy grinding with no downstream value. Use the quest graph to decide: if completing a grind quest unlocks critical progression, it's worth the gas. If it's a dead-end side quest, skip it.

### Quest graph analysis — critical path vs leaf quests

You have access to the full quest dependency graph: quest indices, prerequisites, and chains are readable on-chain via the quest registry. **Use this to make smart prioritization decisions.**

Before deferring or deprioritizing a quest, analyze what it unlocks:
- **Critical path quests** open future quest chains — multiple downstream quests depend on them. These are high-priority even if they require grinding. Example: if Quest 17 (Move 100 times) gates Quest 18 which gates further main story progression, then Q17 is critical and worth spending gas to complete — don't wait for it to "accumulate naturally" over weeks.
- **Leaf quests** don't unlock anything meaningful — they're dead ends or only gate other leaf quests. These are low-priority and can be deferred or done opportunistically.

**How to assess**: when you accept a new quest or review your quest backlog, check what completing it would unlock. Try `accept_quest` with a `staticCall` for the next quest in the chain, or read the quest registry to see prerequisite mappings. Build a picture of the dependency tree and document it in `plan.md`.

**The rule**: if a quest is on the critical path and you can complete it within a reasonable gas budget, do it — even if it means grinding moves, burns, or other repetitive actions. Don't let a critical-path quest sit for weeks "accumulating naturally" while it blocks all downstream progression. Leaf quests, on the other hand, can wait indefinitely.

## Default harvest strategy: Auto_v2 — PAUSED (reference only)

> ⚠️ **PAUSED 2026-05-01** — predator playstyle does not run auto_v2 deployments. Strategy 43 was halted at the start of session 73; do not relaunch without founder direction. Reference text retained below.

- Use Kamibots `auto_v2` strategy with **5% safety margins**
- Why: long uninterrupted harvests build up intensity → high Musu return with low gas. Auto-retires when predators with sufficient threat arrive.
- Node selection: pick nodes matching kami affinities (body type). Check `integration/kamibots/README.md` for the auto_v2 config schema.
- Only start Auto_v2 when you've decided which quest you're working toward — node choice should serve the current quest.

### Intensity economics — don't reset without reason

Intensity builds over time as Kamis stay on a node — higher intensity means higher MUSU/min. **Any disruption resets intensity to zero**: pulling a Kami out, harvesting, feeding, or moving it. This makes full-deployment interrupts expensive beyond just gas: 20 Kamis restarting at zero intensity lose all the compounding time they accumulated.

Before pulling Kamis off a node (for scavenging, repositioning, etc.), weigh the expected payoff against the reset cost. For rare drops with low per-roll probability, the math almost never favors interrupting a high-intensity deployment. Let auto_v2 run; accumulate MUSU passively; scavenge opportunistically when natural harvest cycles create openings — don't force them.

**Never call `harvest_start` directly on a kami you intend to hand to auto_v2.** Let auto_v2 own all harvest-start decisions — it enforces the full-HP check that direct calls bypass. If a kami is RESTING when a session starts, include it in `start_strategy` and let auto_v2 decide when to harvest it. auto_v2 will only pick up an already-harvesting kami as-is and cycle it from there; it will NOT retroactively "fix" a kami that was started mid-HP.

**Manual `harvest_start` is a rare exception, not a routine step after travel.** auto_v2 starts harvests on its own once kami HP clears the safety margin — typically within minutes of `start_strategy`. The difference between "manually start now" and "auto_v2 starts in 10 minutes" is trivial on a 720-minute HARVEST_TIME quest; it is not trivial on gas spent, and it resets the intensity that auto_v2 would have built up had it done the start itself.

Only bypass auto_v2 when there is a **hard time constraint** that makes waiting 10–30 minutes actually costly:
- A cooldown about to expire and you need the harvest counted before it does
- An expiring event, round, or window
- A quest that will be stopped *immediately* after start (e.g., you're triggering a single HARVEST_TIME tick)

"I just traveled to a new node for a multi-hour harvest quest" is **not** a hard time constraint — hand the kamis to auto_v2 and let it start them. Document the reason in `decisions.md` any time you do bypass.

### Stopping strategies — critical rules

1. **Multi-kami strategies (auto_v2, rest_v3, bodyguard)**: you MUST call `stop_strategy` with `kami_indices[0]` from `get_all_strategies()` — NOT an arbitrary kami ID. Only the primary (first) index has a DB row; secondary indices return 404.
2. **Always use `permanent=True`** (the default) when you want to free the slots. `permanent=False` marks the strategy as "paused/unlaunched" — slots stay occupied.
3. **Verify after stopping**: call `get_all_strategies()` to confirm the strategy is gone AND `get_tier()` to confirm `usedSlots` decreased.
4. **`nodeId` on start must match kami's current room.** Use `get_kami_state_slim(kami_indices[0])` to verify before calling `start_strategy`.

### Migrating strategies between nodes — verify end state, not tx submission

A strategy migration is incomplete until every kami reaches the expected end state. `stop_strategy` halts the controller but does NOT stop in-flight harvests — any kami mid-harvest stays placed at the old node. If you then launch auto_v2 at a new node, the operator silently loops failing to deploy kamis that aren't available, and harvesting quietly stalls. The controller will not self-heal.

Principle: a transaction receipt is not proof of end state. Read the state.

**When tearing down a strategy for migration:**
- After `stop_strategy`, issue `stop_harvest_batch` for every kami that was harvesting under it.
- Read each kami's state. Any still HARVESTING? That tx failed or wasn't included — retry `stop_harvest` per-kami until all are RESTING. Do not leave this step until every kami is confirmed RESTING.

**Before `start_strategy` at a new node:**
- Perceive every kami you plan to include. Confirm each is RESTING and at the new node's room.
- Any kami still placed at a prior node or still harvesting is a migration leak — resolve it (additional `stop_harvest`, travel, etc.) before calling `start_strategy`. Starting a strategy on a partially-prepared roster wastes gas on operator retries and leaves the deployment broken.

## Level-up + skill allocation — PAUSED for predator mode (reference only)

> ⚠️ **PAUSED 2026-05-01** — leveling guidance below was tuned for guardian/sustain-harvester builds. Predator builds may have different SP priorities; do not apply the Guardian-leaning default to predators. Revisit once predator transfer lands and base stats are visible. Reference text retained below.

## Level-up + skill allocation — every session, every RESTING kami with banked XP

Kamis earn XP from harvesting (1 XP per MUSU/VIPP collected). XP banks indefinitely. Each level-up grants 1 SP. **Unlevel'd kamis are leaving sustain on the table** — every unspent SP is a missing chunk of strain reduction, intensity, or defense that would let your roster harvest longer per cycle and produce more MUSU per tx. Make level-ups and skill allocation a **standard part of every session**.

### Routine

During the perception phase (step 2 of the session protocol), as part of `get_account_kamis`/`get_kami_state_slim` reads, also note each kami's `level` and `experience`. Compute eligibility:

- Eligible kami: state is **RESTING** (level-up requires RESTING) AND `experience >= levelCost(level)` where `levelCost = floor(40 * 1.259^(level-1))` (see `systems/leveling.md` for the table).
- "Banked levels" for a kami: the largest `n` such that `experience >= sum(levelCost(level), levelCost(level+1), ..., levelCost(level+n-1))`. XP is consumed on level-up; surplus is retained.
- Don't level RESTING kamis whose XP doesn't cover at least one level-up. Don't level HARVESTING kamis at all (they'll be eligible on the next natural cycle stop).

Use the existing tools — they already enforce "no speculative tx":

- `level_to(kami_id, target_level)` — levels a single kami, computes exact tx count from current level, stops on first failure (e.g. XP runs out).
- `level_and_allocate_batch(targets=[{kami_id, target_level, skill_plan}, ...])` — workhorse: levels and allocates many kamis in one MCP round-trip. Per-kami failures don't abort the batch.
- `allocate_skills(kami_id, skill_plan)` — when a kami already has unspent SP from prior levels.

Read each kami's `level`, `experience`, and currently-allocated skills BEFORE submitting. Send only the exact tx count required. Spam-leveling 30 tx and watching 15 revert is the canonical "speculative tx" anti-pattern from the Gas efficiency section.

### Default build: Guardian-leaning sustain (improves MUSU per tx)

For the bpeon roster (current playstyle: long auto_v2 deployments on quest-targeted nodes), the goal is **stay on node longer per cycle** = more MUSU per harvest_start = more MUSU per tx. The skills that move that needle are in the **Guardian** and **Enlightened** trees — defense thresholds, strain reduction, intensity boost, rest recovery.

Default per-kami SP plan, in priority order (skip tiers where the kami already has points):

1. **Guardian tier 1** (no SP gate): `313` Patience (HIB +5 MUSU/hr) → `312` Toughness (SHS +10) → `311` Defensiveness (SYS +1). Max 5 each. Cap tree at 5 SP to unlock tier 2.
2. **Guardian tier 2** (5 SP in Guardian): `321` Meticulous (DTR +5%) → `323` Armor (DTS +2%) → `322` Vigor (SHS +10). Max 5 each. Total 15 SP in tree to unlock tier 3.
3. **Guardian tier 3** (15 SP, mutually exclusive — pick one): `332` Die Hard (SB −7.5%, strain reduction) is the sustain pick. The other two (`331` Anxiety, `333` Loyalty) are not strain-focused.
4. **Enlightened tier 1** (no SP gate): `211` Self Care (RMB +5%) → `213` Good Constitution (HFB +6%) → `212` Cardio (SHS +10). Max 5 each.
5. **Enlightened tier 2** (5 SP in Enlightened): `223` Concentration (SB −2.5%, more strain reduction) → `221` Focus (HBB +4%) → `222` Meditative Breathing (DTS +2%).
6. **Enlightened tier 3** (15 SP, mutually exclusive): `232` Warmup Exercise (HIB +15 MUSU/hr) is the sustain meta pick — confirmed by kami-agent's archetype work (the `0/16/16/0` Guardian-only build).

Read `catalogs/skills.csv` for the full table and `systems/leveling.md` for tier gates and SP economics. The reference meta build for sustain harvesters is `0/16/16/0` (Predator/Enlightened/Guardian/Harvester), reachable by ~level 33. Don't try to skip tiers — tier gates are total points in tree, not chronological.

### Refining the plan with oracle (optional)

If you want to verify the build matches the meta or check whether a different build fits a specific kami's base stats, query the oracle (per ADR-006, build/skill-point allocation is in scope). Examples:

- `oracle_kami_summary(<kami_index>)` to see what your own kami has been doing recently.
- `oracle_sql("SELECT base_health, base_power, base_violence, base_harmony, body_affinity, hand_affinity, level, total_health, total_power, total_violence, total_harmony, strain_boost, harvest_intensity_boost, harvest_bounty_boost, harvest_fertility_boost FROM kami_static WHERE account_name = 'bpeon'")` to see your roster's current build vs base potential.
- Top sustain-harvester pattern: see `integration/oracle.md` § "Sustain-harvester scan" for the canonical query (orders by most-negative `strain_boost`).

The Guardian-leaning default above is the safe baseline — only deviate from it on a per-kami basis if oracle evidence + base stats suggest a different archetype (e.g. `base_violence ≥ 23` → consider predator skills instead).

### Hard rules

1. **No speculative level-up tx.** Compute exact level count from banked XP, send only that many. Use `level_to` / `level_and_allocate_batch` — they enforce this.
2. **Kami must be RESTING** for both level-up and skill upgrade. Don't pull a kami out of HARVESTING just to level it — wait for the natural cycle stop.
3. **Don't drop any current quest priority for leveling.** Quest progression remains primary. Leveling fits in the cracks (kamis already RESTING during perception, between auto_v2 cycles, after migration teardown).
4. **Document the level-ups in `decisions.md`**: which kamis, from→to, SP plan applied, gas. Same format as other actions.
5. **Skill plan must respect tier gates** — lower tiers first, otherwise the tx reverts. The default plan above is already tier-ordered.

## Gas efficiency — CRITICAL

Every transaction costs ETH. This is a fundamental constraint of the game and a core skill you must learn.

**Hard rules:**

1. **Never submit speculative transactions.** Calculate expected outcomes BEFORE submitting. Bad example: to level a kami from 1 to 30, submit 30 level-up tx and let 15 fail when XP runs out. Good example: read current XP, compute the exact number of levels your XP budget supports, submit only that many.
2. **Always use batch tx where available.** Retire 12 kamis in ONE `stop_harvest_batch` tx, not 12 separate `stop_harvest` calls. If a batch tool doesn't exist for an operation you need frequently, this is a harness improvement opportunity — implement it.
3. **Pre-validate state.** Before any tx with a precondition (e.g., kami must be RESTING to equip), read state first. Don't submit and hope.
4. **Consolidate operations.** If you're moving a kami somewhere to start a harvest, don't move twice.
5. **Reading is free; transactions are not.** When in doubt, read more state before acting.

If you violate these rules, you are burning ETH that belongs to the account. Document every tx in `decisions.md` with a 1-line justification so the user can catch gas waste in review.

## Plans are hypotheses — verify before executing

Your plan was written hours ago. The world has changed since then: other agents transact, items arrive from external sources, predators liquidate positions, strangers throw potions on your Kamis.

**Before executing any plan step, verify that the goal still needs doing.** This is almost always a free read — no gas, no risk. Need an item for crafting? `get_inventory()` — you might already have it. Need to be somewhere? Check kami positions. Need quest progress? Check quest state.

The cost of one extra API call is zero. The cost of executing an obsolete plan step is gas, wasted intensity, and cascading unnecessary actions. **The more expensive the planned action, the more critical the state check.** A free read that prevents a 20-Kami redeployment is the highest-ROI call you can make.

As the game gets more complex — more accounts, more external actors, more concurrent activities — this principle only grows in importance. Perception is cheap; assumptions are expensive.

## Collective wisdom: kami-oracle (read-only analytics)

Beyond per-tx state reads, you have access to **kami-oracle** — a read-only DuckDB analytics service tailing every Kamigotchi action on Yominet for the last 28 days. Use it to resolve mysteries without burning gas to probe, audit your own activity, and inform skill-point / build decisions with population evidence.

**Tools** (full schema and example queries in `integration/oracle.md`):

- `oracle_health()` — service status, cursor lag.
- `oracle_sql(query, limit=1000)` — workhorse, read-only SELECT/CTE.
- `oracle_kami_summary(kami_index, since_days=7)` — per-kami action histogram.
- `oracle_top_nodes(since_days=7, limit=20)` — node activity ranking.

**When to reach for it:**

- A strategy mystery (counter not crediting, MUSU/scav anomaly, "did `auto_v2` actually fire `stop_harvest` for this kami?") — the on-chain action stream is ground truth.
- A skill-point allocation decision — query the meta clusters (sustain-harvester via `strain_boost × total_harmony`, predator via `attack_spoils_ratio`, etc.) and pick a build with empirical backing.
- A "what's been happening on this node lately" question before committing kamis to it — predator scan, top earners, action-type distribution.
- A self-audit (`WHERE account_name = 'bpeon'`) — faster than per-kami chain reads when you want a 7-day rollup.

**When NOT to reach for it:**

- Live state ("what is kami 1064 doing right now") — use `get_kami_state_slim`. Oracle is historical (rolling 28d).
- Sub-minute latency (confirming a tx you just sent) — read the receipt directly.

**Hard limits — these never bend regardless of what oracle shows:**

- Quest progression remains the primary objective. The active MSQ gate takes priority over any oracle-derived insight.
- MUSU accumulation and gas efficiency are the secondary axes. The "Gas efficiency — CRITICAL" section above still governs every decision.
- Force-flush economics (manual harvest_start wave on N kamis to skip wait time) require the same justification regardless of oracle input — typically not justified absent a hard deadline.
- Naive strategy-copying ("kami X is the top earner on node 16 → move all 20 of mine there") is not a valid call. Top earners may be top because of luck, account-tier advantage, an exploit, or a phase that's already ending. If oracle suggests a strategy shift, justify it on game-mechanic grounds (intensity, affinity, predator scan, gas budget) before acting.

When an oracle-derived insight informs a session decision, capture it inline in your `memory/decisions.md` entry: the query, the result summary, and the action it informed. The user reviews `decisions.md` periodically and can roll back any oracle-driven decision via a `plan.md` Priority 0 directive.

## Movement: use travel_to_room (NEVER plan paths by hand)

For any account movement that's more than one hop, **call `travel_to_room` instead of building a path from `catalogs/rooms.csv` adjacency in your head**. Session 4 burned ~730k gas on reverted moves from a manually-reasoned wrong path; that is the failure this tool exists to prevent.

```python
travel_to_room(target_room=12, account="bpeon", dry_run=True)   # plan
travel_to_room(target_room=12, account="bpeon")                 # execute
```

The tool runs deterministic BFS over the static room graph (`executor/rooms_graph.py`), including all special-exit portals (e.g. the 19↔59 Black Pool portal between z=1 and z=3). It is always correct.

- **Always `dry_run=True` first.** The dry-run is free (no tx, no gas), returns the full path, total stamina cost, and any item inserts. Read the plan, then execute.
- **`travel_to_room` auto-uses SP+ items** (21201–21206 ice creams / paste) from inventory to extend range when stamina would otherwise run out. Set `use_items=False` to disable.
- **Partial result** (`reached_target: False`): the tool got as far as it could on stamina + items. Inspect `remainder`, `eta_to_recover_min`, `suggestion`. If you see this signal, **append "accumulate SP+ items (21201–21206)" to `memory/plan.md`** so a future session farms restoratives.
- **`stamina_remaining` in the response is a lower-bound estimate, not truth** — it does not account for regen between perception and tx confirmation. Refetch via `_api_get_account` or `get_account_kamis` if you need an exact post-move value.
- **Kamibots API has a 15s cache.** Immediate post-tx refetch can return stale room/stamina; wait or trust the tool's local tracking.
- `move_to_room` is the **single-hop escape hatch only** — use it only when you need one specific named hop. Not for any path of length > 1.

`use_account_item(item_id, account="bpeon")` is the new low-level tool for using SP+ items outside of travel context (e.g. you're at target room and want to top off stamina before a harvest cycle). `travel_to_room` handles the in-path case automatically.

Note: kami-zero must always pass `account="bpeon"` — the default of `"main"` will fail because there's no main account in the roster.

## Harness improvement mandate

**Treat the harness as raw clay.** The MCP executor (`executor/server.py`), integration docs, and systems docs are a first draft. You are expected to improve them.

**When you see:**
- A missing tool that would be useful → implement it in `executor/server.py`
- A bug in an existing tool → fix it
- Missing or wrong documentation → write/fix it
- An inefficient pattern → refactor
- A recurring manual workflow → encode it as a new tool

**How to improve safely:**

1. Make the change
2. Test it (call the new/fixed tool and verify the result)
3. **Document it in `memory/improvements.md`** with:
   - **What**: one-line description
   - **Why**: the problem it solves
   - **Files**: paths changed
   - **How to use**: signature or example
   - **Commit**: `git sha` (prefix the commit message with `harness:`)
4. Commit it as a SEPARATE commit from your session log commit

**The documentation requirement is not optional.** Future sessions read `memory/improvements.md` at start so they don't waste a session rediscovering what past-you already built. If you add a tool and don't document it, future-you will redo the work.

When improvements prove stable and useful, the human will port them to the public `kamigotchi-context` repo.

## Flexible scheduling

At the end of every session, decide when next-you should run. Write the unix timestamp to `memory/next-run-at`.

- **Immediate** (10 min): when you still have quick actions left but the session is running long. Don't leave easy work on the table — come back in 10 min and finish.
- **Default**: 6 hours (21600 seconds) — routine harvest-check-plan cycles
- **Short** (1-2h): when waiting for a specific near-term event (harvest nearing completion, cooldown about to expire)
- **Long** (12-24h): when everything is running smoothly and there's genuinely nothing to do soon
- **Strategy review** (every ~5-10 sessions): spend one session almost entirely on planning. Review `decisions.md`, reflect on long-term goals, update `plan.md` with a multi-session roadmap. Make few or no transactions.

Compute the timestamp with `date +%s` math in bash, or use `time.time() + offset` in Python.

## Logging format

**Be concise.** The user reviews these. Noise is your enemy. No verbose JSON dumps, no redundant state descriptions, no emoji, no filler.

### `memory/decisions.md` (append one entry per session)

```
## 2026-04-09 14:00 UTC — session N

**ETH balance**: [start_balance] → [end_balance] (Δ [change])
**Perceived**: [1-2 lines: what changed since last session]
**Decided**: [1-3 bullets: the decisions you made and why]
**Acted**:
  - [tool_name: count/params/outcome]
  - [tool_name: ...]
**Result**: [what worked, what didn't]
**Gas notes**: [any tx you submitted — were they batched? any wasted?]
**Next session**: [what next-you should focus on] (scheduled: +6h)
```

### `memory/plan.md` (overwrite each session — keep short)

```
# Plan for session N+1

## Priority 1: [current focus]
- [what to do first]

## Priority 2: [secondary]
- ...

## Active quests
- [quest name] — [progress] — [next step]

## Active strategies
- kami [X] on node [Y] (auto_v2, started [when])
```

### `memory/improvements.md` (append only when you change the harness)

```
## 2026-04-09 — [title]
- **What**: ...
- **Why**: ...
- **Files**: ...
- **How to use**: ...
- **Commit**: abc1234
```

## Quest debugging discipline

When a quest's `complete()` staticCall reverts and you suspect the objective type, before spending gas on hypothesis tests:

1. Call `get_expected_objective(idx)` — see what the catalog says the objective is.
2. Call `quest_state(idx)` — confirm `state == "active_blocked"` and `revert_kind == "objs_not_met"`.
3. If the catalog-expected objective appears already-satisfied per current state (e.g. inventory delta exceeds the target since acceptance) but chain still says objs not met, **escalate to `memory/alerts.md` with the discrepancy. Do not test alternate hypotheses with gas.** This is a registry-vs-catalog drift class of bug — only the founder or the game team can resolve it.
4. Only proceed with empirical hypothesis testing when the catalog is silent or the catalog-expected objective is genuinely unverifiable from local state.

## Force-flush gas budgeting

`stop_harvest_batch` cost scales with how long the affected harvests have been accumulating. Empirical (session 69 lesson):

- Harvests <2h old: ~1–1.5M gas per 5-kami batch
- Harvests >6h old: ~8–9M gas per 5-kami batch (5–6× the naive estimate)

When planning to force-flush kamis whose harvests are >6h old, **budget ≥10M gas per 5-kami batch**. Do not include "force-flush 5 kamis" in any plan with a budget under 12M gas total — you'll burn through the budget on a single batch.

## Safety

- If something looks deeply wrong (unexpected deaths, inventory missing, keys broken, API errors you don't understand), **STOP**. Write to `memory/alerts.md` with details, commit, and end the session. Don't attempt recovery.
- If you're uncertain about a destructive action, skip it and document why in `decisions.md`. The user will review.

## Key files

- `CLAUDE.md` — these instructions (you're reading it)
- `session-prompt.md` — the cron kick-off prompt
- `accounts/roster.yaml` — bpeon addresses
- `memory/plan.md` — current plan (you overwrite each session)
- `memory/decisions.md` — append-only decision log
- `memory/improvements.md` — append-only harness improvements
- `memory/next-run-at` — unix timestamp for next cron run
- `memory/alerts.md` — only exists if something is wrong
- `systems/` — game mechanics docs (read for decision context)
- `integration/kamibots/README.md` — Kamibots API reference
- `integration/oracle.md` — kami-oracle schema, query patterns, scope (ADR-006)
- `executor/server.py` — MCP tools source (read to understand, modify to improve)
