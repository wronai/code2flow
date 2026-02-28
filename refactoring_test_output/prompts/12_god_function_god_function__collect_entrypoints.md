## Cel refaktoryzacji
Extract logic from `_collect_entrypoints` to a new method/function.

## Powód (z analizy DFG)
- Function '_collect_entrypoints' has high complexity: fan-out=12, mutations=7.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 93-113)

## Kod źródłowy do refaktoryzacji
```python
def _collect_entrypoints(nodes: Dict[int, Dict[str, Any]]) -> List[Dict[str, Any]]:
    by_file: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for n in nodes.values():
        f = n.get("file")
        if isinstance(f, str):
            by_file[f].append(n)

    entrypoints: List[Dict[str, Any]] = []
    for f, ns in by_file.items():
        if not (f.endswith("__main__.py") or f.endswith("cli.py")):
            continue

        main_funcs = [n for n in ns if n.get("type") == "FUNC" and isinstance(n.get("function"), str)]
        for n in main_funcs:
            entrypoints.append(
                {
                    "kind": "cli" if f.endswith("cli.py") else "module_main",
                    "file": f,
                    "function": n.get("function"),
                    "line": n.get("line"),
                }
            )

    uniq: Dict[str, Dict[str, Any]] = {}
    for ep in entrypoints:
        key = str(ep.get("function") or "")
        if key and key not in uniq:
            uniq[key] = ep

    return list(uniq.values())


def _collect_functions(nodes: Dict[int, Dict[str, Any]]) -> Set[str]:
    out: Set[str] = set()
    for n in nodes.values():
        if n.get("type") != "FUNC":
            continue
        fn = n.get("function")
        if isinstance(fn, str) and fn:
            out.add(fn)
        else:
            parsed = _parse_func_label(str(n.get("label") or ""))
            if parsed:
                out.add(parsed)
    return out


def _node_counts_by_function(nodes: Dict[int, Dict[str, Any]]) -> Counter[str]:
    counts: Counter[str] = Counter()
    for n in nodes.values():

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _collect_entrypoints. Skup się na wydzieleniu operacji o największej liczbie mutacji.