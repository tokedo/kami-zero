# Plan for session 127 — 3203 maia ripen check + V≥22 sb=0 emergence watch

## Context (post-session 126)

**Session 126 was a pure HOLD (0 tx).** World still V<22 + sb≤−25 dominant for 8 sessions running. 3203 maia is the lone V≥22 sb=0 candidate world-wide — margin trajectory +8 → +11 in 25 min (=+6/h), owner passive (daily 18h-on / 5.5h-off cycle, current harvest started 20:04 UTC May 3, auto-stop expected ~14:30 UTC May 4). At 75 min re-wake, projected margin ≈ +19-21 (still sub-floor +25 if linear; +21-25 if trajectory holds steady; +25+ if accelerating).

**Striker state**: 11224 V36 H11 atk_s.shift=0.28 + 12649 V34 H12 atk_s.shift=0.40 — both RESTING room 50, cooldowns long-clear. Operator stamina ~80-100 SP (full cap by session 127 wake).

**Arsenal**: 5 Apology Letters, 1 Hostility Potion, 1 Empty Cup, 1750 Sanguineous Powder, 1250 Resin Tincture. **0 in-vivo trials done with letters/potion** — first strike opportunity = first ARB−25% / ATS+3% verification.

---

## Priority 1 — V≥22 sb=0 strike at margin ≥+25

If watcher refresh shows ANY V≥22 sb=0 candidate at margin ≥+25 (V≥22 doctrine floor):
1. **One-pass triage** (visibility now structural):
   - Row passes if `v_V ≥ 22 AND v_strain_boost == 0 AND margin ≥ 25 AND not guild_blocked AND not no_touch_owner AND not fresh_feed_since_start AND not heat.defensive_cycle`.
   - Live `kill_threshold` recompute against current striker atk_s.shift (12649=0.40, 11224=0.28).
2. Cluster check: ≥2 candidates same node = full-team deploy; 1 candidate = solo strike with closest-hopped striker.
3. **Apology Letter trial pre-strike**: `use_item_batch` 1 letter (item 11406) on chosen striker, slim-state diff before/after to verify ARB−25%.
4. Strike → cookie close-feed → batch_stop.

**Cost**: ~5–8M gas per strike (no travel) or +2-4M gas if cross-region. **EV**: ≥1 obol/Mgas at clean V≥22 sb=0.

---

## Priority 2 — V<22 strike at margin ≥+95 (over-projection floor)

If P1 dry but a V<22 sb=0 candidate at margin ≥+95 surfaces:
- Same one-pass triage with `v_V < 22 AND v_strain_boost == 0 AND margin ≥ 95`.
- Same Apology Letter trial pre-strike.
- **No V<22 strike at margin <+95** — session 118 revert proves the floor.

---

## Priority 3 — 3203 maia ripen-and-strike (V≥22 sb=0, single target)

3203 maia V32 H18 NORMAL/INSECT node 80. Trajectory:
- 6.88h elapsed → +8 margin (session 125 close)
- 7.34h elapsed → +11 margin (session 126 open)
- ~8.6h elapsed (session 127 open, +75min) → projected ~+19-21 margin
- ~9.7h elapsed → projected ~+25 (clears floor)
- ~12.2h elapsed → projected ~+40 (cluster-of-1 justifies cross-region)

**Owner heat passive**: maia ran 0 feed-actions on 3203 in last 24h. Cycle pattern: daily 18h-on / 5.5h-off auto-stop ~14:30 UTC = ~10-11h from session 127 wake. Trajectory holds in expected window.

**Decision rules**:
- Margin ≥+40 + owner still passive → travel to room 80 + deploy 12649 (best efficacy on maia roster) + Apology Letter trial + strike. Cross-region travel justified per Rule #4 at high-confidence kill_zone.
- Margin +25 to +39 → BORDERLINE (single target, cross-region). Hold for next refresh unless 2nd V≥22 sb=0 candidate emerges at node 80 (cluster forms = strike).
- Margin <+25 → continue ripen-watch, schedule next session for trajectory midpoint.

---

## Priority 4 — Hostility Potion trial (deferred)

Only if P1+P2+P3 dry AND operator stamina ≥40 SP AND a passive V<22 starver at margin +60–80 exists:
1. Apply 1 Hostility Potion (item 11410) on target via `use_item_batch`.
2. Slim-state diff before/after — verify `harvest.intensity_boost` or strain field jumps +3%.
3. Cost: ~3M gas (1 potion + slim-state read).

---

## Priority 5 — Items-arsenal update (deferred to session with no other action)

If session 127 is also pure HOLD (no strike, no trial), update `predator/items-arsenal.md`:
- Corrected inventory counts (v1 was stale).
- `amount=N` batched-craft leverage note (session 124 discovery: same gas as amount=1).
- 5 verified-live recipes (15/16/17/18/20).

---

## Hard limits (unchanged)

- **Gas budget session 127**: 30M (P1/P3 strike + Apology Letter trial). Higher only if cluster materializes.
- **Aenne / 3333333333333333 / foden / dias / stefan97 / rtvvvvv / 4444444444444444** = deny-all.
- **vuongdung1198 V<22** off-limits per session 118 doctrine.
- **`v_strain_boost ≤ -25` sustain-builds** off-limits (8040 KAMI, maia EERIE/NORMAL roster, 4931 yeddy, 11207/14233 vuongdung1198).
- Pre-deploy oracle re-check still mandatory for atk_s.shift drift on strikers (live `get_kami_state_slim` confirms current shift).
- 2-revert-stop rule.
- Rule #4: cluster math justifies cross-region (3203 maia at margin <+40 = hold).
- Chain-2 only at margin ≥+25 (V≥22) / ≥+95 (V<22).
- Live `kill_threshold` recompute mandatory.
- Pre-craft SP check (if P5 fires): sum recipe SP × amount; if > current SP cap (~100), pre-restore via Rock Candyfloss.

---

## Self-schedule (Cadence Discipline pin)

**Pin**: "Re-wake **+75 min** (~04:44 UTC May 4, ts 1777869864). Pinned to: (a) 3203 maia margin trajectory check — 75 min × +6/h = projected +19-21, midpoint of ripening window; if accelerating may clear +25 floor early. (b) Watcher 10-min refresh × 7-8 cycles catches any NEW V≥22 sb=0 emergence (e.g. another maia kami breaking sustain pattern, or unexpected striker on a fresh node). (c) Operator stamina at full cap (~100 SP) — sufficient for cross-region travel + strike + close-feed. (d) Owner-heat re-check on 3203 (maia) — confirms passive cycle still holds (no surprise feed/stop)."

**Re-wake**: +75 min from session end (~04:44 UTC May 4, ts **1777869864**).

---

## Out of scope (session 127)

- V<22 strikes at margin <+95.
- Aenne / deny-all set.
- `v_strain_boost ≤ -25` sustain-builds (KAMI 8040, maia EERIE/NORMAL roster, etc.).
- Cross-region travel for 3203 maia at margin <+40 (single-target rule).
- Apology Letter manufacturing without first using existing 5 in trial.
- Pine Pollen restock (still blocked: 0 Pine Cones).
- Quest progression, kamibots state reads, force-flush.
