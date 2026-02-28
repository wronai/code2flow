## Cel refaktoryzacji
Extract logic from `data` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'data' spans 6 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 612+)

## Kod źródłowy do refaktoryzacji
```python
    def _load_state(self) -> None:
        """Load previous analysis state."""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    self.previous_state = data.get('file_hashes', {})
            except:
                pass
    
    def _save_state(self, current_state: Dict[str, str]) -> None:
        """Save current analysis state."""
        with open(self.state_file, 'w') as f:
            json.dump({
                'file_hashes': current_state,
                'timestamp': time.time()
            }, f)
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.