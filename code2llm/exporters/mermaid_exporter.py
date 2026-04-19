"""Mermaid Exporter for code2llm — backward compatibility shim.

Three distinct outputs:
  - export()           → flow.mmd   — full call graph with CC-based styling
  - export_call_graph() → calls.mmd  — simplified call graph (edges only, no isolates)
  - export_compact()    → compact_flow.mmd — module-level aggregation

New 3-level flow diagrams (Plan R1):
  - export_flow_compact()   → flow.mmd — architectural view (~50 nodes)
  - export_flow_detailed()  → flow_detailed.mmd — per-module view (~150 nodes)
  - export_flow_full()      → flow_full.mmd — full debug view (all nodes)

Implementation has been split into:
  - mermaid/utils.py - Identifiers, module extraction, file writing
  - mermaid/classic.py - flow.mmd full graph with CC styling
  - mermaid/calls.py - calls.mmd simplified call graph
  - mermaid/compact.py - compact_flow.mmd module-level aggregation
  - mermaid/flow_compact.py - flow.mmd architectural view
  - mermaid/flow_detailed.py - flow_detailed.mmd per-module view
  - mermaid/flow_full.py - flow_full.mmd full debug view
"""

from pathlib import Path
from typing import Optional

from .base import BaseExporter, export_format
from code2llm.core.models import AnalysisResult

from .mermaid import (
    # Classic
    export_classic,
    # Calls
    export_calls,
    # Compact
    export_compact,
    # Flow
    export_flow_compact,
    export_flow_detailed,
    export_flow_full,
    # Utils for internal use
    readable_id,
    safe_module,
    module_of,
    resolve_callee as _resolve,
    write_file as _write,
    get_cc as _get_cc,
    should_skip_module as _should_skip_module,
    is_entry_point as _is_entry_point,
    find_critical_path as _find_critical_path,
)


@export_format("mermaid", description="Mermaid diagram format", extension=".mmd")
class MermaidExporter(BaseExporter):
    """Export call graph to Mermaid format."""

    # Delegate to package functions
    export = staticmethod(export_classic)
    export_call_graph = staticmethod(export_calls)
    export_compact = staticmethod(export_compact)
    export_flow_compact = staticmethod(export_flow_compact)
    export_flow_detailed = staticmethod(export_flow_detailed)
    export_flow_full = staticmethod(export_flow_full)

    # Keep compatibility aliases
    _readable_id = staticmethod(readable_id)
    _safe_module = staticmethod(safe_module)
    _module_of = staticmethod(module_of)
    _resolve = staticmethod(_resolve)
    _write = staticmethod(_write)
    _get_cc = staticmethod(_get_cc)
    _should_skip_module = staticmethod(_should_skip_module)
    _is_entry_point = staticmethod(_is_entry_point)
    _find_critical_path = staticmethod(_find_critical_path)

