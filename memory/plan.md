# Plan for session 154 — rates-verified strikes only; "parked rates" is the canonical un-killable signal

## Context (post-session 153, 0 kills / 0 reverts; 6-slim sweep confirms parked-rates universality)

**The s152 "continuous-sync" doctrine has been refined**: the actual signal is `harvest.rates.intensity.average == 0 AND harvest.rates.fertility == 0`, NOT the time-triplet equality (which is just normal harvesting). 6/6 slim probes across 3 owners (TrayzinCarpathia, yeddy, Gunnar/alexbuyer) and 3 nodes (60, 53, 31) showed identical parked-rates state. This explains why phantom margins persist across the killable_v2 list: watcher's elapsed-based strain projection is meaningless when intensity=0.

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Strikers HARVESTING node 60 since 17:54:43Z (~4.6h+ at session 154 start).** No HP loss this session. Intensity continues to build.

---

## Priority 1 — Rates-verified strike workflow (UPDATED s153)

### Pre-fire workflow (mandatory; replaces s152's time-triplet check)

1. **Read fresh `world_targets.json`**.
2. **For each candidate margin ≥+30**, call `get_kami_state_slim(v_idx)`:
   - **Step 1 (early-skip)**: read `harvest.rates.intensity.average`. If 0, **skip immediately** — kami is parked, no strain, watcher proj_hp is phantom.
   - **Step 2 (sync verification)**: if rates.intensity > 0, also verify `stats.health.sync` is below `kill_zone − 5`. Watcher's proj_hp may still differ from real HP if recent feed/heal/syncs occurred.
   - **Step 3 (strike gate)**: actual_margin (kill_zone − sync_HP) ≥+30 to fire.
3. **Skip the candidate** if any of: rates parked, sync HP > threshold, recent_revive=true, fresh_feed_since_start=true.

### Strike sequence (1 per MCP response)

- Top candidates from fresh watcher snapshot, filtered by V<22 + sb≥0 + margin ≥+50 (chain-3 floor s151).
- **2-deep-revert-stop unchanged** — if 2 reverts in a session, STOP regardless of remaining candidates.
- Per-owner kill cap 2-3/session.

### Skip list (entered s152-s153)

- **898 / 5420 / 7531 (TrayzinCarpathia node 60)** — confirmed parked rates.
- **1881 / 8038 / 7328 (yeddy node 53)** — confirmed parked rates. Whole-account pattern likely.
- **15409 (Gunnar) / 11494 (alexbuyer) at node 31** — confirmed parked rates.
- **acheron node 87** (7505 verified s152) — likely parked across all candidates.
- **2644 V10 sb=−25** — E006 floor +95 unmet.
- **vuongdung1198 V<22** — off-limits.
- **3333…/4444…/Aenne/foden/dias/stefan97/rtvvvvv** — deny-all.

### Expected outcome
- If world remains parked: 0 strikes, fast slim-only session.
- If 1+ candidate flips rates>0 in the brief window: 1-2 obols possible.
- Net session burn: 0-15M gas depending.

---

## Priority 2 — Design-Mode counter-watch (SECONDARY, build-leaning)

### Trigger
- Session 154 starts a 5-session zero-kill watch (s152 + s153 already 0). If sessions 154+155+156 also 0, hit CLAUDE.md Design-Mode trigger.

### Action when triggered
- Pause hunting. Spend session designing a **rates-aware pre-filter cron** (`predator/scripts/refresh_parked_rates.py`):
  - Every 5 min, slim-check (or web3-direct read) the harvest entity for top 50 killable_v2 candidates.
  - Emit `predator/parked_rates_state.json` with per-candidate `rates.intensity.average`, `rates.fertility`, `balance`.
  - Watcher consumes this file to filter killable_v2 by rates>0.
  - If oracle adds these fields per `ideas_to_founder.md § 6`, switch to oracle (preferred per Data-Plane: Oracle-Only).
- Also test counter-mechanism hypotheses: **does `Animistic Poison` (item 19101, STRAIN+50%) un-park a kami's rates?** If yes, the parked-rates defense has a counter. Currently 0 Blue Pansy stock blocks crafting (see ideas_to_founder § 5a).

---

## Priority 3 — Competitor-victim cluster opportunistic strikes (TERTIARY)

### Trigger
- Slim-check finds rates>0 on any candidate at a node where competitor recently killed (PuppyPriestess Scrapyard Exit, IBCKING Forest: Insect Node).

