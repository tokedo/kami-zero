# Ideas / asks to founder

> kami-zero writes here when it wants something from the founder. Founder reads,
> answers inline (or in the next session prompt), and either resolves the entry
> or moves it to "Standing".

## Pending

### 1. Guild no-touch roster — DELIVERED 2026-05-01 (handles only; IDs to resolve)
- Founder shipped `predator/guild-no-touch.csv` with 82 GUILD-tier handles
  on 2026-05-01. account_id column is empty — kami-zero resolves
  handle → on-chain account/operator ID this session (P5b) and writes the
  resolved IDs back. Until resolved, the gate falls back to handle match.
- Founder will refresh the file from the Guild website every ~7 days.
  Coopes pinged about adding a kamibots roster endpoint to remove the
  manual step long-term.

### 2. Predator team transfer (BLOCKER for hunting)
- Need: founder transfers guardian kamis off bpeon and predator kamis onto bpeon.
- Why: current bpeon roster is guardian-tuned; we need real predators to test
  doctrine.
- Status: founder will signal when complete; kami-zero waits.

### 3. Oracle predator views — propose, do not build
- Useful: a `node_liquidation_activity` view (kills per node, last N days),
  a `recent_liquidation_events` view (raw events with attacker/defender/obol
  delta if visible). Would shorten target-finding queries.
- Status: kami-zero does NOT build oracle views; that's a kami-oracle session.
  Listed here so founder can route to the kami-oracle work.

## Standing
(none yet)

## Resolved
(none yet)
