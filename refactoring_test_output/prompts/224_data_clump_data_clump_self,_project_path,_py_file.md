## Cel refaktoryzacji
Extract logic from `self, project_path, py_file` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, project_path, py_file) are used together in multiple functions: code2flow.core.streaming_analyzer.IncrementalAnalyzer._get_module_name, code2flow.core.streaming_analyzer._get_module_name.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 660-680)

## Kod źródłowy do refaktoryzacji
```python
    def _get_module_name(self, py_file: Path, project_path: Path) -> str:
        """Calculate module name."""
        rel_path = py_file.relative_to(project_path)
        parts = list(rel_path.parts)[:-1]
        if py_file.name == '__init__.py':
            return '.'.join(parts) if parts else project_path.name
        return '.'.join(parts + [py_file.stem])

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.