"""Smoke test: run perceive → filter → pick against captured fixture
data. No chain calls. Asserts the executor would do sensible things at
the operator's actual location and at hypothetical alternatives.

Run from repo root: `python -m pytest tests/test_loop.py -v`
"""

import json
from pathlib import Path

import pytest

from core import config as cfg_module
from core.perception import world
from core.predator import filter as pfilter
from core.predator import targeting

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "tests" / "fixtures"


@pytest.fixture
def cfg():
    return cfg_module.load(ROOT / "core" / "config.yaml").model_dump()


@pytest.fixture
def candidates():
    blob = world.load_world(FIXTURES / "world_targets.json")
    return world.candidates(blob)


@pytest.fixture
def by_idx():
    return world.parked_rates_by_idx(FIXTURES / "parked_rates_state.json")


def _self_state(operator_node, kami_locations):
    """kami_locations: {kami_idx: node_id}"""
    return {
        "operator_node": operator_node,
        "eth_balance_wei": 10**18,
        "kamis": {
            idx: {"node": node, "state": "HARVESTING", "hp": 150, "hp_total": 150}
            for idx, node in kami_locations.items()
        },
    }


def test_fixture_has_candidates(candidates):
    """Confirm fixture is non-trivial."""
    assert len(candidates) > 0


def test_archetype_reject_filters_vuongdung(candidates, by_idx, cfg):
    """vuongdung1198 is the only baked-in archetype reject."""
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, cfg)
    for s in survivors:
        assert s["_resolved_handle"].lower() != "vuongdung1198"


def test_no_strikes_when_operator_at_unproductive_node(candidates, by_idx, cfg):
    """Operator at node 33 (current bpeon location): fixture has no
    co-located candidates there. Expect all rejected, with some
    co-location-related reason dominating (striker check fires before
    operator check, so either reason satisfies the assertion)."""
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, cfg)
    assert len(survivors) == 0
    coloc_rejections = (
        counts.get("striker_not_colocated", 0)
        + counts.get("operator_not_colocated", 0)
    )
    assert coloc_rejections > 0
    # Total rejections must match candidates seen (sanity check)
    assert sum(counts.values()) == len(candidates)


def test_strike_candidate_appears_when_colocated(candidates, by_idx, cfg):
    """If operator + striker are at node 82 (where 3333333333333333
    has the top-margin target), at least one survivor should appear."""
    fake_state = _self_state(operator_node=82, kami_locations={12649: 82})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, cfg)
    assert len(survivors) >= 1
    pick = targeting.rank(survivors)[0]
    assert pick["node_id"] == 82
    assert pick["margin"] >= cfg["predator"]["margin_floor"]


def test_below_margin_floor_rejected(candidates, by_idx, cfg):
    """Tighten the floor and verify previously-passing candidates fall
    out, with below_margin_floor count rising."""
    fake_state = _self_state(operator_node=82, kami_locations={12649: 82})
    base_cfg = json.loads(json.dumps(cfg))
    base_cfg["predator"]["margin_floor"] = 999  # impossibly high
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, base_cfg)
    assert len(survivors) == 0
    assert counts.get("below_margin_floor", 0) > 0


def test_below_min_elapsed_rejected(candidates, by_idx, cfg):
    """At node 12 onlinelink has a margin-24 candidate but elapsed=3.8h
    < 6h floor. Should be rejected for elapsed."""
    fake_state = _self_state(operator_node=12, kami_locations={12649: 12})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, cfg)
    # Whatever else passes/fails at node 12, the onlinelink 6912 with
    # elapsed 3.8h should not appear in survivors
    for s in survivors:
        if s["v_idx"] == 6912:
            pytest.fail("Candidate with elapsed_h<6 was not rejected")


def test_owner_handle_resolution_via_by_idx_fallback(candidates, by_idx):
    """When v_acct is missing on a candidate, by_idx fallback should
    fill it in (if available)."""
    if not candidates or not by_idx:
        pytest.skip("fixture lacks data for this test")
    sample = dict(candidates[0])
    original_handle = sample.get("v_acct")
    sample["v_acct"] = ""  # simulate watcher null regression
    resolved = world.resolve_handle(sample, by_idx)
    fallback = by_idx.get(int(sample["v_idx"]), {})
    expected = fallback.get("v_acct") or ""
    assert resolved == expected
    if original_handle and expected:
        assert resolved == original_handle  # by_idx agrees with watcher when both present


def test_config_validates(cfg):
    """Pydantic schema parse must succeed and produce all sections."""
    assert "predator" in cfg
    assert "limits" in cfg
    assert "anomalies" in cfg
    assert isinstance(cfg["predator"]["margin_floor"], (int, float))
