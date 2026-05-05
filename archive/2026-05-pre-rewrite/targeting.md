# Targeting heuristics

(Hypotheses to test — mark verified/falsified over time.)

- H1 [unverified]: nodes with >5 kamis present have higher target density
  than 1–2 kami nodes. Test via oracle node activity.
- H2 [unverified]: kamis owned by accounts with no recent moves (>24h?) are
  "starving farmers" and likely under-defended.
- H3 [unverified]: kamis at HP ≤ X% of max are liquidatable; the X depends
  on attacker stats. Derive from on-chain history.
- H4 [unverified]: certain attack types (per kami body / hand affinity) yield
  more obol against certain target archetypes. Test with population data
  once we have predators on bpeon.
- H5 [partial-falsified, session 78]: EERIE hand vs SCRAP body affinity
  bonus is large enough (≥ +0.10 to threshold_ratio) to compensate for
  Guardian-tier 0.10 def_shift on H20 prey. **Result**: no — strike
  reverted at HP 194/200 (0.97). Affinity contribution ≤ 0.07. Tactical
  takeaway in `mechanics.md` § "Affinity bonus — provisional null finding".

## Cross-node target distribution (session 78 oracle scan)

Snapshot of active harvesters (last 24h) with **soft defense**
(def_threshold_shift ≤ 50, i.e. ≤ 0.05 normalized) by node and prey body
affinity. Useful as **cluster scan input** when planning cross-region moves.

| node | active harvesters | zero_def | soft (≤50) | SCRAP soft | INSECT soft | EERIE soft |
|------|-------------------|----------|------------|------------|-------------|------------|
| 25   | 68                | 49       | 49         | 0          | 0           | **49**     |
| 86   | 2380              | 28       | 35         | 15         | 12          | 1          |
| 62   | 67                | 18       | 20         | 0          | 11          | 2          |
| 88   | 244               | 11       | 15         | **10**     | 1           | 0          |
| 73   | 486               | 10       | 12         | 5          | 2           | 3          |
| 76   | 156               | 7        | 8          | 4          | 3           | 1          |
| 60   | 173               | 6        | 7          | 5          | 0           | 0          |
| 65   | 9                 | 4        | 4          | 0          | 0           | 4          |

(active_harvesters double-counts kamis that started in a batch; treat
as relative-density indicator, not exact count.)

**Implications by attacker hand affinity**:

- **INSECT hand (10705)** → wants EERIE body. **Node 25 is the
  obvious win**: 49 zero-def EERIE-body soft targets. 7× the
  count of node 86's affinity matchup for any of our hands.
- **EERIE hand (11224)** → wants SCRAP body. Node 88 has 10
  SCRAP-soft targets vs node 86's 15 (mostly guild-protected).
  Node 88 may have higher non-guild fraction.
- **SCRAP hand (6058)** → wants INSECT body. Node 62 has 11
  INSECT-soft targets, the densest after node 86 (12 INSECT-soft
  but most guild-protected).

**Caveat**: must guild-filter every cluster before committing to a
move. Many node 86 candidates were guild-blocked at the gate
(topobadger, erere, 23savage, Tonin, Shadow3X). Repeat the
non-guild filter via oracle for any candidate node before travel.

## Soft-target filter v2 (session 79)

The session 78 filter `defense_threshold_shift ≤ 50` is incomplete: it
ignored the multiplicative `defense_threshold_ratio` field, which Guardian
tier-2+ builds activate via skills 323 (Armor) and 341. Targets with
def_shift = 0 can still have def_ratio = 0.25–0.50, putting kill_zone
50–55% below max even before strain wait.

**Required filter** (use both columns):

```sql
WHERE s.defense_threshold_shift = 0
  AND s.defense_threshold_ratio = 0
```

A truly-soft cluster has BOTH = 0. Always live-spot-check 1–2 candidates
via `get_kami_state_slim` before committing to a move — oracle's
`build_refreshed_ts` can lag by 24h and miss recent skill allocation
(see `mechanics.md` § "Oracle build-snapshot staleness").

