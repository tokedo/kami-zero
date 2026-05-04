# Items Arsenal — Combat & Disruption Inventory (v1)

**Generated**: 2026-05-04 (session 123)
**Sources**: `catalogs/items.csv`, `catalogs/recipes.csv`, `bpeon` inventory snapshot.
**Scope**: Items with combat or disruption applicability for predator play. Pure-food (heal-only HP+N for our own kamis) is **not** catalogued here — covered elsewhere — except the cookies/cheeseburgers we already use as baseline close-feed.

Effect-string conventions (verified across items + skills.csv):
- `ATS` = attack threshold shift (raises HP-floor at which we can liquidate).
- `ATR` = attack type-ratio (multiplies aff-shift on attack).
- `DTS` = defense threshold shift (raises HP-floor at which we get killed).
- `DTR` = defense type-ratio (multiplies aff-shift on defense).
- `ARB` = attack recoil base (HP cost to attacker per strike).
- `ASR` = attack spoils ratio (MUSU spoils % on kill).
- `DSR` = defense spoils retention (MUSU kept on liquidation).
- `STRAIN` = harvest strain rate multiplier.
- `BOUNTY` = next-harvest MUSU multiplier.
- `HIB` = harvest intensity boost (MUSU/hr build rate).
- `HFB` = harvest fertility boost (affinity advantage scalar).
- `COOLDOWN` = cooldown-shift adjustment for next action.
- `NEXT_COOLDOWN+N` = adds N seconds to target's next cooldown timer.
- `_KK` suffix = effect applies kami-on-kami only (not vs operators).

Inventory column = current bpeon balance at session 123 start.

---

## Tier 1 — Active disruption (thrown at ENEMY kami)

| Item ID | Name | Type | Effect | Target / Scope | Ingredient cost | Inventory now |
|---|---|---|---|---|---|---|
| **19001** | Spirit Glue | Potion (Uncommon) | `NEXT_COOLDOWN+180,ITEM1003` | Enemy kami (HARVESTING) | Recipe 23: 1 Plastic Bottle (1003) + 200 Microplastics (1103) + 200 Berry Chalk (1114). Tool: Portable Burner. Stamina 20. | **0** (plastic 9013, microplastics 300k, berry chalk 1M — craftable batches: **~9000** capped by plastic) |
| **19101** | Animistic Poison | Potion (Rare) | `STRAIN+50%` | Enemy kami (HARVESTING) | Recipe 24: 150 Resin Tincture (1202) + 5 Blue Pansy (11314) + 150 Sanguineous Powder (1113). Tool: Portable Burner. Stamina 25. **Min level 15.** | **0** (resin 375, **blue pansy 0**, powder 125 — bottleneck blue pansy + powder; ~0 batches without farming pansies) |
| **19201** | Cthonic Blight | Potion (Rare) | `DTS-5%` | Enemy kami (BYPASS_BONUS_RESET) | Recipe 25: 100 Holy Syrup (1201) + 1 Honeydew Scale (11312) + 1 Fetid Egg (11227). Tool: Portable Burner. Stamina 25. **Min level 15.** | **0** (**holy syrup 0**, scale 61, **fetid egg 0** — bottleneck both syrup + egg) |
| **19301** | Curse Tablet | Potion (Rare) | `ATS-30%_KK` | Enemy kami (no bonus reset noted) | **NO RECIPE** — drop-only or NPC source. | **0** |

**Spirit Glue** is the founder-priority item. We have *all three ingredients in abundance*. Can craft thousands; the throughput limit is operator stamina (20 SP per craft) and gas. Effect: locks an enemy HARVESTING kami to its node for an extra 3 minutes via cooldown extension — the disruption value compounds when applied right before a node-clear or to a defensive farmer's most-active kami.

