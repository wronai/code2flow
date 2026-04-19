"""Mermaid file validation — check for syntax errors and structural issues."""

from pathlib import Path
from typing import List


def validate_mermaid_file(mmd_path: Path) -> List[str]:
    """Validate Mermaid file and return list of errors."""
    if not mmd_path.exists():
        return [f"File not found: {mmd_path}"]

    try:
        content = mmd_path.read_text(encoding='utf-8')
        lines = content.strip().split('\n')
        errors = []

        # Check for proper graph declaration
        if not lines or not any(line.strip().startswith(('graph', 'flowchart')) for line in lines):
            errors.append("Missing graph declaration (should start with 'graph' or 'flowchart')")

        _check_bracket_balance(lines, errors)
        _check_node_ids(lines, errors)

        return errors

    except Exception as e:
        return [f"Error reading file: {e}"]


def _strip_label_segments(s: str) -> str:
    """Remove label segments that frequently contain Mermaid syntax chars."""
    import re
    s = re.sub(r"\|[^|]*\|", "||", s)
    s = re.sub(r"\[\"[^\"]*\"\]", "[]", s)
    s = re.sub(r"\(\"[^\"]*\"\)", "()", s)
    s = re.sub(r"\{\"[^\"]*\"\}", "{}", s)
    s = re.sub(r"\[/[^\]]*?/\]", "[]", s)
    s = re.sub(r"\(/[^)]*?/\)", "()", s)
    return s


def _is_balanced_node_line(line: str) -> bool:
    """Check if a line has balanced brackets — likely a node definition."""
    return (('[' in line and ']' in line) or
            ('(' in line and ')' in line) or
            ('{' in line and '}' in line))


def _check_bracket_balance(lines: List[str], errors: List[str]) -> None:
    """Check for unmatched brackets/parentheses outside label segments."""
    bracket_stack = []
    paren_stack = []

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
        if _is_balanced_node_line(line):
            continue
        check_line = _strip_label_segments(line)
        _scan_brackets(check_line, line_num, bracket_stack, paren_stack, errors)

    for expected, line_num in bracket_stack:
        errors.append(f"Line {line_num}: Unclosed '[' (missing '{expected}')")
    for expected, line_num in paren_stack:
        errors.append(f"Line {line_num}: Unclosed '(' (missing '{expected}')")


def _scan_brackets(text: str, line_num: int, bracket_stack: list,
                   paren_stack: list, errors: List[str]) -> None:
    """Process bracket/paren chars in a single line."""
    for char in text:
        if char == '[':
            bracket_stack.append((']', line_num))
        elif char == ']':
            if not bracket_stack or bracket_stack[-1][0] != ']':
                errors.append(f"Line {line_num}: Unmatched ']'")
            else:
                bracket_stack.pop()
        elif char == '(':
            paren_stack.append((')', line_num))
        elif char == ')':
            if not paren_stack or paren_stack[-1][0] != ')':
                errors.append(f"Line {line_num}: Unmatched ')'")
            else:
                paren_stack.pop()


def _check_node_ids(lines: List[str], errors: List[str]) -> None:
    """Check for invalid node IDs."""
    import re
    node_pattern = re.compile(r'^\s*([A-Z]\d+|[Ff]\d+_\w+)\s*["\'\[\{]')

    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('%%'):
            continue
        if line.startswith('subgraph ') or line == 'end':
            continue
        if _is_balanced_node_line(line):
            continue

        if any(char in line for char in ['[', '(', '{']):
            if not node_pattern.match(line):
                match = re.match(r'^\s*([A-Za-z0-9_]+)', line)
                if match:
                    node_id = match.group(1)
                    if not re.match(r'^[A-Z]\d+$|^[Ff]\d+_\w+$', node_id):
                        errors.append(f"Line {line_num}: Invalid node ID '{node_id}' (should be like 'N1' or 'F123_name')")


__all__ = [
    'validate_mermaid_file',
    '_strip_label_segments',
    '_is_balanced_node_line',
    '_check_bracket_balance',
    '_scan_brackets',
    '_check_node_ids',
]
