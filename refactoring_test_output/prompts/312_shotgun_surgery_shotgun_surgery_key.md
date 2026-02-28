## Cel refaktoryzacji
Extract logic from `key` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'key' spans 5 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_task_generator.py (linie 103-123)

## Kod źródłowy do refaktoryzacji
```python
def parse_llm_task_text(text: str) -> Dict[str, Any]:
    text = _strip_bom(text)
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    sections: Dict[str, List[str]] = {}
    current: Optional[str] = None

    def start_section(name: str) -> None:
        nonlocal current
        current = name
        sections.setdefault(name, [])

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current is not None:
                sections[current].append("")
            continue

        upper = stripped.upper()
        if upper.endswith(":"):
            key = upper[:-1].strip()
            if key in {
                "TITLE",
                "GOAL",
                "CURRENT",
                "DESIRED",
                "INPUTS",
                "OUTPUTS",
                "RULES (MUST)",
                "RULES (MUST NOT)",
                "EDGE CASES",
                "ACCEPTANCE TESTS",
                "DELIVERABLES",
            }:
                start_section(key)
                continue

        if current is None:
            continue
        sections[current].append(line)

    data: Dict[str, Any] = {
        "task": {"title": "", "one_line_goal": ""},
        "context": {"product_area": "", "current_behavior": "", "desired_behavior": ""},
        "deliverables": {"language": "any", "must_generate": [], "files_to_create_or_edit": []},
        "interfaces": {"inputs": [], "outputs": []},
        "rules": {"must": [], "must_not": [], "assumptions": [], "edge_cases": [], "performance": []},
        "acceptance": {"tests": [], "done_definition": []},
        "examples": [],

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.