"""Chunked export functionality — handles multi-subproject analysis export.

Extracted from orchestrator.py to reduce its complexity and separate
the chunked/distributed analysis concerns.
"""

from pathlib import Path
from typing import List

from ..core.large_repo import HierarchicalRepoSplitter
from .orchestrator_handlers import (
    _export_calls,
    _export_project_toon,
    _export_readme,
    _export_index_html,
)


def _export_chunked(
    args,
    result,
    output_dir: Path,
    source_path: Path,
    formats: List[str],
    requested_formats: List[str],
):
    """Export chunked analysis results."""
    from .orchestrator import _export_registry_formats
    from .code2logic import _export_code2logic
    from .prompt import _export_chunked_prompt_txt

    subprojects = _get_filtered_subprojects(args, source_path)
    for sp in subprojects:
        _process_subproject(args, sp, output_dir)

    _export_registry_formats(args, result, output_dir, ['toon', 'map', 'context', 'evolution'])

    if 'calls' in formats or 'calls_toon' in formats:
        _export_calls(args, result, output_dir, formats)
    if 'all' in requested_formats:
        _export_project_toon(args, result, output_dir)

    if source_path is not None:
        _export_code2logic(args, source_path, output_dir, formats)
        _export_chunked_prompt_txt(args, output_dir, requested_formats, source_path, subprojects)

    _export_readme(args, result, output_dir)
    _export_index_html(args, output_dir)


def _get_filtered_subprojects(args, source_path: Path):
    """Get filtered subprojects list based on CLI arguments."""
    splitter = HierarchicalRepoSplitter(size_limit_kb=args.chunk_size)
    subprojects = splitter.get_analysis_plan(source_path)

    if getattr(args, 'only_subproject', None):
        subprojects = [
            sp for sp in subprojects
            if sp.name == args.only_subproject or sp.name.startswith(args.only_subproject + '.')
        ]
    if getattr(args, 'skip_subprojects', None):
        subprojects = [
            sp for sp in subprojects
            if not any(sp.name.startswith(skip) for skip in args.skip_subprojects)
        ]
    return subprojects


def _process_subproject(args, sp, output_dir: Path):
    """Process a single subproject result."""
    sp_output_dir = output_dir / sp.name.replace('.', '_')
    if not sp_output_dir.exists():
        return
    for ext in ['.toon', '.yaml', '.json']:
        result_file = sp_output_dir / f'analysis{ext}'
        if result_file.exists():
            if args.verbose:
                level_name = {0: 'root', 1: 'L1', 2: 'L2'}.get(sp.level, f'L{sp.level}')
                print(f"  - Exported [{level_name}] {sp.name}")
            break


__all__ = [
    '_export_chunked',
    '_get_filtered_subprojects',
    '_process_subproject',
]
