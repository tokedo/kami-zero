# Predator playstyle — kami-zero local knowledge base

This directory is kami-zero's running notebook for the predator chapter. Every
session, read it; every session worth its tx, write to it. It is local-only
(no GDD/context push yet — that promotion happens once the chapter has matured).

## Files

- `README.md` (this) — index + first-principles overview
- `mechanics.md` — what we know about how liquidation actually works on-chain
  (formulas, thresholds, edge cases). Start empty; fill in as you learn from
  oracle queries, on-chain experiments, and GDD reading.
- `targeting.md` — heuristics for finding good targets (node activity patterns,
  account inactivity, kami HP/level distributions worth hunting, cluster
  signals). Start with hypotheses, mark each "verified" or "falsified" as
  evidence accumulates.
- `counter-predator.md` — observed predators on the field, their patterns,
  mutual-kill cases we've hit, who to avoid, who we can counter-counter.
- `learnings.md` — chronological per-session lessons. Append-only.
- `metrics.md` — the diagnostic table. Append one row per session.
- `guild-no-touch.csv` — guild member account IDs (founder-provided). Format:
  `account_id,handle,note`. Treat as load-bearing — the no-liquidate gate
  reads this.

## First principles (placeholder — flesh out as you learn)

- Liquidation thresholds, obol formulas, attack-type matchups: figure these out
  from kamigotchi-context, GDD, and oracle data on past liquidations. The
  founder explicitly wants kami-zero to derive this rather than be spoon-fed.
- Don't ship doctrine until it's verified against on-chain reality.
