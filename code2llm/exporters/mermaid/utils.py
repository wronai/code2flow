"""Mermaid exporter utilities — identifiers, module extraction, file writing."""

import re
from pathlib import Path
from typing import Optional

from code2llm.core.models import FunctionInfo


def readable_id(name: str) -> str:
    """Create human-readable Mermaid-safe unique node ID."""
    return _sanitize_identifier(name, prefix="N")


def safe_module(name: str) -> str:
    """Create safe subgraph name."""
    return _sanitize_identifier(name, prefix="M")


def _sanitize_identifier(name: str, prefix: str) -> str:
    """Convert an arbitrary string into a Mermaid-safe identifier."""
    safe = (name or "").replace('.', '__')
    safe = re.sub(r'[^A-Za-z0-9_]+', '_', safe)
    if not safe:
        return prefix
    if not safe[0].isalpha():
        safe = f"{prefix}_{safe}"
    return safe


def module_of(func_name: str) -> str:
    """Extract module from qualified name.

    Returns up to 2 levels (e.g. 'code2llm.core', 'code2llm.exporters')
    so that subpackage-level cross-edges are visible in compact_flow.
    """
    parts = func_name.split('.')
    if len(parts) >= 3:
        return '.'.join(parts[:2])
    if len(parts) == 2:
        return parts[0]
    return parts[0] if parts else 'unknown'


def resolve_callee(callee: str, funcs: dict) -> Optional[str]:
    """Resolve callee to a known qualified name."""
    if callee in funcs:
        return callee
    candidates = [qn for qn in funcs if qn.endswith(f".{callee}")]
    if len(candidates) == 1:
        return candidates[0]
    return None


def write_file(path: str, lines: list) -> Path:
    """Write lines to file."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    return p


def get_cc(fi: FunctionInfo) -> int:
    """Extract cyclomatic complexity from FunctionInfo."""
    if isinstance(fi.complexity, dict):
        return fi.complexity.get('cyclomatic_complexity', 0)
    return fi.complexity or 0


__all__ = [
    'readable_id',
    'safe_module',
    'module_of',
    'resolve_callee',
    'write_file',
    'get_cc',
]
