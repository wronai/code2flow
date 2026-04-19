"""Evolution exporter render — text output generation for evolution.toon."""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .constants import CC_SPLIT_THRESHOLD


def render_header(ctx: Dict[str, Any]) -> List[str]:
    """Render header line."""
    return [
        f"# code2llm/evolution | {ctx['total_funcs']} func"
        f" | {ctx['total_files']}f | {datetime.now().strftime('%Y-%m-%d')}",
    ]


def render_next(ctx: Dict[str, Any]) -> List[str]:
    """Render NEXT — ranked refactoring queue."""
    actions: List[Dict[str, Any]] = []

    # 1. God modules → split
    for gm in ctx["god_modules"][:3]:
        actions.append({
            "priority": "!!",
            "action": "SPLIT",
            "target": gm["file"],
            "why": f"{gm['lines']}L, {gm['classes']} classes, max CC={gm['max_cc']}",
            "effort": "~4h",
            "impact_score": gm["lines"] * gm["max_cc"],
        })

    # 2. High CC functions → split
    for f in ctx["funcs"][:20]:
        if f["cc"] >= CC_SPLIT_THRESHOLD:
            display = f["name"]
            if f["class_name"]:
                display = f"{f['class_name']}.{f['name']}"
            actions.append({
                "priority": "!!" if f["cc"] >= 25 else "!",
                "action": "SPLIT-FUNC",
                "target": f"{display}  CC={f['cc']}  fan={f['fan_out']}",
                "why": f"CC={f['cc']} exceeds {CC_SPLIT_THRESHOLD}",
                "effort": "~1h",
                "impact_score": f["impact"],
            })

    # 3. Hub types → interface segregation
    for ht in ctx["hub_types"][:3]:
        if ht["consumers"] >= 20:
            actions.append({
                "priority": "!",
                "action": "INTERFACE-SPLIT",
                "target": f"{ht['type']}  consumed:{ht['consumers']}",
                "why": f"Hub type with {ht['consumers']} consumers → split interface",
                "effort": "~6h",
                "impact_score": ht["consumers"] * 10,
            })

    # Sort by impact and limit
    actions.sort(key=lambda x: x["impact_score"], reverse=True)
    actions = actions[:10]

    if not actions:
        return ["NEXT[0]: no refactoring needed"]

    lines = [f"NEXT[{len(actions)}] (ranked by impact):"]
    for i, a in enumerate(actions, 1):
        lines.append(
            f"  [{i}] {a['priority']:2s} {a['action']:15s} {a['target']}"
        )
        lines.append(
            f"      WHY: {a['why']}"
        )
        lines.append(
            f"      EFFORT: {a['effort']}  IMPACT: {a['impact_score']}"
        )
        lines.append("")

    return lines


def render_risks(ctx: Dict[str, Any]) -> List[str]:
    """Render RISKS — potential breaking changes."""
    risks: List[str] = []

    # God module splits may break imports
    for gm in ctx["god_modules"][:3]:
        risks.append(
            f"⚠ Splitting {gm['file']} may break {gm['funcs']} import paths"
        )

    # Hub type splits change public API
    for ht in ctx["hub_types"][:2]:
        if ht["consumers"] >= 20:
            risks.append(
                f"⚠ Splitting {ht['type']} changes API for {ht['consumers']} consumers"
            )

    if not risks:
        return ["RISKS[0]: none"]

    lines = [f"RISKS[{len(risks)}]:"]
    for r in risks:
        lines.append(f"  {r}")
    return lines


def render_metrics_target(ctx: Dict[str, Any]) -> List[str]:
    """Render METRICS-TARGET — baseline vs goals."""
    avg = ctx["avg_cc"]
    max_cc = ctx["max_cc"]
    gods = len(ctx["god_modules"])
    hubs = len(ctx["hub_types"])
    high = ctx["high_cc_count"]

    # Compute targets (halve the worst metrics)
    target_avg = round(min(avg * 0.7, 5.0), 1)
    target_max = min(max_cc // 2, 20)
    target_gods = 0
    target_high = max(high // 2, 0)

    lines = [
        "METRICS-TARGET:",
        f"  CC̄:          {avg} → ≤{target_avg}",
        f"  max-CC:      {max_cc} → ≤{target_max}",
        f"  god-modules: {gods} → {target_gods}",
        f"  high-CC(≥{CC_SPLIT_THRESHOLD}): {high} → ≤{target_high}",
        f"  hub-types:   {hubs} → ≤{max(hubs - 2, 0)}",
    ]
    return lines


def render_patterns(ctx: Dict[str, Any]) -> List[str]:
    """Render PATTERNS — shared language parser extraction patterns."""
    lines = [
        "PATTERNS (language parser shared logic):",
        "  _extract_declarations() in base.py — unified extraction for:",
        "    - TypeScript: interfaces, types, classes, functions, arrow funcs",
        "    - PHP: namespaces, traits, classes, functions, includes",
        "    - Ruby: modules, classes, methods, requires",
        "    - C++: classes, structs, functions, #includes",
        "    - C#: classes, interfaces, methods, usings",
        "    - Java: classes, interfaces, methods, imports",
        "    - Go: packages, functions, structs",
        "    - Rust: modules, functions, traits, use statements",
        "",
        "  Shared regex patterns per language:",
        "    - import: language-specific import/require/using patterns",
        "    - class: class/struct/trait declarations with inheritance",
        "    - function: function/method signatures with visibility",
        "    - brace_tracking: for C-family languages ({ })",
        "    - end_keyword_tracking: for Ruby (module/class/def...end)",
        "",
        "  Benefits:",
        "    - Consistent extraction logic across all languages",
        "    - Reduced code duplication (~70% reduction in parser LOC)",
        "    - Easier maintenance: fix once, apply everywhere",
        "    - Standardized FunctionInfo/ClassInfo models",
    ]
    return lines


def render_history(ctx: Dict[str, Any], output_path: str) -> List[str]:
    """Render HISTORY — load previous evolution.toon.yaml if exists."""
    lines = ["HISTORY:"]

    prev_path = Path(output_path)
    if prev_path.exists():
        try:
            prev_content = prev_path.read_text(encoding="utf-8")
            # Extract previous metrics line
            for line in prev_content.splitlines():
                if line.strip().startswith("CC̄:"):
                    prev_avg = line.split("→")[0].strip().split()[-1]
                    lines.append(f"  prev CC̄={prev_avg} → now CC̄={ctx['avg_cc']}")
                    break
            else:
                lines.append(f"  previous evolution.toon.yaml found but no metrics parsed")
        except Exception:
            lines.append(f"  (could not read previous evolution.toon.yaml)")
    else:
        lines.append(f"  (first run — no previous data)")

    return lines


__all__ = [
    'render_header',
    'render_next',
    'render_risks',
    'render_metrics_target',
    'render_patterns',
    'render_history',
]
