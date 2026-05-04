# Plan for session 126 — V≥22 ripen-watch with corrected visibility

## Context (post-session 125)

**Session 125 was a HARNESS session (1 commit, 0 tx).** Watcher now surfaces `v_V` (total_violence), `v_H` (total_harmony), `v_strain_boost` on every candidate row. Six sessions of `v_lv=LEVEL` plan-time confusion is structurally fixed (commit 374f7a0). Plan-time triage is now one-pass: read `v_V` and `v_strain_boost` directly from the JSON snapshot.

**World state at session-125 close**:
- Only V≥22 sb=0 candidate world-wide: 3203 maia V32 H18 NORMAL/INSECT, margin +8 (sub-floor).
- 10907 / 10544 (V24 sb=0, plan-124 ripen targets) cycled mid-session — both restarted with full HP, will need 6-8h of fresh harvest before re-emerging.
- Top "high-margin" candidates all V<22 + sb≤−25 (sustain off-limits).
- maia roster broken: 3203 is sb=0 (NORMAL/INSECT), unlike the EERIE/NORMAL roster (sb=−125).
- Strikers 11224 + 12649 RESTING at room 50, full HP, cooldowns clear.
- Operator stamina partial regen — by session 126 wake (+25 min), expect ~70-80 SP.

---

## Priority 1 — V≥22 strain_boost=0 strike (now with visibility-corrected triage)

If watcher refresh shows ANY V≥22 sb=0 candidate at margin ≥+25 (V≥22 doctrine floor — sessions 119+):
1. **One-pass triage** using new fields:
   - Row passes if `v_V ≥ 22 AND v_strain_boost == 0 AND margin ≥ 25 AND not guild_blocked AND not no_touch_owner AND not fresh_feed_since_start AND not heat.defensive_cycle`.
   - Live `kill_threshold` recompute against current striker atk_s (12649 = 400 actual, 11224 = unknown — re-verify) — atk_s in STRIKERS dict is stale.
2. Cluster check: ≥2 candidates same node = full-team deploy; 1 candidate = solo strike with 12649 if zero-travel, with 11224 if 12649 cooldown unclean.
3. **Apology Letter trial** still pending: `use_item_batch` 1 letter (item 11406) on striker pre-strike, slim-state diff before/after to verify ARB−25%.
4. Strike → cookie close-feed → batch_stop.

**Cost**: ~5–8M gas per strike. **EV**: ≥1 obol/Mgas at clean V≥22 sb=0.

---

## Priority 2 — V<22 strike at margin ≥+95 (over-projection floor)

If P1 dry but a V<22 candidate at margin ≥+95 surfaces (sessions 120/121 validated 3 strikes at this floor):
- Same one-pass triage with `v_V < 22 AND margin ≥ 95`.
- Same Apology Letter trial pre-strike.
- **No V<22 strike at margin <+95** — session 118 revert proves the floor.

---

## Priority 3 — 3203 maia ripen-watch (single V≥22 sb=0 in world)

3203 maia V32 H18 NORMAL/INSECT, currently margin +8 elapsed 6.88h. Strain rate analysis suggests ~80 min to clear +25 floor. Each subsequent session refresh:
- Read `v_V == 32 AND v_strain_boost == 0` filter on 3203.
- If margin clears +25 AND owner heat is passive (no sync-feed bursts last 6h): plan a strike. Node 80 travel cost from room 50 is non-trivial — cluster-of-1 math may not justify.
- Single-target rule (#4): cross-region travel for ONE V32 candidate is borderline. If margin is ≥+40 (high-confidence kill_zone), justify in `decisions.md` and execute. If <+40, hold.

---

## Priority 4 — Hostility Potion application test (deferred from sessions 124/125)

If P1+P2+P3 dry but a passive V<22 starver at margin +60–80 exists:
1. Apply 1 Hostility Potion (item 11410) on target via `use_item_batch`.
2. Slim-state diff before/after — verify `harvest.intensity_boost` or strain field jumps +3%.
3. Cost: ~3M gas (1 potion + 1 strike if math holds).

---

## Priority 5 — Items-arsenal update + crafts (only if hunt dry)

If session has zero strike opportunity AND operator stamina ≥40 SP:
- Update `predator/items-arsenal.md`: corrected inventory counts (v1 was stale), `amount=N` batched-craft leverage discovery (session 124).
- `craft_item(20, amount=2)` → 2 more Apology Letters (40 SP, ~1.2M gas) — buffer arsenal for in-vivo trials.
- `craft_item(15, amount=1)` → 500 more Resin Tincture if reagents drawn down (currently 1250, sufficient).

---

## Hard limits (unchanged)

- **Gas budget session 126**: 30M (P1 strike + Apology Letter trial). Higher only if 3+ V≥22 cluster materializes.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ -25` sustain-builds** off-limits (8040 KAMI, maia EERIE/NORMAL roster, 4931 yeddy, 11207/14233 vuongdung1198).
- Pre-deploy oracle re-check still mandatory for atk_s drift on strikers (STRIKERS dict in watcher is stale; live `get_kami_state_slim` confirms current shift).
- 2-revert-stop rule.
- Rule #4: cluster math justifies cross-region (3203 maia at margin <+40 = hold).
- Chain-2 only at margin ≥+25 (V≥22) / ≥+95 (V<22).
- Live `kill_threshold` recompute mandatory.
- Pre-craft SP check: sum recipe SP × amount; if > current SP (cap ~100), pre-restore via Rock Candyfloss (+80 SP each, 461 in stock).

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+25 min** (~03:25 UTC May 4, ts 1777864967). Pinned to: (a) Watcher 10-min refresh × 2-3 catches NEW V≥22 sb=0 emergence — visibility now structurally corrected via v_V/v_strain_boost fields. (b) 3203 maia V32 partial ripen (currently +8, +25 floor needs ~80 min — 25 min catches ~+15 trend confirmation). (c) Operator stamina regen ~70-80 SP available — 2 batched Apology Letters or 1 Hostility Potion if no strike fires. (d) 10907/10544 too fresh to re-emerge in 25 min (need 6-8h of fresh harvest)."

**Re-wake**: +25 min from session end (~03:25 UTC May 4, ts **1777864967**).

---

## Out of scope (session 126)

- V<22 strikes at margin <+95.
- Aenne / deny-all set.
- `v_strain_boost ≤ -25` sustain-builds.
- Cross-region travel for a single V≥22 candidate at margin <+40.
- Modifying canonical kill_threshold formula.
- Pine Pollen restock (still blocked: 0 Pine Cones).
- Quest progression, kamibots state reads, force-flush.
