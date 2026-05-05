"""Cross-cutting rules: archetype rejects, hard limits.
Pure-Python predicates over candidate dicts. No I/O.

Optimizer adds/removes archetypes here based on observed kill outcomes.
"""

# Owners whose harvest-state is structurally non-killable or non-rewarding.
# Old system's "archetype REJECT" lived in prose across decisions.md;
# pulled here as code. Optimizer maintains.
#
# vuongdung1198: confirmed in Phase 3 (s178) — zero on-chain
#   harvest_collect events across ~49 kamis × 14 cycles. Bounty pool
#   stays at zero — kills there yield no spoils.
ARCHETYPE_REJECT_OWNERS: set[str] = {
    "vuongdung1198",
}


def is_archetype_rejected(handle: str) -> bool:
    return handle.lower() in {h.lower() for h in ARCHETYPE_REJECT_OWNERS}


def is_self_strike(candidate_account_id: str, our_account_ids: set[str]) -> bool:
    """Defense against any reorg in account ownership. Belt + suspenders;
    executor.liquidate already declines self-strikes via guild gate, but
    the gate is keyed on guild-no-touch.csv and our own accounts may not
    be in that file.
    """
    return candidate_account_id in our_account_ids
