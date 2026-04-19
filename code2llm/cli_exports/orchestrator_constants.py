"""Export orchestrator constants — format filenames, labels, and dry-run mappings.

This module centralizes all format-related constants for the export system
to avoid duplication and enable easier maintenance.
"""

from typing import Dict, List


# Format output filenames
FORMAT_FILENAMES: Dict[str, str] = {
    'toon': 'analysis.toon.yaml',
    'map': 'map.toon.yaml',
    'flow': 'flow.toon.yaml',
    'context': 'context.md',
    'yaml': 'analysis.yaml',
    'json': 'analysis.json',
    'evolution': 'evolution.toon.yaml',
    'readme': 'README.md',
    'project-yaml': 'project.yaml',
}

# Files produced per format in dry-run preview
FORMAT_DRY_RUN_FILES: Dict[str, List[str]] = {
    'toon':      ['analysis.toon'],
    'map':       ['map.toon.yaml'],
    'evolution': ['evolution.toon.yaml'],
    'context':   ['context.md'],
    'mermaid':   ['calls.mmd', 'calls.png'],
    'yaml':      ['analysis.yaml'],
    'json':      ['analysis.json'],
    'readme':    ['README.md'],
}

# Human-readable labels
FORMAT_LABELS: Dict[str, str] = {
    'toon': 'TOON (diagnostics)',
    'map': 'MAP (structure)',
    'flow': 'FLOW (data-flow)',
    'context': 'CONTEXT (LLM narrative)',
    'yaml': 'YAML',
    'json': 'JSON',
    'evolution': 'EVOLUTION (refactoring queue)',
    'readme': 'README (documentation)',
    'project-yaml': 'PROJECT-YAML (single source of truth)',
}

__all__ = [
    'FORMAT_FILENAMES',
    'FORMAT_DRY_RUN_FILES',
    'FORMAT_LABELS',
]
