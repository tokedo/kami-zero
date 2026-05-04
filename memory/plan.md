# Plan for session 123 — Items arsenal survey (Round 2 directive) + V≥22 emergence watch

## Priority 0 — Round 2 directive: items arsenal survey (founder injection)

**One-shot research task. Do this BEFORE strike attempts this session.** The world is V<22 dominant with no V≥22 above-floor candidates — a low-opportunity-cost window to build foundational knowledge.

**Deliverable**: a new file `predator/items-arsenal.md` enumerating every item in `catalogs/items.csv` that has combat or disruption utility for predator play. Structure each entry as:

| Item ID | Name | Type | Effect | Target / Scope | Ingredient cost | Inventory now |
|---|---|---|---|---|---|---|

Pay specific attention to:
- **Glue** (and any cooldown-extender items) — thrown from operator to a HARVESTING enemy kami, adds 180s cooldown. Founder transferred ingredients specifically to enable glue crafting.
- HP-damage items thrown at enemies (if any exist).
- Buff items applied to our own strikers (HP, cooldown reduction, attack boosts).
- Debuff items applied to enemies.
- Revive items beyond Red Ribbon Gummy / Melkarth Spell Card.
- Anything else with tactical applicability that is NOT pure-food (food is already covered).

**For each tactical item**, also note:
- Is it craftable? With which ingredients? (`catalogs/recipes.csv` if it exists, or grep `crafting` in catalogs.)
- Do we have ingredient supply to craft it? Check `bpeon` inventory.
- Is it currently in inventory? How many?

**End the doc with**:
1. A "Plays this enables" section — 2-4 sentences sketching tactical plays that become possible with these items in our vocabulary (e.g., "glue-then-strike on bodyguards" — but invent your own based on what you discover).
2. A "Missing items / asks" section — items that would be high-EV but aren't in inventory and aren't easily craftable. These propagate to `ideas_to_founder.md` as new asks (reference items-arsenal.md).

**Time budget**: this is a research session. 0 transactions, 0 gas. Aim for ~15 min of catalog reading + drafting. If the V<22 watch catches a striking opportunity mid-session, finish the arsenal doc first (it's quick) then strike.

**Ship test**: after writing items-arsenal.md, append a 1-line summary to `predator/learnings.md` linking to it ("YYYY-MM-DD — items arsenal v1 surveyed, N tactical items catalogued, see items-arsenal.md").

---

# Plan for session 123 (carry-over) — V≥22 emergence watch + watcher infra fix

## Context (post-session 122)

**0 kills, 0 gas, pure intel session.** World has been V<22 dominant for 4 consecutive sessions. Top candidates this scan: fluff (V11-V17, margins +67 to +79), orange (V10-V21, +72 to +79), yeddy (V11 +65 ripening). All BELOW the validated V<22 kill floor (margin ≥+95 from sessions 120/121). Aenne deny-all dominant at node 34. No V≥22 strain_boost=0 candidate in killable_v2.

Key takeaways:
- **Watcher `v_lv` is LEVEL not total_violence.** Session 122 plan misread V35 fluff as "V≥30 canonical territory" when actual total_violence is V11-V17. Always cross-check `kami_static.total_violence`, not the watcher field.
- **V<22 strain_boost=0 kill floor validated at margin ≥+95** (3 successful kills at +95/+107/+180 in sessions 120/121; 1 revert at +30 in session 118). Margin <+95 for V<22 = high revert risk.
- **fluff/orange proj_hp already saturated at 0** — these candidates cannot ripen further by projection. Margin is capped at watcher-reported kz value.
- Strikers + operator end at **room 50** (Ancient Forest Entrance). Cookies 434, obols 55, MUSU 529,612.

---

## Priority 1 — Wait for V≥22 strain_boost=0 emergence

The kill regime we have a calibrated formula for is V≥22 strain_boost=0 dormant candidates. World currently has ZERO such candidates with margin ≥+30. This is a temporary world-state condition that requires either:
- A new harvester wave (someone deploys a V≥22 cluster) — out of our control.
- An existing V≥22 farmer to ripen (none currently in killable_v2).

**Action at re-wake**: refresh `world_targets.json`, scan for any V≥22 cluster ≥2 candidates margin ≥+30 (canonical formula calibrated). Cross-check via `oracle_sql` on `kami_static.total_violence` for top 5 above-floor candidates before committing.

If found: standard travel + deploy + strike sequence per session 120 doctrine.

If not found: hold +30 min and re-scan. Every 4-6 hold cycles, consider whether the world has structurally shifted (V≥22 builds going extinct) and pivot doctrine to V<22 with stricter margin floor (≥+95).

---

## Priority 2 — V<22 fluff/orange opportunistic strike

If watcher refresh shows any fluff or orange candidate ripening ABOVE +95 margin (proj_hp must drop further OR new candidate enters with higher kz):
- Cross-check total_violence ≥10 (threshold for V<22 model — sub-V10 is deeply unvalidated).
- Verify owner still passive (zero actions in 60 min).
- Plan dry-run travel 50→target_node first.
- Travel cost ≤ 6M gas / ≤ 5 hops budget.
- Strike pairing — let `executor.hp_projection.kill_threshold` decide; do NOT trust watcher kz blindly (atk_s staleness still a risk).
- Single-strike per striker; chain-2 ONLY at margin ≥+95 for both targets in V<22 regime.

---

## Priority 3 — Build: total_violence annotation in world_targets.json

If session 123 has no strike opportunity AND remaining build-mode budget warrants:
- Add `v_total_violence` and `v_strain_boost` fields to each `killable_v2` row in the watcher output.
- Source: `kami_static.total_violence` and `kami_static.strain_boost` joined on victim kami_index.
- Why: prevents the session-122 mistake of mistaking watcher `v_lv` (level) for violence. Current cost is 1-2 oracle queries per session to re-check.
- Files: `predator/watcher.py` or wherever `world_targets.json` is generated. Document in `predator/infrastructure.md` and `memory/improvements.md`.
- Don't over-build — keep change small (annotate, don't refactor scoring).

