"""C++ analyzer (regex-based, with tree-sitter support)."""

import re
from typing import Dict

from code2llm.core.lang.base import analyze_c_family

# C++-specific patterns
_CPP_PATTERNS = {
    'import': re.compile(r'^\s*#include\s*["<]([^">]+)[">]'),
    'class': re.compile(
        r'^\s*(?:class|struct)\s+(\w+)'
        r'(?:\s*:\s*(?:public|private|protected)\s+(\w+))?'
    ),
    'function': re.compile(
        r'^\s*(?:virtual\s+|static\s+|inline\s+)?'
        r'(?:[\w:*&<>\s]+\s+)?'
        r'(\w+)\s*\([^)]*\)'
    ),
}

_CPP_CONFIG = {
    'index_files': (),
    'brace_track': True,
    'reserved': {'if', 'for', 'while', 'switch', 'return', 'catch', 'class'},
}


def analyze_cpp(content: str, file_path: str, module_name: str,
                ext: str, stats: Dict) -> Dict:
    """Analyze C++ files using shared C-family extraction."""
    return analyze_c_family(
        content, file_path, module_name, stats,
        _CPP_PATTERNS, _CPP_CONFIG, ext=ext,
    )
