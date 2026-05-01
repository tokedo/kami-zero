# Session learnings — append only

## Session 73 — chapter pivot, prep only
- Quests paused; auto_v2 (strategy 43) stopped via `stop_strategy(43, permanent=True)`. Kamibots `get_all_strategies` returns empty; `get_tier` shows 0/21 used slots.
- Doctrine written into CLAUDE.md (blocks A–D), quest sections demoted to PAUSED reference.
- `predator/` directory scaffolded.
- Tooling-gap audit logged to `memory/improvements.md`.
- No on-chain action this session — by design.

### Guild handle resolution (P5b)
Resolved **44/82** handles to on-chain account_ids via `oracle_sql` against `kami_static`. Below the plan's "good first pass" target of 70, but expected: oracle's `kami_static` only sees accounts that own at least one indexed kami, so guild members without indexed kamis don't surface. Casing (LOWER) check confirmed `0xAsimov` is genuinely a separate account from `0xasimov` — only the lowercase form has kamis in the static index.

**Unresolved (38)** — likely accounts without any indexed kamis in oracle's 28d window:
`0xAsimov, apeon, banger, BigDawg, blackmilk, blondie, Boo!, Canzi, coopes, dest1ny, dr.craft, Drunkenfist, endlesschase, epcros, goo, h80h, humblehenry, Jack, jr.craft, juan, killerbee, lookinrare, lundgren, mango!, meme, Milady, mr.craft, saintlaurent, Salazar, Santino, Shell, Spinneum, sr.craft, surprise, sweazy, Vanir, wassieairforces, Whispo`.

Until they're resolved, the no-liquidate gate must continue to match these by **handle string**, exactly as written in the CSV. Future session can retry resolution as the oracle window grows or as a different account-name index becomes available.

