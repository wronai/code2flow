"""C# analyzer (regex-based)."""

import re
from typing import Dict

from ..models import ClassInfo, FunctionInfo, ModuleInfo
from .base import calculate_complexity_regex, extract_calls_regex


def analyze_csharp(content: str, file_path: str, module_name: str,
                   stats: Dict) -> Dict:
    """Analyze C# files using regex-based parsing."""
    result = {
        'module': ModuleInfo(name=module_name, file=file_path, is_package=False),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }

    lines = content.split('\n')

    # Patterns for C#
    using_pattern = re.compile(r'^\s*using\s+([\w.]+)')
    namespace_pattern = re.compile(r'^\s*namespace\s+([\w.]+)')
    class_pattern = re.compile(
        r'^\s*(?:public\s+|private\s+|protected\s+|internal\s+)?'
        r'(?:abstract\s+|sealed\s+|static\s+)?'
        r'(?:class|struct|interface|record)\s+(\w+)'
    )
    method_pattern = re.compile(
        r'^\s*(?:public\s+|private\s+|protected\s+|internal\s+)?'
        r'(?:static\s+|virtual\s+|override\s+|abstract\s+|async\s+)?'
        r'[\w<>,?\[\]]+\s+'  # return type
        r'(\w+)\s*\([^)]*\)'  # method name
    )
    prop_pattern = re.compile(
        r'^\s*(?:public\s+|private\s+|protected\s+|internal\s+)?'
        r'(?:static\s+)?'
        r'[\w<>,?\[\]]+\s+'  # type
        r'(\w+)\s*\{\s*(?:get|set)'  # property name with getter/setter
    )

    current_namespace = None
    current_class = None
    brace_depth = 0
    class_brace_depth = 0

    for line_no, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('/*'):
            continue

        # Track brace depth
        for ch in raw_line:
            if ch == '{':
                brace_depth += 1
            elif ch == '}':
                brace_depth -= 1

        # End of class scope
        if current_class and brace_depth < class_brace_depth:
            current_class = None
            class_brace_depth = 0

        # Usings
        using_match = using_pattern.match(line)
        if using_match:
            result['module'].imports.append(using_match.group(1))
            continue

        # Namespace
        ns_match = namespace_pattern.match(line)
        if ns_match:
            current_namespace = ns_match.group(1)
            continue

        # Classes/structs/interfaces/records
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            if current_namespace:
                qualified_name = f"{module_name}.{current_namespace}.{class_name}"
            else:
                qualified_name = f"{module_name}.{class_name}"
            result['classes'][qualified_name] = ClassInfo(
                name=class_name, qualified_name=qualified_name,
                file=file_path, line=line_no, module=module_name,
                bases=[], methods=[], docstring="",
            )
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1
            current_class = qualified_name
            class_brace_depth = brace_depth
            continue

        # Methods
        method_match = method_pattern.match(line)
        if method_match:
            method_name = method_match.group(1)
            # Skip if it looks like a keyword or property pattern matched
            if method_name in ('if', 'for', 'while', 'switch', 'catch', 'return',
                               'foreach', 'using', 'lock', 'fixed', 'checked', 'unchecked'):
                continue

            if current_class:
                qualified_name = f"{current_class}.{method_name}"
                result['classes'][current_class].methods.append(qualified_name)
                is_method = True
                class_name = current_class.split('.')[-1]
            else:
                # Top-level method (C# 9+)
                if current_namespace:
                    qualified_name = f"{module_name}.{current_namespace}.{method_name}"
                else:
                    qualified_name = f"{module_name}.{method_name}"
                is_method = False
                class_name = None

            result['functions'][qualified_name] = FunctionInfo(
                name=method_name, qualified_name=qualified_name,
                file=file_path, line=line_no, column=0,
                module=module_name, class_name=class_name,
                is_method=is_method, is_private=False,
                is_property=False, docstring="", args=[], decorators=[],
            )
            result['module'].functions.append(qualified_name)
            stats['functions_found'] += 1
            continue

        # Properties (treat as methods with is_property flag)
        prop_match = prop_pattern.match(line)
        if prop_match and current_class:
            prop_name = prop_match.group(1)
            qualified_name = f"{current_class}.{prop_name}"
            result['classes'][current_class].methods.append(qualified_name)
            result['functions'][qualified_name] = FunctionInfo(
                name=prop_name, qualified_name=qualified_name,
                file=file_path, line=line_no, column=0,
                module=module_name, class_name=current_class.split('.')[-1],
                is_method=True, is_private=False,
                is_property=True, docstring="", args=[], decorators=[],
            )
            result['module'].functions.append(qualified_name)
            stats['functions_found'] += 1

    # Regex-based complexity estimation and call extraction
    calculate_complexity_regex(content, result, lang='c_family')
    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result
