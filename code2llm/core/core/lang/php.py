"""PHP analyzer (regex-based)."""

import re
from typing import Dict

from ...models import ClassInfo, FunctionInfo, ModuleInfo
from .base import calculate_complexity_regex, extract_calls_regex


def analyze_php(content: str, file_path: str, module_name: str,
                stats: Dict) -> Dict:
    """Analyze PHP files using regex-based parsing."""
    result = {
        'module': ModuleInfo(name=module_name, file=file_path, is_package=False),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }

    lines = content.split('\n')

    # Patterns for PHP
    include_pattern = re.compile(r'^\s*(?:include|require|include_once|require_once)\s*["\']([^"\']+)["\']')
    namespace_pattern = re.compile(r'^\s*namespace\s+([\\\w]+)')
    use_pattern = re.compile(r'^\s*use\s+([\\\w]+)')
    class_pattern = re.compile(
        r'^\s*(?:abstract\s+|final\s+)?'
        r'class\s+(\w+)'
        r'(?:\s+extends\s+(\w+))?'
        r'(?:\s+implements\s+([\w,\s\\]+))?'
    )
    interface_pattern = re.compile(r'^\s*interface\s+(\w+)')
    trait_pattern = re.compile(r'^\s*trait\s+(\w+)')
    func_pattern = re.compile(
        r'^\s*(?:public\s+|private\s+|protected\s+)?'
        r'(?:static\s+)?'
        r'function\s+(\w+)\s*\('
    )

    current_namespace = None
    current_class = None
    brace_depth = 0
    class_brace_depth = 0
    in_php = False

    for line_no, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()

        # Track PHP context
        if line.startswith('<?php') or line.startswith('<?'):
            in_php = True
            continue
        if line == '?>':
            in_php = False
            continue
        if not in_php and not line.startswith('<?'):
            continue

        if not line or line.startswith('//'):
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

        # Includes
        include_match = include_pattern.match(line)
        if include_match:
            result['module'].imports.append(include_match.group(1))
            continue

        # Namespace
        ns_match = namespace_pattern.match(line)
        if ns_match:
            current_namespace = ns_match.group(1)
            continue

        # Use statements
        use_match = use_pattern.match(line)
        if use_match:
            result['module'].imports.append(use_match.group(1))
            continue

        # Classes
        class_match = class_pattern.match(line)
        if class_match:
            class_name = class_match.group(1)
            bases = []
            if class_match.group(2):
                bases.append(class_match.group(2).strip())
            if class_match.group(3):
                bases.extend([b.strip() for b in class_match.group(3).split(',')])

            if current_namespace:
                qualified_name = f"{module_name}.{current_namespace}.{class_name}"
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
            class_brace_depth = brace_depth
            continue

        # Interfaces
        interface_match = interface_pattern.match(line)
        if interface_match:
            class_name = interface_match.group(1)
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
            continue

        # Traits
        trait_match = trait_pattern.match(line)
        if trait_match:
            class_name = trait_match.group(1)
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
            continue

        # Functions/methods
        func_match = func_pattern.match(line)
        if func_match:
            func_name = func_match.group(1)
            if current_class:
                qualified_name = f"{current_class}.{func_name}"
                result['classes'][current_class].methods.append(qualified_name)
                is_method = True
                class_name = current_class.split('.')[-1]
            else:
                if current_namespace:
                    qualified_name = f"{module_name}.{current_namespace}.{func_name}"
                else:
                    qualified_name = f"{module_name}.{func_name}"
                is_method = False
                class_name = None

            result['functions'][qualified_name] = FunctionInfo(
                name=func_name, qualified_name=qualified_name,
                file=file_path, line=line_no, column=0,
                module=module_name, class_name=class_name,
                is_method=is_method, is_private=func_name.startswith('_'),
                is_property=False, docstring="", args=[], decorators=[],
            )
            result['module'].functions.append(qualified_name)
            stats['functions_found'] += 1

    # Regex-based complexity estimation and call extraction
    calculate_complexity_regex(content, result, lang='c_family')
    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result
