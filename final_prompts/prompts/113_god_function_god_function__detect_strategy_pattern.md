## Cel refaktoryzacji
Extract logic from `_detect_strategy_pattern` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_strategy_pattern' is highly complex: CC=1, fan-out=8, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/patterns/detector.py (linie 132+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_strategy_pattern(self, result: AnalysisResult) -> List[Dict]:
        """Detect strategy pattern."""
        patterns = []
        
        # Look for interface-like classes with execute/run methods
        strategy_candidates = []
        
        for class_name, class_info in result.classes.items():
            methods = class_info.get('methods', [])
            
            # Look for execute, run, or process methods
            if any(m in methods for m in ['execute', 'run', 'process', 'apply']):
                strategy_candidates.append(class_name)
                
        # Check if these are used interchangeably
        if len(strategy_candidates) > 1:
            for func_name, func_info in result.functions.items():
                calls = func_info.calls
                called_strategies = [s for s in strategy_candidates if s in str(calls)]
                
                if len(called_strategies) > 1:
                    patterns.append({
                        'type': 'strategy',
                        'name': f'strategy_in_{func_name}',
                        'context': func_name,
                        'strategies': called_strategies,
                        'confidence': 0.7,
                        'description': f'Function {func_name} uses strategy pattern'
                    })
                    break
                    
        return patterns
        
    def _check_returns_classes(self, result: AnalysisResult, func_name: str) -> Set[str]:
        """Check what classes a function might return."""
        # Simplified - in full implementation would analyze return statements
        return set()  # Placeholder
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_strategy_pattern. Skup się na wydzieleniu operacji o największej liczbie mutacji.