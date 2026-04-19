"""LLM Flow generator package — create compact LLM-friendly app flow summaries.

This package provides:
- utils: YAML reading and type coercion helpers
- parsing: Label parsing for CALL/FUNC nodes
- nodes: Node collection and entrypoint detection
- analysis: Function scoring, summarization, and call graph
- generator: Main flow generation and markdown rendering
- cli: Command-line interface

All public names are re-exported here for backward compatibility
with the original llm_flow.py module structure.
"""

# Utils
from .utils import (
    _FUNC_LABEL_PREFIX,
    _CALL_LABEL_PREFIX,
    _strip_bom,
    _safe_read_yaml,
    _as_dict,
    _as_list,
    _shorten,
)

# Parsing
from .parsing import (
    _parse_call_label,
    _parse_func_label,
)

# Nodes
from .nodes import (
    _collect_nodes,
    _group_nodes_by_file,
    _is_entrypoint_file,
    _extract_entrypoint_info,
    _deduplicate_entrypoints,
    _collect_entrypoints,
    _collect_functions,
)

# Analysis
from .analysis import (
    FuncSummary,
    _node_counts_by_function,
    _pick_relevant_functions,
    _summarize_functions,
    _build_call_graph,
    _reachable,
)

# Generator
from .generator import (
    generate_llm_flow,
    render_llm_flow_md,
)

# CLI
from .cli import (
    create_parser,
    main,
)

__all__ = [
    # Utils
    '_FUNC_LABEL_PREFIX',
    '_CALL_LABEL_PREFIX',
    '_strip_bom',
    '_safe_read_yaml',
    '_as_dict',
    '_as_list',
    '_shorten',
    # Parsing
    '_parse_call_label',
    '_parse_func_label',
    # Nodes
    '_collect_nodes',
    '_group_nodes_by_file',
    '_is_entrypoint_file',
    '_extract_entrypoint_info',
    '_deduplicate_entrypoints',
    '_collect_entrypoints',
    '_collect_functions',
    # Analysis
    'FuncSummary',
    '_node_counts_by_function',
    '_pick_relevant_functions',
    '_summarize_functions',
    '_build_call_graph',
    '_reachable',
    # Generator
    'generate_llm_flow',
    'render_llm_flow_md',
    # CLI
    'create_parser',
    'main',
]
