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

---

## Session 76 — first hunt: tool built, strike reverted (no kill)

**Outcome**: 0 kills, 0 obols, 10.57M gas burned. Liquidate tool built and
end-to-end-tested (the revert proves the contract path is correct; failure
is on game-state semantics, not encoding).

### What happened, in order

1. **Built liquidate MCP tool** — `liquidate(target_kami_id, attacker_kami_id,
   account, target_account_id?, target_handle?)`. ABI: `system.harvest.
   liquidate.executeTyped(uint256 victimHarvestID, uint256 killerKamiID)`.
   Gas limit 7.5M. Wired the **guild-no-touch gate** as in-code hard rule:
   loads `predator/guild-no-touch.csv`, parses `# Updated: YYYY-MM-DD`,
   denies all if missing or > 7 days old, matches by account_id else handle
   (case-insensitive). Verified gate blocks bpeon, tokedo, 0xAsimov,
   lookinrare and passes unknown. (See harness commit + `improvements.md`.)

2. **Recon error in plan**: session 75 plan assumed all 6 predators on
   bpeon were *at* node 86. They were not — bpeon's account room was 15
   (Pinkdrop Park), and the kamis followed the account. Per-kami transfer
   cooldown ended ~00:08 UTC; movement burned 6.34M gas (7 hops, ~900k/hop)
   to get bpeon from room 15 → room 86. **Lesson**: `get_account_kamis`
   tells you which node a kami's *intended* node is, but the *account*
   room is what gates `start_strategy` / liquidate. Read the account room
   first.

3. **Started 12649 harvesting on node 86** (1.5M gas). Required for the
   "both kamis HARVESTING on same node" liquidation eligibility rule.

4. **Picked target 3764 (rtvvvvv)**: V13/H21/HP200, NORMAL/NORMAL,
   zero defense skills, 0 attack/defense bonus shift. Thought to be
   ideal sandbox target — low recoil, clean threshold zone.

5. **Strike reverted** with `revert: kami lacks violence (weak)`. 2.7M
   gas. Root cause: kill threshold formula floors out at ~0.99 × max_HP
   when V/H = 1.6× and shift_diff = 0.30. Strict `current_HP < threshold`
   denies at full HP. See `mechanics.md` § "Empirical: revert messages
   observed (session 76)".

### Strain-decay path forward

3764 is still HARVESTING on node 86, accumulating strain. In ~30–60 min
its current HP will drop a few % below max — re-strike will land. 12649
still HARVESTING on node 86 (no cooldown burn from the revert). Recoil
cost on the eventual kill stays low because attacker strain barely
accumulates at this cadence.

### Roster-wide implication for node 86

Node 86 is **Guardian-defender-heavy**: scanned the active-harvester
population, minimum H is 17 (23savage 325) and **all sub-H18 candidates
carry def_shift ≥ 100**. That neutralizes our 12649's +0.30 atk_shift
nearly to zero. For full-HP one-shots without strain wait we need either
- An **affinity-bonus** path: 10705 (INSECT hand) vs EERIE-body targets,
  6058 (SCRAP hand) vs INSECT-body targets, 11224 (EERIE hand) vs
  SCRAP-body targets, OR
- A **lower-V target** (rtvvvvv/POWELL-tier farmers — currently 3764 is
  the cleanest) waited on for strain decay.

The cluster math hasn't changed — node 86 is still the right node to
camp. We just need to operate in the strain-wait band, not the
one-shot-fresh-target band, on H ≥ 18 targets.

### What did NOT get tested
- Hostility Potion (item 11410) — wasn't fired this session because the
  strike never landed; potion is single-use and we want it under
  conditions that produce a clean delta read.
- Recoil HP cost — also requires a successful strike.
- Cooldown duration — requires back-to-back successful strikes.

These move to session 77.

### 11224's 3 SP — DO NOT ALLOCATE this session
Founder rule: only after observing 11224 in real hunts. Session 76
produced no kills. **3 SP stay unspent.** Allocation deferred to a
session in which 11224 actually strikes.

---

## Session 77 — Hostility-boosted re-strike: two more reverts (no kill)

**Outcome**: 0 kills, 0 obols, 7.81M gas burned. Definitive read on
the kill formula and a provisional verdict on Hostility Potion. Session
budget breakdown:
- Hostility Potion fed to 12649 (`feed_kami` not `use_account_item`):
  2.42M gas. Pre/post slim delta = `attack.threshold.shift 0.30 → 0.33`.
