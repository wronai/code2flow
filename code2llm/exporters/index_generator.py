"""Index HTML Generator — backward compatibility shim.

This module re-exports from index_generator package.
The implementation has been split into:
  - index_generator/scanner.py - FileScanner
  - index_generator/renderer.py - HTMLRenderer  
  - index_generator/__init__.py - IndexHTMLGenerator facade
"""

# Re-export all public names from the new package
from code2llm.exporters.index_generator import (
    IndexHTMLGenerator,
    FileScanner,
    HTMLRenderer,
    generate_index_html,
    get_file_types,
    get_default_file_info,
    FILE_TYPES,
)

__all__ = [
    'IndexHTMLGenerator',
    'FileScanner',
    'HTMLRenderer',
    'generate_index_html',
    'get_file_types',
    'get_default_file_info',
    'FILE_TYPES',
]
