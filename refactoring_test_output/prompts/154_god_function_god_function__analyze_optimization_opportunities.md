## Cel refaktoryzacji
Extract logic from `_analyze_optimization_opportunities` to a new method/function.

## Powód (z analizy DFG)
- Function '_analyze_optimization_opportunities' has high complexity: fan-out=8, mutations=19.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 791-811)

## Kod źródłowy do refaktoryzacji
```python
    def _analyze_optimization_opportunities(self, result: AnalysisResult, data_types: list, data_flow_graph: dict) -> dict:
        """Analyze optimization opportunities for data types and processes."""
        optimization = {
            'potential_score': 0.0,
            'type_consolidation': [],
            'process_consolidation': [],
            'hub_optimization': [],
            'recommendations': [],
        }
        
        # 1. Type consolidation opportunities
        similar_types = {}
        for dt in data_types:
            type_signature = ','.join(sorted(dt['detected_types']))
            if type_signature not in similar_types:
                similar_types[type_signature] = []
            similar_types[type_signature].append(dt)
        
        for type_sig, similar in similar_types.items():
            if len(similar) > 1:
                total_usage = sum(s['usage_count'] for s in similar)
                if total_usage > 10:  # Significant usage
                    optimization['type_consolidation'].append({
                        'type_signature': type_sig,
                        'similar_types': [s['type_name'] for s in similar],
                        'total_usage': total_usage,
                        'potential_reduction': len(similar) - 1,
                    })
        
        # 2. Process consolidation
        process_patterns = self._identify_process_patterns(result)
        for pattern in process_patterns:
            if pattern['count'] > 5:  # Many similar processes
                optimization['process_consolidation'].append({
                    'pattern_type': pattern['pattern_type'],
                    'function_count': pattern['count'],
                    'potential_reduction': pattern['count'] // 3,  # Consolidate 1/3
                })
        
        # 3. Hub optimization (functions with many connections)
        hub_nodes = [n for n in data_flow_graph['nodes'].values() if n['is_hub']]
        for hub in hub_nodes[:10]:  # Top 10 hubs
            optimization['hub_optimization'].append({
                'function': hub['id'],
                'connections': hub['in_degree'] + hub['out_degree'],
                'optimization_type': 'split' if hub['out_degree'] > 10 else 'cache',
            })
        
        # 4. Calculate overall potential score
        type_score = len(optimization['type_consolidation']) * 10

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _analyze_optimization_opportunities. Skup się na wydzieleniu operacji o największej liczbie mutacji.