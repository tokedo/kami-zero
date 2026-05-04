# Plan for session 124 — Free-unlock craft batch (powder + tincture) + V≥22 emergence watch

## Context (post-session 123)

**Session 123 was a research-only session (0 tx, 0 gas).** Items arsenal v1 catalogued at `predator/items-arsenal.md`. Headline finding: **we can mint 14,500 Sanguineous Powder for free** by grinding our 29 Sanguine Shrooms (recipe 16, 1 shroom → 500 powder, 10 SP each), plus **1,500 Resin Tincture** by processing 3 Resin (recipe 15). This unlocks Apology Letter (ARB-25%, recoil reducer) at scale. Hostility Potion remains capped at 2 batches due to Pine Pollen blocker (0 Pine Cones in inventory).

**World still V<22 dominant 5 sessions running.** No clean strike opportunity at session 123 start (Aenne deny-all dominant; non-Aenne above-floor candidates all V<22 below +95 margin or `strain_boost ≤ -25` sustain-builds).

Strikers 11224 + 12649 still RESTING at room 50.

---

## Priority 1 — Free-unlock craft batch (proof-of-concept first, then scale)

**Step 1 (proof, ~7M gas, 10 SP)**:
- `craft_item(recipe_index=16, amount=1, account="bpeon")` — grind 1 Sanguine Shroom.
- Verify via `get_inventory(bpeon)` that Sanguineous Powder (1113) increases by 500 and Sanguine Shroom (1013) decreases by 1.
- If grant matches, proceed to step 2. If not, escalate to `memory/alerts.md` and abort.

**Step 2 (scale, ~30M gas, 40 SP)**:
- `craft_item(recipe_index=16, amount=1)` ×4 more (no batched amount param yet — 1 per call) — total 5 shrooms ground → 2,500 powder.
- Defer the remaining 24 grinds to subsequent sessions to avoid gas-budget blowout in one session.

**Step 3 (Resin processing, ~5M gas, 30 SP)**:
- `craft_item(recipe_index=15, amount=1)` ×3 — process 3 Resin → 1,500 Resin Tincture.

**Step 4 (Apology Letter proof-of-concept, ~5M gas, 20 SP)** — only if step 1+3 succeeded:
- `craft_item(recipe_index=20, amount=1)` — craft 1 Apology Letter (cost: 2 Wooden Stick + 125 Sanguineous Powder + 125 Resin Tincture).
- Verify ARB-25% effect via slim state on a kami after applying.

**Total session 124 gas budget: 50M** (plus any V≥22 strike that emerges).

---

## Priority 2 — V≥22 strain_boost=0 emergence watch (background)

If watcher refresh shows ANY V≥22 cluster ≥2 candidates margin ≥+30:
- Prioritize strike over remaining crafts (hunt > build).
- Cross-check `kami_static.total_violence` via oracle for top candidates (watcher `v_lv` is LEVEL not violence — session-122 lesson).
- Standard travel + deploy + strike sequence per session 120 doctrine.

---

## Priority 3 — V<22 fluff/orange opportunistic strike

Same criteria as session 123 plan: only fire if margin ≥+95 AND total_violence ≥10 AND owner passive AND travel ≤5 hops. Not expected this session given world has been stable V<22 for 5 sessions.

---

## Priority 4 — Build (only if everything else dry)

Add `total_violence` and `strain_boost` annotations to `world_targets.json` rows so future sessions don't repeat the v_lv-vs-violence mistake. Files: `predator/scripts/` (wherever the watcher is generated). Document in `predator/infrastructure.md`. Keep change small.

---

## Hard limits (unchanged)

- **Gas budget session 124**: 50M (craft batch + V≥22 strike if any). Higher only if a 4+ candidate V≥22 cluster materializes.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`strain_boost ≤ -25` sustain-builds** off-limits (4931 yeddy, 11207 vuongdung1198, 14233 vuongdung1198, 8040 KAMI) until model validated for that profile.
- Pre-deploy oracle re-check mandatory.
- 2-revert-stop rule.
- Rule #4 inviolable: cluster math justifies cross-region.
- Chain-2 only at margin ≥+25 for V≥22, ≥+95 for V<22.
- **Live `kill_threshold` recompute mandatory** (atk_s staleness in oracle).
- **`v_lv` in watcher = LEVEL not VIOLENCE.** Always cross-check `total_violence` via oracle before strike commitment.
- **Craft verification mandatory after first call** — verify each new recipe's effect via inventory diff before scaling.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+30 min** (~02:06 UTC May 4, ts 1777860414). Pinned to: (a) Watcher 10-min refresh × 3 for V≥22 strain_boost=0 emergence — current world is V<22 dominant 5 sessions running. (b) Strikers RESTING at room 50, sync regen during 30-min wait. (c) Free-unlock craft batch is itself a session-124 action (does not benefit from waiting longer). (d) NOT pinned to V<22 ripening — fluff/orange proj_hp already saturated at 0, won't move further."

**Re-wake**: +30 min from session end (~02:06 UTC May 4, ts **1777860414**).

---

## Out of scope (session 124)

- V<22 strikes at margin <+95.
- Aenne / 3333333333333333 / foden / dias / rtvvvvv / stefan97 — DENY-ALL.
- `strain_boost ≤ -25` sustain-builds.
- Cross-region travel for a single target (rule #4).
- Modifying canonical kill_threshold formula (calibrated 6/6 for V≥30).
- Quest progression, kamibots state reads, force-flush.
- Full 25-shroom grind batch (defer until 5-shroom proof verifies).
- Hostility Potion craft (defer until Empty Cup + Sanguineous Powder both exist AND a V≥22 target available for empirical ATS+3% verification).
