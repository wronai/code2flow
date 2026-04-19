"""README exporter package — generate comprehensive README.md documentation.

This package provides:
- insights: Extract health metrics from analysis files
- files: Detect which analysis files exist
- sections: Build dynamic documentation tables
- content: Main README template and content generation

All public names are re-exported here for backward compatibility
with the original readme_exporter.py module structure.
"""

# Insights
from .insights import extract_insights

# Files
from .files import get_existing_files

# Sections
from .sections import (
    build_core_files_section,
    build_llm_files_section,
    build_viz_files_section,
)

# Content
from .content import generate_readme_content

__all__ = [
    # Insights
    'extract_insights',
    # Files
    'get_existing_files',
    # Sections
    'build_core_files_section',
    'build_llm_files_section',
    'build_viz_files_section',
    # Content
    'generate_readme_content',
]
