"""Shared utilities for regex-based language analyzers."""

import re
from typing import Dict, List


# Branching keywords per language family
CC_PATTERNS = {
    'c_family': re.compile(
        r'\b(?:if|else\s+if|for|while|do|switch|case|catch)\b'
        r'|&&|\|\||\?\?|\?\.'  # logical operators (not word chars)
        r'|\?\s*[^:]*\s*:'  # ternary
    ),
    'go': re.compile(
        r'\b(?:if|for|switch|case|select|go|defer)\b'
        r'|&&|\|\|'
    ),
    'rust': re.compile(
        r'\b(?:if|else\s+if|for|while|loop|match)\b'
        r'|&&|\|\||\?'
    ),
}

CALL_PATTERN_C_FAMILY = re.compile(
    r'(?<!\bfunction\b\s)'            # not a function declaration
    r'(?<!\bclass\b\s)'               # not a class declaration
    r'\b([a-zA-Z_]\w*)\s*\('          # simple call: foo(
    r'|'
    r'(?:this|self)\s*\.\s*(\w+)\s*\('  # this.method( / self.method(
    r'|'
    r'\b(\w+)\s*\.\s*(\w+)\s*\('      # obj.method(
)


def extract_function_body(content: str, start_line: int) -> str:
    """Extract the body of a function between braces from a start line (1-indexed)."""
    lines = content.split('\n')
    if start_line < 1 or start_line > len(lines):
        return ''
    depth = 0
    body_lines = []
    started = False
    for line in lines[start_line - 1:]:
        for ch in line:
            if ch == '{':
                depth += 1
                started = True
            elif ch == '}':
                depth -= 1
        if started:
            body_lines.append(line)
        if started and depth <= 0:
            break
    return '\n'.join(body_lines)


def calculate_complexity_regex(content: str, result: Dict,
                               lang: str = 'c_family') -> None:
    """Estimate cyclomatic complexity for every function using regex keyword counting."""
    pattern = CC_PATTERNS.get(lang, CC_PATTERNS['c_family'])
    for func_info in result['functions'].values():
        body = extract_function_body(content, func_info.line)
        if not body:
            cc = 1
        else:
            cc = 1 + len(pattern.findall(body))
        rank = 'A' if cc <= 5 else ('B' if cc <= 10 else ('C' if cc <= 20 else 'D'))
        func_info.complexity = {
            'cyclomatic_complexity': cc,
            'cc_rank': rank,
        }


def extract_calls_regex(content: str, module_name: str, result: Dict) -> None:
    """Extract function calls from function bodies using regex."""
    # Build set of known function simple names for resolution
    known_simple: Dict[str, List[str]] = {}
    for qname in result['functions']:
        simple = qname.rsplit('.', 1)[-1]
        known_simple.setdefault(simple, []).append(qname)

    for func_qname, func_info in result['functions'].items():
        body = extract_function_body(content, func_info.line)
        if not body:
            continue
        calls_seen = set()
        for m in CALL_PATTERN_C_FAMILY.finditer(body):
            simple_call = m.group(1) or m.group(2) or m.group(4)
            if not simple_call:
                continue
            # Skip language keywords
            if simple_call in ('if', 'for', 'while', 'switch', 'catch',
                               'return', 'throw', 'new', 'typeof', 'instanceof',
                               'import', 'export', 'require', 'console',
                               'super', 'class', 'function', 'async', 'await',
                               'delete', 'void', 'case', 'default'):
                continue
            # Resolve to known qualified name
            if simple_call in known_simple:
                candidates = known_simple[simple_call]
                # Prefer same-module match
                resolved = None
                my_module = func_qname.rsplit('.', 1)[0]
                for cand in candidates:
                    if cand.rsplit('.', 1)[0] == my_module:
                        resolved = cand
                        break
                if resolved is None:
                    resolved = candidates[0]
                if resolved != func_qname and resolved not in calls_seen:
                    func_info.calls.append(resolved)
                    calls_seen.add(resolved)
            else:
                # External call — store as module.name for downstream
                ext_name = f"{module_name}.{simple_call}"
                if ext_name not in calls_seen:
                    func_info.calls.append(ext_name)
                    calls_seen.add(ext_name)


