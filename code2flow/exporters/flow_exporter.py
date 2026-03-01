"""Flow Exporter — generates flow.toon (data-flow format).

Produces a data-flow-focused format with PIPELINES, TRANSFORMS, CONTRACTS,
DATA_TYPES, and SIDE_EFFECTS sections.

Purpose: "how data flows through the system"
Format: pipeline stages, transform fan-out, contracts, hub-type detection
"""

import ast
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .base import Exporter
from ..core.models import (
    AnalysisResult, FunctionInfo, ClassInfo, ModuleInfo, FlowNode
)

# Thresholds
CC_HIGH = 15
FAN_OUT_THRESHOLD = 10
HUB_TYPE_THRESHOLD = 10

# Patterns to exclude
EXCLUDE_PATTERNS = {
    'venv', '.venv', 'env', '.env', 'publish-env', 'test-env',
    'site-packages', 'node_modules', '__pycache__', '.git',
    'dist', 'build', 'egg-info', '.tox', '.mypy_cache',
}


class FlowExporter(Exporter):
    """Export to flow.toon — data-flow focused format.

    Sections: PIPELINES, TRANSFORMS, CONTRACTS, DATA_TYPES, SIDE_EFFECTS
    """

    def export(self, result: AnalysisResult, output_path: str, **kwargs) -> None:
        """Export analysis result to flow.toon format."""
        ctx = self._build_context(result)

        sections: List[str] = []
        sections.extend(self._render_header(ctx))
        sections.append("")
        sections.extend(self._render_pipelines(ctx))
        sections.append("")
        sections.extend(self._render_transforms(ctx))
        sections.append("")
        sections.extend(self._render_contracts(ctx))
        sections.append("")
        sections.extend(self._render_data_types(ctx))
        sections.append("")
        sections.extend(self._render_side_effects(ctx))

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(sections) + "\n")

    # ------------------------------------------------------------------
    # context builder
    # ------------------------------------------------------------------
    def _build_context(self, result: AnalysisResult) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {}
        ctx["result"] = result
        ctx["timestamp"] = datetime.now().strftime("%Y-%m-%d")

        # Build function lookup excluding venv etc.
        funcs = {
            qname: fi for qname, fi in result.functions.items()
            if not self._is_excluded(fi.file)
        }
        ctx["funcs"] = funcs

        # Detect pipelines from call chains
        ctx["pipelines"] = self._detect_pipelines(funcs, result)

        # Compute transforms (high fan-out functions)
        ctx["transforms"] = self._compute_transforms(funcs)

        # Compute type usage across functions
        ctx["type_usage"] = self._compute_type_usage(funcs)

        # Classify side effects
        ctx["side_effects"] = self._classify_side_effects(funcs, result)

        # Compute contracts per pipeline
        ctx["contracts"] = self._compute_contracts(ctx["pipelines"], funcs)

        return ctx

    # ------------------------------------------------------------------
    # pipeline detection
    # ------------------------------------------------------------------
    def _detect_pipelines(
        self, funcs: Dict[str, FunctionInfo], result: AnalysisResult
    ) -> List[Dict[str, Any]]:
        """Detect pipelines by finding linear call chains grouped by package."""
        # Build adjacency: caller -> [callees within project]
        adj: Dict[str, List[str]] = defaultdict(list)
        all_callees: Set[str] = set()
        for qname, fi in funcs.items():
            for callee in fi.calls:
                # resolve to qualified name
                resolved = self._resolve_callee(callee, funcs)
                if resolved:
                    adj[qname].append(resolved)
                    all_callees.add(resolved)

        # Find entry points: functions that are not called by others in the set
        entry_candidates = set(funcs.keys()) - all_callees

        # Trace longest chains from entry points
        chains: List[List[str]] = []
        for entry in entry_candidates:
            chain = self._trace_chain(entry, adj, set(), max_depth=8)
            if len(chain) >= 3:
                chains.append(chain)

        # Sort by length desc, deduplicate overlapping chains
        chains.sort(key=len, reverse=True)
        used: Set[str] = set()
        pipelines: List[Dict[str, Any]] = []

        for chain in chains:
            # Skip if >50% of chain already used
            overlap = sum(1 for f in chain if f in used)
            if overlap > len(chain) * 0.5:
                continue

            # Determine pipeline name from package
            pkg = self._pipeline_name(chain, funcs)
            stages = []
            for qname in chain:
                fi = funcs.get(qname)
                if fi:
                    cc = fi.complexity.get("cyclomatic_complexity", 0)
                    purity = self._function_purity(fi, result)
                    sig = self._compact_signature(fi)
                    stages.append({
                        "name": fi.name,
                        "qualified": qname,
                        "signature": sig,
                        "cc": cc,
                        "purity": purity,
                    })

            if stages:
                pure_count = sum(1 for s in stages if s["purity"] == "pure")
                bottleneck = max(stages, key=lambda s: s["cc"]) if stages else None
                pipelines.append({
                    "name": pkg,
                    "stages": stages,
                    "entry_type": self._infer_input_type(stages[0], funcs),
                    "pure_count": pure_count,
                    "total_stages": len(stages),
                    "bottleneck": bottleneck,
                })
                used.update(chain)

            if len(pipelines) >= 8:
                break

        return pipelines

    def _trace_chain(
        self, start: str, adj: Dict[str, List[str]],
        visited: Set[str], max_depth: int
    ) -> List[str]:
        """Trace longest linear chain from start."""
        if max_depth <= 0 or start in visited:
            return [start]

        visited = visited | {start}
        best_chain = [start]

        for callee in adj.get(start, []):
            if callee not in visited:
                sub = self._trace_chain(callee, adj, visited, max_depth - 1)
                candidate = [start] + sub
                if len(candidate) > len(best_chain):
                    best_chain = candidate

        return best_chain

    def _pipeline_name(
        self, chain: List[str], funcs: Dict[str, FunctionInfo]
    ) -> str:
        """Derive pipeline name from dominant package in chain."""
        pkg_counts: Dict[str, int] = defaultdict(int)
        for qname in chain:
            fi = funcs.get(qname)
            if fi:
                pkg = fi.module.split(".")[0] if "." in fi.module else fi.module
                # Try second level for more specificity
                parts = fi.module.split(".")
                if len(parts) >= 2:
                    pkg = parts[1]  # e.g. "nlp", "core", "exporters"
                pkg_counts[pkg] += 1

        if pkg_counts:
            dominant = max(pkg_counts, key=pkg_counts.get)
            return dominant.capitalize()
        return "Unknown"

    # ------------------------------------------------------------------
    # transforms — high fan-out functions
    # ------------------------------------------------------------------
    def _compute_transforms(
        self, funcs: Dict[str, FunctionInfo]
    ) -> List[Dict[str, Any]]:
        """Find functions with fan-out >= threshold."""
        transforms = []
        for qname, fi in funcs.items():
            fan_out = len(set(fi.calls))
            if fan_out >= FAN_OUT_THRESHOLD:
                transforms.append({
                    "name": fi.name,
                    "qualified": qname,
                    "fan_out": fan_out,
                    "signature": self._compact_signature(fi),
                    "label": self._transform_label(fi, fan_out),
                })
        transforms.sort(key=lambda x: x["fan_out"], reverse=True)
        return transforms[:15]

    def _transform_label(self, fi: FunctionInfo, fan_out: int) -> str:
        if fi.name == "main" or fi.name == "__main__":
            return "!! script-in-disguise"
        if fan_out >= 30:
            return "!! mutation-heavy"
        if fan_out >= 20:
            return "!! side-effects"
        if fi.class_name:
            return f"PIPELINE:{fi.class_name}.entry"
        return f"fan={fan_out}"

    # ------------------------------------------------------------------
    # type usage — consumed/produced counts
    # ------------------------------------------------------------------
    def _compute_type_usage(
        self, funcs: Dict[str, FunctionInfo]
    ) -> List[Dict[str, Any]]:
        """Count how many functions consume/produce each type."""
        consumed: Dict[str, int] = defaultdict(int)
        produced: Dict[str, int] = defaultdict(int)

        for qname, fi in funcs.items():
            # Types from args (consumed)
            for arg in fi.args:
                if ":" in arg:
                    type_name = arg.split(":")[-1].strip()
                    type_name = self._normalize_type(type_name)
                    if type_name:
                        consumed[type_name] += 1

            # Types from return (produced)
            if fi.returns:
                ret_type = self._normalize_type(fi.returns)
                if ret_type:
                    produced[ret_type] += 1

            # Infer from function name patterns
            inferred = self._infer_types_from_name(fi.name)
            for t in inferred.get("consumed", []):
                consumed[t] += 1
            for t in inferred.get("produced", []):
                produced[t] += 1

        # Merge into ranked list
        all_types = set(consumed.keys()) | set(produced.keys())
        type_list = []
        for t in all_types:
            c = consumed.get(t, 0)
            p = produced.get(t, 0)
            total = c + p
            label = self._type_label(t, c, p)
            type_list.append({
                "type": t,
                "consumed": c,
                "produced": p,
                "total": total,
                "label": label,
            })

        type_list.sort(key=lambda x: x["total"], reverse=True)
        return type_list[:20]

    def _normalize_type(self, t: str) -> str:
        t = t.strip().strip("'\"")
        # Remove Optional[], List[], Dict[] wrappers for base type
        for wrapper in ["Optional[", "List[", "Dict[", "Set[", "Tuple["]:
            if t.startswith(wrapper) and t.endswith("]"):
                t = t[len(wrapper):-1]
        return t if t and t not in ("None", "Any") else ""

    def _type_label(self, t: str, consumed: int, produced: int) -> str:
        if consumed >= HUB_TYPE_THRESHOLD:
            return "!! HUB-TYPE \u2192 split interface"
        if consumed >= 5 and produced <= 1:
            return "input-heavy (read-only flow)"
        if produced >= 5 and consumed <= 1:
            return "output-heavy"
        if consumed >= 10 and produced >= 10:
            return "ubiquitous"
        if consumed + produced <= 4:
            return "narrow scope"
        return ""

    def _infer_types_from_name(self, name: str) -> Dict[str, List[str]]:
        """Infer likely types from function name patterns."""
        result: Dict[str, List[str]] = {"consumed": [], "produced": []}
        name_lower = name.lower()

        if "analyze" in name_lower and "file" in name_lower:
            result["consumed"].append("Path")
            result["produced"].append("AnalysisResult")
        elif "analyze" in name_lower and "project" in name_lower:
            result["consumed"].append("Path")
            result["produced"].append("AnalysisResult")
        elif "export" in name_lower:
            result["consumed"].append("AnalysisResult")
        elif "detect" in name_lower and "smell" in name_lower:
            result["consumed"].append("AnalysisResult")
            result["produced"].append("CodeSmell")
        elif "normalize" in name_lower:
            result["consumed"].append("str")
            result["produced"].append("str")
        elif "match" in name_lower and "intent" in name_lower:
            result["consumed"].append("str")
            result["produced"].append("IntentMatch")
        elif "resolve" in name_lower:
            result["consumed"].append("IntentMatch")
            result["produced"].append("Entity")
        elif "parse" in name_lower:
            result["consumed"].append("str")
            result["produced"].append("dict")

        return result

    # ------------------------------------------------------------------
    # side effect classification
    # ------------------------------------------------------------------
    def _classify_side_effects(
        self, funcs: Dict[str, FunctionInfo], result: AnalysisResult
    ) -> Dict[str, List[str]]:
        """Classify functions by side-effect type."""
        io_funcs: List[str] = []
        cache_funcs: List[str] = []
        mutation_funcs: List[str] = []
        pure_funcs: List[str] = []

        for qname, fi in funcs.items():
            purity = self._function_purity(fi, result)
            short = fi.name
            if fi.class_name:
                short = f"{fi.class_name}.{fi.name}"

            if purity == "IO":
                io_funcs.append(short)
            elif purity == "cache":
                cache_funcs.append(short)
            elif purity == "mutation":
                mutation_funcs.append(short)
            else:
                pure_funcs.append(short)

        return {
            "IO": io_funcs[:15],
            "Cache": cache_funcs[:10],
            "Mutation": mutation_funcs[:15],
            "Pure": pure_funcs[:20],
        }

    def _function_purity(self, fi: FunctionInfo, result: AnalysisResult) -> str:
        """Classify function purity based on name and calls."""
        name_lower = fi.name.lower()
        calls_lower = [c.lower() for c in fi.calls]

        # IO indicators
        io_indicators = ["write", "read", "open", "save", "load", "export",
                         "dump", "print", "mkdir", "rmdir", "remove"]
        if any(ind in name_lower for ind in io_indicators):
            return "IO"
        if any(any(ind in c for ind in io_indicators) for c in calls_lower):
            return "IO"

        # Cache indicators
        cache_indicators = ["cache", "memoize", "lru_cache", "store", "fetch"]
        if any(ind in name_lower for ind in cache_indicators):
            return "cache"
        if any(any(ind in c for ind in cache_indicators) for c in calls_lower):
            return "cache"

        # Mutation indicators
        mutation_indicators = ["set_", "update", "modify", "mutate", "append",
                               "insert", "delete", "fix", "patch"]
        if any(name_lower.startswith(ind) or ind in name_lower
               for ind in mutation_indicators):
            return "mutation"

        return "pure"

    # ------------------------------------------------------------------
    # contracts per pipeline
    # ------------------------------------------------------------------
    def _compute_contracts(
        self, pipelines: List[Dict[str, Any]],
        funcs: Dict[str, FunctionInfo]
    ) -> List[Dict[str, Any]]:
        """Build contracts for each pipeline stage."""
        contracts = []
        for pipeline in pipelines:
            stages_contracts = []
            for stage in pipeline["stages"]:
                fi = funcs.get(stage["qualified"])
                if fi:
                    stages_contracts.append({
                        "name": fi.name,
                        "signature": stage["signature"],
                        "cc": stage["cc"],
                        "purity": stage["purity"],
                        "note": self._contract_note(fi, stage["cc"]),
                    })
            contracts.append({
                "pipeline": pipeline["name"],
                "stages": stages_contracts,
            })
        return contracts

    def _contract_note(self, fi: FunctionInfo, cc: float) -> str:
        if cc >= CC_HIGH:
            return f"SMELL: CC={cc:.0f} \u2192 split"
        if self._function_purity(fi, None) == "IO":
            return "IO"
        return ""

    # ------------------------------------------------------------------
    # render sections
    # ------------------------------------------------------------------
    def _render_header(self, ctx: Dict[str, Any]) -> List[str]:
        result: AnalysisResult = ctx["result"]
        nfuncs = len(ctx["funcs"])
        npipelines = len(ctx["pipelines"])
        nhubs = sum(1 for t in ctx["type_usage"]
                    if t["consumed"] >= HUB_TYPE_THRESHOLD)
        return [
            f"# {Path(result.project_path).name if result.project_path else 'project'}/flow"
            f" | {nfuncs} func | {npipelines} pipelines"
            f" | {nhubs} hub-types | {ctx['timestamp']}",
        ]

    def _render_pipelines(self, ctx: Dict[str, Any]) -> List[str]:
        pipelines = ctx["pipelines"]
        if not pipelines:
            return ["PIPELINES[0]: none detected"]

        lines = [f"PIPELINES[{len(pipelines)}]:"]
        for pl in pipelines:
            lines.append(f"  {pl['name']}:{' ' * max(1, 10 - len(pl['name']))}"
                         f"{pl.get('entry_type', '?')}")
            for stage in pl["stages"]:
                cc_marker = "  !!" if stage["cc"] >= CC_HIGH else ""
                lines.append(
                    f"              \u2192 {stage['signature']}"
                    f"{'':>{max(1, 40 - len(stage['signature']))}}"
                    f"CC={stage['cc']:<4.0f} {stage['purity']}{cc_marker}"
                )
            bn = pl.get("bottleneck")
            bn_str = f"BOTTLENECK: {bn['name']}(CC={bn['cc']:.0f})" if bn else "OK"
            lines.append(
                f"              PURITY: {pl['pure_count']}/{pl['total_stages']} pure"
                f"  {bn_str}"
            )
            lines.append("")

        return lines

    def _render_transforms(self, ctx: Dict[str, Any]) -> List[str]:
        transforms = ctx["transforms"]
        if not transforms:
            return ["TRANSFORMS: none (fan-out < 10)"]

        lines = [f"TRANSFORMS (fan-out \u2265{FAN_OUT_THRESHOLD}):"]
        for t in transforms:
            lines.append(
                f"  {t['signature']:<55s} fan={t['fan_out']:<3}"
                f"  {t['label']}"
            )
        return lines

    def _render_contracts(self, ctx: Dict[str, Any]) -> List[str]:
        contracts = ctx["contracts"]
        if not contracts:
            return ["CONTRACTS: none (no pipelines detected)"]

        lines = ["CONTRACTS:"]
        for contract in contracts:
            lines.append(f"  Pipeline: {contract['pipeline']}")
            for stage in contract["stages"]:
                note = f"  {stage['note']}" if stage["note"] else ""
                lines.append(
                    f"    {stage['signature']:<45s}"
                    f" CC={stage['cc']:<4.0f} {stage['purity']}{note}"
                )
            lines.append("")
        return lines

    def _render_data_types(self, ctx: Dict[str, Any]) -> List[str]:
        types = ctx["type_usage"]
        if not types:
            return ["DATA_TYPES: no type information available"]

        lines = ["DATA_TYPES (by cross-function usage):"]
        for t in types:
            label = f"  {t['label']}" if t["label"] else ""
            lines.append(
                f"  {t['type']:<20s} consumed:{t['consumed']:<3}"
                f" produced:{t['produced']:<3}{label}"
            )

        # Hub types summary
        hubs = [t for t in types if t["consumed"] >= HUB_TYPE_THRESHOLD]
        if hubs:
            lines.append("")
            lines.append("  HUB TYPES (consumed \u226510):")
            for h in hubs:
                lines.append(
                    f"    {h['type']} \u2192 {h['consumed']} consumers"
                    f" \u2192 split into sub-interfaces"
                )

        return lines

    def _render_side_effects(self, ctx: Dict[str, Any]) -> List[str]:
        se = ctx["side_effects"]
        lines = ["SIDE_EFFECTS:"]

        for category, funcs in se.items():
            if funcs:
                lines.append(
                    f"  {category + ':':<10s} {', '.join(funcs[:10])}"
                )

        # Pipeline purity summary
        pipelines = ctx["pipelines"]
        if pipelines:
            lines.append("")
            lines.append("  PIPELINE PURITY:")
            for pl in pipelines:
                ratio = pl["pure_count"] / pl["total_stages"] if pl["total_stages"] else 0
                bar_len = int(ratio * 4)
                bar = "\u2588" * bar_len + "\u2591" * (4 - bar_len)
                pct = int(ratio * 100)
                lines.append(
                    f"    {pl['name']:<15s} {bar} {pct}% pure"
                )

        return lines

    # ------------------------------------------------------------------
    # utility helpers
    # ------------------------------------------------------------------
    def _compact_signature(self, fi: FunctionInfo) -> str:
        """Build compact type signature: name(Type->ReturnType)"""
        args_types = []
        for arg in fi.args:
            if arg == "self":
                continue
            if ":" in arg:
                args_types.append(arg.split(":")[-1].strip())
            else:
                args_types.append(arg)

        input_str = ",".join(args_types) if args_types else ""
        ret = fi.returns or ""
        if ret:
            return f"{fi.name}({input_str}\u2192{ret})"
        return f"{fi.name}({input_str})"

    def _infer_input_type(
        self, first_stage: Dict[str, Any],
        funcs: Dict[str, FunctionInfo]
    ) -> str:
        fi = funcs.get(first_stage["qualified"])
        if fi and fi.args:
            for arg in fi.args:
                if arg == "self":
                    continue
                if ":" in arg:
                    return arg.split(":")[-1].strip()
                return arg
        return "?"

    def _resolve_callee(
        self, callee: str, funcs: Dict[str, FunctionInfo]
    ) -> Optional[str]:
        """Resolve callee name to qualified name."""
        if callee in funcs:
            return callee
        # Try suffix match
        for qname in funcs:
            if qname.endswith(f".{callee}"):
                return qname
        return None

    def _is_excluded(self, path: str) -> bool:
        if not path:
            return False
        path_lower = path.lower().replace('\\', '/')
        for pattern in EXCLUDE_PATTERNS:
            if f'/{pattern}/' in path_lower or path_lower.startswith(f'{pattern}/'):
                return True
            if pattern in path_lower.split('/'):
                return True
        return False
