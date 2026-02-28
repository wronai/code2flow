## Cel refaktoryzacji
Extract logic from `self, message, total, phase, current` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, message, total, phase, current) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingAnalyzer._report_progress, code2flow.core.streaming_analyzer._report_progress.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 585-605)

## Kod źródłowy do refaktoryzacji
```python
    def _report_progress(
        self,
        phase: str,
        current: int,
        total: int,
        message: str
    ) -> None:
        """Report progress via callback."""
        if self._progress_callback:
            self._progress_callback({
                'phase': phase,
                'current': current,
                'total': total,
                'percentage': (current / total * 100) if total > 0 else 0,
                'message': message
            })


class IncrementalAnalyzer:
    """Incremental analysis with change detection."""
    
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.