**Animistic Poison** is the highest-EV missing combat item. STRAIN+50% on a HARVESTING enemy kami *accelerates the strain model directly* — a candidate sitting at margin +50 (sub-floor for V<22) would ripen toward kill-zone in ~⅔ the natural time. This is the lever that unblocks the V<22 sustain-build cluster the world has been dominated by for 5 sessions. **Blocker: Blue Pansy (11314) is HP+25 food found at certain nodes**; we have 0. Once Blue Pansy supply exists, we can craft ~25 batches before Sanguineous Powder caps us.

**Cthonic Blight** lowers enemy DTS by 5% — translation: lowers their defense-side HP floor so the kill_zone math improves by ~5% × (V−H). For V<22 H<13 candidates, that's typically 4–6 HP of effective margin gained. Useful to push margin-borderline targets into the kill window. Blocked on Holy Syrup (recipe 14: 1 Holy Dust → 500 syrup; we have 4 Holy Dust → could mint 2000 syrup) AND Fetid Egg (HP+35 food, drop-only / shop?).

**Curse Tablet** appears drop-only (no recipe). ATS-30% on an enemy kami means *they* lose 30% of their attack threshold shift when *they* try to liquidate — i.e., this is a *defensive* item to throw at an enemy predator, not at a harvester. Useful against Aenne / 3333333333333333 / counter-predators. Worth asking founder to flag if any merchant lists this.

---

## Tier 2 — Self-buff (applied to our own striker before strike)

| Item ID | Name | Type | Effect | Scope | Ingredient cost | Inventory now |
|---|---|---|---|---|---|---|
| **11410** | Hostility Potion | Food (Uncommon) | `ATS+3%,ITEM1102` | Our kami (BYPASS_BONUS_RESET) | Recipe 18: 1 Empty Cup (1102) + 250 Sanguineous Powder (1113) + 250 Pine Pollen (1104). Tool: Portable Burner. Stamina 20. | **0** (cup 1, powder 125, pollen 500 — capped at **0 batches** by powder; Pine Pollen 500 = 2 batches if powder existed) |
| **11409** | Energy Drink | Food (Uncommon) | `COOLDOWN-30s,BYPASS_BONUS_RESET` | Our kami | Recipe 19: 1 Scrap Metal (1005) + 250 Berry Chalk (1114) + 250 Resin Tincture (1202). Tool: Portable Burner. Stamina 20. | **0** (scrap 71, chalk 1M, resin 375 — capped at **1 batch** by resin; bottleneck resin) |
| **11406** | Apology Letter | Food (Uncommon) | `ARB-25%` | Our kami (BYPASS_BONUS_RESET) | Recipe 20: 2 Wooden Stick (1001) + 125 Sanguineous Powder (1113) + 125 Resin Tincture (1202). Tool: Spice Grinder. Stamina 20. | **0** (stick 206, powder 125, resin 375 — capped at **1 batch** by powder) |
| **11407** | MUSU Magnet | Food (Rare) | `DSR+25%` | Our kami (BYPASS_BONUS_RESET) | Recipe 22: 1 Stone (1002) + 50 Powdered Red Amber (1107) + 100 Holy Syrup (1201). Tool: Screwdriver. Stamina 25. | **0** (stone 686, **powdered red amber 0**, **holy syrup 0**) |
| **11408** | Festival Chime | Food (Rare) | `HIB+25` (next harvest) | Our kami (BYPASS_BONUS_RESET) | Recipe 21: 3 Scrap Metal (1005) + 250 Holy Syrup (1201). Tool: Screwdriver. Stamina 25. | **0** (scrap 71, **holy syrup 0**) |
| **11405** | Bless Potion | Food (Uncommon) | `BOUNTY+25%,ITEM1003` (next harvest) | Our kami (BYPASS_BONUS_RESET) | Recipe 5: 1 Plastic Bottle (1003) + 100 Essence of Daffodil (1111). Tool: Portable Burner. Stamina 15. | **1** (bottle 9013, essence 300 — craftable batches: **3** capped by essence) |
| **11404** | Grace Potion | Food (Rare) | `STRAIN-25%,ITEM1003` (next harvest) | Our kami (BYPASS_BONUS_RESET) | Recipe 4: 1 Plastic Bottle (1003) + 100 Essence of Daffodil (1111) + 50 Black Poppy Extract (1110). Tool: Portable Burner. Stamina 25. | **1** (bottle 9013, essence 300, black poppy 450 — craftable batches: **3** capped by essence) |
| **11226** | Ash Pearl | Food (Rare) | `TEMP1HARMONY,TEMP1VIOLENCE` | Our kami (BYPASS_BONUS_RESET) | No recipe (drop only). | **0** |
| **11225** | Teardrop Jewel | Food (Rare) | `HFB+50%` | Our kami (BYPASS_BONUS_RESET) | No recipe (drop only). | **0** |
| **11224** | Inverted Teardrop Jewel | Food (Rare) | `ATR+10%` | Our kami (BYPASS_BONUS_RESET) | No recipe (drop only). | **0** |

