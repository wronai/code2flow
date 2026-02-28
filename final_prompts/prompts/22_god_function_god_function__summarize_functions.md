## Cel refaktoryzacji
Extract logic from `_summarize_functions` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_summarize_functions' is highly complex: CC=14, fan-out=21, mutations=18.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 211+)

## Kod źródłowy do refaktoryzacji
```python
def _summarize_functions(nodes: Dict[int, Dict[str, Any]], limit_decisions: int, limit_calls: int) -> Dict[str, FuncSummary]:
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
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _summarize_functions. Skup się na wydzieleniu operacji o największej liczbie mutacji.