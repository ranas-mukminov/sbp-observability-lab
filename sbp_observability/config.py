"""Configuration helpers for sbp-observability-lab."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

import yaml

DEFAULT_CONFIG_PATH = Path("/etc/sbp_observability/config.yaml")


@dataclass
class ParserConfig:
    column_mapping: Dict[str, str] = field(default_factory=dict)


@dataclass
class AppConfig:
    upstream_url: Optional[str] = None
    mask_keys: tuple[str, ...] = ("pan", "card", "account")
    parser: ParserConfig = field(default_factory=ParserConfig)


def load_config(path: Path | str | None = None) -> AppConfig:
    """Load configuration from YAML file."""
    target = Path(path) if path else DEFAULT_CONFIG_PATH
    if not target.exists():
        return AppConfig()
    with target.open("r", encoding="utf-8") as config_file:
        raw = yaml.safe_load(config_file) or {}
    parser_cfg = raw.get("parser", {})
    return AppConfig(
        upstream_url=raw.get("upstream_url"),
        mask_keys=tuple(parser_cfg.get("mask_keys", ("pan", "card", "account"))),
        parser=ParserConfig(column_mapping=parser_cfg.get("column_mapping", {})),
    )
