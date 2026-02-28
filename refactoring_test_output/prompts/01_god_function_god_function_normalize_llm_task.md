## Cel refaktoryzacji
Extract logic from `normalize_llm_task` to a new method/function.

## Powód (z analizy DFG)
- Function 'normalize_llm_task' has high complexity: fan-out=9, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/llm_task_generator.py (linie 30-50)

## Kod źródłowy do refaktoryzacji
```python
def normalize_llm_task(data: Dict[str, Any]) -> Dict[str, Any]:
    task = data.get("task") or {}
    context = data.get("context") or {}
    deliverables = data.get("deliverables") or {}
    interfaces = data.get("interfaces") or {}
    rules = data.get("rules") or {}
    acceptance = data.get("acceptance") or {}
    examples = data.get("examples")
    notes = data.get("notes_for_llm") or {}

    normalized: Dict[str, Any] = {
        "task": {
            "title": task.get("title") or "",
            "one_line_goal": task.get("one_line_goal") or "",
        },
        "context": {
            "product_area": context.get("product_area") or "",
            "current_behavior": context.get("current_behavior") or "",
            "desired_behavior": context.get("desired_behavior") or "",
        },
        "deliverables": {
            "language": deliverables.get("language") or "any",
            "must_generate": _ensure_list(deliverables.get("must_generate")),
            "files_to_create_or_edit": _ensure_list(deliverables.get("files_to_create_or_edit")),
        },
        "interfaces": {
            "inputs": _ensure_list(interfaces.get("inputs")),
            "outputs": _ensure_list(interfaces.get("outputs")),
        },
        "rules": {
            "must": _ensure_list(rules.get("must")),
            "must_not": _ensure_list(rules.get("must_not")),
            "assumptions": _ensure_list(rules.get("assumptions")),
            "edge_cases": _ensure_list(rules.get("edge_cases")),
            "performance": _ensure_list(rules.get("performance")),
        },
        "acceptance": {
            "tests": _ensure_list(acceptance.get("tests")),
            "done_definition": _ensure_list(acceptance.get("done_definition")),
        },
        "examples": _ensure_list(examples),
        "notes_for_llm": {
            "constraints": _ensure_list(notes.get("constraints")),
            "style": _ensure_list(notes.get("style")),
            "language_specific_hints": _ensure_list(notes.get("language_specific_hints")),
        },
    }

    return normalized


```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji normalize_llm_task. Skup się na wydzieleniu operacji o największej liczbie mutacji.