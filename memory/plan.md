# Plan for session 153 — sync-verified strikes only; watcher proj_hp is broken

## Context (post-session 152, 0 kills / 2 reverts at TrayzinCarpathia 898 with both 11224 and 12649)

**Major doctrine cost discovery**: watcher's proj_hp model is BROKEN for kamis in continuous-sync defense state. Confirmed across TrayzinCarpathia (node 60) AND acheron (node 87) — pattern is systemic, not owner-specific.

**Slim signal for continuous-sync defense (NEW DOCTRINE)**:
- `harvest.balance == 0`
- `harvest.time.last == harvest.time.start == harvest.time.reset`
- `harvest.state == "ACTIVE"`
- `stats.health.sync == stats.health.total` (full HP)

When all four match: watcher's proj_hp is meaningless. Strike WILL revert.

**Lifetime: 72 kills / 74 obols / 4 reverts (+2 doctrine-cost s152). Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool from s151 2141 spoils).**

**Strikers HARVESTING node 60 since 17:54:43Z (~4h+ at session 153 start).** Reverts deducted no HP. Strikers ready.

---

## Priority 1 — Sync-verified strike doctrine (PRIMARY)

### Pre-fire workflow (mandatory; supersedes prior margin-floor checks)

1. **Read fresh `world_targets.json`** (watcher cycles at :30/:35/etc).
2. **For each candidate with margin ≥+30**, call `get_kami_state_slim(v_idx)` BEFORE any strike:
   - Read `stats.health.sync` (the on-chain HP at last touch).
   - Compute `actual_margin = kill_threshold − sync_HP`.
   - Strike only if `actual_margin ≥+30` (or relevant floor).
   - **Skip the candidate** if `harvest.balance == 0 AND harvest.time.last == time.start == time.reset` (continuous-sync defense triplet).
3. **Watcher's `margin` field is now NOT trustworthy** for HARVESTING-but-defended kamis. Treat watcher as a CANDIDATE-FILTER (narrows the search), not a STRIKE-AUTHORITY (says "this will land").

### Strike sequence (1 per MCP response)

- Top candidates (re-derive from fresh watcher snapshot):
  - V<22 sb=0 margin ≥+50: spot-check slim, strike if actual_margin ≥+30.
  - V<22 sb=0 margin +30 to +50: spot-check slim, strike if actual_margin ≥+30 AND chain-2 same-striker rule satisfied (not chain-2 unless margin >+50 OR close-feed).
- **2-deep-revert-stop unchanged** — if 2 reverts in a session, STOP regardless of remaining candidates.

### Skip list (session 153 outlook)

- **898 V14 sb=0** at Trayzin — confirmed continuous-sync state. Add to do-not-strike-without-fresh-sync-check list.
- **5420 V15 sb=0** at Trayzin — confirmed continuous-sync state.
- **Acheron node 87 cluster** (7505 etc.) — confirmed continuous-sync state on at least 7505. Likely all candidates same. Spot-check before pivoting.
- **2644 V10 sb=−25** — E006 floor +95 unmet.
- **wiuuuu, 7531 sustain etc.** — sub-floor.

### Expected outcome
- **0-3 obols** depending on how many candidates pass slim spot-check.
- Net session burn: ~5-15M gas.
- If ALL candidates fail slim: harvest_stop strikers (mint 688 MUSU) and rebuild plan around competitor-victim signals.

---

## Priority 2 — Competitor-predator success signal mining (SECONDARY)

### Trigger
- All sync spot-checks fail.

### Action
- Read `predator/world-liquidations.jsonl` last 6h (cron-maintained).
- For non-self kill rows: victim's account is genuinely-starving-vulnerable at that moment. The same account's OTHER kamis are likely also genuine targets.
- Cross-reference: any of those owners with HARVESTING kamis in `by_node` we can reach?
- Spot-check via slim before pivoting.

---

## Priority 3 — Watcher patch (BUILD TASK, sessions 153-155)

### Goal
Add a sync-state pre-filter to `predator/scripts/refresh_world_targets.py` that disqualifies candidates in continuous-sync state.

