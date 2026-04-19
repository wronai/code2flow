"""LLM Flow label parsing — extract function names from CALL/FUNC labels."""

import re
from typing import Optional

from .utils import _FUNC_LABEL_PREFIX, _CALL_LABEL_PREFIX


def _parse_call_label(label: str) -> Optional[str]:
    """Parse a CALL label to extract function name."""
    label = (label or "").strip()
    if not label.startswith(_CALL_LABEL_PREFIX):
        return None
    rest = label[len(_CALL_LABEL_PREFIX) :].strip()
    rest = rest.replace("<", "").replace(">", "")

    m = re.match(r"([A-Za-z_][A-Za-z0-9_\.]+)\s*\(", rest)
    if m:
        return m.group(1)

    m = re.match(r"([A-Za-z_][A-Za-z0-9_\.]+)$", rest)
    if m:
        return m.group(1)

    return None


def _parse_func_label(label: str) -> Optional[str]:
    """Parse a FUNC label to extract function name."""
    label = (label or "").strip()
    if not label.startswith(_FUNC_LABEL_PREFIX):
        return None
    return label[len(_FUNC_LABEL_PREFIX) :].strip() or None


__all__ = [
    '_parse_call_label',
    '_parse_func_label',
]
