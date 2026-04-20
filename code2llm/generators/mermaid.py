"""Mermaid PNG Generator for code2llm — backward compatibility shim.

This module re-exports from the mermaid package.
Implementation has been split into:
  - mermaid/validation.py - File validation functions
  - mermaid/fix.py - Auto-fix syntax errors
  - mermaid/png.py - PNG generation
  - mermaid/__init__.py - Re-exports
"""

from pathlib import Path
from typing import List, Optional

# Re-export all public names from the new package
from .mermaid import (
    # Validation
    validate_mermaid_file,
    _strip_label_segments,
    _is_balanced_node_line,
    _check_bracket_balance,
    _scan_brackets,
    _check_node_ids,
    # Fix
    fix_mermaid_file,
    _sanitize_label_text,
    _sanitize_node_id,
    _fix_edge_line,
    _fix_edge_label_pipes,
    _fix_subgraph_line,
    _fix_class_line,
    # PNG
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


def run_cli() -> None:
    """Run the CLI interface for generating PNGs from Mermaid files."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PNG from Mermaid files')
    parser.add_argument('input_dir', help='Directory with .mmd files')
    parser.add_argument('output_dir', help='Output directory for PNG files')
    
    args = parser.parse_args()
    
    input_path = Path(args.input_dir)
    output_path = Path(args.output_dir)
    
    count = generate_pngs(input_path, output_path)
    print(f"Generated {count} PNG files")


if __name__ == '__main__':
    run_cli()
