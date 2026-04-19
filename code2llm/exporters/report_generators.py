"""Report generators — produce views from project.yaml (single source of truth).

Thin re-export module. Actual generators live in separate files:
  toon_view.py      → ToonViewGenerator     → project.toon.yaml
  context_view.py   → ContextViewGenerator  → context.md
  article_view.py   → ArticleViewGenerator  → status.md
  html_dashboard.py → HTMLDashboardGenerator → dashboard.html
"""

import yaml
from typing import Any, Dict

from .toon_view import ToonViewGenerator
from .context_view import ContextViewGenerator
from .article_view import ArticleViewGenerator
from .html_dashboard import HTMLDashboardGenerator


def load_project_yaml(path: str) -> Dict[str, Any]:
    """Load and validate project.yaml with detailed error reporting."""
    import yaml
    from yaml.scanner import ScannerError
    from yaml.parser import ParserError

    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise ValueError(f"project.yaml not found: {path}")
    except Exception as e:
        raise ValueError(f"Cannot read project.yaml ({path}): {e}")

    # Check for empty file
    if not content.strip():
        raise ValueError(f"project.yaml is empty: {path}")

    # Try to parse YAML with detailed error reporting
    try:
        data = yaml.safe_load(content)
    except ScannerError as e:
        line = e.problem_mark.line + 1 if e.problem_mark else "?"
        col = e.problem_mark.column if e.problem_mark else "?"
        raise ValueError(
            f"YAML syntax error in {path} at line {line}, column {col}: {e.problem}\n"
            f"Hint: Check indentation and special characters (:, -, #)")
    except ParserError as e:
        line = e.problem_mark.line + 1 if e.problem_mark else "?"
        raise ValueError(
            f"YAML parse error in {path} at line {line}: {e.problem}\n"
            f"Hint: Verify YAML structure (mapping vs list)")
    except Exception as e:
        raise ValueError(f"YAML error in {path}: {e}")

    # Validate structure
    if data is None:
        raise ValueError(f"project.yaml is null/empty: {path}")
    if not isinstance(data, dict):
        raise ValueError(
            f"Invalid project.yaml: expected dict/object, got {type(data).__name__} in {path}\n"
            f"Hint: YAML must start with key-value pairs, not a list")
    if "version" not in data:
        raise ValueError(
            f"Invalid project.yaml: missing required 'version' key in {path}\n"
            f"Required keys: version, project, analysis\n"
            f"Found keys: {list(data.keys())[:10]}")

    return data


__all__ = [
    "load_project_yaml",
    "ToonViewGenerator",
    "ContextViewGenerator",
    "ArticleViewGenerator",
    "HTMLDashboardGenerator",
]
