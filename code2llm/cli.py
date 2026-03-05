#!/usr/bin/env python3
"""
code2llm - CLI for Python code flow analysis

Analyze control flow, data flow, and call graphs of Python codebases.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .core.config import Config, ANALYSIS_MODES
from .core.analyzer import ProjectAnalyzer
from .cli_exports import (
    _export_evolution, _export_data_structures, _export_context_fallback,
    _export_readme, _export_code2logic, _export_prompt_txt, _run_exports,
    _export_simple_formats, _export_yaml, _export_mermaid, _export_refactor_prompts,
    _export_project_yaml, _run_report,
)
from .cli_analysis import _run_analysis



def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog='code2llm',
        description='Analyze Python code control flow, data flow, and call graphs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  code2llm ./                                       # Default: TOON diagnostics + README
  code2llm ./ -f all -o ./docs                      # All formats to ./docs/
  code2llm ./ -f toon,map,flow                      # Diagnostics + structure + data-flow
  code2llm ./ -f context                            # LLM narrative (context.md)
  code2llm ./ --streaming --strategy deep -f all    # Deep streaming analysis, all outputs
  code2llm ./ --strategy quick -f toon              # Fast overview
  code2llm ./ --refactor                            # AI refactoring prompts
  code2llm ./ --refactor --smell god_function       # Filter by smell type
  code2llm ./ -f yaml --split-output                # Split YAML into multiple files
  code2llm ./ -f yaml --separate-orphans            # Separate orphaned functions
  code2llm ./ -f mermaid --no-png                   # Mermaid diagrams without PNG
  code2llm ./ -m static -v -o ./analysis            # Static mode, verbose
  code2llm ./ --no-readme                           # Disable README generation
  code2llm ./ -f project-yaml                       # Unified project.yaml (single source of truth)
  code2llm report --format toon                     # Generate view from project.yaml
  code2llm report --format all                      # All views from project.yaml
  code2llm llm-flow                                 # Generate LLM flow summary
  code2llm llm-context ./                           # Generate LLM context only

Format Options (-f):
  toon         — Health diagnostics (analysis.toon) [default]
  map          — Structural map (map.toon) — modules, imports, signatures
  flow         — Data-flow analysis (flow.toon) — pipelines, contracts, types
  context      — LLM narrative (context.md) — architecture summary
  code2logic   — Generate project logic (project.toon) via external code2logic
  yaml         — Standard YAML format
  json         — Machine-readable JSON
  mermaid      — Flowchart diagrams (flow.mmd, calls.mmd, compact_flow.mmd)
  evolution    — Refactoring queue (evolution.toon)
  project-yaml — Unified project.yaml (single source of truth) + generated views
  all          — Generate all formats (including project-yaml)

Strategy Options (--strategy):
  quick     — Fast overview, fewer files analyzed
  standard  — Balanced analysis [default]
  deep      — Complete analysis, all files
        '''
    )
    
    # Add backward compatibility source argument first
    parser.add_argument(
        'source',
        nargs='?',
        help='Path to Python source file or directory'
    )
    
    parser.add_argument(
        '-m', '--mode',
        choices=list(ANALYSIS_MODES.keys()),
        default='hybrid',
        help=f'Analysis mode (default: hybrid)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='./code2llm_output',
        help='Output directory (default: ./code2llm_output)'
    )
    
    parser.add_argument(
        '-f', '--format',
        default='toon',
        help='Output formats: toon,map,flow,context,code2logic,yaml,json,mermaid,evolution,png,all (default: toon)'
    )
    
    parser.add_argument(
        '--full',
        action='store_true',
        help='Include all fields in output (including empty/null values)'
    )
    
    parser.add_argument(
        '--no-patterns',
        action='store_true',
        help='Disable pattern detection'
    )
    
    parser.add_argument(
        '--max-depth',
        type=int,
        default=10,
        help='Maximum analysis depth (default: 10)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '--no-png',
        action='store_true',
        help='Skip automatic PNG generation from Mermaid files'
    )
    
    parser.add_argument(
        '--strategy',
        choices=['quick', 'standard', 'deep'],
        default='standard',
        help='Analysis strategy: quick (fast overview), standard (balanced), deep (complete)'
    )
    
    parser.add_argument(
        '--streaming',
        action='store_true',
        help='Use streaming analysis with progress reporting'
    )
    
    parser.add_argument(
        '--incremental',
        action='store_true',
        help='Only analyze changed files (requires previous run)'
    )
    
    parser.add_argument(
        '--max-memory',
        type=int,
        default=1000,
        help='Max memory in MB (default: 1000)'
    )
    
    parser.add_argument(
        '--split-output',
        action='store_true',
        help='Split YAML output into multiple files (summary, functions, classes, modules, entry_points)'
    )
    
    parser.add_argument(
        '--separate-orphans',
        action='store_true',
        help='Separate consolidated project from orphaned/isolated functions into different folders'
    )
    
    parser.add_argument(
        '--data-flow',
        action='store_true',
        help='Export data flow analysis (pipelines, state patterns, dependencies, events)'
    )
    
    parser.add_argument(
        '--data-structures',
        action='store_true',
        help='Export data structure analysis (types, flows, optimization opportunities)'
    )
    
    parser.add_argument(
        '--refactor',
        action='store_true',
        help='Enable AI-driven refactoring analysis and prompt generation'
    )
    
    parser.add_argument(
        '--smell',
        help='Filter refactoring by specific code smell (e.g., god_function, feature_envy)'
    )
    
    parser.add_argument(
        '--llm-format',
        choices=['claude', 'gpt', 'markdown'],
        default='markdown',
        help='Format for refactoring prompts (default: markdown)'
    )
    
    parser.add_argument(
        '--readme',
        action='store_true',
        default=True,
        help='Generate README.md with documentation of all output files (default: enabled)'
    )
    
    parser.add_argument(
        '--chunk',
        action='store_true',
        help='Automatically split large repositories into smaller subprojects'
    )

    parser.add_argument(
        '--no-chunk',
        action='store_true',
        help='Disable chunked analysis even for large repositories'
    )
    
    parser.add_argument(
        '--chunk-size',
        type=int,
        default=256,
        help='Maximum output size per chunk in KB (default: 256)'
    )
    
    parser.add_argument(
        '--max-files-per-chunk',
        type=int,
        default=50,
        help='Maximum files per chunk for large repos (default: 50)'
    )
    
    parser.add_argument(
        '--auto-chunk-threshold',
        type=int,
        default=100,
        help='File count threshold to auto-enable chunking (default: 100)'
    )
    
    parser.add_argument(
        '--skip-subprojects',
        nargs='+',
        default=[],
        help='Skip specific subprojects (e.g., --skip-subprojects tests examples)'
    )
    
    parser.add_argument(
        '--only-subproject',
        help='Analyze only specific subproject (e.g., --only-subproject src)'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate generated chunked output - check all chunks have required files'
    )
    
    return parser


def _handle_special_commands() -> Optional[int]:
    """Handle special sub-commands (llm-flow, llm-context, report)."""
    if len(sys.argv) > 1 and sys.argv[1] == 'llm-flow':
        from .generators.llm_flow import main as llm_flow_main
        return llm_flow_main(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'llm-context':
        return generate_llm_context(sys.argv[2:])
    if len(sys.argv) > 1 and sys.argv[1] == 'report':
        return _handle_report_command(sys.argv[2:])
    return None


def _handle_report_command(args_list) -> int:
    """Generate views from an existing project.yaml.

    Usage:
        code2llm report --format toon    # → project.toon
        code2llm report --format context # → context.md
        code2llm report --format article # → status.md
        code2llm report --format html    # → dashboard.html
        code2llm report --format all     # → all views
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog='code2llm report',
        description='Generate views from project.yaml (single source of truth)',
    )
    parser.add_argument(
        '--input', '-i',
        default='./project.yaml',
        help='Path to project.yaml (default: ./project.yaml)',
    )
    parser.add_argument(
        '--format', '-f',
        dest='report_format',
        default='all',
        help='Output format: toon, context, article, html, all (default: all)',
    )
    parser.add_argument(
        '-o', '--output',
        default='.',
        help='Output directory (default: current directory)',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output',
    )

    args = parser.parse_args(args_list)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: project.yaml not found: {input_path}", file=sys.stderr)
        print("Run 'code2llm <source> -f project-yaml' first to generate it.", file=sys.stderr)
        return 1

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.verbose:
        print(f"Generating views from: {input_path}")
        print(f"Output directory: {output_dir}")

    _run_report(args, str(input_path), output_dir)

    if args.verbose:
        print(f"\nAll views saved to: {output_dir}")

    return 0


