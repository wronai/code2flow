## Cel refaktoryzacji
Extract logic from `_identify_process_patterns` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_identify_process_patterns' is highly complex: CC=1, fan-out=10, mutations=7.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 747+)

## Kod źródłowy do refaktoryzacji
```python
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
            
            for pattern_type, indicators in process_indicators.items():
                if any(ind in name_lower or ind in docstring for ind in indicators):
                    patterns[pattern_type].append({
                        'function': func_name,
                        'description': func.docstring[:100] if func.docstring else 'N/A',
                        'data_flow': f"{len(func.called_by)} → {func_name} → {len(func.calls)}",
                    })
                    break
        
        # Convert to list and sort by usage
        process_patterns = []
        for pattern_type, funcs in patterns.items():
            process_patterns.append({
                'pattern_type': pattern_type,
                'functions': funcs[:10],  # Limit per pattern
                'count': len(funcs),
            })
        
        return sorted(process_patterns, key=lambda x: x['count'], reverse=True)
    
    def _analyze_optimization_opportunities(self, result: AnalysisResult, data_types: list, data_flow_graph: dict) -> dict:
        """Analyze optimization opportunities for data types and processes."""
        optimization = {
            'potential_score': 0.0,
            'type_consolidation': [],
            'process_consolidation': [],
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _identify_process_patterns. Skup się na wydzieleniu operacji o największej liczbie mutacji.