- Strike 1 (3764 re-attempt): 2.68M gas, reverted "kami lacks
  violence (weak)".
- Strike 2 (tom 14296, H18 with def_shift 0.10): 2.71M gas, same
  revert.

### What we learned (load-bearing)

1. **Kill formula nailed down**: `threshold_ratio = animosity +
   atk_shift − def_shift`. Additive shift form. `attack.threshold.ratio`
   (slim's 0.5 for 12649) does NOT enter the kill check — see
   `mechanics.md` § "Empirical formula refinement (session 77)" for
   the worked-example fits and the math.
2. **Hostility Potion**: fed via `feed_kami(kami_id, food_item_id=11410)`.
   `use_account_item(11410)` reverts with "not for ACCOUNT" — it's
   kami-targeted. The +0.03 shift visible in slim does NOT cross the
   kill-threshold gate in either of our two test strikes (one of which
   the formula predicted should clear). Either slim shows a stat the
   kill path doesn't read, or animosity is under-estimated by our CDF
   model. **Stop burning Hostility for threshold-clearing purposes.**
3. **Strain decay rate observation**: 12649 (strain_boost 0) lost 7 HP
   over ~85 min active harvest = ~0.082 HP/min. Target 14296 lost 5 HP
   over 158 min = ~0.032 HP/min. **Implication**: waiting for a
   Guardian-defended target (kill_zone ≤ 0.95 maxHP) to bleed below
   threshold takes hours-to-days, not minutes. The "strain wait" lever
   only matters for near-edge targets (kill_zone 0.97–0.99).
4. **Node 86 is Guardian-saturated**. Oracle scan of 40 active
   harvesters at H ≤ 18: every single one has def_threshold.shift ≥
   0.10. Only outlier in our hunting band is 3764 (H21 / def 0). For
   bpeon's V34 spearheads, virtually every node-86 farmer sits in
   `kill_zone ≤ 0.95 × maxHP` band → strain-wait is not viable.
5. **Counter-predator gate clear at session start**: top-15 7d
   liquidator scan crossed against current node-86 active harvesters
   returned only **Aaron's kami 14430** as a node-86 last-start, but
   it's RESTING (harvest INACTIVE since ~16h ago) — no live threat.

### Strategic implication for session 78+

**The "camp on node 86 + strain-wait" plan is not yielding kills.**
Two options for the next pivot:

A) **Affinity hunt** — switch attacker by target body. 11224 (EERIE) →
   SCRAP-body targets, 6058 (SCRAP) → INSECT-body, 10705 (INSECT) →
   EERIE-body. Affinity efficacy bonus may add the missing 5–10% to
   kill_zone. Costs: each hunter needs to be HARVESTING on node 86
   first (1.5M gas/start). Worth it if even one strike lands.
B) **Cluster scan elsewhere** — node 86's saturation by Guardians
   suggests other nodes might be less defended. Per oracle session 73
   data: nodes 73, 16, 60, 9 are next biggest. Probably also Guardian-
   defended at the top of the leaderboard, but maybe softer at the
   margins. Movement cost is non-trivial (6+ M gas per cross-region
   move) so this needs cluster math first.

**Session 78 recommendation: Option A.** Same node, lower marginal
gas, tests the affinity hypothesis explicitly. If 11224 strike on a
SCRAP-body target lands, we have a working hunt loop. If not, we
learn the affinity multiplier is too small to matter and Option B
becomes mandatory.

### What did NOT get tested this session
- Recoil HP cost of a successful strike (no successful strike).
- Cooldown duration (no successful strike).
- Hostility Potion's actual effect (e.g. spoils delta) — would need a
  successful strike to compare against a baseline strike.
- 11224's 3 SP — still unspent per founder rule.

### Hostility Potion availability
- Inventory still shows "Hostility Potion 1" pre-feed → 0 post-feed.
  We've burned the potion. Future characterization requires acquiring
  another (Mina shop? droptable? unknown). **Add to ideas_to_founder.md**
  if we want to characterize spoils delta cleanly.

---

## Session 78 — affinity hunt: revert (no kill)

**Outcome**: 0 kills, 0 obols, 5.33M gas. Tested 11224 (EERIE-hand,
V36/H11, atk_shift 0.28) vs SCRAP-body 13253 (tom, V15/H20, def_shift
0.10, HP 194/200). Strike reverted "kami lacks violence (weak)" at
2.68M gas. **Affinity bonus is < 0.07 contribution to threshold_ratio
for our roster** — insufficient to crack Guardian-defended H20 farmers
at 90%+ HP. Detail in `mechanics.md` § "Affinity bonus — provisional
null finding".

