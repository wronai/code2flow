## Cel refaktoryzacji
Extract logic from `_pick_relevant_functions` to a new method/function.

## Powód (z analizy DFG)
- Function '_pick_relevant_functions' has high complexity: fan-out=9, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 149-169)

## Kod źródłowy do refaktoryzacji
```python
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


```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _pick_relevant_functions. Skup się na wydzieleniu operacji o największej liczbie mutacji.