# Shared declaration extraction for language parsers
def _extract_declarations(
    content: str,
    file_path: str,
    module_name: str,
    patterns: Dict,
    stats: Dict,
    lang_config: Dict,
) -> Dict:
    """Shared extraction logic for language parsers.
    
    Args:
        content: File content
        file_path: Path to file  
        module_name: Module name
        patterns: Dict of compiled regex patterns
        stats: Statistics dict to update
        lang_config: Language-specific config dict
    """
    from ..models import ClassInfo, FunctionInfo, ModuleInfo
    from pathlib import Path
    
    result = {
        'module': ModuleInfo(
            name=module_name,
            file=file_path,
            is_package=Path(file_path).name in lang_config.get('index_files', [])
        ),
        'functions': {},
        'classes': {},
        'nodes': {},
        'edges': [],
    }
    
    lines = content.split('\n')
    current_class = None
    class_brace_depth = 0
    brace_depth = 0
    pending_decorators = []
    
    import_re = patterns.get('import')
    decorator_re = patterns.get('decorator')
    class_re = patterns.get('class')
    interface_re = patterns.get('interface')
    func_re = patterns.get('function')
    arrow_re = patterns.get('arrow_func')
    method_re = patterns.get('method')
    arrow_prop_re = patterns.get('arrow_prop')
    
    track_braces = lang_config.get('brace_track', True)
    reserved = lang_config.get('reserved', {'if', 'for', 'while', 'switch', 'return', 'catch'})
    
    for line_no, line in enumerate(lines, 1):
        raw_line = line
        line = line.strip()
        # Skip empty lines and comments, but NOT preprocessor directives like #include
        if not line:
            continue
        if line.startswith(('//', '/*', '*')):
            continue
        # Skip # comments (Python, Ruby, shell) but NOT #include/#define (C-family)
        if line.startswith('#') and not line.startswith('#include') and not line.startswith('#define'):
            continue
        
        if track_braces:
            for ch in raw_line:
                if ch == '{':
                    brace_depth += 1
                elif ch == '}':
                    brace_depth -= 1
            if current_class and brace_depth < class_brace_depth:
                current_class = None
                class_brace_depth = 0
        
        if decorator_re:
            dm = decorator_re.match(line)
            if dm:
                pending_decorators.append(dm.group(1))
                continue
        
        if import_re:
            im = import_re.match(line)
            if im:
                result['module'].imports.append(im.group(1))
                continue
        
        if class_re:
            cm = class_re.match(line)
            if cm:
                cname = cm.group(1)
                bases = []
                if len(cm.groups()) > 1 and cm.group(2):
                    bases.append(cm.group(2).strip())
                if len(cm.groups()) > 2 and cm.group(3):
                    bases.extend([b.strip() for b in cm.group(3).split(',')])
                qual = f"{module_name}.{cname}"
                result['classes'][qual] = ClassInfo(
                    name=cname, qualified_name=qual, file=file_path,
                    line=line_no, module=module_name, bases=bases,
                    methods=[], docstring="",
                )
                result['module'].classes.append(qual)
                stats['classes_found'] += 1
                current_class = qual
                class_brace_depth = brace_depth
                pending_decorators.clear()
                continue
        
        if interface_re:
            imt = interface_re.match(line)
            if imt:
                cname = imt.group(1)
                qual = f"{module_name}.{cname}"
                result['classes'][qual] = ClassInfo(
                    name=cname, qualified_name=qual, file=file_path,
                    line=line_no, module=module_name, bases=[],
                    methods=[], docstring="",
                )
                result['module'].classes.append(qual)
                stats['classes_found'] += 1
                pending_decorators.clear()
                continue
        
        if not current_class and (func_re or arrow_re):
            fname = None
            if func_re:
                fm = func_re.match(line)
                if fm:
                    fname = fm.group(1) or (fm.group(2) if len(fm.groups()) > 1 else None)
            if not fname and arrow_re:
                am = arrow_re.match(line)
                if am:
                    fname = am.group(1)
            if fname and fname not in reserved:
                qual = f"{module_name}.{fname}"
                result['functions'][qual] = FunctionInfo(
                    name=fname, qualified_name=qual, file=file_path,
                    line=line_no, column=0, module=module_name,
                    class_name=None, is_method=False,
                    is_private=fname.startswith('_'),
                    is_property=False, docstring="", args=[],
                    decorators=pending_decorators[:],
                )
                result['module'].functions.append(qual)
                stats['functions_found'] += 1
                pending_decorators.clear()
                continue
        
        if current_class and (method_re or arrow_prop_re or func_re):
            matched = False
            mname = None
            if arrow_prop_re:
                apm = arrow_prop_re.match(line)
                if apm:
                    mname = apm.group(1)
                    if mname not in reserved and mname != 'constructor':
                        matched = True
            if not matched and method_re:
                mm = method_re.match(line)
                if mm:
                    mname = mm.group(1)
                    if mname not in reserved:
                        matched = True
            if not matched and func_re:
                fm = func_re.match(line)
                if fm:
                    fn = fm.group(1) or (fm.group(2) if len(fm.groups()) > 1 else None)
                    if fn and fn not in reserved:
                        mname = fn
                        matched = True
            if matched and mname:
                qual = f"{current_class}.{mname}"
                result['classes'][current_class].methods.append(qual)
                result['functions'][qual] = FunctionInfo(
                    name=mname, qualified_name=qual, file=file_path,
                    line=line_no, column=0, module=module_name,
                    class_name=current_class.split('.')[-1],
                    is_method=True, is_private=mname.startswith(('_', '#')),
                    is_property=False, docstring="", args=[],
                    decorators=pending_decorators[:],
                )
                result['module'].functions.append(qual)
                stats['functions_found'] += 1
                pending_decorators.clear()
                continue
        
        if pending_decorators:
            all_patterns = [p for p in [func_re, arrow_re, class_re, interface_re, method_re] if p]
            if not any(p and p.match(line) for p in all_patterns):
                pending_decorators.clear()
    
    return result
