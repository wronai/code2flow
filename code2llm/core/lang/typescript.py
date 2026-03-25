"""TypeScript/JavaScript analyzer (regex-based)."""

import re
from pathlib import Path
from typing import Dict

from ..models import ClassInfo, FunctionInfo, ModuleInfo
from .base import calculate_complexity_regex, extract_calls_regex


def analyze_typescript_js(content: str, file_path: str, module_name: str,
                          ext: str, stats: Dict) -> Dict:
    """Analyze TypeScript/JavaScript files using regex-based parsing."""
    result = {
        'module': ModuleInfo(
            name=module_name,
            file=file_path,
            is_package=Path(file_path).name in ('index.ts', 'index.js', 'index.tsx', 'index.jsx')
        ),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }

    lines = content.split('\n')

    # Patterns for TypeScript/JavaScript
    import_pattern = re.compile(r"^\s*import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]")
    class_pattern = re.compile(r"^\s*(?:export\s+)?(?:default\s+)?(?:abstract\s+)?class\s+(\w+)\s*(?:<[^>]+>)?(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?")
    func_pattern = re.compile(r"^\s*(?:export\s+)?(?:async\s+)?(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?[\(\w])")
    interface_pattern = re.compile(r"^\s*(?:export\s+)?interface\s+(\w+)(?:<[^>]+>)?")
    # Decorator pattern: @Component(), @Injectable, etc.
    decorator_pattern = re.compile(r"^\s*@(\w+(?:\.\w+)?)(?:\([^)]*\))?")
    # Standalone arrow function: export const fn = (x: T) => { ... }
    arrow_func_pattern = re.compile(
        r"^\s*(?:export\s+)?\s*"
        r"(?:const|let|var)\s+"
        r"(\w+)\s*(?::\s*[^=]+)?\s*="  # name with optional type annotation
        r"\s*(?:<[^>]+>\s*)?"  # optional generics
        r"(?:async\s+)?"
        r"\([^)]*\)\s*(?::\s*[^=]+)?\s*=>"
    )
    # Class method patterns: shorthand methods, getters, setters, arrow props
    method_pattern = re.compile(
        r"^\s*(?:(?:public|private|protected|static|readonly|abstract|async|override)\s+)*"
        r"(?:get\s+|set\s+)?"
        r"(\w+)\s*(?:<[^>]*>)?\s*\([^)]*\)"
    )
    arrow_prop_pattern = re.compile(
        r"^\s*(?:(?:public|private|protected|static|readonly)\s+)*"
        r"(\w+)\s*(?::\s*[^=]+)?\s*="  # name with optional type
        r"\s*(?:<[^>]+>\s*)?"
        r"(?:async\s+)?"
        r"(?:\([^)]*\)|[a-zA-Z_]\w*)\s*=>"
    )

    current_class = None
    class_brace_depth = 0
    brace_depth = 0
    pending_decorators = []  # Collect decorators before class/method/function

    for line_no, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('/*') or line.startswith('*'):
            # Still track braces in comments? No — skip them
            continue

        # Track brace depth for class scope
        for ch in raw_line:
            if ch == '{':
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1

        # End of class scope
        if current_class and brace_depth < class_brace_depth:
            current_class = None
            class_brace_depth = 0

        # Decorators (accumulate for next entity)
        decorator_match = decorator_pattern.match(line)
        if decorator_match:
            pending_decorators.append(decorator_match.group(1))
            continue

        # Imports
        import_match = import_pattern.match(line)
        if import_match:
            result['module'].imports.append(import_match.group(1))
            continue

        # Classes
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            qualified_name = f"{module_name}.{class_name}"
            bases = []
            if class_match.group(2):
                bases.append(class_match.group(2).strip())
            if class_match.group(3):
                bases.extend([b.strip() for b in class_match.group(3).split(',')])

            class_info = ClassInfo(
                name=class_name,
                qualified_name=qualified_name,
                file=file_path,
                line=line_no,
                module=module_name,
                bases=bases,
                methods=[],
                docstring="",
            )
            result['classes'][qualified_name] = class_info
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1
            current_class = qualified_name
            class_brace_depth = brace_depth
            pending_decorators.clear()
            continue

        # Interfaces (treat as classes)
        interface_match = interface_pattern.match(line)
        if interface_match:
            class_name = interface_match.group(1)
            qualified_name = f"{module_name}.{class_name}"
            result['classes'][qualified_name] = ClassInfo(
                name=class_name,
                qualified_name=qualified_name,
                file=file_path,
                line=line_no,
                module=module_name,
                bases=[],
                methods=[],
                docstring="",
            )
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1
            pending_decorators.clear()
            continue

        # Standalone functions (function declarations & const/let/var arrows)
        func_match = func_pattern.match(line)
        arrow_match = arrow_func_pattern.match(line)
        if not current_class:
            func_name = None
            if func_match:
                func_name = func_match.group(1) or func_match.group(2)
            elif arrow_match:
                func_name = arrow_match.group(1)

            if func_name:
                qualified_name = f"{module_name}.{func_name}"
                result['functions'][qualified_name] = FunctionInfo(
                    name=func_name,
                    qualified_name=qualified_name,
                    file=file_path,
                    line=line_no,
                    column=0,
                    module=module_name,
                    class_name=None,
                    is_method=False,
                    is_private=func_name.startswith('_'),
                    is_property=False,
                    docstring="",
                    args=[],
                    decorators=pending_decorators[:],
                )
                result['module'].functions.append(qualified_name)
                stats['functions_found'] += 1
                pending_decorators.clear()
                continue

        # Class members: methods (shorthand syntax) & arrow property methods
        if current_class:
            _matched_method = False
            # Arrow property: myMethod = (args) => { ... }
            arrow_meth_match = arrow_prop_pattern.match(line)
            if arrow_meth_match:
                method_name = arrow_meth_match.group(1)
                if method_name not in ('constructor', 'if', 'for', 'while', 'switch', 'return'):
                    _matched_method = True

            # Shorthand method: myMethod(args) { ... }
            if not _matched_method:
                meth_match = method_pattern.match(line)
                if meth_match:
                    method_name = meth_match.group(1)
                    if method_name not in ('if', 'for', 'while', 'switch', 'return',
                                           'catch', 'class', 'import', 'export', 'new'):
                        _matched_method = True

            # Also catch const/let/var arrows inside class (rare but valid)
            if not _matched_method and func_match:
                fname = func_match.group(1) or func_match.group(2)
                if fname:
                    method_name = fname
                    _matched_method = True

            if _matched_method:
                qualified_name = f"{current_class}.{method_name}"
                result['classes'][current_class].methods.append(qualified_name)
                result['functions'][qualified_name] = FunctionInfo(
                    name=method_name,
                    qualified_name=qualified_name,
                    file=file_path,
                    line=line_no,
                    column=0,
                    module=module_name,
                    class_name=current_class.split('.')[-1],
                    is_method=True,
                    is_private=method_name.startswith('_') or method_name.startswith('#'),
                    is_property=False,
                    docstring="",
                    args=[],
                    decorators=pending_decorators[:],
                )
                result['module'].functions.append(qualified_name)
                stats['functions_found'] += 1
                pending_decorators.clear()
                continue

        # Clear decorators if we hit a non-matching line (they don't carry over)
        # But only if it's not an empty line or comment (handled above)
        if pending_decorators and not (func_match or arrow_match or class_match or interface_match or method_pattern.match(line)):
            pending_decorators.clear()

    # Regex-based complexity estimation and call extraction
    calculate_complexity_regex(content, result, lang='c_family')
    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result
