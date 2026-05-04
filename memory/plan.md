# Plan for session 155 — fresh-bucket scan + rates-aware partition; parked-rates is now the population default

## Context (post-session 154, 0 kills / 0 reverts; parked-rates pattern UNIVERSAL across 7 owners / 6 nodes)

**Combined sample 10/10 parked** (s153: 6, s154: 4) across TrayzinCarpathia, yeddy, Gunnar, alexbuyer, tamagotcho, orange/zizi, fluff. Owners span 6 nodes (60, 53, 31, 9, 25, 12) and 19h+ of harvest-start timestamps. **Hypothesis upgraded**: parked-rates isn't a per-owner defense — it's the **population-default state** for any harvest >~2h without continuous owner action. The watcher's elapsed-based proj_hp model is wrong for ~70-90% of `killable_v2` rows.

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Strikers HARVESTING node 60 since 17:54:43Z (~5.0h+ at session 155 start).** No HP loss. Intensity continues to build.

**Streak watch**: s152 + s153 + s154 = 3 consecutive 0-kill sessions. **2 more (155, 156) → 5-session Design-Mode trigger.**

---

## Priority 1 — Fresh-bucket-first slim sweep (NEW s154)

### Pre-fire workflow (UPDATED s154 — partitioned)

1. **Read fresh `world_targets.json`**.
2. **Partition `killable_v2`** into:
   - **Fresh bucket**: `elapsed_h < 0.5` AND margin ≥+30 — most likely to have rates>0; small margins are real.
   - **Stale bucket**: `elapsed_h >= 2.0` AND margin ≥+30 — empirically poisoned (10/10 parked across s153+s154 sample); presumptively unkillable until slim verifies.
3. **Slim-check fresh bucket first** (2-4 candidates). Read `harvest.rates.intensity.average` and `stats.health.sync`.
   - Skip if `rates.intensity.average == 0` (parked).
   - Strike if `rates > 0` AND `kill_zone − sync_HP ≥ +30`.
4. **If fresh bucket empty or all skipped**: slim-check 2-3 stale candidates as **CONTROL** to confirm parked-rates persistence (informs design-mode urgency).
5. **If 0 strikes possible**: end fast, schedule short re-wake, count toward streak.

### Strike sequence (1 per MCP response)

- 2-deep-revert-stop unchanged.
- Per-owner kill cap 2-3/session.
- Universal floor: rates-verified actual_margin ≥+30.

### Skip list (parked-rates owners — 7 confirmed)

- **TrayzinCarpathia node 60** (898/5420/7531) — s152
- **yeddy node 53** (1881/8038/7328/5299) — s153
- **Gunnar node 31** (15409) — s153
- **alexbuyer node 31** (11494) — s153
- **acheron node 87** (7505 verified s152) — likely whole account
- **tamagotcho node 9** (7311) — NEW s154
- **orange/zizi node 25** (336/5887/1622) — NEW s154
- **fluff node 12** (7230, presumed 234) — NEW s154

### Deny-set (full block)

- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…**
- **vuongdung1198 V<22**
- **POWELL / PuppyPriestess** (PuppyPriestess is competitor-predator)
- **2644 V10 sb=−25** (E006 floor +95 unmet)

### Expected outcome
- If fresh bucket empty (typical for current world state): 0 strikes, fast slim-only session, ~0 gas.
- If 1+ fresh candidate has rates>0 + actual_margin ≥+30: 1-2 obols possible.
- Net session burn: 0-5M gas depending.

---

## Priority 2 — Design-Mode countdown (build prep)

### Trigger
- s152 + s153 + s154 = 3 zero-kill sessions. If **155 + 156 also 0-kill** → Design Mode per CLAUDE.md (5-session trigger).

### Action when triggered (s157 if streak hits)
- Pause hunting. Spend session designing + building **rates-aware pre-filter cron** (`predator/scripts/refresh_parked_rates.py`):
  - Every 5 min, slim-check (or web3-direct read) the harvest entity for top 50 killable_v2 candidates.
  - Emit `predator/parked_rates_state.json` with per-candidate `rates.intensity.average`, `rates.fertility`, `balance`, `health.sync`.
  - Watcher consumes this file to filter `killable_v2` by `rates>0`.
  - If oracle adds these fields per `ideas_to_founder.md § 6`, switch to oracle (preferred per Data-Plane: Oracle-Only).
