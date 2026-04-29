# kami-oracle — Collective wisdom for kami-zero

> **Read this if you are about to make a strategic decision** (which node
> to harvest on, whether to liquidate, who to feed, what to craft, how
> to spend skill points). The oracle records every on-chain Kamigotchi
> action over the last 28 days. Top players have already optimized —
> query their behavior instead of deducing strategy from first principles.

## Scope for kami-zero (ADR-006)

**Use oracle for:**

- **Diagnostic** — investigate strategy mysteries (e.g. "why is the
  Q47 HARVEST_TIME counter not crediting?", "why did MUSU not change
  when scav points went up?"). Cross-reference your `auto_v2` cycles
  against the on-chain action stream. Confirm or rule out hypotheses
  without burning gas to probe.
- **Gas-efficiency analysis** — identify which action patterns yield
  the highest MUSU per tx (e.g. `musu_per_payout` distributions across
  the meta) and apply the insight to your own action shape.
- **Build / skill-point allocation** — when leveling kamis, query the
  meta clusters (sustain-harvester, predator, guardian) and pick a
  build with empirical evidence, not just first-principles guessing.
- **Self-observation** — query your own kamis / accounts to audit
  recent activity (`WHERE account_name = 'bpeon'` etc.). Faster than
  per-kami chain reads when you want a 7-day rollup.

**Do not use oracle for:**

- **Naive strategy-copying** — "kami X earned the most MUSU on node 16,
  so move my 20 kamis there" is not a valid call. Top earners may be
  top because of luck, account-tier advantage, an exploit, or a phase
  that's already ending. If oracle suggests a strategy shift, justify
  it on game-mechanic grounds (intensity, affinity, predator scan,
  gas budget) before acting — not on rank alone.

**Hard constraints — these never bend regardless of oracle output:**

- Quest progression remains the primary objective. The active MSQ
  gate takes priority over any oracle-derived insight.
- MUSU accumulation and gas efficiency are the secondary axes.
- Force-flush economics (manual harvest_start wave on N kamis to skip
  wait time) require the same justification regardless of oracle
  input — typically not justified absent a hard deadline.

Oracle is informational input to existing decision-making, not a
replacement for it.

## What it is

A read-only DuckDB-backed analytics service running on its own GCP VM
(see `kami-oracle` repo). Continuously tails Yominet, decodes every
tx that touches Kamigotchi systems, and exposes the result as
queryable tables.

You access it through MCP tools — never through raw HTTP, never with
the bearer token in your context. The token lives in
`~/.blocklife-keys/.env` and is loaded by the MCP server only.
Architectural rationale: ADR-005 in `blocklife-ai/context/decisions/`.

## When to use it

| Question | Tool |
|---|---|
| "Is the oracle healthy / what's the cursor lag?" | `oracle_health()` |
| "What's this kami been doing this week?" | `oracle_kami_summary(kami_index, since_days=7)` |
| "Which nodes are busiest right now?" | `oracle_top_nodes(since_days=7)` |
| Anything else | `oracle_sql("SELECT ...")` |

`oracle_sql` is the workhorse. The REST shortcuts are conveniences
for the most common questions.

## When NOT to use it

- **Live state** — oracle is historical (rolling 28d). For "what is
  kami 1064 doing right now" use `get_kami_state(1064)` against
  Kamibots, not the oracle.
- **Sub-minute latency** — cursor lag is seconds in normal operation
  but can spike under load. If you need to confirm a tx you just sent,
  read the receipt directly.
- **Writing anything** — oracle is SELECT-only. INSERT/UPDATE/DELETE/
  DDL are rejected server-side with HTTP 400.

## Schema cheat sheet

Five tables, all read-only:

### `kami_action` — decoded, one row per logical game action

Most queries start here. Key columns:

- `id`, `tx_hash`, `block_number`, `block_timestamp`
- `action_type` — enum (see below)
- `system_id` — e.g. `system.harvest.start`
- `from_addr` — operator signer wallet (NOT the kami's owning Account)
- `kami_id` — VARCHAR decimal of uint256 entity ID, nullable
- `target_kami_id` — for liquidations
- `node_id`, `harvest_id`
- `amount` — VARCHAR decimal uint256. **Cast as `CAST(amount AS HUGEINT)`** — never `/ 1e18`. Generic field; meaning depends on action_type
- `item_index`, `metadata_json`, `status`

Indexed on `(kami_id, block_timestamp)`, `(action_type, block_timestamp)`,
`(from_addr, block_timestamp)`, `block_number`.

### `kami_static` — per-kami traits + current build snapshot

Identity / traits (Sessions 6–9):
- `kami_id` (PK), `kami_index` (the human-readable token #), `name`
- `owner_address`, `account_id`, `account_index`, `account_name`
  (in-game display name like "bpeon")
- `body`, `hand`, `face`, `background` — integer trait indices
- `body_affinity`, `hand_affinity` — affinity strings drawn from
  `{EERIE, NORMAL, SCRAP, INSECT}` (uppercase, as the chain returns
  them). `body_affinity` comes from `getKami(kamiId).affinities[0]`,
  `hand_affinity` from `[1]`. Use these for archetype filtering /
  clustering — **don't** hand-roll a `body_index → affinity` VALUES
  table inline anymore, just `WHERE s.body_affinity = 'EERIE'`.
- `base_health`, `base_power`, `base_violence`, `base_harmony`,
  `base_slots` — pre-skill, pre-equipment values

Build snapshot (Session 10) — current effective loadout, refreshed
daily by the populator:
- `level`, `xp`
- `total_health`, `total_power`, `total_violence`, `total_harmony`,
  `total_slots` — **effective totals** the game uses for combat /
  economic resolution. Resolved on chain via the canonical formula
  `floor((1000 + boost) * (base + shift) / 1000)`. Use these for
  leaderboards and meta-clustering — never recompute from base + skill
  points locally; you'll diverge from in-game truth.
- `skills_json` — JSON array `[{index, points}, ...]` of upgraded
  skills and their current point investment. Skill → stat mapping is
  not stored; cross-reference against the skill catalog if you need
  to break a stat down by source.
- `equipment_json` — JSON array of item indices currently equipped.
  Slot labels are not resolved (chain registry quirk); raw item
  indices only. Empty `[]` for most kamis — equipment is rare today.
- `build_refreshed_ts` — when the build was last fetched from chain.

Skill-effect modifiers (Session 11) — the 12 non-stat skill effects
from `kami_context/systems/leveling.md`. Resolved totals as the game
uses them, summed across skills + equipment. Stored at on-chain
precision: percent values are ×1000 (e.g. `strain_boost = -200` means
-20% strain), `cooldown_shift` is seconds, `harvest_intensity_boost`
is Musu/hr. Same `build_refreshed_ts` as the build columns.

| Column | Skill key | Tree | Effect |
|---|---|---|---|
| `strain_boost`             | `SB`  | Enlightened/Harvester | strain formula multiplier; **negative = less strain** |
| `harvest_fertility_boost`  | `HFB` | Harvester             | % boost to base income rate |
| `harvest_intensity_boost`  | `HIB` | Guardian              | flat Musu/hr add |
| `harvest_bounty_boost`     | `HBB` | Enlightened/Harvester | % boost to total bounty |
| `rest_recovery_boost`      | `RMB` | Enlightened           | % heal-rate multiplier |
| `cooldown_shift`           | `CS`  | Predator              | collect cooldown delta (negative = shorter) |
| `attack_threshold_shift`   | `ATS` | Predator              | additive shift to attack threshold |
| `attack_threshold_ratio`   | `ATR` | Predator              | multiplicative ratio on attack threshold |
| `attack_spoils_ratio`      | `ASR` | Predator              | % of victim's bounty captured on liquidation |
| `defense_threshold_shift`  | `DTS` | Guardian              | additive shift to defense threshold |
| `defense_threshold_ratio`  | `DTR` | Guardian/Harvester    | multiplicative ratio on defense threshold |
| `defense_salvage_ratio`    | `DSR` | Guardian              | % of own bounty saved when liquidated |

Population data as of late April 2026 (7,021 kamis): `strain_boost`
non-zero on 24% of kamis (min -325, max 0); `harvest_bounty_boost > 0`
on 737 kamis; `attack_spoils_ratio > 0` on 72 kamis; rest mostly 0
across the population — sparse-by-design, not a fetch bug.

Refreshed on transfer / rename (traits) and on the daily sweep
(build + modifiers). Join on `kami_id` for named leaderboards,
build-aware queries, or archetype clustering.

#### What `kami_static` is NOT

Transient and per-second state is **not** stored — read it from chain
directly when you need it (via the agent's `get_kami_state` /
Kamibots, not the oracle):

- `currHP` (kami) and `currMusu` (on the harvest entity, not the kami)
  — these change every block.
- Projected HP / projected bounty — computed at decision time from
  the live `sync` snapshot.
- **Stamina is account-level, not kami-level.** Read it from
  `getAccount(accountId).currStamina`. Kamis don't have stamina.
- Per-stat `shift` and `boost` components separately — only the
  resolved `total_*` is stored. If you need to know "how much of
  Harmony comes from skill points vs equipment", read the four-tuple
  `[base, shift, boost, sync]` from the chain getter directly.
- Per-skill investment broken down by tree
  (`harvester_points` / `predator_points` / `guardian_points` /
  `enlightened_points`) — derive in SQL from `skills_json` × the
  skill catalog if you need it; not stored as columns.

### `raw_tx` — one row per tx touching Kamigotchi systems

`tx_hash`, `block_number`, `block_timestamp`, `from_addr`, `to_addr`,
`method_sig`, `system_id`, `status`, `gas_used`, `gas_price_wei`.
Use this for gas-spend analytics.

### `system_address_snapshot`

`(system_id, address)` rows — Kamigotchi redeploys system contracts
periodically; this table unions all observed addresses per system so
historical decode survives redeploys.

### `ingest_cursor`

Single-row ops state. Usually only `oracle_health()` cares about this.

### action_type values (rough volumes, 7d window)

```
harvest_stop      137k     feed         ~20k    skill_upgrade   ~6k
harvest_start     116k     move          ~3k    item_craft      ~4k
harvest_collect    4.1k    rest_*       rare    quest_*         ~100
harvest_liquidate  1.1k    lvlup         ~5k    scavenge_claim  ~400
                                                 item_use        ~300
                                                 listing_buy     ~200
                                                 gacha_mint/reroll ~130
```

Run a fresh count anytime:
```sql
SELECT action_type, COUNT(*) AS n
FROM kami_action GROUP BY 1 ORDER BY n DESC;
```

## Critical caveats — read before ranking anything

### MUSU semantics: gross vs net

`kami_action.amount` for harvest payouts is **gross MUSU pre-tax** —
the integer item-count drained from the harvest entity before the
on-chain tax split. **Always use gross for kami comparisons**
(leaderboards, productivity rankings); tax varies by node (6%
standard, 12%+ on premium nodes) and would distort rankings if folded
in. A medium kami on a 0%-tax node would falsely outrank a strong
kami on a 12%-tax node if you ranked by net.

For operator-side economics (net-of-tax), join to the matching
`harvest_start` row's `metadata_json` field:
`net = gross - gross * taxAmt / 1e4`.

### `amount` is integer item-count, not wei

MUSU is item index 1 — a plain integer count, not an ERC-20 token.
**Cast as `CAST(amount AS HUGEINT)`. Never divide by `1e18`.**

### `amount IS NULL` is meaningful

NULL is a real on-chain no-op, not a decoder gap:
- `harvest_start` is 100% NULL by design (no payout phase).
- `harvest_stop` ~17% NULL — call hit an already-empty harvest entity.
- `harvest_liquidate` ~13% NULL — same reason.

Always filter `amount IS NOT NULL` when summing/ranking by MUSU.

### Operator name vs signer wallet

`kami_static.account_name` is the in-game Account display name
("bpeon", "tokedo"). Right label for kami-centric queries.
`kami_action.from_addr` is the *signer wallet* — could be a Kamibots
automation key, not the same as the kami's owning Account. They
coincide for manual operators, diverge under automation. Pick the
form that matches your question.

### Window is still filling

Retention config is 28 days but the DB only holds ~7 days of
accumulated data as of late April 2026. Window fills naturally by
~2026-05-24. Until then, `since_days=28` returns the same rows as
`since_days=14` once the DB has 14 days. Not a bug.

## Example queries

### Top earners × build (7d) — meta-clustering starter

The flagship query for "what builds are actually winning right now":

```python
oracle_sql("""
    WITH perf AS (
      SELECT kami_id,
             SUM(CAST(amount AS HUGEINT)) AS musu_gross_7d,
             COUNT(*) FILTER (WHERE action_type IN ('harvest_collect','harvest_stop'))
               AS payouts,
             COUNT(*) FILTER (WHERE action_type = 'harvest_start') AS starts
      FROM kami_action
      WHERE amount IS NOT NULL
        AND action_type IN ('harvest_collect','harvest_stop')
        AND block_timestamp > now() - INTERVAL 7 DAY
      GROUP BY 1
    )
    SELECT s.kami_index, s.name, s.account_name AS operator,
           s.level, s.total_health, s.total_power, s.total_violence,
           s.total_harmony, s.total_slots,
           p.musu_gross_7d, p.payouts, p.starts,
           p.musu_gross_7d / NULLIF(p.payouts, 0) AS musu_per_payout,
           s.skills_json, s.equipment_json
    FROM perf p JOIN kami_static s USING (kami_id)
    ORDER BY p.musu_gross_7d DESC NULLS LAST
    LIMIT 50
""")
```

Pull the result into pandas, run k-means / DBSCAN on
`(total_harmony, total_power, total_violence, level)` to surface
emergent build clusters, then look at `musu_per_payout` and
`musu_gross_7d` distributions per cluster. Confirmed clusters can be
written up in `memory/oracle-findings.md`.

### Sustain-harvester scan — strain reduction × MUSU earned

Surfaces gas-efficient long-session players (most-negative
`strain_boost` = highest sustain investment):

```python
oracle_sql("""
    WITH p AS (
      SELECT kami_id,
             SUM(CAST(amount AS HUGEINT)) AS musu_7d,
             COUNT(*) AS payouts
      FROM kami_action
      WHERE amount IS NOT NULL
        AND action_type IN ('harvest_collect','harvest_stop')
        AND block_timestamp > now() - INTERVAL 7 DAY
      GROUP BY 1
    )
    SELECT s.kami_index, s.name, s.account_name,
           s.level, s.total_harmony,
           s.strain_boost, s.harvest_bounty_boost,
           p.musu_7d, p.payouts,
           p.musu_7d / NULLIF(p.payouts, 0) AS musu_per_payout
    FROM kami_static s LEFT JOIN p USING (kami_id)
    WHERE s.strain_boost IS NOT NULL
    ORDER BY s.strain_boost ASC
    LIMIT 20
""")
```

Pair `strain_boost` with `total_harmony` for "true sustain capacity"
(strain depends on both). High `musu_per_payout` × deeply-negative
`strain_boost` = the gas-efficient meta — fewer txs per Musu earned.

### Predator scan by attack stats

```python
oracle_sql("""
    SELECT s.kami_index, s.name, s.account_name,
           s.level, s.total_violence,
           s.attack_threshold_shift, s.attack_threshold_ratio,
           s.attack_spoils_ratio,
           COUNT(a.id) FILTER (WHERE a.action_type = 'harvest_liquidate'
                                AND a.block_timestamp > now() - INTERVAL 7 DAY)
             AS liqs_7d
    FROM kami_static s
    LEFT JOIN kami_action a ON a.kami_id = s.kami_id
    WHERE s.attack_spoils_ratio > 0
    GROUP BY s.kami_index, s.name, s.account_name, s.level,
             s.total_violence, s.attack_threshold_shift,
             s.attack_threshold_ratio, s.attack_spoils_ratio
    ORDER BY s.attack_spoils_ratio DESC
    LIMIT 20
""")
```

### Average MUSU/7d by harmony bracket

Quick "is the meta actually X?" sanity check:

```python
oracle_sql("""
    SELECT
      CAST(FLOOR(s.total_harmony / 10) * 10 AS INTEGER) AS harmony_bucket,
      COUNT(DISTINCT s.kami_id) AS kamis,
      AVG(p.musu_gross_7d) AS avg_musu_7d
    FROM kami_static s
    LEFT JOIN (
      SELECT kami_id, SUM(CAST(amount AS HUGEINT)) AS musu_gross_7d
      FROM kami_action
      WHERE amount IS NOT NULL
        AND action_type IN ('harvest_collect','harvest_stop')
        AND block_timestamp > now() - INTERVAL 7 DAY
      GROUP BY 1
    ) p USING (kami_id)
    WHERE s.total_harmony IS NOT NULL
    GROUP BY 1 ORDER BY 1
""")
```

### Top earners by gross MUSU (7d) — name-only leaderboard

```python
oracle_sql("""
    SELECT s.kami_index, s.name AS kami_name,
           s.account_name AS operator,
           SUM(CAST(a.amount AS HUGEINT)) AS musu_gross
    FROM kami_action a LEFT JOIN kami_static s USING (kami_id)
    WHERE a.action_type IN ('harvest_collect', 'harvest_stop')
      AND a.amount IS NOT NULL
      AND a.block_timestamp > now() - INTERVAL 7 DAY
    GROUP BY s.kami_index, s.name, s.account_name
    ORDER BY musu_gross DESC NULLS LAST
    LIMIT 20
""")
```

### What's happening on node 16 right now (last 24h)?

```python
oracle_sql("""
    SELECT action_type, COUNT(*) AS n, COUNT(DISTINCT kami_id) AS unique_kamis
    FROM kami_action
    WHERE node_id = 16
      AND block_timestamp > now() - INTERVAL 1 DAY
    GROUP BY 1 ORDER BY n DESC
""")
```

### Predator scan: who's been actively liquidating (7d)?

```python
oracle_sql("""
    SELECT s.kami_index, s.name AS kami_name,
           s.account_name AS operator,
           COUNT(*) AS hits,
           SUM(CAST(a.amount AS HUGEINT)) AS musu_taken
    FROM kami_action a LEFT JOIN kami_static s USING (kami_id)
    WHERE a.action_type = 'harvest_liquidate'
      AND a.amount IS NOT NULL
      AND a.block_timestamp > now() - INTERVAL 7 DAY
    GROUP BY s.kami_index, s.name, s.account_name
    ORDER BY musu_taken DESC NULLS LAST
    LIMIT 20
""")
```

### Liquidation pairing — who hit whom on which node

```python
oracle_sql("""
    SELECT
      ls.kami_index   AS attacker_idx, ls.name AS attacker_name,
      ls.account_name AS attacker_op,
      vs.kami_index   AS victim_idx,   vs.name AS victim_name,
      vs.account_name AS victim_op,
      CAST(l.amount AS HUGEINT) AS musu_taken,
      l.node_id, l.block_timestamp
    FROM kami_action l
    LEFT JOIN kami_static ls ON l.kami_id = ls.kami_id
    LEFT JOIN kami_action h ON l.harvest_id = h.harvest_id
                           AND h.action_type = 'harvest_start'
    LEFT JOIN kami_static vs ON h.kami_id = vs.kami_id
    WHERE l.action_type = 'harvest_liquidate'
      AND l.amount IS NOT NULL
      AND l.block_timestamp > now() - INTERVAL 1 DAY
    ORDER BY l.block_timestamp DESC
    LIMIT 50
""")
```

### My own activity (substitute the operator wallet)

```python
oracle_sql("""
    SELECT action_type, COUNT(*) AS n,
           SUM(CAST(amount AS HUGEINT)) AS musu_gross
    FROM kami_action
    WHERE from_addr = '0xYOUR_OPERATOR_ADDR'
      AND block_timestamp > now() - INTERVAL 7 DAY
    GROUP BY 1 ORDER BY n DESC
""")
```

Or by Account (kami-centric):

```python
oracle_sql("""
    SELECT a.action_type, COUNT(*) AS n,
           SUM(CAST(a.amount AS HUGEINT)) AS musu_gross
    FROM kami_action a JOIN kami_static s USING (kami_id)
    WHERE s.account_name = 'caw'
      AND a.block_timestamp > now() - INTERVAL 7 DAY
    GROUP BY 1 ORDER BY n DESC
""")
```

### Gas spend (ETH) by an operator wallet

```python
oracle_sql("""
    SELECT SUM(gas_used * gas_price_wei) / 1e18 AS eth_spent
    FROM raw_tx
    WHERE from_addr = '0xYOUR_OPERATOR_ADDR'
      AND block_timestamp > now() - INTERVAL 7 DAY
""")
```

## Limits & errors

- **10s query timeout** per `/sql` call.
- **10,000 row cap** per response. `truncated: true` in the response means hit the cap; raise `limit` (max 10,000) or paginate by time window.
- **60 req/min per token.** `oracle_sql` returns `{"error": "rate_limited", "status": 429}` if you exceed it. Back off and retry.
- **400 on bad SQL or write attempts.** Returned as `{"error": "bad_query", "detail": "...", "status": 400}` — the `detail` carries the DuckDB error.
- **401** = token rejected. Means the token has been rotated; see ADR-005 for the rotation procedure (re-pull from oracle VM into `~/.blocklife-keys/.env`, restart MCP server).

## Decision logging (kami-zero)

Per ADR-006, kami-zero does NOT maintain a parallel
`memory/oracle-findings.md` — calibration was cleared by kami-agent.
Instead, when an oracle-derived insight informs a per-session
decision, capture it inline in your standard `memory/decisions.md`
entry: the query you ran, the result summary, the action it informed,
and the decision rationale. The founder reviews `decisions.md`
periodically and can roll back any oracle-driven decision via a
`plan.md` Priority 0 directive.

Oracle output is collective behavior, not received truth. Top kamis
may be top because of luck, an exploit, an account-tier advantage we
can't see, or a phase that's already ending. Treat oracle data the
same way you treat the in-game `sync` snapshot: a useful prior, not
a verdict.

## Operations notes (rare, mostly for the founder)

- **Endpoint:** `https://136-112-224-147.sslip.io` (TLS via Let's Encrypt E8 through 2026-07-23).
- **VM:** `kami-oracle` in project `kami-agent-prod`, zone `us-central1-a`, static IP `136.112.224.147`.
- **Service control on the VM:** `sudo systemctl status|restart kami-oracle`.
- **Backups:** nightly to `gs://kami-oracle-backups/` at 04:15 UTC, 14-day retention.
- **Token rotation:** see ADR-005 in `blocklife-ai/context/decisions/`.
- **Full Colab/exploration guide:** `blocklife-ai/context/kami-oracle-bootstrap/colab-setup.md`.
