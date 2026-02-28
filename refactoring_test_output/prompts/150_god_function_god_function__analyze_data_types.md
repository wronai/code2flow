## Cel refaktoryzacji
Extract logic from `_analyze_data_types` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_data_types' has high complexity: fan-out=16, mutations=16.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 588-608)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_data_types(self, result: AnalysisResult) -> list:
        """Analyze data types and their usage patterns."""
        data_types = {}
        
        # Common data type indicators in function names and docstrings
        type_indicators = {
            'list': ['list', 'array', 'items', 'elements', 'collection', 'sequence'],
            'dict': ['dict', 'map', 'mapping', 'key_value', 'record', 'object'],
            'str': ['string', 'text', 'content', 'message', 'input_text'],
            'int': ['int', 'integer', 'count', 'index', 'number', 'id'],
            'float': ['float', 'decimal', 'score', 'probability', 'rate'],
            'bool': ['bool', 'boolean', 'flag', 'is_', 'has_', 'can_'],
            'tuple': ['tuple', 'pair', 'coordinate', 'point'],
            'set': ['set', 'unique', 'collection_unique'],
        }
        
        for func_name, func in result.functions.items():
            # Analyze function name for type hints
            func_name_lower = func.name.lower()
            docstring = func.docstring.lower() if func.docstring else ''
            
            detected_types = []
            for type_name, indicators in type_indicators.items():
                if any(ind in func_name_lower or ind in docstring for ind in indicators):
                    detected_types.append(type_name)
            
            # Analyze parameter patterns (simplified)
            param_types = self._infer_parameter_types(func)
            
            # Analyze return patterns
            return_types = self._infer_return_types(func)
            
            if detected_types or param_types or return_types:
                type_key = f"{','.join(sorted(set(detected_types + param_types + return_types)))}"
                
                if type_key not in data_types:
                    data_types[type_key] = {
                        'type_name': type_key,
                        'detected_types': list(set(detected_types)),
                        'parameter_types': list(set(param_types)),
                        'return_types': list(set(return_types)),
                        'functions': [],
                        'usage_count': 0,
                        'cross_module_usage': 0,
                    }
                
                data_types[type_key]['functions'].append(func_name)
                data_types[type_key]['usage_count'] += 1
                
                # Check cross-module usage

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_data_types. Skup się na wydzieleniu operacji o największej liczbie mutacji.