### Action
- Cross-reference `world-liquidations.jsonl` last 6h non-self kills with current `by_node` snapshot.
- Slim-check top 3 candidates per such node BEFORE pivoting (cluster-economics gate: ≥3 rates-verified candidates needed).
- If verified: cross-region travel (operator + all 6 strikers → batch harvest_stop, travel, batch harvest_start).

---

## Heat-window monitoring (passive)

- **TrayzinCarpathia / acheron / yeddy** = parked-rates defenders. owner_heat doesn't flag them. Update `predator/targeting.md` next opportunity.
- **Gunnar / alexbuyer** = parked-rates DEFENDERS too (despite recent competitor kills against them) — confirm s153 finding is post-kill state.
- **maia 80 / wiuuuu** — re-evaluate via slim rates-check rather than `owner_heat`.

---

## Carry-over learnings

### Session 153 NEW
1. **Parked-rates pattern is universal** (6/6 across 3 owners, 3 nodes, 3 hbsv timestamp ranges): `rates.intensity.average == 0 AND rates.fertility == 0` while `state == "ACTIVE"` = unkillable.
2. **`harvest.rates.intensity.average` is the canonical strike-go signal**, NOT the time-triplet equality. s152 doctrine is refined to drop time-triplet as primary signal.
3. **Watcher's proj_hp is invalid** for any high-elapsed kami until oracle surfaces rates.
4. **6 slim probes is sufficient** to declare a session dead when all show parked rates. Don't burn more.
5. **Competitor kills at Scrapyard/Forest 5h ago do NOT signal current killability** — those owners' OTHER kamis are now parked.

### Session 152 (carry-over, refined)
- Continuous-sync defense pattern was the right hypothesis but wrong signal — refined to rates>0 in s153.

### Session 151 (carry-over)
- Striker-rotation chain-3 floor +50 (only meaningful if rates-verified).

### Session 149 (carry-over)
- 180s post-harvest_start cooldown for liquidate.
- Glue-raid premise: glue-on-parked might un-park (untested but worth testing in design mode).

---

## Hard limits

- **Gas budget session 154**: ~5M (if 0-1 strikes). Aborted on first revert.
- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL / PuppyPriestess** avoid (PuppyPriestess is competitor-predator, not target).
- **TrayzinCarpathia / acheron / yeddy / Gunnar / alexbuyer** = parked-rates defenders; only strike via fresh slim-rates-check.
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 (post-rates-verified).
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floors (UPDATED s153)**:
  - **Rates-verified actual_margin ≥+30** = universal floor.
  - +50 chain-3 striker-rotation floor (s151) — only meaningful if rates-verified.
- **Per-owner kill cap 2-3/session**.
- **Cross-region travel**: gate on cluster EV ≥3 rates-verified ≥+30 candidates.
- **180s harvest_start cooldown** + **180s post-strike cooldown** on attackers.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+12 min** (~22:37 UTC May 4, ts **1777934220**). Pinned to:
- (a) **Rates-flip opportunism**: 2-3 watcher cycles + 3 cron ticks of fresh data within window.
- (b) **Cluster turnover**: defenders may rotate kamis on uneven schedules; new candidates may surface with strain-bleeding rates.
- (c) Striker post-strike cooldowns long cleared (~5h ago).
- Cache stays warm (<300s)."

**Re-wake**: **1777934220** (~22:37 UTC May 4).

---

## Out of scope (session 154)

- Pivot to acheron / TrayzinCarpathia / yeddy / Gunnar / alexbuyer without fresh rates-check.
- Glue-raid (untested vs parked rates; saved for design-mode hypothesis).
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set.
- Quest progression, kamibots state reads, force-flush.
- Striking 898 / 1881 / 8038 / 7328 / 15409 / 11494 / 5420 / 7531 / 7505 without fresh rates>0 verification.

---

## Bias fire-now

Default action ladder:
1. **Slim spot-check top 3-5 V<22 sb=0 candidates margin ≥+50** (early-skip on rates.intensity == 0).
2. **Strike any candidate where rates>0 AND actual_margin ≥+30** (1 strike per MCP response).
3. **harvest_stop + mint** if all parked AND staying parked across multiple cycles.
4. **Mine `world-liquidations.jsonl`** for fresh non-self competitor wins → rates-verify their owners' current cluster.
5. **If 5-session zero-kill streak hits** (s152, s153, 154, 155, 156) → Design Mode: build the rates-aware filter cron.
