## Cel refaktoryzacji
Extract logic from `label` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'label' spans 8 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 61+)

## Kod źródłowy do refaktoryzacji
```python
def _parse_func_label(label: str) -> Optional[str]:
    label = (label or "").strip()
    if not label.startswith(_FUNC_LABEL_PREFIX):
        return None
    return label[len(_FUNC_LABEL_PREFIX) :].strip() or None


@dataclass(frozen=True)
class FuncSummary:
    name: str
    file: Optional[str]
    line: Optional[int]
    decisions: Tuple[str, ...]
    calls: Tuple[str, ...]


def _collect_nodes(analysis: Dict[str, Any]) -> Dict[int, Dict[str, Any]]:
    nodes = analysis.get("nodes")
    if not isinstance(nodes, dict):
        return {}

    parsed: Dict[int, Dict[str, Any]] = {}
    for k, v in nodes.items():
        try:
            node_id = int(k)
        except Exception:
            continue
        if isinstance(v, dict):
            parsed[node_id] = v
    return parsed


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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.