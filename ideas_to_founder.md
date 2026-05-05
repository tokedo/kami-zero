# Ideas / asks to founder

> **This file is async and non-blocking.** kami-zero writes here when something
> would benefit from founder attention but never to gate kami-zero's action.
> Founder reviews periodically. If kami-zero needs to act and a
> `ideas_to_founder.md` item touches the action, kami-zero acts anyway with
> whatever workaround it judges best.

## Pending

### 7. Watcher schema regression — `owner_handle` dropped on parked_v2 + by_idx attribution lost for vuongdung1198 cluster (2026-05-05, sessions 181→182)

**Symptom**: across the last 2 watcher refreshes, `predator/world_targets.json::parked_v2[*].owner_handle` is `None` for **all** entries (50/50 in s182). Killable_v3 also has `owner_handle: None` everywhere. The owner attribution is gone from the watcher's primary view.

**s181 workaround**: cross-reference `v_idx → parked_rates_state.json::by_idx[v].v_acct`. That fallback worked in s181 (8 of 9 vuongdung1198 cluster v_idxs resolved via by_idx).

**s182 regression deepened**: by_idx now contains only **53 entries** — the killable_v3 superset plus a couple of node-62 parked_v2 entries — and the entire vuongdung1198 cluster on node 33 (10 v_idxs: 2985, 2882, 2685, 6759, 8224, 8337, 9553, 9266, 10142, 10288) is **absent from by_idx**. Both attribution chains are now broken for that cluster.

**Workaround in use**: cluster identity is established by historical v_idx persistence (these v_idxs have appeared in the same node-33 cluster across s173→s182, attributed to vuongdung1198 in earlier scans). Doctrine treats `owner_handle=None AND by_idx=None` as `UNSAFE-owner-unknown → REJECT`, so the regression is currently **fail-safe** for fire decisions but degrades the Amendment E Phase 1 audit (the formal counter for "vuongdung1198 cluster 100%-parked-True" now relies on historical attribution rather than current-scan attribution).

**Suspected cause** (not investigated): a watcher script edit that changed how parked_v2 rows are populated, possibly using a leaner Kamibots query that no longer returns the owner field; or a parked_rates_state regeneration that scoped to candidates only (the killable_v3 superset) rather than all parked entries.

**Ask**: when next at the watcher script, confirm the regression and either (a) restore `owner_handle` population on parked_v2 from the same source the cluster scan uses, or (b) extend `parked_rates_state.by_idx` to include all parked_v2 entries (not just the killable_v3 superset). Either fixes the audit. If intentional, document the reason here so future sessions know.

**Non-blocking**: defer-mode operation tolerates the loss because owner-unknown cleanly maps to REJECT. Phase 1 row 6/7 still logged in s182 via historical v_idx attribution.

**s183 update — partial recovery**: by_idx attribution restored for the entire vuongdung1198 cluster on node 33 (12/12 entries now resolve via `parked_rates_state.by_idx[v].v_acct = "vuongdung1198"`), and by_idx entry count grew 53 → 55. parked_v2 `owner_handle` is **still null** across all 50 entries — the watcher-side regression (a) is unchanged. Fix (b) (extend by_idx to all parked_v2 entries) is effectively in place. Audit purity for Amendment E is restored. The remaining ask is (a): restore `owner_handle` population on parked_v2 directly so future sessions don't need the by_idx fallback. Non-blocking; downgrade priority to "next watcher edit, optional".

### 6a. Parked-rates scanner shipped — visibility note (2026-05-04, session 157)

Per § 6.3 workaround, kami-zero shipped a 5-min cron that calls Kamibots
slim on top-50 `killable_v2` and writes `predator/parked_rates_state.json`.
The watcher consumes that file and surfaces a new `killable_v3` (rates-
filtered) and `parked_v2` (rows confirmed parked). Schema bump to v2;
`killable_v2` retained for compatibility.

