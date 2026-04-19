"""Map Exporter — backward compatibility shim.

Implementation has been split into:
  - map/utils.py - Path handling, line counting, language detection
  - map/alerts.py - Alerts and hotspots for header
  - map/header.py - Header rendering with stats
  - map/module_list.py - M[] module list rendering
  - map/details.py - D: details per module
  - map/yaml_export.py - YAML structured export
"""

from pathlib import Path
from typing import List, Optional

from .base import BaseExporter, export_format
from .flow_constants import is_excluded_path
from code2llm.core.models import AnalysisResult

from .map import (
    render_header,
    render_module_list,
    render_details,
    export_to_yaml,
)


@export_format("map", description="Structural map format", extension=".toon.yaml")
class MapExporter(BaseExporter):
    """Export to map.toon.yaml — structural map with a compact project header.

    Keys: M=modules, D=details, i=imports, e=exports, c=classes, f=functions,
    m=methods
    """

    def export(self, result: AnalysisResult, output_path: str, **kwargs) -> Optional[Path]:
        """Export analysis result to .map format."""
        lines: List[str] = []
        lines.extend(render_header(result, output_path, is_excluded_path))
        lines.extend(render_module_list(result, is_excluded_path))
        lines.extend(render_details(result, is_excluded_path))

        path = self._ensure_dir(output_path)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        return path

    def export_to_yaml(self, result: AnalysisResult, output_path: str, **kwargs) -> None:
        """Export analysis result to map.toon.yaml format (structured YAML)."""
        export_to_yaml(result, output_path, is_excluded_path)

