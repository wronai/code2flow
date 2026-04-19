"""Map exporter module list — render M[] list with line counts."""

from typing import List

from code2llm.core.models import AnalysisResult

from .utils import rel_path, file_line_count


def render_module_list(result: AnalysisResult, is_excluded_path) -> List[str]:
    """Render M[] — module list with line counts."""
    modules = []
    for mname, mi in sorted(result.modules.items()):
        if is_excluded_path(mi.file):
            continue
        rel = rel_path(mi.file, result.project_path)
        lc = file_line_count(mi.file)
        modules.append((rel, lc))

    lines = [f"M[{len(modules)}]:"]
    for rel, lc in modules:
        lines.append(f"  {rel},{lc}")
    return lines


__all__ = ['render_module_list']
