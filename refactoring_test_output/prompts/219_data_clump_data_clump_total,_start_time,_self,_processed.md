## Cel refaktoryzacji
Extract logic from `total, start_time, self, processed` to a new method/function.

## Powód (z analizy DFG)
- Arguments (total, start_time, self, processed) are used together in multiple functions: code2flow.core.streaming_analyzer.StreamingAnalyzer._estimate_eta, code2flow.core.streaming_analyzer._estimate_eta.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 569-589)

## Kod źródłowy do refaktoryzacji
```python
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

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.