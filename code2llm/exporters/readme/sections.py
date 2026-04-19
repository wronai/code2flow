"""README section builders — dynamically build file documentation tables."""

from typing import Any, Dict


def build_core_files_section(existing: Dict[str, bool], insights: Dict[str, Any]) -> str:
    """Build the Core Analysis Files section dynamically."""
    lines = ["### 🎯 Core Analysis Files", ""]
    lines.append("| File | Format | Purpose | Key Insights |")
    lines.append("|------|--------|---------|--------------|")
    
    if existing.get('analysis.toon'):
        lines.append(f"| `analysis.toon` | **TOON** | **🔥 Health diagnostics** - Health, LAYERS, COUPLING | {insights['critical_functions']} critical functions, {insights['god_modules']} god modules |")
    if existing.get('evolution.toon.yaml'):
        lines.append(f"| `evolution.toon.yaml` | **YAML** | **📋 Refactoring queue** - Prioritized improvements | {insights['refactoring_actions']} refactoring actions needed |")
    if existing.get('map.toon.yaml'):
        lines.append("| `map.toon.yaml` | **YAML** | **🗺️ Structural map + project header** - Modules, imports, exports, signatures, stats, alerts, hotspots, trend | Project architecture overview |")
    
    lines.append("")
    return "\n".join(lines)


def build_llm_files_section(existing: Dict[str, bool]) -> str:
    """Build the LLM-Ready Documentation section dynamically."""
    lines = ["### 🤖 LLM-Ready Documentation", ""]
    lines.append("| File | Format | Purpose | Use Case |")
    lines.append("|------|--------|---------|----------|")
    
    if existing.get('prompt.txt'):
        lines.append("| `prompt.txt` | **Text** | **📝 Ready-to-send prompt** - Lists all files with instructions | Attach to LLM conversation as context guide |")
    if existing.get('context.md'):
        lines.append("| `context.md` | **Markdown** | **📖 LLM narrative** - Architecture summary | Paste into ChatGPT/Claude for code analysis |")
    if existing.get('analysis.yaml'):
        lines.append("| `analysis.yaml` | **YAML** | **📊 Structured data** - Machine-readable | For scripts and automated processing |")
    if existing.get('analysis.json'):
        lines.append("| `analysis.json` | **JSON** | **🔧 API format** - Programmatic access | For integration with other tools |")
    
    lines.append("")
    return "\n".join(lines)


def build_viz_files_section(existing: Dict[str, bool]) -> str:
    """Build the Visualizations section dynamically."""
    has_mermaid = existing.get('flow.mmd') or existing.get('calls.mmd') or existing.get('compact_flow.mmd')
    if not has_mermaid:
        return ""
        
    lines = ["### 📊 Visualizations", ""]
    lines.append("| File | Format | Purpose | Description |")
    lines.append("|------|--------|---------|-------------|")
    
    if existing.get('flow.mmd'):
        lines.append("| `flow.mmd` | **Mermaid** | **🔄 Control flow diagram** | Function call paths with complexity styling |")
    if existing.get('calls.mmd'):
        lines.append("| `calls.mmd` | **Mermaid** | **📞 Call graph** | Function dependencies (edges only) |")
    if existing.get('compact_flow.mmd'):
        lines.append("| `compact_flow.mmd` | **Mermaid** | **📦 Module overview** | Aggregated module-level view |")
    
    lines.append("")
    return "\n".join(lines)


__all__ = [
    'build_core_files_section',
    'build_llm_files_section',
    'build_viz_files_section',
]