### Baseline oracle reconnaissance
- Oracle healthy: chain head lag 9.6s, 567,372 kami_action rows in 28d window.
- `harvest_liquidate` action_type confirmed in oracle vocabulary: **1,676 events in 28d**, all routed through `system.harvest.liquidate`. Schema: attacker = `kami_id`; node and target are NOT populated (`node_id` NULL on every liquidation, `target_kami_id` also NULL). Target is encoded via `harvest_id` — links to the harvest entity that was liquidated, which in turn maps to the target kami via on-chain entity lookup. **Implication for tooling**: any "scan recent kills on node X" query needs to join `harvest_liquidate.harvest_id` to a harvest→node mapping, OR query the metadata. Sample row's `amount` field carries integer values (851, 606, 970) — plausibly obol/musu yield per kill, but unverified. **mechanics.md TODO**: confirm what `amount` represents, and recover node from harvest_id.
- Top 7d nodes by `harvest_start`: 86 (76,741 / 9.4× #2), 73 (17,442), 16 (8,288), 60 (6,275), 9 (3,509). Node 86 is the dominant farming hub by far. Target-density implication: **node 86 is where most prey are likely to be**. (Not actionable this session — predator transfer pending.)
- bpeon's pre-transfer roster snapshot: 17 HARVESTING / 3 RESTING (3874, 3983, 7722) at session start. Per-kami token IDs and entity hashes captured in decisions.md. **None of these are predators**; founder's transfer will swap them.
- bpeon inventory baseline: MUSU 507,785, VIPP 49,744, plus a deep larder of food/restoratives (Ghost Gum 1,057; Cheeseburger 116; Ice Cream 78; Rock Candyfloss 63) and crafting materials. **Predator-relevant items present**: Hostility Potion (1) — boosts attack? need mechanics.md research; Flash Talisman (1) — unknown; Respec Potion (1) — useful when predator transfer arrives. Bone Chunks (115), Cigarette Butts (266), Patinated Pipes (340), Dried Stems (367), Honeydew Scales (61) — all materials, not directly predator-relevant.

## Session 75 — Roster brief (predator transfer landed)

Transfer landed at ~2026-05-01 23:30 UTC. **6-kami predator roster** now on bpeon, all from cpeon (kami-agent's account). All RESTING, all parked at node **86** (Guardian Skull, EERIE-INSECT affinity), per-kami transfer cooldown ends ~2026-05-02 00:08 UTC. Inventory delta: +500 Gakki Cookie Sticks, +1000 Pom-Pom Fruit Candy, +400 Rock Candyfloss (now 463 total), +13 Booster Packs, +99 Red Ribbon Gummy (REVIVE), +Cultivation/Paeon/Melkarth/Neith spell cards, +Holy Dust 4, +Grace Potion, +XP Potion, +Bless Potion. MUSU 507,785 → 518,699.

### Per-kami brief (oracle `kami_static` + `get_kami_state_slim`)

Convention below: `total_*` = current with skills/equipment; `base_*` = innate. attack_threshold/spoils given in slim's normalized form (slim ratio 0.5 ≈ oracle 250 = 1e3-precision scale; both encode the same value).

**12649 — "Spearhead-A"** (L56, NORMAL/NORMAL)
- Stats: HP 270, Power 12, Violence 34, Harmony 20.
- Bonuses: spoils ratio 0.20 (highest), threshold ratio 0.5 / shift 0.30 (highest combined), defense salvage 0.08, defense threshold shift 0.10, **general cooldown −150 (slim) / −40 (oracle)**.
- Skills: 56 SP all in **Predator tree** — full tier 1 (111/112/113), full tier 2 (121/122/123), Warmonger 131(1), full tier 4 (142/143), full tier 5 (151/152(4)/153), Assassin 163(1). Pure assassin build.
- Best target archetype: anyone with mid harmony (10–18) who's farming bounty on a NORMAL or affinity-neutral node. Universally usable (NORMAL hand = no affinity penalty anywhere). Re-strikes fastest because of cooldown reduction; strongest spoils share due to the 0.20 ratio + L56 base Power 12.
- **Spearhead pick #1**.

**11224 — "Spearhead-B"** (L48, NORMAL/EERIE)
- Stats: HP 230, Power 13, **Violence 36 (highest in roster)**, Harmony 11 (lowest).
- Bonuses: spoils 0.08, threshold ratio 0.5 / shift 0.28, def threshold shift 0.10, cooldown −100 (slim) / 0 (oracle).
- Skills: 45 SP in Predator (111–113, 121–123, 131(1), 142, 143, 151) + **3 unspent SP**.
- Best target archetype: high-harmony defenders (V/H ratio matters; only kami in roster that breaks against H 16+). EERIE hand → strong vs SCRAP-body targets, weak vs INSECT-body. Use deliberately by target body.
- 3 SP allocation: pending observation in real hunts. Initial read — push to tier 2 cap (Sniper 123 already 5; finish 113 Mercenary 4→5 = +1) and start tier 3 (Vampire 132 or Bandit 133, mutually exclusive with Warmonger). Decision deferred per founder rule until we see 11224 in action.
- **Spearhead pick #2**, deployed when target H ≥ 16 makes 12649's V:H ratio drop into the 1.5–1.8x band.

**10705 — "Tank-Striker-A"** (L46, NORMAL/INSECT)
- Stats: HP 240 (highest), Power 11, Violence 32, Harmony 19.
- Bonuses: threshold ratio 0.5 / shift 0.28, def threshold shift 0.10, cooldown −40, no spoils ratio.
- Skills: Predator (111–113(4), 121–123(4), 131(1), 142) + Guardian (312, 322, 323, Anxiety 331(1)) — hybrid sustain/strike.
- Best target archetype: EERIE-body targets (INSECT hand wins). High HP + Guardian skills → can absorb recoil from hitting tougher targets. Designate as second-line striker for tougher fights.

**6058 — "Tank-Striker-B"** (L46, NORMAL/SCRAP)
- Stats: HP 200, Power 11, Violence 31, Harmony 18.
- Bonuses: threshold ratio 0.25 / shift 0.28, def threshold shift 0.10, cooldown −40, no spoils ratio.
- Skills: Predator (111–113, 121–123(4), 131(1), 142) + Guardian (312, 322, 323, Anxiety 331(1)).
- Best target archetype: INSECT-body targets (SCRAP hand wins). Lowest stats among Tank-Strikers; deploy when affinity matchup matters more than raw V.

**12225 — "Tank-Striker-C"** (L45, NORMAL/NORMAL)
- Stats: HP 220, Power 13, Violence 30, Harmony 19.
- Bonuses: spoils 0.08, threshold ratio 0.25 / shift 0.26, def threshold shift 0.10, cooldown 0.
- Skills: Predator (111–113(4), 121–123(4), 131(1), 142(4)) + Guardian (312, 322, 323, Anxiety 331(1)).
- Best target archetype: anyone neutral; second-line vs NORMAL or affinity-neutral targets. Lowest base violence (22) — least efficient striker but tankiest after 10705.

**15540 — "Tank-Striker-D"** (L46, NORMAL/NORMAL)
- Stats: HP 190 (lowest among tanks), Power 12, Violence 31, **Harmony 21 (highest)**.
- Bonuses: spoils 0.08, threshold ratio 0.25 / shift 0.28, def threshold shift 0.10, cooldown 0.
- Skills: Predator (111–113(4), 121–123, 131(1), 142) + Guardian (Defensiveness 311, 312, 323, Anxiety 331(1)).
- Best target archetype: lure / anti-counter. Highest harmony in roster makes it the *hardest* to counter-liquidate — it's the kami you leave on a node when you need a non-strain-zero presence to deter retaliators. Secondary striker role for NORMAL-body targets.

### Affinity coverage
Hand affinities cover all three triangle slots: **EERIE (11224), SCRAP (6058), INSECT (10705)**, plus three NORMAL hands (12649, 12225, 15540). The team is tactically diverse — for any given victim's body affinity we have a hand-strong option. Body affinity is NORMAL across the roster, so we're never affinity-penalized as defenders. Net: in a contested node we don't suffer affinity recoil-nudge from any hand-affinity attacker.

### What this means for hunt planning
- 12649 + 11224 are the spearheads. Lead with one and (if cooldown stalls) follow with the other.
- The four hybrids are second-line. Pick by affinity matchup against the target body.
- Recoil math is the binding constraint, not threshold math. The roster wins virtually all V:H matchups against farm kamis (V 30–36 vs typical H 10–18 = 1.7–3.6x — easy threshold). Recoil is what limits cadence.
- **Use Hostility Potion (1×) on the first sandbox kill** to characterize its effect on threshold/spoils. Use Grace Potion (1×) to reset HP/strain after a high-recoil strike.

---

## First Hunt Plan — session 76 candidate (do NOT execute this session)

### Target node — primary: **node 86 (Guardian Skull)**, EERIE-INSECT affinity

Rationale:
1. **Already there**. All 6 predators sit at node 86 already. Movement cost = 0.
2. **Highest harvest density on the entire chain**. 76,741 harvest_starts in
   the trailing 7d window (per `oracle_top_nodes`) — 9.4× the next node.
   This is where the prey lives.
3. **Affinity neutral against our 3 NORMAL bodies**. EERIE-INSECT node
   bonus does not penalize NORMAL-body predators, so the 4 NORMAL-bodied
   kamis (4/6) are unaffected. The 2 NORMAL-handed kamis (12649, 12225,
   15540 — three actually) likewise get no affinity threshold bonus from
   the node, but no penalty either.

### Backup nodes (if 86 is suddenly empty or all guild)
- **Node 73**: 17,442 starts in 7d (#2). One-room hop investigation only;
  travel cost likely small if adjacent.
- **Node 16**: 8,288 starts (#3). Old bpeon farm node; likely populated.

### Counter-predator scan
Top 7d liquidator: kami `0x808e...` — 80 kills / 53,657 MUSU spoils
(~671 MUSU/kill). 14 distinct kamis with 12+ kills in 7d. The top-tier
predator population is large enough that node 86 likely has at least one
active predator at any moment.

We don't yet have a per-node liquidator breakdown (oracle limitation —
`harvest_liquidate.node_id` is NULL). Mitigation for first hunt:
- At wake-time, call `get_all_kamis()` and filter for kamis on node 86 with
  `state=HARVESTING`. From the list, identify any kami appearing in the
  top-15 7d-liquidator IDs above (their token indices we'd cross-resolve
  via a follow-up oracle query). If a top-tier predator is currently on
  the node, **defer the strike** — recoil math (their high V) makes us
  the easier kill.

### Target shortlist build (at wake)
1. `get_all_kamis()` — full population with current node.
2. Filter `node == 86 && state == "HARVESTING"`.
3. Drop guild-no-touch matches (account_id first, handle fallback).
4. For each remaining candidate, fetch `get_kami_state_slim(kami_id)` to
   get HP%, Harmony, body-affinity. **Live targets are kamis with
   HP/maxHP × 100% < projected_threshold(attacker, victim)**.
5. Compute threshold per the formula in `predator/mechanics.md` for our
   spearhead 12649 against each candidate. Rank by `expected_obol +
   expected_spoils − recoil_cost`.

### Strike execution (at wake, if conditions met)
- **Attacker pick**: 12649 unless top-3 candidate has H ≥ 18, in which case
  switch to 11224 (V 36 better breaks higher-harmony targets).
- **Tx**: `system.harvest.liquidate.executeTyped(victimHarvestID,
  killerKamiID)` with gas limit 7,500,000. Tool not yet built — see
  `memory/improvements.md` Gap 1; this is the first build of session 76.
- **Item usage**: pop **Hostility Potion** (item 11410) before first
  strike — characterize its effect by reading attacker stats before/after.
  This is data work disguised as a hunt; even a no-strike outcome would be
  worth one consumable.

### Trigger condition (for session 76)
Execute the first hunt **iff** at wake-time:
- ≥ 5 non-guild HARVESTING kamis on node 86, AND
- At least 3 of those have V:H ratio ≤ 2 (i.e. their harmony is at least
  half our spearhead's violence — the easy-kill band), AND
- No top-15 7d-liquidator currently HARVESTING on node 86 (counter-
  predator gate).

**Bail-out** (revise plan, don't strike):
- If guild-no-touch CSV `Updated:` timestamp is > 7 days old → defer per
  CLAUDE.md hard rule #1.
- If `liquidate` tool isn't built yet (almost certainly the case at session
  76 start) → priority shifts to building it: read `system.harvest.liquidate`
  ABI from `integration/ids/systems.json` (encoded ID confirmed), wire into
  `executor/server.py` with the 7.5M gas limit, then strike.
- If our spearhead's HP is < 90% (which can happen if the new owner sees
  any harvest tick before strike), top off with a Cheeseburger / Better
  Ice Cream first.

### Estimated yields per first hunt
- Per kill: 1 obol (fixed) + spoils MUSU (top-15 average ~671 MUSU/kill).
- Gas per strike: ~7.5M (GDD ceiling). Strike-and-rest cadence:
  with 12649's cooldown shift, expect 1 strike per ~30–60 minutes
  (unverified; cooldown base unknown).
- Session 76 target: **1–3 kills** if conditions hold. **0 kills** is also
  acceptable if the recon shows no clean targets — better than a misjudged
  strike that gets us counter-killed.

### Plan revision rule
After session 76, regardless of strike count, append a new section to this
file with: actual targets seen, who we hit (or didn't), gas spent vs
yield, recoil HP cost, whether Hostility Potion fired and what it changed.
The First Hunt Plan above gets superseded by version 2 in session 76's
end-of-session update.
