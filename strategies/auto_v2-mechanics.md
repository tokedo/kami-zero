# auto_v2 Strategy Mechanics

> CANONICAL: how Kamibots' `auto_v2` strategy actually drives the harvest cycle.
> Read this BEFORE planning around auto_v2 timing or tuning its parameters.
>
> Source: founder explanation 2026-04-28, correcting a misconception recorded
> in sessions 57-59 of `memory/decisions.md`.

## Summary

**`auto_v2`'s harvest cycle is HP-driven, not threshold-driven.** The flush of
MUSU (and the 1:1 scavenge-point credit that comes with it) is triggered by
auto_v2 calling `stop_harvest` when a kami's HP drops into the configured
"dangerous zone" — NOT by `bountyCollectThreshold` firing.

`bountyCollectThreshold` at the standard value of `10000` is **effectively dead
code** under normal conditions. Treat it as inert.

## The Cycle

Per kami, the loop auto_v2 actually runs:

1. **Wait for HP.** auto_v2 will not call `harvest_start` until kami HP is at
   or above the `safety` margin off full (default 5% → start when HP ≥ ~95%).
2. **Start harvest.** `harvest_start` fires at the configured node.
3. **Accumulate untouched.** Kami harvests passively. MUSU/hr (intensity)
   *ramps up* the longer the kami is left untouched. **Intensity is the prize.**
4. **HP drains** at a rate driven by node predator density (and the kami's
   Harmony stat — see [systems/harvesting.md](../systems/harvesting.md)).
5. **Health-driven stop.** When HP enters the configured "danger zone" (also
   default 5%), auto_v2 fires `stop_harvest`.
6. **Auto-collect on stop.** `stop_harvest` *atomically* collects all
   accumulated MUSU AND credits the scavenge bar 1:1. No separate
   `harvest_collect` call is involved.
7. **Rest and regen.** Kami enters RESTING. HP regens.
8. **Loop.** Once HP ≥ ~95% again, auto_v2 calls `harvest_start` again.

## Why `bountyCollectThreshold` is Inert

The parameter exists in the API and accepts numeric values, but at typical
configurations it never fires:

- A kami can't realistically accumulate 10,000 MUSU before its HP forces a
  rest at any reasonable predator-density node.
- Health-driven stop reliably fires first.

**Empirical evidence** (session 59, 2026-04-28): at node 77 post-migration,
the first auto_v2 cycle delivered MUSU delta = +18,024 and scav delta =
+18,024 (exact 1:1). Distributed across multiple kamis cycling through stops
over the same window — not one kami crossing a 10k threshold.

## Why Lowering the Threshold is an Anti-Pattern

Tempting reaction: "set `bountyCollectThreshold: 500` to flush faster."
**Don't.** Here's why:

- An explicit `harvest_collect` call **counts as an action on the kami**.
- Any action **resets the kami's intensity accumulation** to baseline.
- Intensity is the source of MUSU/hr — it grows the longer the kami is left
  untouched. Resetting it via forced collects sabotages long-run yield.
- Health-driven `stop_harvest` is the only desirable collect trigger because
  it happens at the natural end of an intensity-pumped cycle.

In short: explicit collects steal yield from your own future cycles to give
you slightly faster scav-credit *now*. Bad trade.

## Parameter Recommendations

| Parameter | Recommended | Rationale |
|---|---|---|
| `bountyCollectThreshold` | `10000` | High no-op value. Don't tune. |
| `safety` (HP margin to start) | `5` (5%) | Default. Keeps yields healthy without leaving HP-headroom on the table. No strong reason to deviate. |
| dangerous-zone (HP margin to stop) | `5` (5%) | Configurable in `start_strategy`. 5% gives the kami room to recover without flirting with liquidation. |

## What Determines First-Cycle Timing After Migration

When auto_v2 is launched fresh at a new node (or migrated from one node to
another), the time to the **first** scav-point flush is dominated by:

1. **HP regen of post-migration kamis** — kamis that came off the prior grind
   below full HP can't start at the new node until they regen back to ≥95%.
   This was a major contributor to the 18.75h first-flush at node 77 in
   session 59 (see decisions.md correction).
2. **Intensity ramp** — fresh-intensity MUSU/hr is low; it grows over time.
3. **Time-to-health-danger** — once harvesting, the kami still needs to drain
   HP into the danger zone before stop fires.

**Budget**: 18-24h end-to-end for the first flush after a migration. Subsequent
cycles are much faster because intensity stays warm across the rest/harvest
loop (only resets on actions outside the loop).

## What This Replaces

The model recorded in `memory/decisions.md` sessions 57-59 framed
`bountyCollectThreshold: 10000` as "the bottleneck" and "the trigger for the
collect tx that flushes scav points." That framing is **wrong** in two ways:

- The threshold doesn't trigger the collect under normal conditions
  (health-driven stop does).
- Lowering it would not speed up flushes in any useful sense; it would damage
  yield by forcing intensity resets.

The session-60 insight ("post-migration HP regen is the rate-limiter") is
**correct** and is the right mental model going forward.

## Related Reading

- [systems/harvesting.md](../systems/harvesting.md) — chain-side harvest
  mechanics: strain, HP drain, liquidation, collect side-effects.
- [integration/kamibots/README.md](../integration/kamibots/README.md) —
  Kamibots API reference (where the `auto_v2` strategy is launched and the
  parameters are passed).
- [memory/decisions.md](../memory/decisions.md) sessions 57-60 — the
  correction trail that produced this doc.
