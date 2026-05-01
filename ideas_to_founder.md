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