### What happened, in order

1. Read state: 11224 RESTING at 90/140 HP, cooldown clear. 12649 still
   HARVESTING node 86 from session 77 (HP 163/170, atk_shift 0.33
   Hostility-buff persists across full sessions).
2. Oracle scan for SCRAP-body active harvesters at node 86. 40 rows.
   Filter against guild-no-touch.csv: most low-H candidates (23savage,
   erere, Tonin, Shadow3X, topobadger) are guild-protected.
3. **Validated guild gate end-to-end**: tried `liquidate(target=12433
   topobadger)` → tool returned `blocked: true, reason: "target
   account_id matches guild member 'topobadger'"`. **No tx submitted.**
   First real proof the in-code gate works under live conditions.
4. Pivoted to **non-guild SCRAP candidates 13253 + 11332** (both tom).
   Both V20/H20, def_shift 0.10, HP near full. Predicted threshold_ratio
   without affinity = 0.902.
5. Healed 11224 (Cheeseburger 50 HP) → started harvest on node 86.
6. Strike 13253 → revert. Result documented above.

### Strategic implication for session 79

**Three cumulative strike-test sessions, zero kills, ~24M gas burned.**
Doctrine says: change something. The change is **cluster move off
node 86**. Oracle cross-node scan (session 78, see `targeting.md` §
"Cross-node target distribution") shows:

- **Node 25**: 49 zero-def EERIE-body harvesters. Perfect for 10705
  (INSECT hand). 7× node 86's best affinity bucket.
- **Node 88**: 10 SCRAP-soft (vs node 86's 15 mostly-guild). Worth
  scoping for 11224.
- **Node 62**: 11 INSECT-soft. Worth scoping for 6058.

**Session 79 plan**: oracle scan + guild-filter + non-guild cluster
math for node 25 first (highest density, best affinity for 10705).
If clean ≥ 5 non-guild zero-def candidates exist, plan the move
(travel cost ~5–6M gas). Strike with 10705 to test affinity at scale.

If node 25 cluster also disappoints, the working hypothesis becomes
**affinity doesn't propagate to kill formula at all** — and the lever
shifts to either prey strain decay or finding pure low-V/low-HP
targets independent of affinity.

### What did NOT get tested (still)

- Recoil HP cost — no successful strike again.
- Cooldown duration — no successful strike.
- Full effect of Hostility (it persisted on 12649 across sessions but
  did not enable any kill against tested targets).
- 11224's 3 SP — still unspent per founder rule.

### State left at session end

- 11224 HARVESTING node 86 (started 07:33 UTC ≈ 1777707222). Will
  accumulate strain over the gap to next session.
- 12649 still HARVESTING node 86 from session 77.
- Other 4 predators RESTING at node 86.
- bpeon account at room 86.

If the next session decides to leave node 86 for cluster-move target,
the migration teardown is: stop both 11224 + 12649 harvests + all
bpeon kamis on node 86 → travel → harvest_start at new node. Gas
estimate ~12–15M for the move + new starts (per session 76 reference).

## Session 79 — first kill in our roster, but on us

**Headline**: 12649 (Spearhead-A, V34/H20/HP270, our top striker) was
**liquidated by Nova Heat 10943** (Assassins guild, V36/H10) at
2026-05-02T07:38:47Z. Hit-and-run: 10943 started a harvest on node 86
at 07:37:20, killed 12649 within 2 min, and stopped its own harvest at
07:41:06 — a 4-minute window. By 11:56 UTC (session 79 wake) the
attacker was long gone from node 86. Cross-node hit-and-run is an
attack pattern we hadn't budgeted for.

Roster: **6 → 5**. No revive this session — `revive_kami` requires
33 Onyx Shards (inventory has 0). Red Ribbon Gummy (99 in stock) and
Melkarth Spell Card (1) are listed as type=REVIVE but the use mechanism
is unverified; deferred to a session with research bandwidth.

### Plan vs reality

Session 79's plan was to evaluate a node 25 cluster move (49 zero-def
EERIE-body candidates from session 78 oracle scan). The plan died at
multiple stages:

