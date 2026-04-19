"""Evolution Exporter — backward compatibility shim.

Generates evolution.toon.yaml with refactoring queue.

Implementation has been split into:
  - evolution/constants.py - Thresholds and patterns
  - evolution/exclusion.py - Path filtering
  - evolution/computation.py - Metrics calculation
  - evolution/render.py - Text output generation
  - evolution/yaml_export.py - Structured YAML output
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .base import BaseExporter, export_format
from code2llm.core.models import AnalysisResult

from .evolution import (
    # Constants
    CC_SPLIT_THRESHOLD,
    EXCLUDE_PATTERNS,
    # Exclusion
    is_excluded,
    # Computation
    build_context,
    # Render
    render_header,
    render_next,
    render_risks,
    render_metrics_target,
    render_patterns,
    render_history,
    # YAML Export
    export_to_yaml as _export_to_yaml,
)


@export_format("evolution", description="Evolution refactoring queue format", extension=".toon.yaml")
class EvolutionExporter(BaseExporter):
    """Export evolution.toon.yaml — prioritized refactoring queue."""

    # Exclude patterns (mirrors ToonExporter)
    EXCLUDE_PATTERNS = EXCLUDE_PATTERNS

    def _is_excluded(self, path: str) -> bool:
        """Check if path should be excluded (venv, site-packages, etc.)."""
        return is_excluded(path)

    def export(self, result: AnalysisResult, output_path: str, **kwargs) -> Optional[Path]:
        """Generate evolution.toon."""
        ctx = build_context(result)

        sections: List[str] = []
        sections.extend(render_header(ctx))
        sections.append("")
        sections.extend(render_next(ctx))
        sections.append("")
        sections.extend(render_risks(ctx))
        sections.append("")
        sections.extend(render_metrics_target(ctx))
        sections.append("")
        sections.extend(render_patterns(ctx))
        sections.append("")
        sections.extend(render_history(ctx, output_path))

        path = self._ensure_dir(output_path)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(sections) + "\n")
        return path

    def export_to_yaml(self, result: AnalysisResult, output_path: str, **kwargs) -> None:
        """Generate evolution.toon.yaml (structured YAML)."""
        _export_to_yaml(result, output_path)
