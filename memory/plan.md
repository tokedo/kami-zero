# Plan for session 81

## Context carrying over from session 80

Session 80 executed the founder's doctrine corrections (read `systems/*.md`, hunt by current HP, aggressive cadence) but landed 0 kills in 5 tx / ~42M gas. The doctrine itself is not yet falsified — both attempted clusters had structural issues that don't refute the heuristic:

- **theplux node-9 cluster**: 7 of 8 candidates were LISTED (mass-listed for sale), not HARVESTING. Oracle has no listing-event action-row, so `latest=harvest_start` mis-flagged them. **Doctrine update**: any oracle scan must be live-filtered for `state == 'HARVESTING' AND bounty > 0`.
- **rtvvvvv node-86 farmers (15538/8761/10775)**: 15538 deep-reverted (HP > threshold even at 525min). 8761 cycled to RESTING within ~10min of scanner output. **Doctrine update**: H25+ skill-boosted farmers strain at ≤0.072 HP/min — much slower than the H-only formula projects. Use that as upper bound when target has Guardian/Enlightened SP.
- **rtvvvvv soft-stop**: 3 reverts across sessions 76/78/80 on this owner's roster. Stop hunting them.

11224 is RESTING node 86, sync HP ~140, cooldown clear.

## Priority 1 — First kill on the new doctrine

**Scan**: oracle for HARVESTING kamis on open-tier nodes with **long harvest duration AND low Harmony** (H<20 = strain rate ~0.10–0.15 HP/min, much higher than H25 farmers). Long-running low-H kamis are the prime current-HP-doctrine targets.

Pre-flight checklist before any strike:
1. Live `get_kami_state_slim(target)`: confirm `harvest.state == 'ACTIVE' AND harvest.balance > 0` (ACTIVE harvest with bounty — guards listing false-positive).
2. Read `bonuses.defense.threshold.shift` and `.ratio` live (oracle staleness on builds > 24h).
3. Compute kill threshold using the canonical formula from `systems/liquidation.md`:
   - animosity = GaussianCDF(ln(V_atk / H_vic)) × KAMI_LIQ_ANIMOSITY[2] / 1e(18+prec−6)
   - efficacy = KAMI_LIQ_THRESHOLD[2] + affinityShift + atkRatio − defRatio
   - shift = (atkShift − defShift)
   - threshold_HP = (animosity × efficacy + shift) × maxHP / precision
4. Project current HP using strain formula. Use **0.072 HP/min cap for H≥25 with skill SP**, and the H-formula (~0.10–0.15) for unboosted low-H targets.
5. Strike only when projected_HP < threshold_HP with **margin ≥ 15 HP** (buffer for projection error).

**Owner blacklist** (3+ reverts → stop targeting): rtvvvvv. Add to `predator/targeting.md`.

If 11224 is the right striker (V36, EERIE-hand), hunt SCRAP-body targets for the affinity bonus. Otherwise pick the kami whose V/affinity matchup gives the highest threshold.

## Priority 2 — Tighten scan→strike loop

Target churn observed at ~10 min on auto-managed farms. Mitigations:
- **Inline pre-strike re-read**: in the same MCP round-trip as the liquidate call, do a slim read of the target. If state/balance changed, abort the strike (saves the 0.28M early-revert gas).
- Or: accept early-revert as a 0.28M cost of doing business; budget 2–3 0.28M reverts per session as expected churn cost.

If a `liquidate_with_precheck` tool would save gas systematically, document and build per `harness:` discipline.

## Priority 3 — Reconcile predator/mechanics.md (carried from session 80 P1)

Did NOT happen in session 80 (chased the kill instead). Do this **only after Priority 1 has been attempted** — don't write docs as a procrastination move when the hunt is live. If a strike lands, mechanics work waits.

The reconciliation: replace empirical sections with cross-references to `systems/liquidation.md`. Keep agent-discovered gotchas (oracle staleness, listing-event gap, strain rate cap on H25+ skill-boosted) as a clearly-marked "Empirical layer on top of canonical mechanics" section.

## Priority 4 — Update CLAUDE.md doctrine (carried from session 80 P2)

Block F (Knowledge Sources) + targeting heuristic + cadence norms — all unchanged from session 80 plan. Defer until after a kill if hunting is productive.

## Priority 5 — Self-schedule

After this session: re-wake 30–45 min if 11224 is healing. If 11224 is healthy at session start and a candidate is already identified, re-wake 15 min after.

## Stop conditions (unchanged from session 80)

- First kill → scan and chain on same node.
- 3 consecutive deep-reverts despite passing pre-flight → stop, log, re-read `systems/harvesting.md` strain section.
- Roster ≤3 healthy strikers → defensive mode.
- Total gas > 50M without a kill → end session, post-mortem.

## Active state

- **Account**: bpeon, room 86 (Guardian Skull, EERIE/INSECT).
- **Roster (5 alive)**: 11224 (V36 EERIE-hand, RESTING ~140 HP, 3 SP unspent), 6058 (SCRAP-hand), 10705 (INSECT-hand), 12225, 15540 — last 4 RESTING node 86 per session 78/79 brief, refetch at session start.
- **12649 DEAD** (revive deferred — no Onyx Shards).
- **Inventory**: ~75 Ice Cream, Cheeseburger count unverified, 99 Red Ribbon Gummy.
- **Soft-stop owners**: rtvvvvv (3 reverts).

## Out of scope

- 11224 SP allocation (no kill yet).
- Quest progression (paused).
- 12649 revive (defer).
- Cluster moves to nodes 60/62 (cancelled session 80).
