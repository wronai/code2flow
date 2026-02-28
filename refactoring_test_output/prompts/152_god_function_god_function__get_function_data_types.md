## Cel refaktoryzacji
Extract logic from `_get_function_data_types` to a new method/function.

## Powód (z analizy DFG)
- Function '_get_function_data_types' has high complexity: fan-out=5, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 720-740)

## Kod źródłowy do refaktoryzacji
```python
    def _get_function_data_types(self, func) -> list:
        """Get data types associated with a function."""
        types = []
        
        # Check function name
        name_lower = func.name.lower()
        if 'list' in name_lower or 'items' in name_lower:
            types.append('list')
        if 'dict' in name_lower or 'map' in name_lower:
            types.append('dict')
        if 'text' in name_lower or 'string' in name_lower:
            types.append('str')
        if 'count' in name_lower or 'index' in name_lower:
            types.append('int')
        
        # Check docstring
        if func.docstring:
            docstring_lower = func.docstring.lower()
            if 'list' in docstring_lower:
                types.append('list')
            if 'dict' in docstring_lower:
                types.append('dict')
            if 'string' in docstring_lower or 'text' in docstring_lower:
                types.append('str')
        
        return list(set(types))
    
    def _identify_process_patterns(self, result: AnalysisResult) -> list:
        """Identify common data processing patterns."""
        patterns = {
            'filter': [],
            'map': [],
            'reduce': [],
            'aggregate': [],
            'transform': [],
            'validate': [],
        }
        
        process_indicators = {
            'filter': ['filter', 'select', 'where', 'find', 'search'],
            'map': ['map', 'transform', 'convert', 'apply', 'process'],
            'reduce': ['reduce', 'sum', 'count', 'aggregate', 'fold'],
            'aggregate': ['group', 'bucket', 'cluster', 'partition'],
            'transform': ['transform', 'convert', 'normalize', 'standardize'],
            'validate': ['validate', 'check', 'verify', 'ensure', 'assert'],
        }
        
        for func_name, func in result.functions.items():
            name_lower = func.name.lower()
            docstring = func.docstring.lower() if func.docstring else ''

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _get_function_data_types. Skup się na wydzieleniu operacji o największej liczbie mutacji.