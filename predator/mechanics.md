# Liquidation mechanics — what we know

Sources: GDD `systems/liquidation.md` (canonical), `executor/server.py`, oracle
sample reads, `integration/ids/systems.json`, `catalogs/skills.csv`.

## On-chain entry point — confirmed

- **System**: `system.harvest.liquidate` (encoded ID
  `0x743810742beaf8b355d13d6badc55ccd4d31b7c3c930a2eb0339cd37362aff02`).
- **ABI**: `executeTyped(uint256 victimHarvestID, uint256 killerKamiID)` —
  victim's harvest entity, attacker's kami entity. Single-shot only; no batch
  variant published in the GDD.
- **Gas limit**: **7,500,000 required** (GDD specifies this minimum;
  PvP path is gas-heavy).
- **Sender wallet**: operator (same wallet as `harvest_start`/`harvest_stop`).
  Not owner.

## Harvest_id traversal — confirmed

- `harvest_entity_id = keccak256("harvest", kamiEntityId)` — same convention
  the executor's `_harvest_entity_id(kami_id)` already uses for stop/collect.
- This means **scanning targets on a node only requires kami entities** — we
  hash to get harvest IDs locally, no on-chain lookup needed for the
  oracle-blind liquidation tx.
- Oracle's `kami_action.harvest_id` carries the target's harvest entity for
  liquidation rows, but `node_id` and `target_kami_id` are NULL — to map
  harvest_id → kami_id → node from oracle alone, we'd need the
  inverse (`getEntitiesWithValue` against the harvest's kami component).
  Out of scope for now; live perception via `get_kami_state_slim` is cheaper.

## Eligibility — six conditions (all must hold)

1. Both kamis are `HARVESTING` on the **same node** at the same moment.
2. Attacker owns the attacking kami (i.e. the kami is in our roster).
3. Attacker's account is in the same room as the node.
4. Attacker is not on cooldown.
5. Attacker HP > 0 (not starving).
6. Victim's HP < kill threshold (see formula).

This means: we cannot strike a victim who has already left the node, and we
cannot strike at all if our attacker is RESTING / on cooldown / starving.

## Kill threshold — formula

```
threshold = (animosity × efficacy + shift) × victimMaxHP / precision
```

If the combined value goes negative, threshold = 0 (target unkillable
from this attacker).

### animosity — Gaussian CDF on Violence:Harmony ratio

```
combatRatio = ln(attackerViolence / victimHarmony)   # WAD precision
base        = GaussianCDF(combatRatio)               # 0..1e18
animosity   = base × KAMI_LIQ_ANIMOSITY[2] / 10^(18 + KAMI_LIQ_ANIMOSITY[3] − 6)
```

Result is in 1e6 precision (proportion of victim max-HP).

| atk Violence : vic Harmony | CDF (~) | Behavior |
|---|---|---|
| 1 : 2 | 16% | Threshold tiny — generally not killable |
| 1 : 1 | 50% | Moderate — kill on low HP |
| 2 : 1 | 84% | Easy kill — most healthy targets within threshold |
| 3 : 1 | 95% | Nearly max threshold |

Implication for our roster: against a typical mid-harmony target
(harmony 10–18), our spearhead 12649 (V=34) and 11224 (V=36) sit at ratios
1.9–3.6x — the upper-easy band. The hybrids (V=30–32) are 1.7–3.2x — solid.

### efficacy — affinity matchup (attacker hand vs victim body)

Triangle: `EERIE > SCRAP > INSECT > EERIE`. NORMAL is neutral both ways.

```
efficacy = KAMI_LIQ_THRESHOLD[2] + affinityShift + atkBonus − defBonus
```

- `atkBonus` = `ATK_THRESHOLD_RATIO` from attacker's skills/equipment.
- `defBonus` = `DEF_THRESHOLD_RATIO` from victim's skills/equipment.

| Matchup (atk-hand → vic-body) | Effect |
|---|---|
| Strong vs (e.g. EERIE → SCRAP) | Threshold up — easier kill |
| Weak vs (e.g. SCRAP → EERIE) | Threshold down — harder kill |
| NORMAL ↔ NORMAL | Neutral |

Implication: 12649/12225/15540 (NORMAL hand) are universally neutral —
never get an affinity bonus, but never get a penalty. The three
affinity-tipped hybrids (6058 SCRAP, 10705 INSECT, 11224 EERIE) get +matchup
bonuses against their respective prey body and −matchup penalties against
their counter — pick them by target body, not at random.

### shift — flat predator/guardian skill add

```
shift = (ATK_THRESHOLD_SHIFT − DEF_THRESHOLD_SHIFT) × shiftPrecision
```

Predator-tree skills push `ATK_THRESHOLD_SHIFT` up. Guardian-tree skills push
`DEF_THRESHOLD_SHIFT` up on the victim. Our roster has 160–200 raw shift
(per `kami_static`); a Guardian-tier-3+ defender with similar shift could
neutralize this entirely — so guardian-built targets are the worst-case
case, low-skill farm kamis are the best-case case.

## Recoil — the cost of striking

```
karma  = GaussianCDF(ln(victimViolence / attackerHarmony))
         × KAMI_LIQ_KARMA[2] / 10^(18 + KAMI_LIQ_KARMA[3] − 3)
nudge  = max(0, KAMI_LIQ_RECOIL[0] / 10^KAMI_LIQ_RECOIL[1] + affinityShift)
boost  = max(0, KAMI_LIQ_RECOIL[6] + DEF_RECOIL_BOOST + ATK_RECOIL_BOOST)
recoil = (karma + nudge) × attackerStrain × boost
         / 10^(KAMI_LIQ_RECOIL[1] + KAMI_LIQ_KARMA[3] + KAMI_LIQ_RECOIL[7])
```

Three drivers for the attacker:
1. **victim's Violence** (high-V targets hit back hard via karma).
2. **affinity nudge** — *reverse* direction from threshold. Victim's hand vs
   attacker's body; advantaged +1000, NORMAL-vs-NORMAL +400.
3. **attacker's accumulated harvest strain** — how much HP we've already lost
   to harvest. Strike fresh (low strain) to minimize recoil.

**Practical rule**: don't strike high-violence victims while strained.
Use consumables to reset HP/strain before hunting tough targets.

## Loot distribution per successful kill

Three buckets: salvage (victim retains), spoils (attacker steals), destroyed
(lost forever).

### Victim's salvage

```
ratio   = KAMI_LIQ_SALVAGE[2] + (KAMI_LIQ_SALVAGE[0] + victimPower) × scaleFactor
          + DEF_SALVAGE_RATIO
salvage = bounty × ratio / 10^(KAMI_LIQ_SALVAGE[1] + KAMI_LIQ_SALVAGE[3])
```

Higher victim Power → larger salvage. Guardian-tree `DEF_SALVAGE_RATIO`
boosts retention. Capped at 100% of bounty. Victim gets XP equal to the
salvage amount.

### Attacker's spoils

```
ratio  = KAMI_LIQ_SPOILS[2] + (KAMI_LIQ_SPOILS[0] + attackerPower) × scaleFactor
         + ATK_SPOILS_RATIO
spoils = (bounty − salvage) × ratio / 10^(KAMI_LIQ_SPOILS[1] + KAMI_LIQ_SPOILS[3])
```

- Higher attacker Power → more spoils.
- Predator-tree `ATK_SPOILS_RATIO` adds.
- Spoils are added to **attacker's harvest bounty** (not inventory directly).
- **Attacker's account receives 1 Obol** (item index 1015). One obol per kill,
  fixed.

Implication: obol accumulation per session = number of successful liquidations.
MUSU accumulation per session ≈ sum of MUSU spoils, scales with target
bounty and our Power+spoils-skills.

### What `amount` represents in oracle's `harvest_liquidate` rows

Top liquidator in 7d: kami 0x808e... 80 kills / 53,657 MUSU summed amount =
**~671 MUSU/kill average**. That's the spoils MUSU stolen, not obol (obol is
1 per kill, would sum to 80). **Confirmed**: `amount` = MUSU spoils stolen
this strike. Not obol; obol is implicit (1 per row).

