# Optimizer notes — terse change log

Append-only. ≤30 lines total. When this file exceeds 30 lines, the
optimizer MUST drop the oldest entries before adding new ones (FIFO).

Format: one line per change, prefix with date.

```
2026-05-05 — bootstrap. Initial rules: margin_floor=25, min_elapsed_h=6, vuongdung1198 archetype reject. Tight defaults to keep first-day revert rate near zero while we calibrate.
```
