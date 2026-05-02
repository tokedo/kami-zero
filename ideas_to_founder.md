# Ideas / asks to founder

> **This file is async and non-blocking.** kami-zero writes here when something
> would benefit from founder attention but never to gate kami-zero's action.
> Founder reviews periodically. If kami-zero needs to act and a
> `ideas_to_founder.md` item touches the action, kami-zero acts anyway with
> whatever workaround it judges best.

## Pending

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
