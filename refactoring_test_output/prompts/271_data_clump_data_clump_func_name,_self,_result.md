## Cel refaktoryzacji
Extract logic from `func_name, self, result` to a new method/function.

## Powód (z analizy DFG)
- Arguments (func_name, self, result) are used together in multiple functions: code2flow.patterns.detector.PatternDetector._check_returns_classes, code2flow.patterns.detector._check_returns_classes.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/patterns/detector.py (linie 165-185)

## Kod źródłowy do refaktoryzacji
```python
    def _check_returns_classes(self, result: AnalysisResult, func_name: str) -> Set[str]:
        """Check what classes a function might return."""
        # Simplified - in full implementation would analyze return statements
        return set()  # Placeholder

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.