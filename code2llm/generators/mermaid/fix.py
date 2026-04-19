"""Mermaid file fixer — auto-repair common syntax errors."""

from pathlib import Path
from typing import List, Optional


def _sanitize_label_text(txt: str) -> str:
    """Replace Mermaid syntax chars in labels with HTML entities."""
    return (
        txt.replace('&', '&amp;')
        .replace('"', '&quot;')
        .replace('[', '&#91;')
        .replace(']', '&#93;')
        .replace('(', '&#40;')
        .replace(')', '&#41;')
        .replace('{', '&#123;')
        .replace('}', '&#125;')
        .replace('|', '&#124;')
    )


def _sanitize_node_id(node_id: str) -> str:
    """Make a Mermaid-safe node identifier."""
    import re
    node_id = (node_id or '').strip()
    node_id = re.split(r"[\[\]\(\)\{\}\"\|\s]", node_id, maxsplit=1)[0]
    node_id = re.sub(r"[^A-Za-z0-9_]", "_", node_id)
    return node_id or "N"


def fix_mermaid_file(mmd_path: Path) -> bool:
    """Attempt to fix common Mermaid syntax errors."""
    try:
        content = mmd_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        fixed_lines = []

        for line in lines:
            line = _fix_edge_line(line)
            line = _fix_subgraph_line(line)
            result = _fix_class_line(line)
            if result is not None:
                fixed_lines.extend(result)
            else:
                fixed_lines.append(line)

        fixed_content = '\n'.join(fixed_lines)
        if fixed_content != content:
            mmd_path.write_text(fixed_content, encoding='utf-8')
            return True

    except Exception as e:
        print(f"Error fixing {mmd_path}: {e}")

    return False


def _fix_edge_line(line: str) -> str:
    """Fix edge labels and endpoint issues."""
    import re

    if '-->' not in line:
        return line

    # Fix edge labels with pipe issues
    line = _fix_edge_label_pipes(line)

    # Fix stray trailing '|' after node IDs
    line = re.sub(r"(\b[A-Za-z]\w*)\|\s*$", r"\1", line)

    # Sanitize edge label content inside |...|
    def _sanitize_edge_label(m):
        return f"|{_sanitize_label_text(m.group(1))}|"

    if '|' in line:
        line = re.sub(r"\|([^|]{1,200})\|", _sanitize_edge_label, line)

    # Sanitize edge endpoints (lines without labels)
    if '|' not in line:
        m = re.match(r"^(\s*)([^\s-]+)\s*-->\s*([^\s]+)\s*$", line)
        if m:
            indent, src, dst = m.groups()
            line = f"{indent}{_sanitize_node_id(src)} --> {_sanitize_node_id(dst)}"

    return line


def _fix_edge_label_pipes(line: str) -> str:
    """Fix edge labels with pipe/parenthesis issues."""
    if '|' not in line or '-->|' not in line:
        return line
    parts = line.split('-->|', 1)
    if len(parts) != 2:
        return line
    label_and_target = parts[1]
    if '|' not in label_and_target:
        return line
    parts2 = label_and_target.split('|', 1)
    if len(parts2) != 2:
        return line
    label_content, target = parts2
    label_content = label_content.strip('|')
    if label_content.endswith('('):
        label_content = label_content[:-1]
    elif label_content.count('(') > label_content.count(')'):
        missing = label_content.count('(') - label_content.count(')')
        label_content += ')' * missing
    return f"{parts[0]}-->|{label_content}|{target}"


def _fix_subgraph_line(line: str) -> str:
    """Fix malformed subgraph IDs."""
    if line.strip().startswith('subgraph '):
        subgraph_part = line.strip()[9:].split('(', 1)
        if len(subgraph_part) == 2:
            subgraph_id, rest = subgraph_part
            subgraph_id = subgraph_id.replace('.', '_').replace('-', '_').replace(':', '_')
            line = f"    subgraph {subgraph_id}({rest}"
    return line


def _fix_class_line(line: str) -> Optional[List[str]]:
    """Fix class definitions with too many nodes. Returns list of lines or None."""
    if line.strip().startswith('class ') and ',' in line:
        class_parts = line.split(' ', 1)
        if len(class_parts) == 2:
            nodes_and_class = class_parts[1]
            nodes, class_name = nodes_and_class.rsplit(' ', 1)
            node_list = nodes.split(',')
            if len(node_list) > 10:
                result = []
                for i in range(0, len(node_list), 10):
                    chunk = ','.join(node_list[i:i+10])
                    result.append(f"    class {chunk} {class_name}")
                return result
    return None


__all__ = [
    'fix_mermaid_file',
    '_sanitize_label_text',
    '_sanitize_node_id',
    '_fix_edge_line',
    '_fix_edge_label_pipes',
    '_fix_subgraph_line',
    '_fix_class_line',
]
