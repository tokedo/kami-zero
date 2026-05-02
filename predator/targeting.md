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
