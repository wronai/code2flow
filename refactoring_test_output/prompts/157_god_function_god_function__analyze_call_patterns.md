## Cel refaktoryzacji
Extract logic from `_analyze_call_patterns` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_call_patterns' has high complexity: fan-out=8, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 1206-1226)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_call_patterns(self, result: AnalysisResult) -> dict:
        """Analyze common call patterns in the codebase."""
        patterns = {
            'entry_to_api': [],
            'api_to_internal': [],
            'cross_module': [],
        }
        
        # Find entry points that call public API
        seen_functions = set()  # Deduplicate
        for ep_name in result.entry_points[:30]:
            # Skip duplicates (class methods vs module functions)
            base_name = ep_name.split('.')[-1]
            if base_name in seen_functions:
                continue
            seen_functions.add(base_name)
            ep_func = result.functions.get(ep_name)
            if not ep_func:
                continue
                
            for called in ep_func.calls:
                called_func = result.functions.get(called)
                if called_func:
                    # Check if called function is public API
                    if not called_func.name.startswith('_'):
                        patterns['entry_to_api'].append((ep_name, called))
                    # Check if cross-module
                    ep_module = ep_name.rsplit('.', 1)[0] if '.' in ep_name else ''
                    called_module = called.rsplit('.', 1)[0] if '.' in called else ''
                    if ep_module != called_module:
                        patterns['cross_module'].append((ep_name, called))
        
        return patterns

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_call_patterns. Skup się na wydzieleniu operacji o największej liczbie mutacji.