- Also: design `fresh_harvest_index.json` — surface kamis with `harvest.time.start` within last 30 min (where rates >0 is most likely). Possibly already implicit in watcher elapsed_h field — verify.
- Test counter-mechanism hypothesis: **does `Animistic Poison` (item 19101, STRAIN+50%) un-park a kami's rates?** Currently 0 Blue Pansy stock blocks crafting (see ideas_to_founder § 5a).

### Pre-build (optional s155-156 if hunting empty)
- If session 155 finds 0 candidates and we have time, draft the rates-aware filter cron schema. Don't ship yet — wait for trigger.

---

## Priority 3 — Competitor-victim cluster opportunistic strikes (TERTIARY)

### Trigger
- Slim-check finds rates>0 on any FRESH candidate at a node where competitor recently killed.

### Action
- Cross-reference `world-liquidations.jsonl` last 6h non-self kills.
- Cross-region travel only if cluster EV ≥3 rates-verified ≥+30 candidates.

---

## Heat-window monitoring (passive)

- All 7 parked-rates owners — owner_heat doesn't flag them. Update `predator/targeting.md` next opportunity.
- **maia 80 / wiuuuu** — re-evaluate via slim rates-check rather than `owner_heat`.

---

## Carry-over learnings

### Session 154 NEW
1. **Parked-rates is universal across long harvests** (10/10 sample now), not per-owner defense. Working hypothesis: game-system equilibrium for high-DTS kamis under no-action condition.
2. **Fresh-bucket-first scan** — bias slim verification toward `elapsed_h <0.5` candidates where rates haven't yet decayed.
3. **Skip-list now spans 7 owners + 6 nodes** — almost the entire surfaced killable population. Watcher is essentially blind; rates-aware filter is now urgent.
4. **Stale bucket is presumptively poisoned** — only slim-check stales as control samples (2-3) to track parked-rates persistence.

### Session 153 (carry-over)
- `harvest.rates.intensity.average == 0` is canonical strike-go signal.
- 6-slim sample sufficient to declare session dead; competitor kills at hot nodes don't imply current killability.

### Session 152 (carry-over, refined)
- Continuous-sync defense pattern was right hypothesis but wrong signal — refined to rates>0 in s153, broadened to population-default in s154.

### Session 151 (carry-over)
- Striker-rotation chain-3 floor +50 (only meaningful if rates-verified — and almost no rates-verified candidates currently exist).

### Session 149 (carry-over)
- 180s post-harvest_start cooldown for liquidate.

---

## Hard limits

- **Gas budget session 155**: ~3M (if 0-1 strikes — typical fresh-bucket scenario).
- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…** = deny-all.
- **vuongdung1198 V<22** off-limits.
- **POWELL / PuppyPriestess** avoid.
- **All 7 parked-rates owners** = only strike via fresh slim-rates-check (rates>0 verified).
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

**Pin**: "Re-wake **+15 min** (~22:55 UTC May 4, ts **1777935315**). Pinned to:
- (a) **Fresh-harvest opportunism**: ~3 watcher cycles + 3 cron ticks of fresh data within window; new harvest_start events from owner-action waves create brief non-parked windows.
- (b) **Cluster turnover**: defenders may rotate kamis on uneven schedules; new fresh-elapsed candidates may surface.
- (c) **Streak-counter**: if s155 + s156 also 0-kill → DESIGN MODE in s157.
- Cache miss (>300s) accepted — investigation amortizes."

**Re-wake**: **1777935315** (~22:55 UTC May 4).

---

## Out of scope (session 155)

- Pivot to any of the 7 parked-rates owners without fresh rates-check.
- Glue-raid (untested vs parked rates; saved for design-mode hypothesis).
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set.
- Quest progression, kamibots state reads, force-flush.
- Striking stale-bucket candidates without rates-verified slim.
- Premature design-mode build (wait for trigger or session 157).

---

## Bias fire-now

Default action ladder:
1. **Partition killable_v2 fresh vs stale**.
2. **Slim-check fresh bucket first** (early-skip on rates.intensity == 0).
3. **Strike first fresh candidate where rates>0 AND actual_margin ≥+30** (1 strike per MCP response).
4. **Slim-check 2-3 stale candidates as control** to track parked-rates persistence.
5. **harvest_stop + mint** if 5+ sessions of no kills accumulate AND staying parked across multiple cycles (unlikely given 12649's intensity build).
6. **If 5-session zero-kill streak hits** (s152, s153, 154, 155, 156) → Design Mode in s157: build the rates-aware filter cron.
