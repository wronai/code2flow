## Cel refaktoryzacji
Extract logic from `results, prioritized, self` to a new method/function.

## Powód (z analizy DFG)
- Arguments (results, prioritized, self) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingAnalyzer._select_important_files, code2flow.core.streaming_analyzer._select_important_files.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 512-532)

## Kod źródłowy do refaktoryzacji
```python
    def _select_important_files(
        self,
        prioritized: List[FilePriority],
        results: List[Dict]
    ) -> List[FilePriority]:
        """Select files for deep analysis based on importance."""
        important = []
        
        for p in prioritized:
            # Entry points are important
            if p.is_entry_point:
                important.append(p)
                continue
            
            # Find result for this file
            for r in results:
                mod = r.get('module')
                if mod and mod.name == p.module_name:
                    # Files with many functions are important
                    if len(mod.functions) > 5:
                        important.append(p)
                        break
                    
                    # Files called by many others
                    if p.import_count > 3:
                        important.append(p)
                        break
        
        return important
    
    def _collect_files(self, project_path: Path) -> List[Tuple[str, str]]:
        """Collect Python files with filtering."""
        files = []
        
        for py_file in project_path.rglob("*.py"):
            file_str = str(py_file)
            
            # Apply filters
            if self.strategy.skip_test_files:
                if any(x in file_str.lower() for x in ['test', '_test', 'conftest']):
                    continue
            
            if any(x in file_str.lower() for x in ['__pycache__', '.venv', 'venv']):
                continue
            
            # Calculate module name
            rel_path = py_file.relative_to(project_path)
            parts = list(rel_path.parts)[:-1]
            if py_file.name == '__init__.py':
                module_name = '.'.join(parts) if parts else project_path.name

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.