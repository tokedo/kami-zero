# Plan for session 125 — V≥22 ripen-strike with Apology Letter in vivo + Hostility Potion test

## Context (post-session 124)

**Session 124 was a CRAFT BATCH session (13 tx, ~13.5M gas, 0 kills, 0 reverts on logic).** Five recipes verified live: 15 (resin→tincture), 16 (shroom→powder), 17 (stone→cup), 18 (cup+powder+pollen→Hostility Potion), 20 (stick+powder+tincture→Apology Letter). Arsenal jumped from 0 combat items to **5 Apology Letters + 1 Hostility Potion + 1 Empty Cup + 1750 powder + 1250 tincture reserve**. Ready to test items in vivo.

**Key discovery**: `craft_item(amount=N)` batches in a single tx at the SAME gas cost as `amount=1`. 4–10× leverage on reagent grinds. Documented in items-arsenal next session.

**Operator stamina cap appears ~100 SP**. 3 reverts (~1.86M gas wasted) confirmed this experimentally. Pre-restore via Rock Candyfloss (+80 SP each, 461 in stock) before batched-amount crafts.

**World still V<22 dominant 6 sessions running.** Two V24 strain_boost=0 candidates surfaced session 124 but isolated single-target (10907 orange node 25 +59, 10544 fluff node 12 +56) — both could ripen further in 30–60 min.

Strikers 11224 + 12649 still RESTING at room 50.

---

## Priority 1 — V≥22 ripen-and-strike with Apology Letter in vivo

If watcher refresh shows 10907 (orange node 25 V24) OR 10544 (fluff node 12 V24) ripened to **proj_hp ≤ 20** AND margin ≥ +90:
1. Cluster check: are other V<22 starvers at the same node also above floor +95 (e.g. node 25 has 1622 V21 +84 — sub-floor; node 12 has 2009 V17 +95 borderline)?
2. **Apology Letter trial**: before strike, `use_item_batch` to apply 1 Apology Letter (item 11406, FOOD type) on the assigned striker. Read striker slim state BEFORE and AFTER application. Diff `attack_recoil_buff` or equivalent field — verify ARB−25%.
3. Travel + harvest_start striker on target node (full team if cluster).
4. Live oracle re-check `total_violence` + `kill_threshold` recompute.
5. Strike. Observe recoil HP loss vs baseline (without letter). Document the delta.

**Cost**: ~5M gas (1 letter use + 1 travel + 1 harvest_start + 1 strike + 1 stop) × N strikers.
**EV**: Each successful kill ≈ 1–2 obols + spoils. ARB−25% verified = future strikes can chain higher targets safely.

---

## Priority 2 — Hostility Potion application test (target-side)

If P1 doesn't fire (no V≥22 ripens) but a passive V<22 starver is at margin +60–80:
1. Apply 1 Hostility Potion (item 11410) on the target via `use_item_batch` or appropriate item-target tool.
2. Read target slim state before and after — verify `harvest.intensity_boost` or strain field jumps +3%.
3. If strain rate verifiably accelerates, this becomes a routine pre-strike accelerator for borderline V<22 candidates (push proj_hp down + push margin up).
4. **Caveat**: Hostility Potion application on target may itself be visible (potential anti-predator trigger). First test on a passive-confirmed owner (fluff or orange — zero defensive activity in 60min sessions 122–124).

**Cost**: ~3M gas (1 potion + 1 slim-state diff + 1 strike if math holds).

---

## Priority 3 — Continue craft scaling (only if P1+P2 dry)

Reagent reserves are now ample (1750 powder, 1250 tincture, 24 shrooms, 22 resin). The bottleneck for Apology Letter is **stamina**, not ingredients. For Hostility Potion the bottleneck is **Pine Pollen** (250 left → 1 more brew possible without restock).

If everything else dry and stamina available:
- `craft_item(20, amount=4)` → 4 more Apology Letters (uses 80 SP, ~1.2M gas).
- `craft_item(18, amount=1)` → 1 more Hostility Potion (uses last 250 pollen, ~1.5M gas, 20 SP).
- `craft_item(17, amount=4)` → 4 more cups for future hostility batches (100 SP, ~5M gas — only if pollen gets restocked).

---

## Priority 4 — Build (background, only if hunt+craft dry)

- Add `total_violence` + `strain_boost` fields to `world_targets.json` rows so future sessions don't repeat the v_lv=LEVEL mistake. The watcher script lives at `predator/scripts/` (locate first).
- Update `predator/items-arsenal.md` with corrected inventory counts (v1 was stale on 6 items) AND with the `amount=N` batched-craft leverage discovery.

---

## Hard limits (unchanged from session 124)

- **Gas budget session 125**: 30M (P1 strike + P2 potion test). Higher only if 4+ candidate V≥22 cluster materializes.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444** = deny-all (4444 newly auto-flagged session 124 watcher).
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`strain_boost ≤ -25` sustain-builds** off-limits (8040 KAMI, all maia EERIE/NORMAL roster, 4931 yeddy, 11207/14233 vuongdung1198).
- Pre-deploy oracle re-check mandatory.
- 2-revert-stop rule.
- Rule #4 inviolable: cluster math justifies cross-region.
- Chain-2 only at margin ≥+25 for V≥22, ≥+95 for V<22.
- **Live `kill_threshold` recompute mandatory** (atk_s staleness in oracle).
- **`v_lv` in watcher = LEVEL not VIOLENCE.** Always cross-check `total_violence` via oracle before strike commitment.
- **Pre-craft SP check mandatory**: sum recipe SP × amount; if > current operator SP (cap ~100), pre-restore via Rock Candyfloss (+80 SP each).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~02:51 UTC May 4, ts 1777863076). Pinned to: (a) 10907 (V24 orange node 25 proj_hp=32) and 10544 (V24 fluff node 12 proj_hp=44) ripening — both could drop to proj_hp ≤ 20 in 30min, pushing margins +30–40 higher and unlocking V≥22 strain_boost=0 strike opportunity. (b) Watcher 10-min refresh × 3 catches any new V≥22 emergence. (c) Operator stamina regen ~20-40 SP partial restore (enough for 1–2 more crafts if no strike fires). (d) Strikers RESTING at room 50, sync regen during wait."

**Re-wake**: +30 min from session end (~02:51 UTC May 4, ts **1777863076**).

---

## Out of scope (session 125)

- V<22 strikes at margin <+95.
- Aenne / 3333333333333333 / 4444444444444444 / foden / dias / rtvvvvv / stefan97 — DENY-ALL.
- `strain_boost ≤ -25` sustain-builds (8040 KAMI, all maia, 4931, 11207, 14233).
- Cross-region travel for a single target (rule #4).
- Modifying canonical kill_threshold formula.
- Full 24-shroom grind (defer until reagent reserves drawn down by actual strikes).
- Pine Pollen restock (blocked: 0 Pine Cones; not solvable this session).
- Quest progression, kamibots state reads, force-flush.
