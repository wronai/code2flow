"""Map exporter alerts and hotspots — build compact alert lists for header."""

import re
from pathlib import Path
from typing import List, Tuple, Optional

from code2llm.core.models import FunctionInfo


def build_alerts(funcs: List[FunctionInfo]) -> List[str]:
    """Build a compact list of top alerts for the header."""
    alerts: List[Tuple[int, int, str]] = []
    for fi in funcs:
        display = fi.name if not fi.class_name else f"{fi.class_name}.{fi.name}"
        cc = fi.complexity.get("cyclomatic_complexity", 0)
        if cc >= 15:
            severity = 0 if cc >= 25 else 1
            alerts.append((severity, cc, f"CC {display}={cc}"))

        fan_out = len(set(fi.calls))
        if fan_out >= 10:
            severity = 0 if fan_out >= 20 else 1
            alerts.append((severity, fan_out, f"fan-out {display}={fan_out}"))

    alerts.sort(key=lambda item: (item[0], -item[1], item[2]))
    return [label for _, _, label in alerts[:5]]


def build_hotspots(funcs: List[FunctionInfo]) -> List[str]:
    """Build a compact list of top fan-out hotspots for the header."""
    spots: List[Tuple[int, str]] = []
    for fi in funcs:
        fan_out = len(set(fi.calls))
        if fan_out >= 5:
            display = fi.name if not fi.class_name else f"{fi.class_name}.{fi.name}"
            spots.append((fan_out, f"{display} fan={fan_out}"))

    spots.sort(key=lambda item: item[0], reverse=True)
    return [label for _, label in spots[:5]]


def load_evolution_trend(evolution_path: Path, current_cc: float) -> str:
    """Summarize the latest CC trend from the previous evolution.toon.yaml file."""
    previous_cc = _read_previous_cc_avg(evolution_path)
    if previous_cc is None:
        return "baseline"

    delta = round(current_cc - previous_cc, 1)
    if delta < 0:
        direction = "improved"
    elif delta > 0:
        direction = "regressed"
    else:
        direction = "flat"

    sign = "+" if delta > 0 else ""
    return f"CC̄ {previous_cc:.1f}→{current_cc:.1f} ({direction} {sign}{delta:.1f})"


def _read_previous_cc_avg(evolution_path: Path) -> Optional[float]:
    """Read the previous CC average from an existing evolution.toon.yaml file."""
    if not evolution_path.exists():
        return None

    try:
        content = evolution_path.read_text(encoding="utf-8")
    except Exception:
        return None

    for line in content.splitlines():
        match = re.search(r"CC̄:\s*([0-9]+(?:\.[0-9]+)?)\s*→", line)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
    return None


__all__ = [
    'build_alerts',
    'build_hotspots',
    'load_evolution_trend',
]