## Cluster intel — session 79 oracle scan + live spot-check

Refined scan (`def_shift = 0 AND def_ratio = 0`, `account_name != 'bpeon'`,
last action = harvest_start within 24h, guild-filtered):

| node | non-guild softs | breakdown | hand-affinity match |
|------|----------------|-----------|---------------------|
| 60 | 7 | 6× wiuuuu SCRAP, 1× pranshu.init SCRAP, 1× TrayzinCarpathia NORMAL | 11224 (EERIE-hand → SCRAP) |
| 62 | 8 | 8× buja723 INSECT (V10–17, H21–25, HP110–160) | 6058 (SCRAP-hand → INSECT) |
| 73 | ?? | POWELL+Yeahta — **STALE oracle, live shows Guardian-built**; do NOT trust | — |
| 35 | 0 | wassa + 0xasimov, both guild | — |
| 88 | 0 | KCS + dmi, both guild | — |
| 86 | mostly guild | erere/pleaseonemoretim/etc | — |

**Live confirmations**:

- `757` (buja723, RESTING at scan time): skills `[311×5,313×5,322×5,
  331×1,411×5,413×5,422×5,431×1,421×2]` — no 323, no 341 →
  def_ratio = 0 ✓. Stats V14/H23/HP110/sync 83 (RESTING).
  Predicted kill_zone for 11224 V36 atk_shift 0.28: 0.953 × 110 = 105.
  At sync 83 → IN kill zone (when HARVESTING).
- `1451` (wiuuuu, HARVESTING node 60): skills
  `[411×5,311×5,413×5,212×5,422×5,412×5,431×1,421×1]` — no 323, no
  341 → def_ratio = 0 ✓. Stats V14/H24/HP180/sync 180. Predicted
  kill_zone 0.937 × 180 = 169 — full HP target sits 11 above kill zone,
  needs ~6% strain decay (~3h).
- `9545–17250` (POWELL, multiple): live shows full Guardian tier-2
  (26 SP in 311/312/321/322/323/331), def_ratio 0.25. Oracle was
  19h stale — false positive. Do NOT travel for this cluster.

**Best targets per striker**:

- **6058** (SCRAP-hand, V32 oracle, NORMAL body) → node 62 buja723.
  8 INSECT-soft, low-V (10–17), low-H affinity-friendly. Strongest
  numerical case across our roster.
- **11224** (EERIE-hand, V36 H11) → node 60 wiuuuu (6× SCRAP-soft).
  Mid-HP targets need ~3h strain wait at full HP, but striker is the
  highest-V we have. Two-trip option: bring 11224 to node 60 + restart,
  wait 3–4h, strike.
- **NORMAL hands** (12225, 15540) — universal-neutral, use as second-line
  on whichever cluster the affinity-tipped striker cracks first.

**Travel cost** (from node 86, the current room):

| target | hops | stamina | items needed | est. gas |
|--------|-----:|--------:|--------------|---------:|
| 60 | 25 | 125 | 3× Ice Cream | ~25M |
| 62 | 26 | 130 | 4× Ice Cream | ~26M |

**Cluster math**: a 25–26-hop move costs ~25M gas. Amortization
requires ≥3–4 successful kills (at 7.5M kill cost) + obol/spoils
yield to break even on the round trip. Both 60 and 62 plausibly
support that, but **must verify counter-predator scan and live
strain on the 8 buja723 / 7 wiuuuu kamis right before the move** —
not pre-commit. Doctrine: data-then-move, never the reverse.

## Owner stop-rule: rtvvvvv — REMOVED 2026-05-04 (R3 lobotomy)

Prior rule blacklisted rtvvvvv unconditionally based on 3 reverts at high HP across sessions 76/78/80. **Removed**: never re-tested at low HP, no first-principles basis (rtvvvvv farms are SCRAP-sustain builds, killable per canonical formula at sufficient strain). Re-evaluate per target via canonical `kill_threshold(...)` and live HP projection. If empirical re-validation shows a real pattern, log to `predator/strategic-experiments.md` as a hypothesis with N≥20 observations bar before re-codifying.