**Energy Drink** is the only stat-bump for our strikers we can craft *now* (1 batch with current inventory; bottleneck 250 Resin Tincture/batch, we have 375). COOLDOWN-30s would let a striker fire faster after `harvest_start`, shaving the 100s post-deploy cooldown to 70s. Not transformative for our current pace but useful for chain-strike sequences.

**Apology Letter** (ARB-25%) reduces strike recoil by a quarter — bigger lever than energy drink for striker survivability over multi-kill sessions. Bottleneck chain: Sanguineous Powder (125 per craft, current 125 → 1 batch) AND Resin Tincture (125 per craft, current 375 → 3 batches). **Free unlocks**: grind 29 Sanguine Shrooms via recipe 16 → 14,500 powder, AND process 25 Resin via recipe 15 (1 Resin → 500 Resin Tincture) → 12,500 tincture. After both, Wooden Stick is the bottleneck (206 / 2 = 103 Apology Letters available).

**Hostility Potion** (ATS+3%) raises our striker's attack threshold by 3% — directly improves kill_zone math. ATS is the most direct stat for predator striker EV. Bottleneck chain: Sanguineous Powder (250/craft) AND Pine Pollen (250/craft, current 500 → 2 batches) AND Empty Cup (1/craft, current 1 → 1 batch). **Free unlocks**: shroom-grind (above) covers powder. Pine Pollen requires Pine Cones (item 1004) which we have 0 of — Pine Pollen restocking blocked. Empty Cup recipe 17 chisels 1 Stone → 1 cup using Screwdriver (we have 686 stones, plenty). Net: Hostility Potion supply currently capped at 2 batches even after shroom-grind, until Pine Cones are sourced.

**Bless Potion / Grace Potion** are next-harvest buffs, not strike buffs — useful for when a striker pre-deploys to a node and we want their harvest to bank more MUSU (Bless) or shed less HP (Grace). Marginal for current playstyle (sub-30-min deployments).

**Festival Chime / MUSU Magnet** require Holy Syrup, blocked.

**Teardrop Jewels / Ash Pearl** are drop-only, BYPASS_BONUS_RESET, persistent buffs. ATR+10% (11224) is a strong striker buff. None in inventory; unknown drop sources.

---

## Tier 3 — Buffs already in active rotation (close-feed reference, not predator-specific)

| Item ID | Name | Effect | Inventory now | Use |
|---|---|---|---|---|
| 11304 | Gakki Cookie Sticks | HP+100 | 434 | Standard close-feed after strike. |
| 11303 | Pom-Pom Fruit Candy | HP+50 | 1000 | Mid-tier close-feed. |
| 11302 | Cheeseburger | HP+50 | 114 | Mid-tier close-feed. |
| 11301 | Maple-Flavor Ghost Gum | HP+25 | 1056 | Low-tier close-feed / starver-bait. |
| 11312 | Honeydew Scale | HP+75 | 61 | Reserve close-feed; ALSO ingredient for Cthonic Blight. |
| 11313 | Golden Apple | HP+150 | 1 | Heavy emergency feed (single dose). |
| 11305 | Paeon's Field of Flowers | HP+100 | 5 | Spell card close-feed. |
| 11311 | Resin | HP+35 | 25 | Light feed. |
| 11001 | Red Ribbon Gummy | REVIVE STATE-RESTING,HP+10 | 296 | **Revive on dead kami only.** Same primitive as feed; 11001 fires on DEAD targets. |
| 11002 | Melkarth's Heroic Awakening | REVIVE STATE-RESTING,HP+50 | 1 | Bigger revive (single). |

