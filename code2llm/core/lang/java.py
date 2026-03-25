"""Java analyzer (regex-based)."""

import re
from typing import Dict

from ..models import ClassInfo, FunctionInfo, ModuleInfo
from .base import calculate_complexity_regex, extract_calls_regex


def analyze_java(content: str, file_path: str, module_name: str,
                 stats: Dict) -> Dict:
    """Analyze Java files using regex-based parsing."""
    result = {
        'module': ModuleInfo(name=module_name, file=file_path, is_package=False),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }

    lines = content.split('\n')

    import_pattern = re.compile(r'^\s*import\s+([\w.]+)')
    class_pattern = re.compile(r'^\s*(?:public\s+|private\s+|protected\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?')
    interface_pattern = re.compile(r'^\s*(?:public\s+)?interface\s+(\w+)')
    method_pattern = re.compile(r'^\s*(?:public\s+|private\s+|protected\s+)?(?:static\s+)?(?:final\s+)?(?:abstract\s+)?[\w<>,\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{?')

    current_class = None

    for line_no, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('/*') or line.startswith('*'):
            continue

        # Imports
        import_match = import_pattern.match(line)
        if import_match:
            result['module'].imports.append(import_match.group(1))

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

            result['classes'][qualified_name] = ClassInfo(
                name=class_name, qualified_name=qualified_name,
                file=file_path, line=line_no, module=module_name,
                bases=bases, methods=[], docstring="",
            )
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1
            current_class = qualified_name

        # Interfaces
        interface_match = interface_pattern.match(line)
        if interface_match:
            class_name = interface_match.group(1)
            qualified_name = f"{module_name}.{class_name}"
            result['classes'][qualified_name] = ClassInfo(
                name=class_name, qualified_name=qualified_name,
                file=file_path, line=line_no, module=module_name,
                bases=[], methods=[], docstring="",
            )
            result['module'].classes.append(qualified_name)
            stats['classes_found'] += 1

        # Methods
        method_match = method_pattern.match(line)
        if method_match:
            method_name = method_match.group(1)
            if current_class and not method_name[0].isupper():  # Skip constructors
                qualified_name = f"{current_class}.{method_name}"
                result['functions'][qualified_name] = FunctionInfo(
                    name=method_name, qualified_name=qualified_name,
                    file=file_path, line=line_no, column=0,
                    module=module_name, class_name=current_class.split('.')[-1],
                    is_method=True, is_private=False,
                    is_property=False, docstring="", args=[], decorators=[],
                )
                result['module'].functions.append(qualified_name)
                result['classes'][current_class].methods.append(qualified_name)
                stats['functions_found'] += 1

    # Regex-based complexity estimation and call extraction
    calculate_complexity_regex(content, result, lang='c_family')
    extract_calls_regex(content, module_name, result)

    stats['files_processed'] += 1
    return result
