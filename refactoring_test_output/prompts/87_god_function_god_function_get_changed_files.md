## Cel refaktoryzacji
Extract logic from `get_changed_files` to a new method/function.

## Powód (z analizy DFG)
- Function 'get_changed_files' has high complexity: fan-out=9, mutations=11.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 630-650)

## Kod źródłowy do refaktoryzacji
```python
    def get_changed_files(
        self,
        project_path: Path
    ) -> Tuple[List[Tuple[str, str]], List[Tuple[str, str]]]:
        """Get changed and unchanged files."""
        changed = []
        unchanged = []
        current_state = {}
        
        for py_file in project_path.rglob("*.py"):
            try:
                content = py_file.read_bytes()
                file_hash = hashlib.md5(content).hexdigest()
                file_str = str(py_file)
                
                current_state[file_str] = file_hash
                
                if file_str in self.previous_state:
                    if self.previous_state[file_str] == file_hash:
                        unchanged.append((file_str, self._get_module_name(py_file, project_path)))
                    else:
                        changed.append((file_str, self._get_module_name(py_file, project_path)))
                else:
                    changed.append((file_str, self._get_module_name(py_file, project_path)))
            except:
                pass
        
        self._save_state(current_state)
        return changed, unchanged
    
    def _get_module_name(self, py_file: Path, project_path: Path) -> str:
        """Calculate module name."""
        rel_path = py_file.relative_to(project_path)
        parts = list(rel_path.parts)[:-1]
        if py_file.name == '__init__.py':
            return '.'.join(parts) if parts else project_path.name
        return '.'.join(parts + [py_file.stem])

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji get_changed_files. Skup się na wydzieleniu operacji o największej liczbie mutacji.