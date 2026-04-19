"""Map exporter package — generates map.toon.yaml (structural map).

This package provides:
- utils: Path handling, line counting, language detection
- alerts: Build alerts and hotspots for header
- header: Render header lines with project stats
- module_list: Render M[] module list
- details: Render D: details per module
- yaml_export: Export to structured YAML format

All public names are re-exported here for backward compatibility
with the original map_exporter.py module structure.
"""

# Utils
from .utils import (
    rel_path,
    file_line_count,
    count_total_lines,
    detect_languages,
)

# Alerts
from .alerts import (
    build_alerts,
    build_hotspots,
    load_evolution_trend,
)

# Header
from .header import render_header

# Module list
from .module_list import render_module_list

# Details
from .details import render_details

# YAML export
from .yaml_export import export_to_yaml

__all__ = [
    # Utils
    'rel_path',
    'file_line_count',
    'count_total_lines',
    'detect_languages',
    # Alerts
    'build_alerts',
    'build_hotspots',
    'load_evolution_trend',
    # Header
    'render_header',
    # Module list
    'render_module_list',
    # Details
    'render_details',
    # YAML export
    'export_to_yaml',
]