(Slight caveat: amount is gross pre-tax per oracle docs; consistent with
"spoils added to attacker's harvest bounty" interpretation.)

## Cooldowns

GDD section "Eligibility" mentions attacker cooldown but does not give a
public formula. Empirically: kami's `general.cooldown` bonus reduces this.
Our roster:
- 12649 / 6058 / 10705: cooldown_shift = −40 (oracle), slim shows 12649 at
  −150 (skill-driven dynamic shift). Inconsistency to investigate next session.
- 11224: cooldown_shift = 0 oracle, slim shows −100.
- 12225 / 15540: cooldown_shift = 0.

Until we know the base cooldown duration, treat the spearhead 12649 as
"can re-strike fastest" without putting a number on it.

## Scale conventions (oracle vs slim)

- Oracle `kami_static` exposes shifts/ratios as raw integers (e.g. spoils=100,
  threshold_ratio=250, shift=200) — these appear to be 1e3 precision.
- `get_kami_state_slim` returns the same fields normalized (spoils=0.10,
  threshold ratio=0.25, shift=0.20). **Cross-check both whenever
  threshold/recoil math matters**; they encode the same underlying value
  but at different scales.

## Items potentially relevant (un-tested)

- **Hostility Potion** (item 11410, x1 in inventory) — likely buffs
  ATK_THRESHOLD_RATIO/SHIFT or spoils for a window. Test once first
  liquidation lands.
