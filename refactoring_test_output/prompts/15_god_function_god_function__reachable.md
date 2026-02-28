## Cel refaktoryzacji
Extract logic from `_reachable` to a new method/function.

## Powód (z analizy DFG)
- Function '_reachable' has high complexity: fan-out=9, mutations=4.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 267-287)

## Kod źródłowy do refaktoryzacji
```python
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


def generate_llm_flow(
    analysis: Dict[str, Any],
    max_functions: int,
    limit_decisions: int,
    limit_calls: int,
) -> Dict[str, Any]:
    nodes = _collect_nodes(analysis)
    entrypoints = _collect_entrypoints(nodes)

    known_functions = _collect_functions(nodes)
    func_summaries = _summarize_functions(nodes, limit_decisions=limit_decisions, limit_calls=limit_calls)

    reachable = _pick_relevant_functions(
        entrypoints=entrypoints,
        known_functions=known_functions,
        func_summaries=func_summaries,
        nodes=nodes,
        max_functions=max_functions,
    )

    functions_out: List[Dict[str, Any]] = []
    for fn in sorted(reachable):
        s = func_summaries.get(fn)
        if not s:
            continue
        functions_out.append(
            {
                "name": s.name,
                "file": s.file,
                "line": s.line,
                "decisions": list(s.decisions),
                "calls": list(s.calls),
            }
        )

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _reachable. Skup się na wydzieleniu operacji o największej liczbie mutacji.