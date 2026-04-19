"""Mermaid exporter package — generate Mermaid diagrams from analysis.

This package provides:
- utils: Mermaid-safe identifiers, module extraction, file writing
- classic: flow.mmd full graph with CC styling
- calls: calls.mmd simplified call graph
- compact: compact_flow.mmd module-level aggregation
- flow_compact: flow.mmd architectural view (~50 nodes)
- flow_detailed: flow_detailed.mmd per-module view (~150 nodes)
- flow_full: flow_full.mmd full debug view

All public names are re-exported here for backward compatibility
with the original mermaid_exporter.py module structure.
"""

# Utils
from .utils import (
    readable_id,
    safe_module,
    module_of,
    resolve_callee,
    write_file,
    get_cc,
)

# Classic
from .classic import export_classic

# Calls
from .calls import export_calls

# Compact
from .compact import export_compact

# Flow exports
from .flow_compact import (
    export_flow_compact,
    should_skip_module,
    is_entry_point,
    find_critical_path,
)
from .flow_detailed import export_flow_detailed
from .flow_full import export_flow_full

__all__ = [
    # Utils
    'readable_id',
    'safe_module',
    'module_of',
    'resolve_callee',
    'write_file',
    'get_cc',
    # Classic
    'export_classic',
    # Calls
    'export_calls',
    # Compact
    'export_compact',
    # Flow
    'export_flow_compact',
    'export_flow_detailed',
    'export_flow_full',
    'should_skip_module',
    'is_entry_point',
    'find_critical_path',
]
