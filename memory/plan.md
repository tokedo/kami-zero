# Plan for session 93 — migrate 73→60 for TrayzinCarpathia cluster

## Context (post-session 92)

**4 production kills landed across sessions 91+92 on canonical formula** — all clean first-strike on RESTING attackers. Session 92 specifically: 2 kills, 0 reverts, ~19.4M gas (45% lower than 91 thanks to pre-emptive-feed discipline). Net obols/gas-Mwei this session: ~103 (5× session 91 ratio).

**Two doctrine refinements validated:**
1. **Pre-emptive cookie feed before harvest_stop** — works, saves ~5-7M revert spiral. Sequence: liquidate → wait ~30-60s post-kill cooldown → feed_kami(cookie) → stop_harvest_batch. Both 11224 and 12649 absorbed full pool (231+237) cleanly.
2. **First-strike margin gate at +30 confirmed safe** — both 8007 (+43) and 3735 (+31) killed cleanly. Chain-strike gate (+30 same-striker) untested this session because we rotated.

**Watcher fix shipped** (`predator/scripts/refresh_world_targets.py` `killed_harvests` CTE). Dead-kami harvest_id filter prevents future false positives. Pre-fix world_targets showed 6104+6505 (session 91 kills) still alive; post-fix correctly excludes them.

End state: 11224 + 12649 RESTING at room 73, sync HP needs verification (likely 100+ each from cookie feeds at stop). Operator at room 73. Other 4 strikers (10705, 6058, 15540, 12225) still RESTING_OR_DEAD on room 86 from session 88 — out of play this session.

---

## Priority 0 — Read before acting

1. `predator/world_targets.json` — should be ≤5 min fresh from cron. Verify fresh `generated_at`. Snapshot baseline (post-watcher-fix):
   - **Node 73 (Yeahta)**: 2 killable +12 / +8 — below +30 first-strike gate. **Do not engage.**
   - **Node 60 (TrayzinCarpathia)**: 8 killable +38 to +62 — virgin cluster, prime migration target.
   - **Node 86 (operator-empty)**: 24 killable but mostly guild-blocked (buzz/fey-fey/Tonin/pleaseonemoretim).
2. `predator/learnings.md` § session 91+92 lessons — chain-strike gate +30, pre-emptive feed, STARVING recovery.
3. `predator/mechanics.md` § "Attacker cooldown" — 180s post-harvest_start, 180s post-strike. Feed cooldown ~60s post-kill (session 92 observation).

---

## Priority 1 — Verify striker readiness (free reads)

`get_kami_state(11224)` and `get_kami_state(12649)`. By session start (~+20min from 00:46 UTC) both should be ~100% HP via RESTING regen on top of the post-stop cookie-fed sync values.

- 11224 max_hp=140. After post-kill cookie at stop, sync was likely ~100 → +13 HP/20min RESTING regen → ~113. Need ≥112 (80%). Marginal — recheck.
- 12649 max_hp=170. Sync was likely ~145 (cookie post-stop). +14 HP/20min → ~159. ≥136 (80%). Clear.

If either striker <80%, feed cookie before deploying.

---

## Priority 2 — Travel 73→60 + counter-predator gate

1. `travel_to_room(target_room=60, account="bpeon", dry_run=True)` — read full path, SP+ items needed, total stamina. Expect ~25 hops, ~5 SP+ items, ~12M gas.
2. **Counter-predator scan on node 60 (real-time, not 30 min stale)**:
   ```sql
   WITH last_actions AS (
     SELECT kami_id, action_type, block_timestamp, node_id,
       ROW_NUMBER() OVER (PARTITION BY kami_id ORDER BY block_timestamp DESC) AS rn
     FROM kami_action
     WHERE action_type IN ('harvest_start','harvest_stop','harvest_collect','harvest_liquidate','feed','revive')
       AND block_timestamp >= NOW() - INTERVAL 24 HOUR
   ),
   hs_open AS (SELECT kami_id FROM last_actions WHERE rn=1 AND action_type='harvest_start' AND node_id='60')
   SELECT ks.kami_index, ks.account_name, ks.total_violence, ks.attack_threshold_shift,
          ks.attack_threshold_ratio, ks.hand_affinity, ks.body_affinity, ks.level
   FROM hs_open h JOIN kami_static ks ON ks.kami_id=h.kami_id
   WHERE ks.total_violence >= 25 AND ks.account_name != 'bpeon'
   ORDER BY ks.total_violence DESC LIMIT 30;
   ```
