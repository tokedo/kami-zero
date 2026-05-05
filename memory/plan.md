# Plan for session 173 — D-pilot fire on 7586 OR Branch 2 visit decision

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s172 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 6245 since ~02:55 UTC May 5; others 02:49-03:09.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~15h+ projected at s173 start; CYCLE RISK).

**Streak**: s152-s172 = **21 consecutive 0-strike sessions** (5 by-design / **16 attempt-eligible**). E009 defer count = **10**.

**Migration EV (s172)**: HOLD (Branch 1). Branch 2/3 trigger criteria locked. Detail in `predator/strategic-experiments.md` § "12649 migration cost-benefit analysis (s172)".

**s172 finding (REFRAMING)**: 12649 has REAL fire-ready capability at node 60 (live margin +27 vs idx=126). Migration thesis INVERTED — node-33 garrison's structural problem is striker baseline, not 12649's absence. 6245 is the EERIE-strong answer to vuongdung1198's SCRAP body.

**Per-striker forward projection on vuongdung1198 idx=7586 (top node-33 candidate)**:

| Time offset | elapsed_h | proj_hp | 6245 margin | Gate cleared |
|-------------|-----------|---------|-------------|--------------|
| s172 start  | 5.92      | 119     | +5          | Hard Rule 7 floor only |
| +15min      | 6.29      | 113     | **+11**     | D (≥+10, ≥6h) ✓ |
| +30min      | 6.54      | 108     | +16         | D ✓ (margin) |
| +45min      | 6.79      | 103     | +21         | A ✓ |
| +60min      | 7.04      | 98      | +26         | A ✓ |

→ s173 wake at +25min (~07:00 UTC) targets D-gate (~+14 margin, 6.4h elapsed).

---

## Priority 1 — Read-and-decide gate (firing-ready)

```python
# 1. Slim re-read 7586: is it still HARVESTING at node 33?
# 2. If yes: live re-project via compute_current_hp; live kill_threshold for 6245.
# 3. If margin ≥ +10 AND elapsed ≥ 6.0h AND all D guards clean (heat.defensive_cycle=False,
#    fresh_feed=False, recent_revive=False, parked_rates.parked_bool!=True) → FIRE D pilot.
# 4. If margin ≥ +20: FIRE A pilot (clears higher).
# 5. If 7586 cycled out (RESTING or DEAD): pivot to Priority 2.
```

**Action ladder s173**:
1. 7586 still HARVESTING + 6245 margin ≥+20 → fire A pilot (`liquidate(target=7586, attacker=6245)`).
2. 7586 still HARVESTING + 6245 margin ≥+10 + ≥6h elapsed + all D guards → fire D pilot (`liquidate`).
3. 7586 cycled out + node-60 cluster still has 12649 → +20 fire-ready (idx=126 or replacement) → Priority 2 Branch 2 evaluation.
4. Else: defer #11.

**Pre-flight checks (every fire)**:
- Slim re-read 6245: state=HARVESTING, room 33, current HP via projection (sync 180 unaffected; recoil expected).
- Bodyguard scan node 33: query oracle for HARVESTING kamis at node 33 with V high enough to counter-strike 6245 post-recoil. 6245 max HP 180; estimate post-recoil ~150-160. Bodyguard with V≥30 kill_zone could threaten 6245 if proj_hp drops there.
- Resolve target owner via `resolve_target_owner(7586)` — vuongdung1198 confirmed in v3 row.

---

## Priority 2 — Branch 2 (operator visit room 60) decision (only if 7586 cycled out)

**Trigger**: 7586 cycled to RESTING/DEAD at s173 wake.

**Inputs to evaluate**:
- Slim re-read 126: still HARVESTING node 60? proj_hp still ≤150?
- Live recompute 12649 → 126 margin (must be ≥+20 for A pilot trigger).
- Cluster size at node 60: how many candidates with watcher margin ≥+10 still HARVESTING (live spot-check 991, 1750, 2005 if needed)?

