"""Evolution exporter package — prioritized refactoring queue for iterative improvement.

This package provides:
- constants: Thresholds and exclusion patterns
- exclusion: Path filtering logic
- computation: Metrics calculation (god modules, hub types, etc.)
- render: Text output generation for evolution.toon
- yaml_export: Structured YAML output for evolution.toon.yaml

All public names are re-exported here for backward compatibility
with the original evolution_exporter.py module structure.
"""

# Constants
from .constants import (
    CC_SPLIT_THRESHOLD,
    FAN_OUT_THRESHOLD,
    GOD_MODULE_LINES,
    HUB_TYPE_THRESHOLD,
    EXCLUDE_PATTERNS,
)

# Exclusion
from .exclusion import is_excluded

# Computation
from .computation import (
    compute_func_data,
    scan_file_sizes,
    aggregate_file_stats,
    make_relative_path,
    filter_god_modules,
    compute_god_modules,
    compute_hub_types,
    build_context,
)

# Render
from .render import (
    render_header,
    render_next,
    render_risks,
    render_metrics_target,
    render_patterns,
    render_history,
)

# YAML Export
from .yaml_export import export_to_yaml

__all__ = [
    # Constants
    'CC_SPLIT_THRESHOLD',
    'FAN_OUT_THRESHOLD',
    'GOD_MODULE_LINES',
    'HUB_TYPE_THRESHOLD',
    'EXCLUDE_PATTERNS',
    # Exclusion
    'is_excluded',
    # Computation
    'compute_func_data',
    'scan_file_sizes',
    'aggregate_file_stats',
    'make_relative_path',
    'filter_god_modules',
    'compute_god_modules',
    'compute_hub_types',
    'build_context',
    # Render
    'render_header',
    'render_next',
    'render_risks',
    'render_metrics_target',
    'render_patterns',
    'render_history',
    # YAML Export
    'export_to_yaml',
]
