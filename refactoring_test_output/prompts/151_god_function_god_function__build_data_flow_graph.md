## Cel refaktoryzacji
Extract logic from `_build_data_flow_graph` to a new method/function.

## Powód (z analizy DFG)
- Function '_build_data_flow_graph' has high complexity: fan-out=8, mutations=6.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 679-699)

## Kod źródłowy do refaktoryzacji
```python
    def _build_data_flow_graph(self, result: AnalysisResult) -> dict:
        """Build data flow graph showing how data moves between functions."""
        nodes = {}
        edges = []
        
        # Create nodes for functions
        for func_name, func in result.functions.items():
            # Determine data type for this function
            data_types = self._get_function_data_types(func)
            
            nodes[func_name] = {
                'id': func_name,
                'name': func.name.split('.')[-1],
                'module': func_name.rsplit('.', 1)[0] if '.' in func_name else 'root',
                'data_types': data_types,
                'in_degree': len(func.called_by),
                'out_degree': len(func.calls),
                'is_hub': len(func.calls) > 5 or len(func.called_by) > 5,
            }
        
        # Create edges for data flow
        for func_name, func in result.functions.items():
            for called in func.calls[:15]:  # Limit for performance
                if called in result.functions:
                    edges.append({
                        'from': func_name,
                        'to': called,
                        'data_flow': True,
                        'weight': 1,
                    })
        
        return {
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'hub_nodes': sum(1 for n in nodes.values() if n['is_hub']),
            }
        }
    
    def _get_function_data_types(self, func) -> list:
        """Get data types associated with a function."""
        types = []
        
        # Check function name
        name_lower = func.name.lower()
        if 'list' in name_lower or 'items' in name_lower:
            types.append('list')
        if 'dict' in name_lower or 'map' in name_lower:

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _build_data_flow_graph. Skup się na wydzieleniu operacji o największej liczbie mutacji.