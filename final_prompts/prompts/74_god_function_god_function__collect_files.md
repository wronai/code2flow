## Cel refaktoryzacji
Extract logic from `_collect_files` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_collect_files' is highly complex: CC=1, fan-out=8, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 542+)

## Kod źródłowy do refaktoryzacji
```python
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
            else:
                module_name = '.'.join(parts + [py_file.stem])
            
            files.append((file_str, module_name))
        
        return files
    
    def _estimate_eta(
        self,
        start_time: float,
        processed: int,
        total: int
    ) -> float:
        """Estimate remaining time."""
        if processed == 0:
            return 0.0
        
        elapsed = time.time() - start_time
        rate = processed / elapsed
        remaining = total - processed
        
        return remaining / rate if rate > 0 else 0.0
    
    def _report_progress(
        self,
        phase: str,
        current: int,
        total: int,
        message: str
    ) -> None:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _collect_files. Skup się na wydzieleniu operacji o największej liczbie mutacji.