## Cel refaktoryzacji
Extract logic from `_detect_state_machines` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_state_machines' is highly complex: CC=1, fan-out=6, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/patterns/detector.py (linie 55+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_state_machines(self, result: AnalysisResult) -> List[Dict]:
        """Detect state machine patterns in classes."""
        patterns = []
        
        for class_name, class_info in result.classes.items():
            # Look for state-related attributes and transition methods
            has_state = False
            transition_methods = []
            
            for method in class_info.get('methods', []):
                method_lower = method.lower()
                if 'state' in method_lower:
                    has_state = True
                if any(word in method_lower for word in ['transition', 'change', 'set', 'next', 'prev']):
                    transition_methods.append(method)
                    
            if has_state or transition_methods:
                patterns.append({
                    'type': 'state_machine',
                    'name': f'state_machine_{class_name}',
                    'class': class_name,
                    'transitions': transition_methods,
                    'confidence': 0.8 if transition_methods else 0.5,
                    'description': f'Class {class_name} appears to implement a state machine'
                })
                
        return patterns
        
    def _detect_factory_pattern(self, result: AnalysisResult) -> List[Dict]:
        """Detect factory method pattern."""
        patterns = []
        
        for func_name, func_info in result.functions.items():
            # Check if function returns instances of different classes
            name_lower = func_name.lower()
            if 'create' in name_lower or 'factory' in name_lower or 'build' in name_lower:
                # Check if it returns different types
                returns_classes = self._check_returns_classes(result, func_name)
                if returns_classes:
                    patterns.append({
                        'type': 'factory',
                        'name': f'factory_{func_name}',
                        'function': func_name,
                        'creates': list(returns_classes),
                        'confidence': 0.7,
                        'description': f'Function {func_name} appears to be a factory'
                    })
                    
        return patterns
        
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_state_machines. Skup się na wydzieleniu operacji o największej liczbie mutacji.