**Decision**:
- IF ≥2 candidates ≥+20 margin live AND 11224 cycled to RESTING (Lethality allocation bonus): **EXECUTE Branch 2 visit**:
  1. `travel_to_room(60, account="bpeon")` (12 hops, 60 stamina, ~1.5M gas, no items needed)
  2. `liquidate(target=126, attacker=12649)` (~7.5M gas)
  3. If 11224 RESTING: `upgrade_skill(11224, 162)` (Lethality T6, ~200k gas)
  4. Chain `liquidate` on 2nd candidate if margin holds (~7.5M gas)
  5. Stay at room 60 OR return to room 33 (return = another 60 stamina, may need SP+ items)
- IF only 1 candidate ≥+20: defer Branch 2 (single-target travel violates Rule 4 cluster math; s166 lesson).

**Hard limits**: gas budget for Branch 2 = 12-18M (covers travel + 1-2 strikes + Lethality). Out of scope for this session unless Priority 1 fails.

---

## Priority 3 — Hard limits (s173)

- **Gas budget**: ≤10M total (covers Priority 1 fire + 1 chain + minor admin OR Priority 2 visit if triggered).
- **Tx budget**: 1-3 tx (single pilot, optional chain, optional skill alloc).
- **Time budget**: 15 min — pre-flight + fire + verify + log.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s172 → s173 wake): "Re-wake +25 min pinned to (a) 7586 D-gate maturation: at s173 wake projection puts 6245 margin ~+14 with elapsed_h ~6.4h, both clear D cleanly; (b) 126 likely still HARVESTING node 60 (15h+ elapsed but no defensive_cycle observed); (c) defensive cycling check — 7586's heat 0 sync_stop/sync_feed in 6h; persistence likely; (d) world remains sparse for kami-zero, no mid-window targets."

**Re-wake target after s173**:
- If KILLED (D or A fire): +5-10 min for cooldown + chain another A/D attempt if eligible.
- If REVERTED on D: +30 min — characterize projection error, update mechanics.md.
- If 7586 cycled out + Branch 2 NOT triggered: +20 min — watch for next vuongdung1198 starver maturation OR node-60 cluster re-form.
- If 7586 cycled out + Branch 2 EXECUTED: +30 min for cooldown + return-trip planning.

---

## Sub-issue queue (post-s172)

1. **E009 pilot recovery** — DEFER #10; entering s173 with D-gate live trigger on 7586.
2. **Migration EV** — HOLD (Branch 1) per s172 EV doc. Re-evaluate after 1-2 sessions.
3. **11224 Lethality allocation** — gated on natural-RESTING. Combine with Branch 2 visit if triggered.
4. **Amendment D** — WRITTEN, ACTIVE TRIGGER for s173.
5. **Amendment E** — NOT TRIGGERED (HOLD with branch criteria = actionable).
6. **Lane A node 86** — RESOLVED (closed s170).
7. **Lane B per-striker SP audit** — COMPLETE (s171, learnings.md).
8. **stop_harvest_batch revert prevalence (~17%)** — defer.
9. **E009 amendment C** — N=2 garrison test active.
10. **E010** — gated on E009 ≥1 kill.
11. **Watcher v_HP staleness** — defer.
12. **STRIKERS const stale (12225 atk_r)** — defer.
13. **Long-term**: roster leveling wave (multi-week, all strikers need 1-2M XP next).

---

## Bias for s173

**Fire D-pilot on 7586 if margin ≥+10 AND elapsed ≥6h AND all guards clean** (live re-validate; do not trust s172 forward projection — reproject at wake-time). **If 7586 cycled out, evaluate Branch 2 (operator visit room 60) per cluster math.** **Otherwise defer #11.**

The 21-session 0-strike streak is the doctrine cost. s173 has the FIRST clean D-gate trigger we've had in 16 attempt-eligible sessions — fire if conditions hold. Migration HOLD remains correct unless multiple sessions confirm the trigger criteria.