def _validate_and_setup(args) -> tuple[Path, Path]:
    """Validate source path and setup output directory."""
    if not args.source:
        print("Error: missing required argument: source", file=sys.stderr)
        print("Usage: code2llm <source> [options]", file=sys.stderr)
        print("   or: code2llm llm-flow [options]", file=sys.stderr)
        sys.exit(2)

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    return source_path, output_dir


def _print_start_info(args, source_path: Path, output_dir: Path) -> None:
    """Print analysis start information if verbose."""
    if args.verbose:
        print(f"Analyzing: {source_path}")
        print(f"Mode: {args.mode}")
        print(f"Output: {output_dir}")


def _validate_chunked_output(output_dir: Path, args) -> bool:
    """Validate generated chunked output.
    
    Checks:
    1. All chunks have required files (analysis.toon, context.md, evolution.toon)
    2. Files are not empty
    3. Report summary
    
    Returns True if valid, False otherwise.
    """
    import sys
    from pathlib import Path
    
    if not output_dir.exists():
        print(f"✗ Output directory does not exist: {output_dir}", file=sys.stderr)
        return False
    
    # Find all chunk directories
    chunk_dirs = [d for d in output_dir.iterdir() if d.is_dir()]
    
    if not chunk_dirs:
        print(f"✗ No chunk directories found in: {output_dir}", file=sys.stderr)
        return False
    
    required_files = ['analysis.toon', 'context.md', 'evolution.toon']
    issues = []
    valid_chunks = []
    
    print(f"\n🔍 Validating {len(chunk_dirs)} chunks in: {output_dir}")
    print("-" * 50)
    
    for chunk_dir in sorted(chunk_dirs):
        chunk_name = chunk_dir.name
        chunk_issues = []
        
        for req_file in required_files:
            file_path = chunk_dir / req_file
            if not file_path.exists():
                chunk_issues.append(f"  missing {req_file}")
            elif file_path.stat().st_size == 0:
                chunk_issues.append(f"  empty {req_file}")
        
        if chunk_issues:
            issues.append((chunk_name, chunk_issues))
            print(f"✗ {chunk_name}")
            for issue in chunk_issues:
                print(f"    {issue}")
        else:
            # Get file sizes
            sizes = []
            for req_file in required_files:
                size = (chunk_dir / req_file).stat().st_size
                sizes.append(f"{req_file}:{size//1024}KB" if size > 1024 else f"{req_file}:{size}B")
            valid_chunks.append(chunk_name)
            print(f"✓ {chunk_name} ({', '.join(sizes)})")
    
    print("-" * 50)
    print(f"\n📊 Validation Summary:")
    print(f"  Total chunks: {len(chunk_dirs)}")
    print(f"  Valid: {len(valid_chunks)}")
    print(f"  Issues: {len(issues)}")
    
    if issues:
        print(f"\n⚠️  {len(issues)} chunk(s) have issues:")
        for chunk_name, chunk_issues in issues:
            print(f"    - {chunk_name}")
        return False
    else:
        print(f"\n✅ All {len(valid_chunks)} chunks are valid!")
        return True


