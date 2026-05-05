"""Config schema. Validates `core/config.yaml` at executor startup so
typos (the most likely optimizer mistake) fail loud instead of bricking
every tick silently.
"""

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class PredatorConfig(BaseModel):
    margin_floor: float
    min_elapsed_h: float
    max_minutes_idle_for_strike: float | None = None
    reject_if_anti_predator_automation: bool = True
    reject_if_defensive_cycle: bool = True
    require_parked_bool: bool = False
    require_owner_resolved: bool = True
    reject_owner_unknown: bool = True
    require_colocation: bool = True
    # Roaming-assassin mode: executor migrates striker to target's node
    # before each strike (~15-25M gas/kill). Bypasses co-location gate;
    # uses higher margin floor instead.
    hunting_mode: bool = False
    hunting_margin_floor: float = 25.0


class LimitsConfig(BaseModel):
    max_strikes_per_tick: int = Field(ge=0, le=5)
    max_gas_per_tick: int = Field(ge=0)


class AnomaliesConfig(BaseModel):
    defer_streak_alert_threshold: int = Field(ge=1)
    owner_handle_null_pct_alert: float = Field(ge=0, le=100)


class AccountConfig(BaseModel):
    primary: str


class PathsConfig(BaseModel):
    world_targets: str
    parked_rates_state: str
    guild_no_touch: str
    runs_log: str
    anomalies_log: str
    changes_log: str


class Config(BaseModel):
    predator: PredatorConfig
    limits: LimitsConfig
    anomalies: AnomaliesConfig
    account: AccountConfig
    paths: PathsConfig


def load(path: Path | str) -> Config:
    with open(path) as f:
        raw = yaml.safe_load(f)
    return Config.model_validate(raw)