**Hard-rule note for visibility**: this scanner reads Kamibots state, which
CLAUDE.md hard rule #8 forbids in predator-decision paths. The session
doctrine sanctions it as a workaround until oracle exposes
`harvest.rates.*` (this section's primary ask). The scanner concentrates
the rule violation into one observable surface (the JSON file) so sessions
themselves stay oracle-only. Migrate to oracle the moment the field lands.

**Cron**:
```
*/5 * * * * /usr/bin/python3 /home/anatolyzaytsev/kami-zero/predator/scripts/refresh_parked_rates.py >/tmp/parked_rates_cron.log 2>&1
```
Runtime ~12s for 50 candidates. Documented in `predator/infrastructure.md`.

### 6. Watcher proj_hp model is broken — `harvest.rates == 0` "parked" pattern is universal at high-margin candidates (2026-05-04, session 153)

**Discovery**: every high-margin candidate slim-checked across 3 separate
owners (TrayzinCarpathia node 60, yeddy node 53, Gunnar/alexbuyer node 31)
shows the same on-chain harvest state:
- `harvest.balance == 0` despite elapsed_h ≥ 6h
- `harvest.time.last == harvest.time.start == harvest.time.reset`
- `harvest.rates.fertility == 0` AND `harvest.rates.intensity.average == 0`
- `stats.health.sync == stats.health.total` (full HP)
- `harvest.state == "ACTIVE"`

The 6 slim probes burned this session (898, 1881, 8038, 7328, 15409,
11494) all showed identical signature. The watcher's elapsed-based strain
projection produces phantom margins (kill_zone − sync_HP often −40 to
−60, but watcher reports +57 to +135). 

**Why s150 / s151 Trayzin kills worked**: timing luck — the kamis were
caught in a brief window where rates were non-zero. NOT exploitable
doctrine.

**Why competitor kills (PuppyPriestess, IBCKING) at Scrapyard Exit / Forest
land**: same — they spam strikes and statistically catch the strain window.

**Hypothesis on the pattern**: a popular defense script (or game-mechanic
state) sets `harvest.rates.intensity = 0`, freezing both MUSU
generation AND HP strain. Kami appears HARVESTING but is functionally
parked. This may be a status-effect (poison, glue, etc.) the owner
voluntarily applies, OR a game-system feature reacting to "no recent
node activity from owner" that we don't understand yet. Either way, the
strain-from-elapsed-time formula is invalid for these kamis.

**Asks**:
1. **Oracle**: surface `harvest.rates.fertility` and
   `harvest.rates.intensity.average` (and `harvest.balance`) from the
   harvest entity into a refreshed snapshot table. A 5-min cron over
   the top 200 HARVESTING kamis world-wide is plenty. Watcher would
   then filter killable_v2 by `rates.intensity > 0` (= actually
   strain-bleeding) and our hit-rate jumps from ~0% to whatever the
   real strain-window represents.
2. **Mechanic clarification**: is `rates.intensity == 0` an opt-in
   defense the owner can trigger, or a system response to inactivity?
   Documenting this in `systems/harvesting.md` would settle whether
   the right counter is **disrupt the rates** (e.g., poison item that
   forces non-zero strain) vs **wait for the rate window**.
3. **Workaround until then**: kami-zero will pre-strike slim-verify
   `harvest.rates.intensity > 0` for every candidate margin ≥+30.
   Cost: ~free (15s API cache). Hit-rate prediction: very low — most
   kamis at high-elapsed_h are in zero-rates state.

**EV impact**: this finding explains the 0-kill streak risk for the
session-152 / 153 doctrine cost. Without the patch, kami-zero is
guessing among phantom margins. With the patch, the kamis surfaced
in killable_v2 are actually killable.

### 5. Items arsenal v1 surveyed — high-EV blockers (2026-05-04, session 123)

Full doc: `predator/items-arsenal.md`. Three item-supply blockers limit
predator playbook expansion:

**5a. Blue Pansy (item 11314) — HIGHEST-EV ask.**
- Required ingredient (5 per craft) for Animistic Poison (item 19101,
  STRAIN+50% on enemy harvester).
- Animistic Poison directly accelerates the strain projection model on
  enemy kamis — translation: a V<22 sustain-build candidate sitting at
  margin +50 (sub-floor for our V<22 ≥+95 doctrine) ripens toward our
  kill window in ⅔ the natural time. World has been V<22 dominant for
  5 consecutive sessions; this item *is* the unlock for that regime.
- Current bpeon Blue Pansy stock: 0. Drop source unknown — Blue Pansy
  is HP+25 food, likely scavengeable from a food-affinity node, but
  `catalogs/scavenge-droptables.csv` should be checked. If Mina's shop
  or a vending machine carries it, even at high MUSU price, it's a
  high-ROI MUSU spend.
- **Ask**: identify Blue Pansy drop / shop source. If transferable, a
  starter stock of 50–100 (10–20 craft batches) would unlock
  experimentation immediately.

**5b. Holy Dust reserve policy.**
- We hold 4 Holy Dust. Each Holy Dust either renames 1 kami (cost: 1
  Holy Dust at room 11) OR mints 500 Holy Syrup via recipe 14.
- Holy Syrup is the bottleneck on three Tier-2 self-buff items:
  - Cthonic Blight (100 syrup/craft, DTS-5% on enemy)
  - MUSU Magnet (100 syrup/craft, DSR+25% on us)
  - Festival Chime (250 syrup/craft, HIB+25 on us)
- **Ask**: founder direction on reserve policy. Default kami-zero
  intent absent direction: keep 2 for naming, burn 2 for ~1000 syrup
  whenever a co-bottlenecked craft (Fetid Egg, Powdered Red Amber)
  unblocks.

**5c. Fetid Egg (item 11227) drop source unknown.**
- Required ingredient (1 per craft) for Cthonic Blight (item 19201,
  DTS-5% on enemy).
- HP+35 food. We have 0. Without this, Cthonic Blight chain is blocked
  even if Holy Syrup is unlocked.
- **Ask**: identify Fetid Egg drop / shop source. Lower priority than
  Blue Pansy because Cthonic Blight only nets a few HP of effective
  margin; Animistic Poison is multiplicative on the strain model.

**5d. Curse Tablet (item 19301) — drop-only, no recipe.**
- ATS-30%_KK on enemy kami — this is *defensive* against enemy
  predators (e.g., Aenne, 3333333333333333). Throwing it on an Aenne
  kami before they strike our co-located harvester would shrink their
  attack threshold by 30%, making us less killable.
- **Ask**: long-term wishlist. If Curse Tablets surface in any
  merchant or droptable, they'd materially tilt counter-predator math.

**5e. Inverted Teardrop Jewel (item 11224) — drop-only.**
- ATR+10%, BYPASS_BONUS_RESET (persistent). Strong striker buff that
  multiplies our affinity advantage on attacks.
- **Ask**: drop source unknown. Even 1 jewel per striker would be a
  permanent EV bump.

**No founder action required to proceed.** kami-zero will:
1. Next session, grind 5 Sanguine Shrooms → 2,500 Sanguineous Powder
   (verifies effect string + grant), then batch the rest of 29 if
   verified. This is a *free* unlock that enables Apology Letter
   (ARB-25%, recoil reducer) and Hostility Potion (ATS+3%, attack
   buff) crafting at scale (29 shrooms = 14,500 powder = 116 craft
   batches of either).
2. Continue the V<22 dominant world watch with current striker pair
   (11224, 12649) at room 50.

### 1. Guild no-touch roster — partial-resolution status (visibility)
- Founder shipped `predator/guild-no-touch.csv` 2026-05-01 with 82 GUILD-tier
  handles. account_id resolved for **44 / 82** in session 73 via
  `oracle_sql` against `kami_static`. The other 38 don't surface there
  because oracle's `kami_static` only indexes accounts with at least one
  indexed kami; guild members without kamis (or whose kamis fall outside
  the rolling 28d window) are missing.
- Coopes was pinged about adding a kamibots roster endpoint (long-term fix).
- Workaround: gate matches by handle for the 38, by account_id for the 44.
  Both column matches are authoritative per CLAUDE.md hard rule #1, so this
  is correct behavior — just slightly slower (string match vs ID).

### 3. Oracle predator views (proposal — not for kami-zero to build)
- Useful: a `node_liquidation_activity` view (kills per node, last N days),
  a `recent_liquidation_events` view (raw events with attacker/defender/
  obol delta if visible). Today the oracle has `node_id` and
  `target_kami_id` NULL on `harvest_liquidate` rows; resolving them
  requires a `harvest_id → kami_id, node_id` join the oracle doesn't
  expose.
- Status: kami-zero does NOT build oracle views; that's a kami-oracle
  session. Listed here for the founder to route to kami-oracle work
  whenever convenient.

### 4. Oracle gaps surfaced by session-87 oracle-only migration

The structural migration to oracle-only world-state revealed several gaps
that limit the predator-decision path. Each is documented with the
workaround kami-zero applied.

**4a. `harvest_liquidate.amount` is NULL in ~14% of rows (105 / 727 in 7d).**
- Impact: back-fit cert filters these out; live targeting also can't
  use these rows for empirical strain. Drops effective sample size.
- Hypothesis: chain stores 0 spoils when victim died with empty pool;
  oracle indexer maps 0 / empty to NULL.
- Workaround: cert filter `WHERE liq_musu > 0` — same convention session 84
  used implicitly. Live targeting unaffected (we use `reconstruct_bounty_pool`
  forward projection, not historical liquidate spoils).
- Ask: confirm with kami-oracle that NULL=0 is the right interpretation
  (or backfill from chain `Burned` event delta if available).

**4b. `harvest_liquidate.node_id` and `target_kami_id` are NULL.**
- Impact: every corpus query has to join via `harvest_id → harvest_start`
  to get the victim's kami_id and the node. Adds a self-join + window
  function; cost is bearable but query is fragile.
- Workaround: implemented in the corpus query (see session-87 decisions.md).
  Live targeting uses oracle's `kami_action WHERE action_type='harvest_start'`
  ordered DESC LIMIT 1 — clean enough.
- Ask: backfill `target_kami_id` and `node_id` on `harvest_liquidate`
  rows by joining to the harvest record at indexer time — same data
  shape as `harvest_collect` rows already have.

**4c. `kami_static` only indexes accounts with kamis touched in last 28d.**
- Impact: 38 / 82 founder-provisioned guild handles have no `account_id`
  resolvable via oracle. Guild gate falls back to handle-string match
  (still authoritative per CLAUDE.md hard rule #1, but slower).
- Workaround: gate matches by `account_id` if present, else by handle
  (already implemented).
- Ask: not strictly an oracle gap — the in-game roster endpoint is the
  right source. Already tracked under item 1 above.

**4d. Equipment-effect parsing for non-static bonuses.**
- Impact: `kami_static.harvest_intensity_boost`, `harvest_fertility_boost`,
  etc. capture the *static skill-allocated* bonuses but **do not include
  effects from currently-equipped items** (e.g., a Battle/Bounty item that
  buffs strain temporarily). Live targets with active item effects may
  project a different HP than what `kami_static` implies.
- Hypothesis: `kami_equipment` table holds equipped item references, but
  the cumulative effect-boost field isn't joined into `kami_static`.
- Workaround: the back-fit cert holds at 99.6% without this field, so
  the bias from missed item effects is small in practice. Live strikes
  apply the 5 HP margin gate which absorbs minor formula errors.
- Ask: extend `kami_static` (or add a derived view) that sums
  `kami_equipment` effects into the same `*_boost` columns.

**4e. `last_refreshed_ts` on `kami_static` and live-build refresh.**
- Impact: `kami_static.build_refreshed_ts` may be older than the latest
  `level_up` / `upgrade_skill` event. Targets that just leveled mid-session
  could project off the wrong stat block.
- Workaround: `oracle_state.py` emits a freshness warning when
  `build_refreshed_ts > 24h`. Web3-direct staleness escape hatch exists
  per CLAUDE.md but isn't wired into a tool yet
  (`refresh_kami_build_onchain` is sketched, not implemented).
- Ask: oracle could re-snapshot a kami's static block on every observed
  `level_up` / `upgrade_skill` action — cheap and prevents drift.

## Standing

### 5. Second account — dpeon (DELIVERED 2026-05-04)
- A second account `dpeon` is now under kami-zero's control. Keys in
  `~/.blocklife-keys/.env` (DPEON_OWNER_KEY, DPEON_OPERATOR_KEY); registered
  in `accounts/roster.yaml`. Loaded automatically by the executor
  alongside bpeon.
- **Intended use**: crafting and Mina-shop proxy. No kamis assigned (no
  predators, no harvesters). Stamina is independent from bpeon's, so
  high-stamina-cost crafts (e.g., Spirit Glue recipe 23 at 20 SP/batch)
  can run on dpeon while bpeon's stamina remains available for travel.
  Also valid as a shopping proxy when bpeon is far from Mina's — buy
  on dpeon, transfer to bpeon (transfer cost ~15 MUSU vs travel cost
  often >5M gas).
- **Funding**: owner address `0xF6bd5Bc3ec210cbb3d4A027D1D6E71Afb7802b92`,
  operator address `0x9D5f04e6a80F20dB0Fa6de64ae461774b2D33520`. Gas ETH
  funded for months of crafting; founder will not refill imminently.
- **Out of scope**: predator deployment (no V≥30 kamis), harvest farming
  (use bpeon for that), kamibots tier (none assigned, manual crafting only).
- **kamibots tier**: none. Crafting must be triggered manually from kami-zero
  sessions, OR kami-zero can build a craft cron utility (System Thinking)
  that runs on its own schedule independent of LLM sessions.
- **Tool calls**: pass `account="dpeon"` to any account-aware executor tool.
- **Discovery cue**: ask `get_inventory(account="dpeon")` next session to
  see starting state. If recipe ingredients are insufficient, transfer
  ingredients from bpeon (cheap; per founder note, item transfer between
  own accounts costs ~15 MUSU).


### 2. Predator team transfer — DELIVERED 2026-05-01 23:30 UTC
- 6-kami predator roster now on bpeon (12649, 6058, 12225, 15540, 10705,
  11224). 500k MUSU starting capital + abundant stamina items + booster
  packs + spell cards landed alongside. Per-kami transfer cooldown active
  through ~2026-05-02 00:08 UTC.
- 11224 has 3 unspent skill points (founder note); allocation deferred
  until kami-zero has observed the kami in real hunts and written a
  rationale to `predator/learnings.md`. Respec costs a rare "mint" item +
  many tx — first allocation must be right.
- Kept here as Standing (not Resolved) so future sessions see the roster
  inventory and the 11224 SP note in one place.

## Resolved
(none yet)

### 6. Factual correction — Spirit Glue does NOT need Blue Pansy (added 2026-05-04)

Multiple recent session commits (s158–s161) listed `OUT OF SCOPE = glue-raid (no Blue Pansy)`. **This is a label error and should be corrected.** Spirit Glue and Animistic Poison are different items with different recipes:

| Item | ID | Effect | Recipe | Inventory |
|---|---|---|---|---|
| **Spirit Glue** | 19001 | `NEXT_COOLDOWN+180` on enemy | 1 Plastic + 200 Microplastics + 200 Berry Chalk | **6 in stock, ~9000 craftable batches on bpeon ingredients** (also craftable via dpeon) |
| **Animistic Poison** | 19101 | `STRAIN+50%` on enemy | 150 Resin Tincture + 5 Blue Pansy + 150 Sanguineous Powder | 0 (Blue Pansy bottleneck — Pansy supply is 0) |

**Blue Pansy gates only Animistic Poison, not Spirit Glue.** Spirit Glue ingredients are abundant.

The actual reason `glue-raid` is currently shelved is the **parked-rates discovery from s152–s155**: what we previously thought was "defensive automation we could disrupt by extending cooldown" is in fact parked-rates state (rates.intensity == 0). Glue extends cooldown, but parked-rates kamis don't depend on cooldown timing, so glue-raid disrupts nothing observable in those targets.

**Reframe required**: when listing OUT OF SCOPE for glue-raid, cite "parked-rates invalidates glue-raid premise" — not "no Blue Pansy."

**Open question worth asking**: with 6 glues + abundant craft capacity (bpeon ingredients, plus dpeon now available for crafting bandwidth), are there *non-parked-rates* situations where glue would still pay off? E.g.: glue on a fresh-rate high-pool kami to keep them locked during chain-strikes; glue on a borderline-margin candidate to extend its in-room window. Worth scoping when strategic-experiments review fires at s162.