def main():
    """Main CLI entry point."""
    # Handle special sub-commands first
    special_result = _handle_special_commands()
    if special_result is not None:
        return special_result

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    source_path, output_dir = _validate_and_setup(args)
    _print_start_info(args, source_path, output_dir)
    
    # Validate mode - only check existing output
    if args.validate:
        is_valid = _validate_chunked_output(output_dir, args)
        return 0 if is_valid else 1

    # Analyze → Export
    result = _run_analysis(args, source_path, output_dir)
    _run_exports(args, result, output_dir, source_path=source_path)
    
    # Auto-validate after chunked analysis
    if args.chunk and args.verbose:
        print(f"\n🔍 Auto-validating chunked output...")
        _validate_chunked_output(output_dir, args)

    if args.verbose:
        print(f"\nAll outputs saved to: {output_dir}")

    return 0


# Analysis functions are in cli_analysis.py — imported at top of file


def generate_llm_context(args_list):
    """Quick command to generate LLM context only."""
    import argparse
    
    parser = argparse.ArgumentParser(
        prog='code2llm llm-context',
        description='Generate LLM-friendly context for a project'
    )
    parser.add_argument('source', help='Path to Python project')
    parser.add_argument('-o', '--output', default='./llm_context.md', help='Output file path')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    
    args = parser.parse_args(args_list)
    
    from pathlib import Path
    from . import ProjectAnalyzer, FAST_CONFIG
    from .exporters import ContextExporter
    
    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source path not found: {source_path}", file=sys.stderr)
        return 1
    
    if args.verbose:
        print(f"Generating LLM context for: {source_path}")
    
    # Use fast config with parallel disabled for stability
    FAST_CONFIG.performance.parallel_enabled = False
    
    analyzer = ProjectAnalyzer(FAST_CONFIG)
    result = analyzer.analyze_project(str(source_path))
    
    exporter = ContextExporter()
    exporter.export(result, args.output)
    
    # Print summary
    print(f"\n✓ LLM context generated: {args.output}")
    print(f"  Functions: {len(result.functions)}")
    print(f"  Classes: {len(result.classes)}")
    print(f"  Modules: {len(result.modules)}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
