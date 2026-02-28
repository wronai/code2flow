## Cel refaktoryzacji
Extract logic from `detect_patterns` to a new method/function.

## Powód (Głęboka Analiza)
- Function 'detect_patterns' is highly complex: CC=1, fan-out=6, mutations=6.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/patterns/detector.py (linie 16+)

## Kod źródłowy do refaktoryzacji
```python
    def detect_patterns(self, result: AnalysisResult) -> List[Dict]:
        """Detect all behavioral patterns in analysis result."""
        patterns = []
        
        # Detect recursive patterns
        if self.config.detect_recursion:
            patterns.extend(self._detect_recursion(result))
            
        # Detect state machines
        if self.config.detect_state_machines:
            patterns.extend(self._detect_state_machines(result))
            
        # Detect factory patterns
        patterns.extend(self._detect_factory_pattern(result))
        
        # Detect singleton pattern
        patterns.extend(self._detect_singleton(result))
        
        # Detect strategy pattern
        patterns.extend(self._detect_strategy_pattern(result))
        
        return patterns
        
    def _detect_recursion(self, result: AnalysisResult) -> List[Dict]:
        """Detect recursive function calls."""
        patterns = []
        
        for func_name, func_info in result.functions.items():
            if func_name in func_info.calls:
                patterns.append({
                    'type': 'recursive',
                    'name': f'recursive_{func_name}',
                    'function': func_name,
                    'confidence': 1.0,
                    'description': f'Function {func_name} calls itself recursively'
                })
                
        return patterns
        
    def _detect_state_machines(self, result: AnalysisResult) -> List[Dict]:
        """Detect state machine patterns in classes."""
        patterns = []
        
        for class_name, class_info in result.classes.items():
            # Look for state-related attributes and transition methods
            has_state = False
            transition_methods = []
            
            for method in class_info.get('methods', []):
                method_lower = method.lower()
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji detect_patterns. Skup się na wydzieleniu operacji o największej liczbie mutacji.