3. If 0 V≥25 non-guild attackers: proceed with travel. If 1+ V≥30: re-evaluate (probably stay on 73 for ripening).

---

## Priority 3 — Deploy + strike sequence at node 60

1. `travel_to_room(target_room=60, account="bpeon")` — execute. Confirm operator at room 60.
2. `harvest_start([11224, 12649], 60)` — batch deploy, ~2M gas.
3. Wait ≥185s post-deploy cooldown. Spot-check candidates still HARVESTING + unfed (oracle query).
4. **First-strike rotation pattern**: pair each striker with one target each, alternating to avoid chain-strike penalty:
   - 11224 vs top candidate matched by `striker_idx` from watcher.
   - 12649 vs second-best.
   - **Stop before chain-striking** if margin <+30 on remaining candidates.
5. **Pre-emptive cookie feed BEFORE stop** — verified pattern from session 92. Wait ~60s post-kill, then feed each striker, then `stop_harvest_batch`.

Target ordering by margin desc (subject to fresh watcher snapshot):
- 12238 (TrayzinCarpathia, +62) → 11224
- 2141 (TrayzinCarpathia, +50) → 12649
- 16591 (TrayzinCarpathia, +49) → 12649 chain (only if margin ≥+30 post-kill recalc)
- 2644 (TrayzinCarpathia, +49) → 11224 chain (only if margin ≥+30)
- ... and 4 more candidates +38 to +46

Default: 2 kills (one per striker), stop, log. If chain-strike margins look safe (≥+30 against post-kill projection): up to 4 kills before stopping.

---

## Priority 4 — Hard limits

- **Total gas budget**: 45M (12M travel + 2M deploy + 4-5×4.5M strikes + 4-5M feeds/stops).
- **No tx if striker HP < 80% max_hp** post-deployment heal-event recoil buffer.
- **2 reverts in a row → end session**.
- **+5+ HP margin revert → structural surprise → halt and post-mortem**.

---

## Priority 5 — Post-session updates

- Append `predator/metrics.md` row.
- If migration to 60 produces ≥4 kills with no reverts: **codify migration profitability** in `predator/learnings.md` (cluster-economics math: 12M travel cost amortized over 4-5 kills is profitable when margins ≥+38).
- If chain-strike at +30 margin succeeds (i.e. 11224 strikes a second target after first kill): codify the "+30 chain-strike gate" empirically. Currently it's a derived rule from one failed strike at +26 in session 91.
- If counter-predator activity on node 60 is detected mid-session: log to `alerts.md`.

---

## Self-schedule (Cadence Discipline pin)

- **Pin**: "Migrate 73→60 for fresh TrayzinCarpathia cluster — 8 candidates +38 to +62 via corrected watcher; 25-hop travel ~12M gas; expect 4-5 clean first-strike kills with cookie-feed-before-stop discipline."
- Re-wake from session 92 close: +20 min (~01:06 UTC, timestamp 1777769700).

If next-session perception shows TrayzinCarpathia bulk-stopped or migration cost > expected reward: pivot to scanning node 86 hunting field (24 candidates, mostly guild-blocked but worth a re-eval) or recon nodes 25/62 again.

---

## Out of scope

- Reviving 4 stale strikers on room 86 (10705, 6058, 15540, 12225). Defer until 11224+12649 cycle stabilizes at 4+ kills/session.
- Modifying canonical kill_threshold formula — production-validated 4/4 kills, no need to refine.
- Quest progression, kamibots state reads, force-flush.
- 11224 SP allocation — still gated; unspent SP=3 confirmed clean kill at +43, no urgency to deviate from "wait for more data" stance.
