# CLAUDE.md — kami-zero v2 (shared orientation)

This file is loaded into every kami-zero session. It describes the
system. The session-specific instructions are in the prompt that
invoked you (see `executor-prompt.md` or `optimizer-prompt.md`).

## What kami-zero is

A fully autonomous Kamigotchi predator agent on the bpeon account
(YomiNet). Two roles, both LLM-driven, separated by cron:

- **Executor** — Sonnet 4.6, every 5 min, ≤15 turns. Plays one tick of
  the game by following `executor-prompt.md`. No prose. No strategy.
  Logs structured outcomes to `history/runs.jsonl`.

- **Optimizer** — Opus 4.7, every 6 hours, ≤30 turns. Reads history,
  proposes ≤1 rule edit by following `optimizer-prompt.md`. The
  artifact that compounds is `executor-prompt.md` + `rules/*.md`.

## Anti-patterns (these are how kami-zero v0 died)

The previous incarnation (sessions 152–187, archived in
`archive/2026-05-pre-v2/`) entered a 35-session 0-strike dead-loop
because the LLM was unbounded:

- It wrote a 7900-line `decisions.md` and never re-read it.
- It layered gates ("§PARTIAL §A ARMED", "Phase 1 P1-CONFIRMED") and
  never relaxed any.
- Each session inherited prose bloat that mutated into more bloat.
- Eventually no candidate could pass all gates simultaneously.

In v2, prevention is structural:

1. **Forbidden files**: never write `decisions.md`, `plan.md`,
   `strategic-experiments.md`, `learnings.md`, `improvements.md`,
   `metrics.md`, `targeting.md`, or any prose journal. They are
   forbidden by name.
2. **Output is JSONL only**: `history/runs.jsonl` and
   `history/anomalies.jsonl` (executor) or `history/rule_changes.jsonl`
   (optimizer). One line per event. No paragraphs.
3. **Doctrine layers are forbidden**: no Phase X, no §SECTION,
   no Amendment Y. If you find yourself writing those words, stop.
4. **Per-session edit cap**: optimizer edits ≤1 rule per session.
   Executor edits ZERO rules per session.
5. **Rule-file size cap**: `executor-prompt.md` ≤200 lines. If it
   grows past, the optimizer must compress before any other change.

## Files of record

- `executor-prompt.md` — the playbook. Reviewed by founder. Edited only by optimizer.
- `rules/rejects.md` — archetype reject list (kamis whose owners we don't strike for empirical reasons).
- `rules/safety.md` — hard limits (gas caps, strike caps, founder-approved invariants).
- `rules/notes.md` — optimizer's terse change log (≤30 lines, append-only).
- `history/runs.jsonl` — executor tick outcomes.
- `history/anomalies.jsonl` — executor's "I saw something I don't know how to handle" queue.
- `history/rule_changes.jsonl` — optimizer's structured edit log.

## Files you DO NOT touch (either role)

- `archive/` — frozen prose from prior versions. For founder reference.
- `predator/scripts/`, `scripts/fetch-discord-liquidations.py` —
  watcher crons. Already deterministic-Python; do not modify.
- `executor/server.py` — MCP tool source. ONE exception: optimizer
  may bug-fix when an anomaly clearly identifies a defect, with
  commit prefix `bugfix:` and a specific anomaly cite. No new tools,
  no refactors.
- `predator/guild-no-touch.csv` — founder maintains. Do not edit.
- `accounts/`, `catalogs/`, `integration/`, `systems/` — game
  knowledge data. Read-only.

## Account context

- Primary account: `bpeon` (predator strikers + operator)
- Secondary: `dpeon` (crafting; not used in predator loop)
- Roster: 7 strikers (12649, 6058, 12225, 15540, 10705, 11224, 6245)
- Strikers are tools, not farmers. Default state: RESTING with operator.
  They do not earn passive MUSU; they exist to liquidate.