### Approach (simplest first)
- Cron sub-process: every 5 min, for each kami in `killable_clean` (top 30), fetch `get_kami_state_slim` (or web3 direct read of harvest entity).
- Read `harvest.balance`, `harvest.time.last/start/reset`, `stats.health.sync`.
- Emit per-candidate `actual_proj_hp` (= sync if balance=0+all-times-equal, else watcher's strain-projection).
- Filter killable_v2 by `kill_zone − actual_proj_hp ≥ +30`.

### Caveats
- Cost: ~30 slim calls per cron cycle. 15s cache mitigates. Can be batched if web3 direct.
- Per CLAUDE.md "Data Plane: Oracle-Only" — slim is allowed for staleness escape but should be avoided. If oracle adds a `harvest_balance` / `harvest_time_last` snapshot table → use that instead. Write the ask to `ideas_to_founder.md`.

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia**: RECLASSIFIED from "passive farmer" → "continuous-sync defender" (subset of defensive-cycle but watcher heat misses). owner_heat shows {} because heat checks miss this pattern. Update `predator/targeting.md` next session.
- **acheron**: NEW classification — continuous-sync defender at node 87. Was target-of-opportunity in s152 plan; now skip without sync verification.
- **maia 80 / wiuuuu / others**: re-evaluate via slim spot-check rather than `owner_heat`.

---

## Carry-over learnings

### Session 152 NEW
1. **Continuous-sync defense pattern**: kami appears HARVESTING but actual HP = full sync. Detected via slim triplet (balance=0, time.start=last=reset, ACTIVE). Watcher proj_hp is meaningless for these.
2. **Pre-strike sync verification mandatory** at margin ≥+30. One slim call per candidate, ~free.
3. **Watcher's margin field is candidate-filter, not strike-authority**. Reframe.
4. **owner_heat misses sync-defense automation**. heat checks for harvest_stop spam, not heal/sync spam.
5. **S150/s151 Trayzin kills were luck-of-timing**, not exploitable doctrine. The 4 successful kills landed when target's sync hadn't fired recently (real starvation HP).

### Session 151 (carry-over, but now superseded by sync doctrine)
- "Chain-3 striker-rotation floor +50" — irrelevant for continuous-sync defenders. Margin floors only matter when watcher's proj_hp is right.

### Session 149 (carry-over)
- 180s post-harvest_start cooldown for liquidate.
- Glue-raid premise revisited: continuous-sync defense ≠ defensive-cycle. Glue might still disrupt sync (untested).

---

## Hard limits

- **Gas budget session 153**: ~10M for slim-verified strikes (lower than s152 — uncertainty about hit-rate).
- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL / PuppyPriestess** avoid.
- **TrayzinCarpathia** — RECLASSIFIED continuous-sync-defender; only strike via fresh slim spot-check.
- **acheron** — same.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 (post-sync-verified).
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floors (UPDATED s152)**:
  - **Sync-verified actual_margin ≥+30** is the new universal floor, supersedes prior nominal floors.
  - +25 plan-floor (active-owner zero-travel) — only valid if sync-verified.
  - +27 validated travel-cost — same.
  - **+50 chain-3 striker-rotation floor (s151)**: only meaningful if sync-verified.
- **Per-owner kill cap 2-3/session**.
- **Cross-region travel**: gate on cluster EV ≥3 sync-verified ≥+30 candidates.
- **180s harvest_start cooldown** + **180s post-strike cooldown** on attackers.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~22:20 UTC May 4, ts **1777933200**). Pinned to:
- (a) **Cluster turnover**: continuous-sync defenders' sync timers may briefly expose real strain mid-cycle. Catching that window requires more frequent observation.
- (b) **Slim spot-check doctrine** is the next concrete action — apply it as soon as possible, not after over-thinking.
- (c) **Mid-evening hunt rhythm**: 22:00-22:30 UTC is typical Western-Europe-asleep / NA-evening — competitor predator activity may surface fresh kills in `world-liquidations.jsonl`.
- (d) Striker post-strike cooldowns long cleared.
- Cache miss accepted (>300s) — wait amortizes across multiple specific signals."

**Re-wake**: **1777933200** (~22:20 UTC May 4).

---

## Out of scope (session 153)

- Pivot to acheron or any cross-region cluster without sync-verifying ≥3 candidates first.
- Glue-raid (untested vs sync-defense; glue saves preserved for genuine sync-stop-burst defenders).
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set.
- Quest progression, kamibots state reads, force-flush.
- Striking 898 / 5420 without fresh slim showing actual_margin ≥+30.

---

## Bias fire-now

Default action ladder:
1. **Slim spot-check top 3-5 V<22 sb=0 candidates** (margin ≥+30 in watcher).
2. **Strike any candidate where actual_margin ≥+30** (1 strike per MCP response).
3. **harvest_stop + mint** if all spot-checks fail.
4. **Mine `world-liquidations.jsonl`** for non-self competitor wins → pivot scout.
5. **Patch watcher** if 2-3 sessions of slim-spot-checking shows the verifier loop is the binding constraint on hunt rate.
