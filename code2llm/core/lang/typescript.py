import re
from typing import Dict
from code2llm.core.lang.base import calculate_complexity_regex, extract_calls_regex, _extract_declarations

def get_typescript_patterns() -> Dict[str, re.Pattern]:
    """Returns regex patterns for TypeScript/JavaScript parsing."""
    return {
        'import': re.compile(r"^\s*import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]"),
        'decorator': re.compile(r"^\s*@(\w+(?:\.\w+)?)(?:\([^)]*\))?"),
        'class': re.compile(
            r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)\s*(?:<[^>]+>)?(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?"
        ),
        'interface': re.compile(r"^\s*(?:export\s+)?interface\s+(\w+)(?:<[^>]+>)?"),
        'function': re.compile(
            r"^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?[\(\w])"
        ),
        'arrow_func': re.compile(
            r"^\s*(?:export\s+)?\s*(?:const|let|var)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:<[^>]+>\s*)?(?:async\s+)?\([^)]*\)\s*(?::\s*[^=]+)?\s*=>"
        ),
        'method': re.compile(
            r"^\s*(?:(?:public|private|protected|static|readonly|abstract|async|override)\s+)*(?:get\s+|set\s+)?(\w+)\s*(?:<[^>]*>)?\s*\([^)]*\)"
        ),
        'arrow_prop': re.compile(
            r"^\s*(?:(?:public|private|protected|static|readonly)\s+)*(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:<[^>]+>\s*)?(?:async\s+)?(?:\([^)]*\)|[a-zA-Z_]\w*)\s*=>"
        ),
    }

def get_typescript_lang_config() -> Dict:
    """Returns language configuration for TypeScript/JavaScript."""
    return {
        'index_files': ('index.ts', 'index.js', 'index.tsx', 'index.jsx'),
        'brace_track': True,
        'reserved': {'if', 'for', 'while', 'switch', 'return', 'catch', 'constructor',
                     'class', 'import', 'export', 'new'},
    }

def analyze_typescript_js(content: str, file_path: str, module_name: str,
                          ext: str, stats: Dict) -> Dict:
    """Analyze TypeScript/JavaScript files using shared extraction."""

    patterns = get_typescript_patterns()
    lang_config = get_typescript_lang_config()

    result = _extract_declarations(
        content, file_path, module_name,
        patterns, stats, lang_config
    )

    calculate_complexity_regex(content, result, lang='c_family')
    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result