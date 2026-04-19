"""LLM Flow analysis — function scoring, summarization, and call graph."""

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple
from collections import deque

from .utils import _shorten
from .parsing import _parse_call_label


@dataclass(frozen=True)
class FuncSummary:
    name: str
    file: Optional[str]
    line: Optional[int]
    decisions: Tuple[str, ...]
    calls: Tuple[str, ...]


def _node_counts_by_function(nodes: Dict[int, Dict[str, Any]]) -> Counter[str]:
    """Count nodes per function for scoring relevance."""
    counts: Counter[str] = Counter()
    for n in nodes.values():
        fn = n.get("function")
        if isinstance(fn, str) and fn:
            counts[fn] += 1
    return counts


def _pick_relevant_functions(
    *,
    entrypoints: List[Dict[str, Any]],
    known_functions: Set[str],
    func_summaries: Dict[str, FuncSummary],
    nodes: Dict[int, Dict[str, Any]],
    max_functions: int,
) -> List[str]:
    """Pick a compact but meaningful subset of functions.

    In many real projects, the CFG "CALL" labels often point to external
    functions (e.g. click.echo), so a pure call-graph reachability may select
    almost nothing. Here we fall back to a scoring heuristic:
    - start with entrypoints
    - boost functions that have many nodes (more logic)
    - boost functions with important keywords (extract, schema, openapi, dom, cli)
    """

    roots = [str(ep.get("function") or "") for ep in entrypoints]
    roots = [r for r in roots if r in known_functions]

    counts = _node_counts_by_function(nodes)

    keyword_boosts = [
        (".cli.", 50),
        (".extract.", 80),
        ("extract_schema", 120),
        ("extract_schema_to_file", 120),
        ("extract_appspec_to_file", 120),
        ("openapi", 60),
        ("dom", 40),
        ("makefile", 40),
        ("shell", 40),
        ("python", 40),
        ("validate", 20),
        ("discover", 20),
    ]

    def score(fn: str) -> int:
        s = 0
        s += min(500, counts.get(fn, 0))  # node count baseline
        for needle, boost in keyword_boosts:
            if needle in fn:
                s += boost
        if fn in roots:
            s += 1000
        if fn in func_summaries and func_summaries[fn].decisions:
            s += min(200, 10 * len(func_summaries[fn].decisions))
        return s

    scored = [(fn, score(fn)) for fn in known_functions]
    scored.sort(key=lambda x: x[1], reverse=True)

    picked: List[str] = []
    for fn, _ in scored:
        if len(picked) >= max_functions:
            break
        picked.append(fn)

    return picked


def _summarize_functions(nodes: Dict[int, Dict[str, Any]], limit_decisions: int, limit_calls: int) -> Dict[str, FuncSummary]:
    """Summarize functions with their decisions, calls, and location info."""
    decisions_by_func: Dict[str, List[str]] = defaultdict(list)
    calls_by_func: Dict[str, List[str]] = defaultdict(list)
    loc_by_func: Dict[str, Tuple[Optional[str], Optional[int]]] = {}

    for n in nodes.values():
        fn = n.get("function")
        if not isinstance(fn, str) or not fn:
            continue

        if fn not in loc_by_func:
            loc_by_func[fn] = (
                n.get("file") if isinstance(n.get("file"), str) else None,
                n.get("line") if isinstance(n.get("line"), int) else None,
            )

        ntype = n.get("type")
        label = str(n.get("label") or "")

        if ntype == "IF":
            decisions_by_func[fn].append(_shorten(label, 120))
        elif ntype == "CALL":
            callee = _parse_call_label(label)
            if callee:
                calls_by_func[fn].append(callee)

    summaries: Dict[str, FuncSummary] = {}
    for fn in set(list(decisions_by_func.keys()) + list(calls_by_func.keys()) + list(loc_by_func.keys())):
        file, line = loc_by_func.get(fn, (None, None))

        decision_counts = Counter(decisions_by_func.get(fn, []))
        call_counts = Counter(calls_by_func.get(fn, []))

        decisions = tuple([d for d, _ in decision_counts.most_common(limit_decisions)])
        calls = tuple([c for c, _ in call_counts.most_common(limit_calls)])

        summaries[fn] = FuncSummary(
            name=fn,
            file=file,
            line=line,
            decisions=decisions,
            calls=calls,
        )

    return summaries


def _build_call_graph(func_summaries: Dict[str, FuncSummary], known_functions: Set[str]) -> Dict[str, Set[str]]:
    g: Dict[str, Set[str]] = defaultdict(set)
    for fn, s in func_summaries.items():
        for callee in s.calls:
            if callee in known_functions:
                g[fn].add(callee)
    return g


def _reachable(g: Dict[str, Set[str]], roots: Iterable[str], max_nodes: int) -> List[str]:
    seen: Set[str] = set()
    q: deque[str] = deque([r for r in roots if r])

    while q and len(seen) < max_nodes:
        cur = q.popleft()
        if cur in seen:
            continue
        seen.add(cur)
        for nxt in sorted(g.get(cur, set())):
            if nxt not in seen:
                q.append(nxt)

    return list(seen)


__all__ = [
    'FuncSummary',
    '_node_counts_by_function',
    '_pick_relevant_functions',
    '_summarize_functions',
    '_build_call_graph',
    '_reachable',
]
