"""Prompt generation — prompt.txt for LLM consumption (regular and chunked)."""

import sys
from pathlib import Path
from typing import List, Optional, Tuple


def _export_prompt_txt(args, output_dir: Path, formats: list[str], source_path: Optional[Path] = None) -> None:
    """Generate prompt.txt useful to send to an LLM."""
    if 'code2logic' not in formats and 'all' not in formats:
        return

    project_path, output_rel_path = _get_prompt_paths(source_path, output_dir)
    lines = _build_prompt_header(project_path)
    lines.extend(_build_main_files_section(output_dir, output_rel_path))

    missing = _get_missing_files(output_dir)
    if missing:
        lines.append("")
        lines.append("Missing files (not generated in this run):")
        for name in missing:
            lines.append(f"- {output_rel_path}/{name}")

    lines.extend(_build_prompt_footer(chunked=False))

    prompt_path = output_dir / 'prompt.txt'
    prompt_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    if args.verbose:
        print(f"  - PROMPT: {prompt_path}")


def _export_chunked_prompt_txt(args, output_dir: Path, formats: list[str], source_path: Optional[Path] = None, subprojects: list = None) -> None:
    """Generate prompt.txt for chunked analysis with all subproject files."""
    if 'code2logic' not in formats and 'all' not in formats:
        return

    project_path, output_rel_path = _get_prompt_paths(source_path, output_dir)
    lines = _build_prompt_header(project_path)
    lines.extend(_build_main_files_section(output_dir, output_rel_path))

    if subprojects:
        lines.extend(_build_subprojects_section(subprojects, output_dir, output_rel_path))

    lines.extend(_build_missing_files_section(output_dir, output_rel_path))
    lines.extend(_build_prompt_footer(chunked=True))

    prompt_path = output_dir / 'prompt.txt'
    prompt_path.write_text("\n".join(lines) + "\n", encoding='utf-8')
    if args.verbose:
        print(f"  - PROMPT (chunked): {prompt_path}")


# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------
def _get_prompt_paths(source_path: Optional[Path], output_dir: Path) -> Tuple[str, str]:
    """Determine project name and relative output path."""
    if source_path:
        project_path = source_path.name if source_path.name else str(source_path)
        try:
            output_rel_path = str(output_dir.relative_to(source_path))
        except ValueError:
            output_rel_path = str(output_dir)
    else:
        cwd = Path.cwd()
        project_path = cwd.name
        try:
            output_rel_path = str(output_dir.relative_to(cwd))
        except ValueError:
            output_rel_path = str(output_dir)
    return project_path, output_rel_path


_MAIN_FILES = [
    ('analysis.toon', 'Health diagnostics - complexity metrics, god modules, coupling issues, refactoring priorities'),
    ('context.md', 'LLM narrative - architecture summary, key entry points, process flows, public API surface'),
    ('evolution.toon', 'Refactoring queue - ranked actions by impact/effort, risks, metrics targets, history'),
    ('project.toon', 'Project logic - compact module view from code2logic, file sizes, dependencies overview'),
    ('README.md', 'Documentation - complete guide to all generated files, usage examples, interpretation'),
]


def _build_prompt_header(project_path: str) -> List[str]:
    """Build header section of prompt."""
    return [
        "You are an AI assistant helping me understand and improve a codebase.",
        "Use the attached/generated files as the authoritative context.",
        "",
        f"we are in project path: {project_path}",
        "",
        "Files for analysis:",
    ]


def _build_main_files_section(output_dir: Path, output_rel_path: str) -> List[str]:
    """Build main files section."""
    lines = []
    for name, desc in _MAIN_FILES:
        if (output_dir / name).exists():
            lines.append(f"- {output_rel_path}/{name}  ({desc})")
    return lines


def _get_missing_files(output_dir: Path) -> List[str]:
    """Return names of expected main files that are missing."""
    return [name for name, _ in _MAIN_FILES if name != 'project.toon' and not (output_dir / name).exists()]


def _build_subprojects_section(subprojects: list, output_dir: Path, output_rel_path: str) -> List[str]:
    """Build subprojects section."""
    lines = [
        "",
        "Subproject Analysis Files (hierarchical chunking for large repository):",
    ]

    for sp in subprojects:
        sp_dir = output_dir / sp.name.replace('.', '_')
        if not sp_dir.exists():
            continue

        level_name = {0: 'root', 1: 'L1', 2: 'L2', 3: 'chunk'}.get(sp.level, f'L{sp.level}')
        sp_files = [f for f in ['analysis.toon', 'context.md', 'evolution.toon'] if (sp_dir / f).exists()]

        if sp_files:
            file_list = ', '.join(sp_files)
            lines.append(f"- {output_rel_path}/{sp.name.replace('.', '_')}/  [{level_name}] ~{sp.estimated_size_kb}KB - Contains: {file_list}")

    return lines


def _build_missing_files_section(output_dir: Path, output_rel_path: str) -> List[str]:
    """Build missing files section."""
    missing = _get_missing_files(output_dir)
    if not missing:
        return []
    lines = ["", "Missing files (not generated in this run):"]
    for name in missing:
        lines.append(f"- {output_rel_path}/{name}")
    return lines


def _build_prompt_footer(chunked: bool = False) -> List[str]:
    """Build footer section of prompt."""
    lines = [
        "",
        "Task:",
        "- Summarize the architecture and main flows.",
        "- Identify the highest-risk areas and propose a refactoring plan.",
        "- If you suggest changes, keep behavior backward compatible and provide concrete steps.",
        "",
        "Constraints:",
        "- Prefer minimal, incremental changes.",
        "- If uncertain, ask clarifying questions.",
    ]
    if chunked:
        lines.extend([
            "",
            "Note: This repository was analyzed using hierarchical chunking due to its size.",
            "      Start with the main files (analysis.toon, context.md) for overview,",
            "      then examine specific subproject directories as needed.",
        ])
    return lines
