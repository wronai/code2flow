## Cel refaktoryzacji
Move method `func_name, result, self` from module `detector` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (func_name, result, self) are used together in multiple functions: code2flow.patterns.detector.PatternDetector._check_returns_classes, code2flow.patterns.detector._check_returns_classes.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `detector`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/patterns/detector.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
```python
    def _check_returns_classes(self, result: AnalysisResult, func_name: str) -> Set[str]:
        """Check what classes a function might return."""
        # Simplified - in full implementation would analyze return statements
        return set()  # Placeholder
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.