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
