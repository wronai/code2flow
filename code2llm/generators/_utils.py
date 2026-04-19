"""Shared utilities for generators — avoids circular imports."""

import yaml
from typing import Any, Dict


def dump_yaml(data: Dict[str, Any]) -> str:
    """Shared YAML serialiser (sort_keys=False, unicode, width=100)."""
    return yaml.safe_dump(
        data,
        sort_keys=False,
        allow_unicode=True,
        width=100,
        default_flow_style=False,
    )
