## Cel refaktoryzacji
Extract logic from `__init__` to a new method/function.

## Powód (z analizy DFG)
- Function '__init__' has high complexity: fan-out=2, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 606-626)

## Kod źródłowy do refaktoryzacji
```python
    def __init__(self, config: Optional[Config] = None):
        self.config = config or FAST_CONFIG
        self.state_file = Path(".code2flow_state.json")
        self.previous_state: Dict[str, str] = {}
        self._load_state()
    
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji __init__. Skup się na wydzieleniu operacji o największej liczbie mutacji.