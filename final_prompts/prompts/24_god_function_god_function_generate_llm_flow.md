## Cel refaktoryzacji
Extract logic from `generate_llm_flow` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'generate_llm_flow' is highly complex: CC=5, fan-out=10, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 283+)

## Kod źródłowy do refaktoryzacji
```python
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

    package_names = sorted({fn.split(".")[0] for fn in known_functions if "." in fn})

    return {
        "format": "llm_flow.v1",
        "app": {
            "packages": package_names,
            "entrypoints": entrypoints,
        },
        "flow": {
            "selected_functions": functions_out,
        },
    }


def render_llm_flow_md(flow: Dict[str, Any]) -> str:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji generate_llm_flow. Skup się na wydzieleniu operacji o największej liczbie mutacji.