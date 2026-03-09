#!/usr/bin/env python3
"""
code2llm - CLI for Python code flow analysis

Analyze control flow, data flow, and call graphs of Python codebases.
"""

import sys

from .cli_parser import create_parser
from .cli_commands import (
    handle_special_commands, validate_and_setup, print_start_info,
    validate_chunked_output,
    # Backward compatibility aliases
    handle_report_command as _handle_report_command,
    generate_llm_context,
)
from .cli_exports import (
    _export_evolution, _export_data_structures, _export_context_fallback,
    _export_readme, _export_code2logic, _export_prompt_txt, _run_exports,
    _export_simple_formats, _export_yaml, _export_mermaid, _export_refactor_prompts,
    _export_project_yaml, _run_report,
)
from .cli_analysis import _run_analysis


# Backward compatibility aliases
_handle_special_commands = handle_special_commands
_validate_and_setup = validate_and_setup
_print_start_info = print_start_info
_validate_chunked_output = validate_chunked_output


def main():
    """Main CLI entry point."""
    # Handle special sub-commands first
    special_result = handle_special_commands()
    if special_result is not None:
        return special_result

    # Parse arguments
    parser = create_parser()
    args = parser.parse_args()

    source_path, output_dir = validate_and_setup(args)
    print_start_info(args, source_path, output_dir)
    
    # Validate mode - only check existing output
    if args.validate:
        is_valid = validate_chunked_output(output_dir, args)
        return 0 if is_valid else 1

    # Analyze → Export
    result = _run_analysis(args, source_path, output_dir)
    _run_exports(args, result, output_dir, source_path=source_path)
    
    # Auto-validate after chunked analysis
    if args.chunk and args.verbose:
        print(f"\n🔍 Auto-validating chunked output...")
        validate_chunked_output(output_dir, args)

    if args.verbose:
        print(f"\nAll outputs saved to: {output_dir}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