---

## Tier 4 — Operator stamina (relevant for long-travel sessions)

| Item ID | Name | Effect | Inventory now |
|---|---|---|---|
| 21205 | Rock Candyfloss | SP+80 | 463 |
| 21204 | Neith's River of Life | SP+80 | 8 |
| 21202 | Better Ice Cream | SP+40 | 10 |
| 21201 | Ice Cream | SP+20 | 65 |

Stamina is **not currently a bottleneck** — Rock Candyfloss alone covers 463 × 80 = 37,040 SP equivalent, more than any session burns. `travel_to_room` auto-uses these.

---

## Plays this enables

1. **Glue-then-walk-away on defensive farmers.** Throw Spirit Glue at a harvester run by a bulk-stop defender (stefan97, foden, dias, rtvvvvv). Their kami's next cooldown gains 180s — meaning their owner's `harvest_stop`-on-arrival reflex fires *late*, locking the kami at the node a wall-clock window longer. Multiplies disruption-raid value: every glued kami extends our window to convert nearby clean candidates. Cheap (1 plastic + 200 microplastics + 200 berry chalk per shot) — we can carpet a node.

2. **Poison-ripen V<22 sustain-builds (BLOCKED).** Animistic Poison's STRAIN+50% on an enemy harvester *accelerates the strain projection model*. A V12 +50-margin candidate that would naturally ripen to +95 in 3 hours ripens in 2 hours. Combined with V<22 margin ≥+95 doctrine (validated kill floor), this directly converts the 5-session V<22 dominant world into a hunting ground we can actually extract from. **Blocker: zero Blue Pansy supply** — see asks below.

3. **Strike-recoil amortization on multi-kill sessions.** Apology Letter (ARB-25%) on our striker before a 3-kill chain reduces total recoil across kills from baseline ~30 HP → ~22 HP. Saves a close-feed, frees a cookie. **Unlock: grind our 29 Sanguine Shrooms → 14,500 Sanguineous Powder → 116 Apology Letters available.** Free lift, do this next session.

4. **ATS+3% Hostility-Potion-then-strike for borderline V<22 candidates.** A target sitting at margin +90 (just below the +95 V<22 floor) becomes margin ~+93 after Hostility Potion buff to our striker — close enough to consider striking with the safer formula error envelope. Same shroom unlock as #3. Pairs well with Energy Drink (COOLDOWN-30s) for chain-strike pacing. **Caveat: BYPASS_BONUS_RESET items stack on the kami until consumed by a strike or harvest start; verify whether Hostility Potion persists across multiple strikes or is single-use.**

5. **Cursed-tablet defensive screen (BLOCKED, drop-only).** If we ever stockpile Curse Tablets, throwing one on an Aenne-cluster kami lowers *their* ATS by 30%, weakening their counter-predator strikes against our co-located kamis. Speculative until we have a supply.

---

## Missing items / asks (propagated to ideas_to_founder.md)

