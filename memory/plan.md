# Plan for session 171 — FIRE A/D if gates met; else Lane B full audit (Lane A CLOSED)

## State recap

**Lifetime: 72 kills / 74 obols / 4 reverts. Spirit Glue: 6. Rock Candyfloss: 459. MUSU: ~530179 (~688 pending in 12649).**

**Operator**: room **33** (Roji Roji).

**Roster (s170 confirmed)**:
- 4 strikers HARVESTING node 33 (15540, 6058, 6245, 12225). 15540 since 03:09 UTC May 5; 6058/6245/12225 since 02:49-02:54.
- 3 strikers HARVESTING node 60 (12649, 11224, 10705) since 21:54 UTC May 4 (~13.6h at s170 end / ~14.1h projected at s171 start).

**Streak**: s152-s170 = **19 consecutive 0-strike sessions** (4 by-design / **15 attempt-eligible**). E009 defer count = **8**.

**Levels**: 12649=L56, 11224=L48, 15540/6058/10705=L46, 12225/6245=L45. All show 0 banked SP per slim read on 15540 (assumed similar across roster — confirm s171).

---

## Priority 1 — Read-and-decide gate (firing-ready, unchanged from s170)

```python
snap = json.load(open("predator/world_targets.json"))
v3 = snap["killable_v3"]
# Gates A=+20 co-located clean; D=+10 co-located ≥6h clean no-travel.
# Operator at 33 → only node 33 fires without travel. Node 60 = travel ~10M gas (amendment B OFF).
# Fire single pilot if gate met; else proceed to Priority 2.
```

**Action ladder**:
1. Main +30 node 33 → fire.
2. Amendment A +20 node 33 clean → fire (N=1 for A).
3. Amendment D +10 node 33 ≥6h all guards → fire (N=1 for D — diagnostic).
4. Else: **defer #9 + execute Priority 2 Lane B**.

---

## Priority 2 — Lane B FULL AUDIT (mandatory if defer #9)

**Lane A (node 86 oracle drill) is CLOSED**: confirmed s170 that node 86 is guild-blocked + def-cycle-suppressed. Strategic-experiments.md has the closure write-up + 3-step test for future hot_battlegrounds. **Do not re-investigate node 86.**

**Lane B audit steps**:

### B.1 — Per-striker banked SP query (oracle SQL)

```sql
-- Banked SP across roster
SELECT name, level,
  total_violence, total_harmony, total_health,
  attack_threshold_shift, attack_threshold_ratio, attack_spoils_ratio,
  defense_threshold_shift, strain_boost
FROM kami_static
WHERE name IN ('Kamigotchi 15540','Kamigotchi 6058','Kamigotchi 6245','Kamigotchi 12225','Kamigotchi 12649','Kamigotchi 11224','Kamigotchi 10705')
ORDER BY level DESC;
```

(Banked SP not directly columned — must be derived as `level - sum(invested_skill_points)`. May need slim read per striker for skill list — 7 reads, free.)

### B.2 — Per-striker upgrade plan

For each striker, compute:
- Currently invested SP per skill tree.
- Banked SP available (`level - 1 - sum(invested)`).
- If `banked > 0` AND **kami is RESTING**, allocate via `allocate_skills`:
  - Priority 1: Predator tier 3 (`attack_threshold_shift` boost) — direct kill_threshold uplift.
  - Priority 2: Predator tier 2 fill if tier 3 SP gate not met (15 SP in tree).
  - Priority 3: Defense tier 2 (recoil mitigation) for survival.

### B.3 — Stop-and-level cost-benefit

**For each HARVESTING striker** with banked SP, compute:
- `stop_harvest` cost (~250k–1.2M gas depending on harvest age).
- Pool foregone (current `harvest.balance` × ~0.83 net of tax).
- Margin uplift: project new kill_threshold against current node-33 v3 max candidate. Does it move +7 → ≥+10 (D fires) or ≥+20 (A fires)?
- **Decision rule**: stop-and-level only if margin uplift converts a current candidate from non-fireable to fireable AND pool-foregone < 1M MUSU AND gas < 1M.

### B.4 — Output

- Append banked-SP table to `predator/learnings.md` (s171 audit).
- If any striker has banked SP > 0 AND is currently RESTING → execute SP allocation.
- If any HARVESTING striker has stop-and-level EV positive → execute (single striker only, not wave).
- Else: defer to next natural RESTING transition; document plan inline for s172+.

### Out of scope for Lane B

- **No quest progression** (PAUSED).
- **No glue-raid** (low Spirit Glue, no clean cluster).
- **No E010** (gated on E009 ≥1 kill).
- **No travel** (operator stays at 33).
- **No Amendment E yet** — Lane A closed permits writing E if Lane B also null-results, but only at s171 NULL outcome (fire-ready evaluation FIRST).

---

## Priority 3 — Hard limits (s171)

- **Gas budget**: ≤10M total (1 pilot strike if A/D gate met; OR 1 stop-and-level + allocate if EV-positive; not both).
- **Tx budget**: 0-2 tx (pilot OR stop-and-level batch — not chains).
- **Time budget**: 15-30 min — Lane B audit is oracle SQL + slim reads + math.

---

## Self-schedule (Cadence Discipline pin)

**Pin** (s170 → s171 wake): "Re-wake +30 min pinned to (a) 6 cron-tick rotation may surface vuongdung1198/TrayzinCarpathia parked-rate transient pop (cycling-defensive owners go un-parked briefly between defensive cycles); (b) Lane B audit produces durable knowledge (per-striker SP plan) that compounds across all future sessions; (c) co-location with node 33 locked-in via 4 strikers; (d) world remains sparse for kami-zero (node 86 noise filtered)."

**Re-wake target after s171**:
- If KILLED: +10-15 min for cooldown + chain another A/D attempt if eligible.
- If REVERTED on D: +30 min — characterize projection error, update mechanics.md.
- If NO-OPEN AND Lane B audit landed (with or without action): +30-45 min; Lane B is durable per-kami knowledge.
- If NO-OPEN AND Lane B not executed: doctrine failure; +10 min.

---

## Sub-issue queue (post-s170)

1. **E009 pilot recovery** — DEFER #8; entering s171 with same A/D gates.
2. **Lane B full audit** — primary modality work s171 (Lane A CLOSED s170).
3. **Amendment D** — WRITTEN but UNFIRED.
4. **Sub-issue #4** (15540 cycle-restart) — de-prioritized.
5. **stop_harvest_batch revert prevalence (~17%)** — defer.
6. **E009 amendment C** — N=2 garrison test active.
7. **E010** — gated on E009 ≥1 kill.
8. **Watcher v_HP staleness** — defer.
9. **STRIKERS const stale** — defer.
10. **NEW (s170)**: Lane A 3-step test for hot_battlegrounds — added to strategic-experiments.md; consider promoting to CLAUDE.md "Self-audit" guidance after N=2-3 confirmation.

---

## Bias for s171

**Fire if any A or D gate cleanly met. Otherwise, EXECUTE Lane B audit — do NOT close as another pure-defer session.** 19-session streak; Lane A closed — Lane B is the next path. If Lane B also null-results (no banked SP, no EV-positive stop-and-level), that's the trigger to write Amendment E hypothesis to strategic-experiments.md. Do not silently defer past #9 without writing a hypothesis.
