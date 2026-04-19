"""README file checking — detect which analysis files exist."""

from pathlib import Path
from typing import Dict


def get_existing_files(output_dir: Path) -> Dict[str, bool]:
    """Check which files exist in the output directory."""
    files_to_check = {
        'analysis.toon': 'Health diagnostics',
        'evolution.toon.yaml': 'Refactoring queue',
        'flow.toon': 'Data flow analysis',
        'map.toon.yaml': 'Structural map',
        'project.toon.yaml': 'Project logic',
        'prompt.txt': 'LLM prompt',
        'context.md': 'LLM narrative',
        'analysis.yaml': 'YAML data',
        'analysis.json': 'JSON data',
        'flow.mmd': 'Flow diagram',
        'calls.mmd': 'Call graph',
        'compact_flow.mmd': 'Module view',
    }
    return {name: (output_dir / name).exists() for name in files_to_check}


__all__ = ['get_existing_files']