- **Flash Talisman** (11412, x1) — unknown, possibly attack-related.
- **Grace Potion** (11404, x1) — likely defensive (heal/regen).
- **Bless Potion** (11405, x1) — unknown buff.
- **Respec Potion** (11403, x1) — for re-allocating skills (not predator-specific).

Use the first 1–2 sandbox kills to characterize Hostility/Flash. Document
observed delta on a controlled hit.

## Open questions still

- Base cooldown duration in seconds. Need an empirical observation across
  back-to-back strikes.
- Whether equipping the Aetheric Sextant (key item, in inventory) does
  anything in PvP context.
- Real-world dispersion of `amount` (spoils MUSU): top kami avg 671, but
  variance unknown — single-strike spoils could be much higher on
  bounty-rich targets. Sample a few more rows next session to estimate.
- Whether liquidator's account receives the obol immediately or claims it
  later (worth confirming via `get_inventory` delta after first kill).

## Empirical: revert messages observed (session 76)

- `revert: kami lacks violence (weak)` — fired when target's CURRENT HP
  exceeds the computed kill threshold. Empirical case: attacker 12649
  (V34, atk_threshold_shift 0.30) vs target 3764 (H21, def_shift 0,
  max_HP 200, full HP at strike). The contract's kill check is **strict
  `current_HP < threshold`**, not `≤`. Threshold ≈ (animosity × efficacy
  + shift) × max_HP; with our numbers threshold ≈ 0.99 × 200 = 198, so
  full-HP (200) target was 1% above the bar — deny.
- **Practical implication**: at full HP, with NORMAL/NORMAL affinity and
  zero defender shift, V34 cannot one-shot a target with H ≥ ~21. Either
  wait for strain to decay target HP a few percent, OR pick lower-H
  targets (H ≤ 17 with zero def_shift = comfortable kill at full HP for
  V34 spearhead). On node 86, almost all H ≤ 17 prey carry def_shift
  ≥ 100, which pushes the threshold back below 1.0. Net: node 86 is a
  Guardian-defender-heavy node. Spearheads need either **strain wait**
  on bigger H targets OR an **affinity bonus** (10705 INSECT-hand vs
  EERIE body, 6058 SCRAP-hand vs INSECT body, 11224 EERIE-hand vs SCRAP)
  to clear shift_diff > 0.
- A revert costs ~2.7M gas (vs 7.5M ceiling for a successful strike).
  Failure is cheap-ish but not free; budget reverts at ~1/3 of a kill cost.
- Reverts do NOT consume cooldown nor break the harvest. Re-strike
  available immediately after target HP decays.

## Practical pre-flight checklist (do BEFORE every strike)

1. Pull `get_kami_state_slim(target)` and check `health.sync` (current HP,
   not max).
2. Compute approximate threshold:
   `threshold ≈ GaussianCDF(ln(V_atk / H_vic)) × (1 + atk_shift − def_shift) × max_HP`.
   (Affinity efficacy adjusts the multiplier inside the parens; NORMAL/NORMAL
   = 1.0 baseline. EERIE→SCRAP / SCRAP→INSECT / INSECT→EERIE add a positive
   nudge; the reverse three subtract.)
3. **If threshold ≤ current_HP, skip — the strike will revert**. Pick
   another target or wait.
4. As a quick rule-of-thumb for our V34 spearhead (12649) at full-HP
   targets: clean kills require either H ≤ ~16 with def_shift ≤ 80, OR
   matching affinity to lift efficacy.
