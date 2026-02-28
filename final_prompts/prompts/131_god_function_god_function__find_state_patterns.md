## Cel refaktoryzacji
Extract logic from `_find_state_patterns` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_find_state_patterns' is highly complex: CC=1, fan-out=8, mutations=10.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 427+)

## Kod źródłowy do refaktoryzacji
```python
    def _find_state_patterns(self, result: AnalysisResult) -> list:
        """Find state management patterns and lifecycles."""
        patterns = []
        
        # State-related keywords
        state_indicators = ['state', 'status', 'mode', 'phase', 'lifecycle', 'session', 'context']
        transition_indicators = ['transition', 'change', 'update', 'set_state', 'switch']
        
        for func_name, func in result.functions.items():
            name_lower = func.name.lower()
            
            # Check for state management functions
            is_state_related = any(ind in name_lower for ind in state_indicators + transition_indicators)
            
            if is_state_related:
                # Find what states this function affects
                affected_states = []
                for call in func.calls[:10]:
                    call_func = result.functions.get(call)
                    if call_func:
                        call_lower = call_func.name.lower()
                        if any(ind in call_lower for ind in state_indicators):
                            affected_states.append(call)
                
                patterns.append({
                    'function': func_name,
                    'type': 'state_manager' if 'set' in name_lower or 'update' in name_lower else 'state_reader',
                    'affects_states': affected_states[:5],
                    'description': func.docstring[:150] if func.docstring else 'N/A',
                })
                
                if len(patterns) >= 20:
                    break
        
        return patterns
    
    def _find_data_dependencies(self, result: AnalysisResult) -> list:
        """Find cross-module data dependencies."""
        deps = []
        
        # Track which modules share data
        module_data_flow = {}
        
        for func_name, func in result.functions.items():
            func_module = func_name.rsplit('.', 1)[0] if '.' in func_name else 'root'
            
            for called in func.calls[:15]:
                called_module = called.rsplit('.', 1)[0] if '.' in called else 'root'
                
                if func_module != called_module and called in result.functions:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _find_state_patterns. Skup się na wydzieleniu operacji o największej liczbie mutacji.