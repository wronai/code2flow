"""Context View Generator — deduplicated LLM narrative (~150 lines).

Generates context.md from project.yaml data.
"""

from pathlib import Path
from typing import Any, Dict, List


class ContextViewGenerator:
    """Generate context.md from project.yaml data."""

    def generate(self, data: Dict[str, Any], output_path: str) -> None:
        lines = self._render(data)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    def _render(self, data: Dict[str, Any]) -> List[str]:
        proj = data.get("project", {})
        health = data.get("health", {})
        modules = data.get("modules", [])
        hotspots = data.get("hotspots", [])
        refactoring = data.get("refactoring", {})

        lines: List[str] = []
        lines.extend(self._render_overview(proj, health))
        lines.extend(self._render_architecture(modules))
        lines.extend(self._render_exports(modules))
        lines.extend(self._render_hotspots(hotspots))
        lines.extend(self._render_refactoring(refactoring))
        lines.extend(self._render_guidelines())
        return lines

    @staticmethod
    def _render_overview(proj: Dict, health: Dict) -> List[str]:
        stats = proj.get("stats", {})
        return [
            "# System Architecture Analysis",
            "",
            "## Overview",
            "",
            f"- **Project**: {proj.get('name', '?')}",
            f"- **Language**: {proj.get('language', '?')}",
            f"- **Files**: {stats.get('files', 0)}",
            f"- **Lines**: {stats.get('lines', 0)}",
            f"- **Functions**: {stats.get('functions', 0)}",
            f"- **Classes**: {stats.get('classes', 0)}",
            f"- **Avg CC**: {health.get('cc_avg', 0)}",
            f"- **Critical (CC≥{health.get('critical_limit', 10)})**: {health.get('critical_count', 0)}",
            "",
        ]

    @staticmethod
    def _render_architecture(modules: List[Dict]) -> List[str]:
        lines = ["## Architecture", ""]
        dir_groups: Dict[str, List[Dict]] = {}
        for m in modules:
            path = m.get("path", "")
            parts = Path(path).parts
            dir_key = str(Path(*parts[:-1])) if len(parts) > 1 else "root"
            if dir_key not in dir_groups:
                dir_groups[dir_key] = []
            dir_groups[dir_key].append(m)

        for dir_name in sorted(dir_groups.keys()):
            group = dir_groups[dir_name]
            total_lines = sum(m.get("lines", 0) for m in group)
            total_funcs = sum(m.get("methods", 0) for m in group)
            lines.append(f"### {dir_name}/ ({len(group)} files, {total_lines}L, {total_funcs} functions)")
            lines.append("")
            for m in sorted(group, key=lambda x: x.get("cc_max", 0), reverse=True)[:5]:
                fname = Path(m.get("path", "")).name
                lines.append(
                    f"- `{fname}` — {m.get('lines', 0)}L, "
                    f"{m.get('methods', 0)} methods, "
                    f"CC↑{m.get('cc_max', 0)}"
                )
            if len(group) > 5:
                lines.append(f"- _{len(group) - 5} more files_")
            lines.append("")
        return lines

    @staticmethod
    def _render_exports(modules: List[Dict]) -> List[str]:
        lines = ["## Key Exports", ""]
        for m in modules:
            for exp in m.get("exports", []):
                if exp.get("type") == "class":
                    methods = exp.get("methods", [])
                    flagged = [me for me in methods if me.get("flag")]
                    if flagged or exp.get("cc_avg", 0) >= 5:
                        lines.append(f"- **{exp['name']}** (class, CC̄={exp.get('cc_avg', 0)})")
                        for me in flagged:
                            lines.append(f"  - `{me['name']}` CC={me.get('cc', 0)} ⚠ {me.get('flag', '')}")
                elif exp.get("type") == "function" and exp.get("flag"):
                    lines.append(f"- **{exp['name']}** (function, CC={exp.get('cc', 0)}) ⚠ {exp.get('flag', '')}")
        lines.append("")
        return lines

    @staticmethod
    def _render_hotspots(hotspots: List[Dict]) -> List[str]:
        if not hotspots:
            return []
        lines = ["## Hotspots (High Fan-Out)", ""]
        for h in hotspots[:7]:
            lines.append(f"- **{h['name']}** — fan-out={h['fan_out']}: {h.get('note', '')}")
        lines.append("")
        return lines

    @staticmethod
    def _render_refactoring(refactoring: Dict) -> List[str]:
        priorities = refactoring.get("priorities", [])
        if not priorities:
            return []
        lines = [
            "## Refactoring Priorities",
            "",
            "| # | Action | Impact | Effort |",
            "|---|--------|--------|--------|",
        ]
        for i, p in enumerate(priorities[:10], 1):
            lines.append(
                f"| {i} | {p.get('action', '?')} | {p.get('impact', '?')} | {p.get('effort', '?')} |"
            )
        lines.append("")
        return lines

    @staticmethod
    def _render_guidelines() -> List[str]:
        return [
            "## Context for LLM",
            "",
            "When suggesting changes:",
            "1. Start from hotspots and high-CC functions",
            "2. Follow refactoring priorities above",
            "3. Maintain public API surface — keep backward compatibility",
            "4. Prefer minimal, incremental changes",
            "",
        ]
