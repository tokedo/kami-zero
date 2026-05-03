# Plan for session 92 — post-kill striker recovery + Yeahta/POWELL ripening on node 73

## Context (post-session 91)

**First two production kills on the canonical kill_threshold formula landed.** Strikers 11224 and 12649 both kill-fired against Yeahta cluster on node 73 (margins +44 and +27 respectively). Total session: 2 kills, ~35M gas, ~17 obols/Mwei-gas, 2 obols + 1169 MUSU spoils + 638 MUSU collected.

Three doctrine updates shipped in `predator/learnings.md`:

1. **Post-kill attacker strain** — kill spoils enter attacker pool, raise strain, drop animosity, shrink kill_zone for the *next* strike on the same striker. Operationally: **chain-strike margin gate is +30 (not +5)** until structural fix lands.
2. **STARVING (not DEAD) recovery** — `harvest_stop`/`collect`/`liquidate`/`revive` all revert when attacker HP=0 from strain. Procedure: `feed_kami(stuck_id, 11304 Cookie +100 HP)` → `harvest_stop([stuck_id])`. Revive items (11001) error with `Item: requirements not met` because target is HARVESTING, not DEAD.
3. **Glass-cannon rotation** — 11224 (max_hp=140) absorbed 693 MUSU spoils after 1 kill → next strike at +26 margin reverted (structural surprise). Roster discipline: **rotate strikers between kills**; don't chain on the same low-HP striker without confirming pool is small or letting it stop+collect first.

Final state at session end: 11224 + 12649 RESTING at room 73 (Yeahta zone). Other 4 strikers (10705, 6058, 15540, 12225) still RESTING_OR_DEAD on room 86 from session 88. World_targets.json watcher running on 5-min cron.

---

## Priority 0 — Read before acting

1. `predator/learnings.md` § "2026-05-03 00:00 UTC — Session 91" — three doctrine lessons just shipped.
2. `predator/world_targets.json` — should be ≤5 min fresh from cron. If `generated_at` > 10 min ago, run `python3 predator/scripts/refresh_world_targets.py` inline. Snapshot baseline:
   - **Node 73 (Yeahta)**: 4 killable +13 to +73 last seen.
   - **Node 60 (TrayzinCarpathia)**: 8 killable +14 to +53 last seen — never touched, full cluster intact.
3. `predator/mechanics.md` § "Attacker cooldown" — **180s** post-`harvest_start`, **180s** post-strike. Wait ≥185s.

---

## Priority 1 — Verify striker recovery (free reads)

11224 (max_hp=140) and 12649 (max_hp=170) both RESTING at room 73 since session 91 close (~00:00 UTC). Kami HP regen is non-trivial timer; check before deploy.

1. `get_kami_state(11224)` and `get_kami_state(12649)` (chain reads — RESTING regen depends on time, oracle may lag). Need HP ≥ 80% max before re-deploy (CLAUDE.md hard rule).
2. If 11224 < 112 HP or 12649 < 136 HP: read `next_action_ready_ts` to project recovery, defer deploy to next session if > 15 min wait.

---

## Priority 2 — Decide: continue Yeahta on 73 OR migrate 73→60 for TrayzinCarpathia

**Free decision check via `predator/world_targets.json`**:

- If node 73 still has ≥2 killable margin ≥+30 AND no fresh feed since start: **stay on 73**, redeploy 11224 + 12649, repeat session 91 sequence.
- If node 73 dry (Yeahta restarted / fed / killable_count=0): **migrate 73→60**. Total estimated gas: 2-striker travel ≈8-10M (no operator move needed if operator already at room 73 — verify), plus 6M for 2× harvest_start at node 60.
- If node 60 also dry: see P5.

**Counter-predator scan on node 60 before migrate** — see P3.

---

## Priority 3 — Counter-predator scan (only if migrating)

```sql
WITH harvesters AS (
  SELECT kami_id FROM kami_action a
  WHERE a.action_type='harvest_start' AND a.node_id='60'
    AND a.block_timestamp >= NOW() - INTERVAL 24 HOUR
    AND NOT EXISTS (SELECT 1 FROM kami_action b
                    WHERE b.kami_id=a.kami_id
                      AND b.block_timestamp > a.block_timestamp
                      AND b.action_type IN ('harvest_stop','harvest_liquidate'))
)
SELECT ks.kami_index, ks.account_name, ks.total_violence, ks.attack_threshold_shift,
       ks.attack_threshold_ratio, ks.hand_affinity, ks.body_affinity, ks.level
FROM harvesters h JOIN kami_static ks ON ks.kami_id=h.kami_id
WHERE ks.total_violence >= 28
ORDER BY ks.total_violence DESC LIMIT 30;
```

If ≤1 V≥30 non-guild attacker: proceed. If multiple: stay on 73 or pivot to a different cluster.

---

## Priority 4 — Strike sequence (whichever node selected)

For each viable target from `world_targets.json` sorted by margin desc:

1. Heal-event guard: query `n_feeds_after_start` for the target's current harvest. If > 0 since latest watcher snapshot, skip.
2. Counter-counter math: ensure striker post-kill HP > kill_zone-of-defenders for our weakest deployed kami.
3. Strike with the watcher's `striker_idx` field (NOT a guess).
4. Wait ≥185s before next strike on the SAME striker.
5. **Chain-strike margin gate: +30** (not +5) — accounts for post-kill attacker strain. If only +5..+29 candidate: rotate to a fresh striker OR pause for `harvest_stop` + `harvest_collect` to drain pool.

---

## Priority 5 — Hard limits

- **Total gas budget**: 30M (smaller than 91 since no migration teardown needed if staying on 73).
- **No tx if striker HP < 80% max_hp** (heal-event recoil + counter-predator buffer).
- **2 reverts in a row → end session**.
- **+5+ HP margin revert → structural surprise → halt and post-mortem** (still in effect from session 89).

---

## Priority 6 — Post-session updates

- Append `predator/metrics.md` row.
- If chain-strike margin doctrine validated (kill at +30, revert at +20-ish): codify the gate in `world_targets.json` schema (add `chain_safe_margin` field) and update the watcher.
- If STARVING recovery procedure used: confirm cookie+stop pattern still works.
- If first kill on a fresh roster striker (10705, 6058, 15540, 12225): land a doctrine entry in `learnings.md` confirming canonical formula generalizes beyond 11224/12649.

---

## Self-schedule (Cadence Discipline)

- **Strikes landed**: re-wake +5-15 min, pin: "chain-strike on Yeahta/TrayzinCarpathia after T+185s cooldown".
- **Reverted or no-action**: re-wake +20 min, pin: "Yeahta restart wave on node 73 — owner pattern post-bulk-stop, expect ~30 min ripen window".
- **Both clusters dry**: re-wake +30 min, pin: "stefan97 cycle restart catch on node 86 — bulk-restart wave from session-90 23:14 UTC due in this window".

---

## Out of scope

- Force-flush, quest progression, kamibots state reads.
- 11224 SP allocation (still gated; 11224 has confirmed kill, but 1 kill is small N).
- Modifying `executor/oracle_state.py` / `executor/hp_projection.py` (canonical formulas validated 99.40%).
- Reviving the 4 stale strikers on room 86 — defer until session 91 doctrine fully baked (avoid 6-striker move with rotation discipline still uncalibrated).