These are high-EV items we cannot craft from current inventory. Asks live in `ideas_to_founder.md` (see this session's entry).

1. **Blue Pansy (11314, HP+25 Food)** — required for Animistic Poison. **HIGHEST-EV ask.** 5 per craft × N batches. Unblocks the strain-acceleration play, which directly addresses the 5-session V<22 dominant world. Drop source unknown — needs founder identification or a node sweep. (As HP+25 food, likely scavengeable from a food-affinity node; check `catalogs/scavenge-droptables.csv`.)

2. **Holy Dust → Holy Syrup conversion budget.** We have 4 Holy Dust. Recipe 14 mints 500 Holy Syrup per dust. Burning 2 dust → 1000 syrup unlocks ~10 Cthonic Blight (100 syrup each) AND 4 Festival Chime (250 syrup) AND 10 MUSU Magnet (100 syrup) — *if* we resolve the other co-bottlenecks (Fetid Egg, Powdered Red Amber). **Need founder direction on whether Holy Dust should be reserved for kami naming (1 dust = 1 rename) vs burned for craft chain.** Currently bpeon has 4; future-proof reserve = 2 for naming, 2 for syrup batch.

3. **Powdered Red Amber (1107)** — required for MUSU Magnet. We have 1 Red Amber Crystal (1007); recipe 13 grinds it for 500 powder. One-time burn unlocks 10 MUSU Magnets if Holy Syrup is also unblocked. Defer until syrup decision lands.

4. **Fetid Egg (11227, HP+35 Food)** — required for Cthonic Blight. Drop-only. Source unknown — needs founder identification or scavenge sweep.

5. **Curse Tablet (19301)** — drop-only, source unknown. Defensive item against counter-predators (esp. Aenne). Long-term wishlist; flag if a merchant or droptable surfaces.

6. **Inverted Teardrop Jewel (11224, ATR+10%)** — drop-only, BYPASS_BONUS_RESET persistent striker buff. Currently 0 in inventory. Source unknown. Worth asking founder where these drop.

---

## Action items for next operational sessions

- **[Free unlock, do next session]** Craft 5× Recipe 16 (Grind Sanguine Shroom → 500 Sanguineous Powder each) — 50 SP, ~7M gas estimate. Verify Sanguineous Powder balance grant and effect string match expectations. If clean, batch the remaining 24 grinds. Total stamina if full batch: 290 SP (covered by Rock Candyfloss 463 stock).
- **[Free unlock, do next session]** Process 3× Recipe 15 (Resin → 500 Resin Tincture each) — 30 SP, light gas. Brings Resin Tincture from 375 → 1,875, removing the Apology Letter co-bottleneck. We have 25 Resin in stock; processing 3 leaves 22 for future use.
- **[Free unlock, do next session]** Craft 1× Recipe 17 (Stone → Empty Cup, 25 SP) for the immediate Hostility Potion craft. Defer batch cup minting until Pine Pollen restock is unblocked.
- **[Conditional, after powder + tincture exist]** Craft 5× Apology Letter (Recipe 20) as a baseline striker reserve. Reapply before any 3+-kill chain session. Verify ARB-25% bonus shows in slim state and survives the strike (effect strings here are unverified empirically).
- **[Conditional, after powder + cup exist]** Craft 1× Hostility Potion (Recipe 18) as proof-of-concept. Verify ATS+3% bonus surfaces in slim state. **Test against a V≥22 candidate, not a V<22 borderline** — formula error in V<22 regime is the variable we're hedging, and we don't want to confound a Hostility Potion verification with strain-model uncertainty.
- **[Founder ask]** Resolve Blue Pansy and Fetid Egg drop sources (entries above). These two unblock the highest-EV item (Animistic Poison) and a defense-shred item (Cthonic Blight).
- **[Founder ask]** Reserve policy for Holy Dust (4 in stock; naming vs syrup-craft).

---

## Maintenance

This doc is `v1`. Refresh triggers:
- Inventory changes large enough to flip a craftability cap (e.g., new Blue Pansy supply, new Holy Dust).
- New recipes added to `catalogs/recipes.csv`.
- New items added to `catalogs/items.csv` with combat utility.
- After any in-game balance patch (e.g., effect-string change).

Cross-references: `predator/mechanics.md` for kill_zone math; `executor/hp_projection.py` for `kill_threshold`; `predator/learnings.md` for empirical effect verifications when items get used.
