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
    """Loaded config — note hunting_mode defaults to True in config.yaml.
    Tests that exercise the co-located strike path should override
    hunting_mode=False explicitly (see _legacy_cfg)."""
    return cfg_module.load(ROOT / "core" / "config.yaml").model_dump()


@pytest.fixture
def legacy_cfg(cfg):
    """Cfg with hunting_mode disabled — the co-located-only filter path."""
    c = json.loads(json.dumps(cfg))
    c["predator"]["hunting_mode"] = False
    return c


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
        "kamis": {
            idx: {"node": node, "state": "HARVESTING"}
            for idx, node in kami_locations.items()
        },
    }


def test_fixture_has_candidates(candidates):
    """Confirm fixture is non-trivial."""
    assert len(candidates) > 0


def test_archetype_reject_filters_vuongdung(candidates, by_idx, legacy_cfg):
    """vuongdung1198 is the only baked-in archetype reject."""
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, legacy_cfg)
    for s in survivors:
        assert s["_resolved_handle"].lower() != "vuongdung1198"


def test_no_strikes_when_operator_at_unproductive_node(candidates, by_idx, legacy_cfg):
    """Legacy (non-hunting) mode at node 33 (current bpeon location):
    fixture has no co-located candidates there. Expect all rejected."""
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, legacy_cfg)
    assert len(survivors) == 0
    coloc_rejections = (
        counts.get("striker_not_colocated", 0)
        + counts.get("operator_not_colocated", 0)
        + counts.get("striker_not_harvesting", 0)
    )
    assert coloc_rejections > 0
    assert sum(counts.values()) == len(candidates)


def test_strike_candidate_appears_when_colocated(candidates, by_idx, legacy_cfg):
    """Legacy mode: striker at node 82 → top-margin candidate (3333...)
    should survive."""
    fake_state = _self_state(operator_node=82, kami_locations={12649: 82})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, legacy_cfg)
    assert len(survivors) >= 1
    pick = targeting.rank(survivors)[0]
    assert pick["node_id"] == 82
    assert pick["margin"] >= legacy_cfg["predator"]["margin_floor"]


def test_below_margin_floor_rejected(candidates, by_idx, legacy_cfg):
    """Legacy mode: tighten floor → previously-passing candidates fall out."""
    fake_state = _self_state(operator_node=82, kami_locations={12649: 82})
    base_cfg = json.loads(json.dumps(legacy_cfg))
    base_cfg["predator"]["margin_floor"] = 999
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, base_cfg)
    assert len(survivors) == 0
    assert counts.get("below_margin_floor", 0) > 0


def test_below_min_elapsed_rejected(candidates, by_idx, legacy_cfg):
    """Legacy mode: onlinelink 6912 elapsed=3.8h must be rejected."""
    fake_state = _self_state(operator_node=12, kami_locations={12649: 12})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, legacy_cfg)
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
    assert isinstance(cfg["predator"]["hunting_margin_floor"], (int, float))


def test_hunting_mode_drops_colocation_gate(candidates, by_idx, cfg):
    """In hunting_mode, the co-location gate is removed but the higher
    hunting_margin_floor applies. With operator at node 33 and
    hunting_margin_floor=25, candidates at OTHER nodes with margin>=25
    should now survive (where they would have failed co-location)."""
    hcfg = json.loads(json.dumps(cfg))
    hcfg["predator"]["hunting_mode"] = True
    hcfg["predator"]["hunting_margin_floor"] = 25
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, hcfg)
    # No 'striker_not_colocated' or 'striker_not_harvesting' rejections in hunting mode
    assert counts.get("striker_not_colocated", 0) == 0
    assert counts.get("striker_not_harvesting", 0) == 0
    # Some candidates with margin>=25 must survive (regardless of node)
    assert len(survivors) >= 1
    for s in survivors:
        assert s["margin"] >= 25


def test_hunting_floor_higher_than_baseline(candidates, by_idx, cfg):
    """hunting_margin_floor must be the gate when hunting_mode=true,
    NOT margin_floor. So a candidate with margin between margin_floor
    and hunting_margin_floor must be rejected for below_hunting_margin_floor."""
    hcfg = json.loads(json.dumps(cfg))
    hcfg["predator"]["hunting_mode"] = True
    hcfg["predator"]["margin_floor"] = 5
    hcfg["predator"]["hunting_margin_floor"] = 200  # impossibly high
    fake_state = _self_state(operator_node=33, kami_locations={12649: 33})
    survivors, counts = pfilter.apply(candidates, by_idx, fake_state, hcfg)
    assert len(survivors) == 0
    assert counts.get("below_hunting_margin_floor", 0) > 0
    # Must NOT have used the co-located floor name
    assert counts.get("below_margin_floor", 0) == 0
