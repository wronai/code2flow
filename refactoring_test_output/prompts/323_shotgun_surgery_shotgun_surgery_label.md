## Cel refaktoryzacji
Extract logic from `label` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'label' spans 8 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_flow_generator.py (linie 43-63)

## Kod źródłowy do refaktoryzacji
```python
def _parse_call_label(label: str) -> Optional[str]:
    label = (label or "").strip()
    if not label.startswith(_CALL_LABEL_PREFIX):
        return None
    rest = label[len(_CALL_LABEL_PREFIX) :].strip()
    rest = rest.replace("<", "").replace(">", "")

    m = re.match(r"([A-Za-z_][A-Za-z0-9_\.]+)\s*\(", rest)
    if m:
        return m.group(1)

    m = re.match(r"([A-Za-z_][A-Za-z0-9_\.]+)$", rest)
    if m:
        return m.group(1)

    return None


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



```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.