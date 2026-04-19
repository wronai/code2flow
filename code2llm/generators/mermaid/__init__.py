"""Mermaid generators package — validation, fixing, and PNG generation.

This package provides:
- validation: Mermaid file validation (validate_mermaid_file)
- fix: Auto-fix common syntax errors (fix_mermaid_file)
- png: PNG generation from .mmd files (generate_pngs, generate_single_png)

All public names are re-exported here for backward compatibility
with the original mermaid.py module structure.
"""

# Validation exports
from .validation import (
    validate_mermaid_file,
    _strip_label_segments,
    _is_balanced_node_line,
    _check_bracket_balance,
    _scan_brackets,
    _check_node_ids,
)

# Fix exports
from .fix import (
    fix_mermaid_file,
    _sanitize_label_text,
    _sanitize_node_id,
    _fix_edge_line,
    _fix_edge_label_pipes,
    _fix_subgraph_line,
    _fix_class_line,
)

# PNG generation exports
from .png import (
    generate_pngs,
    generate_single_png,
    generate_with_puppeteer,
    _is_png_fresh,
    _prepare_and_render,
    _setup_puppeteer_config,
    _build_renderers,
    _run_mmdc_subprocess,
)

__all__ = [
    # Validation
    'validate_mermaid_file',
    '_strip_label_segments',
    '_is_balanced_node_line',
    '_check_bracket_balance',
    '_scan_brackets',
    '_check_node_ids',
    # Fix
    'fix_mermaid_file',
    '_sanitize_label_text',
    '_sanitize_node_id',
    '_fix_edge_line',
    '_fix_edge_label_pipes',
    '_fix_subgraph_line',
    '_fix_class_line',
    # PNG
    'generate_pngs',
    'generate_single_png',
    'generate_with_puppeteer',
    '_is_png_fresh',
    '_prepare_and_render',
    '_setup_puppeteer_config',
    '_build_renderers',
    '_run_mmdc_subprocess',
]