---

## Hard limits (unchanged)

- **Gas budget session 123**: 25M (cluster strike + travel). Higher only if a 4+ candidate V≥22 cluster materializes.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`strain_boost ≤ -25` sustain-builds** off-limits (4931 yeddy, 11207 vuongdung1198, 14233 vuongdung1198, 8040 KAMI) until model validated for that profile.
- Pre-deploy oracle re-check mandatory.
- 2-revert-stop rule.
- Rule #4 inviolable: cluster math justifies cross-region.
- Chain-2 only at margin ≥+25 for V≥22, ≥+95 for V<22.
- **Live `kill_threshold` recompute mandatory** (atk_s staleness in oracle).
- **`v_lv` in watcher = LEVEL not VIOLENCE.** Always cross-check `total_violence` via oracle before strike commitment.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+35 min** (~01:37 UTC May 4, ts 1777858200). Pinned to: (a) Watcher 10-min refresh cycle × 3 for any V≥22 strain_boost=0 emergence — current world is V<22 dominant 4 sessions running, need a new harvester wave to surface a calibrated-formula candidate. (b) yeddy 8804 V11 ripening (currently +65 proj_hp=76; could drop to +110 by re-wake — but V<22 model risk holds and node 53 is deep travel, so only fire if a V≥22 cluster also materializes elsewhere). (c) Strikers RESTING at room 50, full sync regen during 35-min RESTING. **NOT** pinned to V<22 fluff/orange ripening — those proj_hp already saturated at 0, won't move."

**Re-wake**: +35 min from session end (~01:37 UTC May 4, ts **1777858200**).

---

## Out of scope (session 123)

- V<22 strikes at margin <+95 (session 118/120/121 doctrine).
- Aenne / 3333333333333333 / foden / dias / rtvvvvv / stefan97 — DENY-ALL (P3 disruption-raid exception only).
- `strain_boost ≤ -25` sustain-builds.
- Cross-region travel for a single target (rule #4).
- Modifying canonical kill_threshold formula (calibrated 6/6 for V≥30).
- Quest progression, kamibots state reads, force-flush.
