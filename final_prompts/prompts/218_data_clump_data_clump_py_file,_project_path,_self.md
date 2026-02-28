## Cel refaktoryzacji
Move method `py_file, project_path, self` from module `streaming_analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (py_file, project_path, self) are used together in multiple functions: code2flow.core.streaming_analyzer.IncrementalAnalyzer._get_module_name, code2flow.core.streaming_analyzer._get_module_name.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `streaming_analyzer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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