1. **Node 25 cluster — 100% guild-protected**. All 49 candidates owned
   by `jun` (account_id 451845...723) — guild deny-listed. Cluster DEAD.
2. **Node 88 fallback — 100% guild-protected**. KCS + dmi own all 8
   non-bpeon zero-def SCRAP candidates. DEAD.
3. **Node 73 false cluster**. Refined oracle scan (`def_shift = 0 AND
   def_ratio = 0`, the v2 filter) returned 12 POWELL+Yeahta candidates
   on node 73. **Live spot-check killed the plan**: POWELL kamis show
   in oracle as `[{"index":311,"points":1}]` (1 SP) but live state
   carries full Guardian tier-2 build (26 SP) yielding def_ratio = 0.25.
   `kami_static.build_refreshed_ts` was 19h stale — the kamis leveled
   up between snapshot and now. **The move was almost executed.**
4. **Strain-wait fallback on node 86 (Priority 3)**: 11332 has def_ratio
   0.45 (5 SP in 323 + 4 SP in 341), 13253 has def_ratio 0.50. Live
   sync HP 200/210 and 196/200 respectively, both well above the
   ratio-adjusted kill_zone (~104, ~90). Strain wait won't crack them
   in this lifetime.

### What did get learned (high value)

1. **Hidden defense source identified**: skills 323 (Armor) + 341
   together produce `defense.threshold.ratio = 0.05 × (SP_323 +
   SP_341)`. Maxes at 0.50. This is the multiplicative defense the
   session 78 strike on 13253 hit (predicted kill at 0.97×maxHP, real
   kill_zone with ratio = 0.45×maxHP). See `mechanics.md` § "Hidden
   defense — `defense.threshold.ratio` source".
2. **Oracle build-snapshot staleness**: `build_refreshed_ts` lags by
   up to ~24h. Cluster scans must always be live-confirmed by spot-check
   on 1–2 candidates before a move. Adding to doctrine.
3. **Soft-target filter v2**: `def_shift = 0 AND def_ratio = 0` (the
   v1 filter `def_shift ≤ 50` returned false positives on Guardian-
   ratio targets).
4. **Two viable session-80 clusters identified and live-confirmed**:
   - **Node 60** (wiuuuu cluster, 7 SCRAP-soft non-guild) for 11224
     (EERIE-hand). 11224 V36 vs typical wiuuuu V14/H24/HP180 — kill_zone
     ~169, full-HP target sits 11 above; needs ~3h strain wait.
   - **Node 62** (buja723 cluster, 8 INSECT-soft non-guild) for 6058
     (SCRAP-hand). buja723 typical V14/H23/HP110–160 — kill_zone
     ~105, well below typical mid-strain HP. **Best near-term
     execution candidate.**
5. **Travel cost from node 86**: 86→60 = 25 hops/125 stam/3 ice cream;
   86→62 = 26 hops/130 stam/4 ice cream. Inventory has 78 ice cream
   so neither limits. Gas budget: ~25–26M for move alone; cluster math
   needs ≥3 kills (≥22.5M kill gas) plus obol/spoils to amortize.

### What was actually executed

Single tx: `harvest_stop(11224)` at 11:55 UTC. 2.43M gas. **Why**:
12649's hit-and-run killer (Nova Heat) showed cross-node attack
pattern; leaving 11224 (sole healthy striker, V36) HARVESTING on
node 86 with no defender presence is an open invitation. Session
ended with 11224 RESTING node 86 (sync HP 107/140 = 76%, strain caught
up post-stop). No travel — cluster was confirmed but cost (25–26M)
demands fuller pre-flight: counter-predator scan on 60 + 62, live
strain on the 8 buja723 / 7 wiuuuu candidates close to strike time.

### State left at session end

- bpeon at room 86. 11224 RESTING (76% HP, no cooldown).
- 6058, 10705, 12225, 15540 RESTING node 86 (per session 78 brief —
  not re-checked).
- 12649 DEAD (entity persists; revive deferred until Onyx Shards or
  REVIVE-item mechanism understood).
- New doctrine in `mechanics.md` (def_ratio formula, oracle staleness)
  and `targeting.md` (soft-filter v2, cluster intel).

### What did NOT get tested (still)

- Recoil HP cost on a successful strike — 79 sessions, 0 kills by us.
- Cooldown duration empirical.
- 11224's 3 unspent SP — still deferred (founder rule).
- REVIVE-type item mechanism (Red Ribbon Gummy, Melkarth Spell Card).
