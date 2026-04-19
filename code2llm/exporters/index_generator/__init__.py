"""Index HTML Generator — web-based file browser for all generated outputs.

Generates index.html that provides a GitHub Pages-ready interface
for browsing all generated analysis files (toon, md, yaml, json, etc.)

This package provides three components:
  - FileScanner: scans output directory and collects file metadata
  - HTMLRenderer: generates HTML with CSS and JavaScript
  - IndexHTMLGenerator: facade combining scanner and renderer
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

from .scanner import FileScanner, get_file_types, get_default_file_info, FILE_TYPES
from .renderer import HTMLRenderer


class IndexHTMLGenerator:
    """Generate index.html for browsing all generated files.

    This is a facade class that combines FileScanner and HTMLRenderer
    to provide a simple interface for generating the index file.
    """

    # Backward compatibility: expose FILE_TYPES at class level
    FILE_TYPES = FILE_TYPES

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir).resolve()
        self._scanner = FileScanner(self.output_dir)
        self._renderer = HTMLRenderer()

    def generate(self) -> Path:
        """Generate index.html in the output directory."""
        files = self._scanner.scan()
        html = self._renderer.render(files)
        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(html)
        return index_path

    def scan_files(self) -> List[Dict[str, Any]]:
        """Scan and return file metadata without generating HTML."""
        return self._scanner.scan()

    def render_html(self, files: List[Dict[str, Any]]) -> str:
        """Render HTML from pre-scanned file list."""
        return self._renderer.render(files)


# Convenience function for direct usage
def generate_index_html(output_dir: Path) -> Path:
    """Generate index.html in the specified directory.

    Args:
        output_dir: Directory containing generated analysis files

    Returns:
        Path to the generated index.html file
    """
    return IndexHTMLGenerator(output_dir).generate()


__all__ = [
    'IndexHTMLGenerator',
    'FileScanner',
    'HTMLRenderer',
    'generate_index_html',
    'get_file_types',
    'get_default_file_info',
    'FILE_TYPES',
]
