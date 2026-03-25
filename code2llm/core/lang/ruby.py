"""Ruby analyzer (regex-based)."""

import re
from typing import Dict

from ..models import ClassInfo, FunctionInfo, ModuleInfo
from .base import extract_calls_regex


def _extract_ruby_body(content: str, start_line: int) -> str:
    """Extract Ruby function body from def to corresponding end."""
    lines = content.split('\n')
    if start_line < 1 or start_line > len(lines):
        return ''

    # Find the def line
    def_line_idx = start_line - 1
    while def_line_idx < len(lines):
        if re.match(r'^\s*def\s+', lines[def_line_idx]):
            break
        def_line_idx += 1

    if def_line_idx >= len(lines):
        return ''

    # Count indentation of def line
    def_indent = len(lines[def_line_idx]) - len(lines[def_line_idx].lstrip())

    body_lines = []
    # Track nested blocks: def, if, unless, while, until, for, case, begin, class, module
    nested_depth = 1  # Start at 1 for the def itself
    i = def_line_idx + 1

    while i < len(lines) and nested_depth > 0:
        line = lines[i]
        stripped = line.strip()

        # Check if this line is at same indentation level or less than def
        # and starts with an end
        if line.startswith('end') and len(line) == 3 or line.startswith('end '):
            nested_depth -= 1
            if nested_depth == 0:
                break
        elif re.match(r'^\s*(def|if|unless|while|until|for|case|begin|class|module)\b', line):
            # Another block starter at same or deeper level
            nested_depth += 1

        body_lines.append(line)
        i += 1

    return '\n'.join(body_lines)


# Ruby CC pattern: 'if', 'unless', 'while', 'until', 'for', 'case/when', '&&', '||', ternary
# Note: && and || are not word chars, so we can't use \b on both sides
_RUBY_CC_PATTERN = re.compile(
    r'\b(?:if|unless|while|until|for|case|when)\b|&&|\|\||\?\s*[^:]*\s*:'
)


def analyze_ruby(content: str, file_path: str, module_name: str,
                 stats: Dict) -> Dict:
    """Analyze Ruby files using regex-based parsing."""
    result = {
        'module': ModuleInfo(name=module_name, file=file_path, is_package=False),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }

    lines = content.split('\n')

    # Patterns for Ruby
    require_pattern = re.compile(r'^\s*require\s*["\']([^"\']+)["\']')
    module_pattern = re.compile(r'^\s*module\s+(\w+)')
    class_pattern = re.compile(
        r'^\s*class\s+(\w+)'
        r'(?:\s*<\s*(\w+))?'
    )
    def_pattern = re.compile(r'^\s*def\s+(?:self\.)?(\w+[?!]?)')

    current_module = None
    current_class = None
    brace_depth = 0
    class_depth = 0
    module_depth = 0

    for line_no, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Track brace/end depth (Ruby uses 'end' mostly)
        # Simple heuristic: count 'def', 'class', 'module', 'if', 'while', 'for' as depth increases
        # and 'end' as depth decreases
        control_starts = len(re.findall(r'\b(def|class|module|if|unless|while|until|for|begin|case)\b', line))
        if line.startswith('end'):
            control_starts -= 1

        # Requires
        require_match = require_pattern.match(line)
        if require_match:
            result['module'].imports.append(require_match.group(1))
            continue

        # Modules
        mod_match = module_pattern.match(line)
        if mod_match:
            module_name_inner = mod_match.group(1)
            current_module = module_name_inner
            module_depth = control_starts
            continue

        # Classes
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            bases = []
            if class_match.group(2):
                bases.append(class_match.group(2).strip())

            if current_module:
                qualified_name = f"{module_name}.{current_module}.{class_name}"
            else:
                qualified_name = f"{module_name}.{class_name}"
            result['classes'][qualified_name] = ClassInfo(
                name=class_name, qualified_name=qualified_name,
                file=file_path, line=line_no, module=module_name,
                bases=bases, methods=[], docstring="",
            )
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1
            current_class = qualified_name
            class_depth = control_starts
            continue

        # Methods (def)
        def_match = def_pattern.match(line)
        if def_match:
            method_name = def_match.group(1)
            # Skip keywords
            if method_name in ('if', 'unless', 'while', 'until', 'for', 'class', 'module'):
                continue

            if current_class:
                qualified_name = f"{current_class}.{method_name}"
                result['classes'][current_class].methods.append(qualified_name)
                is_method = True
                class_name = current_class.split('.')[-1]
            else:
                if current_module:
                    qualified_name = f"{module_name}.{current_module}.{method_name}"
                else:
                    qualified_name = f"{module_name}.{method_name}"
                is_method = False
                class_name = None

            result['functions'][qualified_name] = FunctionInfo(
                name=method_name, qualified_name=qualified_name,
                file=file_path, line=line_no, column=0,
                module=module_name, class_name=class_name,
                is_method=is_method, is_private=method_name.startswith('_'),
                is_property=False, docstring="", args=[], decorators=[],
            )
            result['module'].functions.append(qualified_name)
            stats['functions_found'] += 1

    # Regex-based complexity estimation
    for func_info in result['functions'].values():
        body = _extract_ruby_body(content, func_info.line)
        if not body:
            cc = 1
        else:
            cc = 1 + len(_RUBY_CC_PATTERN.findall(body))
        rank = 'A' if cc <= 5 else ('B' if cc <= 10 else ('C' if cc <= 20 else 'D'))
        func_info.complexity = {
            'cyclomatic_complexity': cc,
            'cc_rank': rank,
        }

    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result
