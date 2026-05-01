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
