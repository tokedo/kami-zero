# Plan for session 156 — fresh-bucket scan; if empty, write Design-Mode trigger entry and prep s157 build

## Context (post-session 155, 0 kills / 0 reverts; combined 12/12 parked-rates sample across 8 owners / 6 nodes)

s152+s153+s154+s155 = **4 consecutive 0-kill sessions**. **s156 is the streak-gate**: if it lands 0 kills, the 5-session Design-Mode trigger from CLAUDE.md fires and s157 is a mandatory build session.

Watcher's `killable_v2` is essentially hallucinated for stale candidates. s155 confirmed: zero strikable candidates in the entire 50-row killable_v2 (after deny-set + parked-rates skip-list filtering). 12/12 stale-bucket controls slim-checked across s153+s154+s155 all showed `rates.intensity.average == 0 AND balance == 0 AND sync == total` — parked-rates is the population default for any harvest >~2h.

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: 530179 (~688 pending in 12649's pool).**

**Strikers HARVESTING node 60 since 17:54:43Z (~5.1h+ at session 155 end, ~5.4h+ at session 156 start).** No HP loss this session. Intensity continues to build.

---

## Priority 1 — Fresh-bucket-first slim sweep (UNCHANGED from s155)

### Pre-fire workflow (s154-doctrine, s155-validated)

1. **Read fresh `world_targets.json`**.
2. **Partition `killable_v2`** into:
   - **Fresh bucket**: `elapsed_h < 0.5` AND margin ≥+30 — most likely to have rates>0.
   - **Mid bucket**: `0.5 ≤ elapsed_h < 2.0` AND margin ≥+30 — possibly rates>0.
   - **Stale bucket**: `elapsed_h >= 2.0` AND margin ≥+30 — empirically poisoned (12/12 parked across s153-s155 sample).
3. **Slim-check fresh bucket first** (2-4 candidates). Read `harvest.rates.intensity.average` and `stats.health.sync`.
   - Skip if `rates.intensity.average == 0` (parked).
   - Strike if `rates > 0` AND `kill_zone − sync_HP ≥ +30`.
4. **If fresh + mid empty**: do NOT slim-check stales (12/12 sample is conclusive — additional probes are wasted cycles). Move directly to streak-gate handling (P2).
5. **If 0 strikes possible**: write design-mode-trigger entry, schedule longer re-wake (~30 min), prep s157 build queue.

### Strike sequence (1 per MCP response)

- 2-deep-revert-stop unchanged.
- Per-owner kill cap 2-3/session.
- Universal floor: rates-verified actual_margin ≥+30.

### Skip list (parked-rates owners — 8 confirmed)

- **TrayzinCarpathia node 60** (898/5420/7531) — s152
- **yeddy node 53** (1881/8038/7328/5299) — s153, s155 reconfirmed
- **Gunnar node 31** (15409) — s153
- **alexbuyer node 31** (11494) — s153
- **acheron node 87** (7505 verified s152) — likely whole account
- **tamagotcho node 9** (7311) — s154
- **orange/zizi node 25** (336/5887/1622) — s154, s155 reconfirmed (336)
- **fluff node 12** (7230, presumed 234/6307/10544) — s154

### Deny-set (full block)

- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…**
- **vuongdung1198 V<22** (V=22 row exists but sb=-125 puts under E006 +95 floor)
- **POWELL / PuppyPriestess** (PuppyPriestess is competitor-predator)
- **2644 V10 sb=−25** (E006 floor +95 unmet)

### Expected outcome
- If fresh bucket has any candidate: 1-2 obols possible.
- If fresh + mid empty (the s155 outcome — most likely): 0 strikes, design-mode trigger, prep s157 build.

---

## Priority 2 — Design-Mode entry (s157 if streak triggers)

### Trigger
- s152+s153+s154+s155 = 4 consecutive 0-kill. **s156 0-kill = 5-session trigger.**

### Action when triggered (s157)

#### Build queue (in priority order)

1. **`predator/scripts/refresh_parked_rates.py`** — slim-rate scanner cron (~5-10 min interval).
   - Input: top 50 candidates from latest `world_targets.json` (rank by margin desc).
   - For each: call `get_kami_state_slim(victim)` → extract `harvest.rates.intensity.average`, `harvest.rates.fertility`, `harvest.balance`, `stats.health.sync`, `stats.health.total`.
   - Output: `predator/parked_rates_state.json` keyed by victim_idx with `{rates_intensity_avg, fertility, balance, sync, total, last_checked_ts, parked_bool}`.
   - Optional: rate-limit / batch with asyncio if 50 calls is too slow per cycle.
2. **Watcher integration**: modify watcher to read `parked_rates_state.json` if present and filter `killable_v2` rows where `parked_bool == true` OR (`elapsed_h >= 2.0` AND no rates entry — fail-safe).
3. **`fresh_harvest_index.json`** (optional, may already be implicit in watcher's elapsed_h field — verify): a separate surface for kamis with `harvest.time.start` within last 30 min.
4. **Counter-mechanism hypothesis test (low priority, gated on Blue Pansy supply)**: does `Animistic Poison` (item 19101, STRAIN+50%) un-park a kami's rates? Currently 0 Blue Pansy stock blocks crafting (see ideas_to_founder § 5a). Don't pursue until ingredient available.

#### Design-mode session shape (s157 if triggered)
- No strikes.
- Spend session: scaffold `refresh_parked_rates.py`, dry-run on top 5 candidates manually, validate output schema, write cron entry to `infrastructure.md` (per CLAUDE.md), commit.
- Test integration: read `parked_rates_state.json` from a fresh watcher cycle and confirm fresh bucket would surface non-parked candidates if any exist.

---

## Priority 3 — Competitor-victim cluster opportunistic strikes (TERTIARY)

### Trigger
- Slim-check finds rates>0 on any FRESH candidate at a node where competitor recently killed.

### Action
- Cross-reference `world-liquidations.jsonl` last 6h non-self kills.
- Cross-region travel only if cluster EV ≥3 rates-verified ≥+30 candidates.

---

## Heat-window monitoring (passive)

- All 8 parked-rates owners — owner_heat doesn't flag them. Targeting/owner-defense doc updates remain on `predator/targeting.md` backlog (low priority during streak watch).
- **maia 80 / wiuuuu** — re-evaluate via slim rates-check rather than `owner_heat`.

---

## Carry-over learnings

### Session 155 NEW (incremental)
1. **Stale-bucket slim probes are now wasted cycles** (12/12 parked). Stop probing stales for control sampling — the doctrine is settled. Probe only fresh bucket.
2. **vuongdung1198 V=22 row is dual-blocked** (sb=-125 → E006 floor +95 > margin +34). Even if rates>0, doctrine deny.
3. **Streak now 4 consecutive 0-kill** — Design Mode is one session away. Plan-156 should pre-stage the build queue so s157 entry is fast.

### Session 154 (carry-over)
- Parked-rates is universal across long harvests, not per-owner defense.
- Fresh-bucket-first scan is the binding tactic until rates-aware filter ships.

### Session 153 (carry-over)
- `harvest.rates.intensity.average == 0` is canonical strike-go signal.
- 6-slim sample sufficient to declare a session dead.

### Session 152 (carry-over, refined)
- Continuous-sync defense pattern was right hypothesis but wrong signal — refined to rates>0 in s153, broadened to population-default in s154-155.

### Session 151 (carry-over)
- Striker-rotation chain-3 floor +50 (only meaningful if rates-verified — no rates-verified candidates currently exist in surfaced population).

### Session 149 (carry-over)
- 180s post-harvest_start cooldown for liquidate.

---

## Hard limits

- **Gas budget session 156**: ~2M (most likely 0M; reserved for 1-2 strikes if fresh bucket surprises).
- **Aenne / 3333… / foden / dias / stefan97 / rtvvvvv / 4444… / 1444…** = deny-all.
- **vuongdung1198 V<22** off-limits; V=22 row dual-blocked by E006.
- **POWELL / PuppyPriestess** avoid.
- **All 8 parked-rates owners** = only strike via fresh slim-rates-check (rates>0 verified).
- **2-deep-revert-stop rule** unchanged.
- **V<22 chain-2 forbidden** without close-feed-then-strike or margin >+50 (post-rates-verified).
- **Pre-strike Apology Letter** ONLY when target V≥30.
- **Always pass `target_handle`** to `liquidate`.
- **Never dispatch two `liquidate` (or any state-mutating tx) in the same MCP tool-call response**.
- **Margin floors**:
  - **Rates-verified actual_margin ≥+30** = universal floor.
  - +50 chain-3 striker-rotation floor (s151) — only meaningful if rates-verified.
- **Per-owner kill cap 2-3/session**.
- **Cross-region travel**: gate on cluster EV ≥3 rates-verified ≥+30 candidates.
- **180s harvest_start cooldown** + **180s post-strike cooldown** on attackers.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+15 min** (~23:15 UTC May 4, ts **1777936511**). Pinned to:
- (a) **Fresh-harvest opportunism**: ~3 watcher cycles + 3 cron ticks of fresh data within window; new harvest_start events from owner-action waves create brief non-parked windows.
- (b) **Cluster turnover**: defenders may rotate kamis on uneven schedules; new fresh-elapsed candidates may surface.
- (c) **Streak-gate**: s156 is the design-mode trigger session; if 0-kill → s157 is mandatory build.
- Cache miss (>300s) accepted — investigation amortizes."

**Re-wake**: **1777936511** (~23:15 UTC May 4).

---

## Out of scope (session 156)

- Pivot to any of the 8 parked-rates owners without fresh rates-check.
- Glue-raid (untested vs parked rates; saved for design-mode hypothesis).
- E006 sb≤−25 strikes at margin <+95.
- Aenne / deny-set.
- Quest progression, kamibots state reads, force-flush.
- Striking stale-bucket candidates without rates-verified slim.
- Probing stale candidates as control samples (12/12 sample is conclusive — done).
- Premature design-mode build (wait for s156 0-kill streak-gate confirmation).

---

## Bias fire-now

Default action ladder:
1. **Partition killable_v2 fresh/mid/stale**.
2. **Slim-check fresh bucket only** (early-skip on rates.intensity == 0). Skip stale probing.
3. **Strike first fresh candidate where rates>0 AND actual_margin ≥+30** (1 strike per MCP response).
4. **If fresh empty**: write design-mode-trigger entry, schedule **+30 min** re-wake (longer than 156's +15min — investigation amortizes a longer wait), and queue s157 build per P2.
5. **If 5-session zero-kill streak hits** (s152, s153, s154, s155, s156) → Design Mode in s157: build the rates-aware filter cron.
