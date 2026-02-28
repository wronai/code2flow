## Cel refaktoryzacji
Extract logic from `export_grouped` to a new method/function.

## Powód (z analizy DFG)
- Function 'export_grouped' has high complexity: fan-out=14, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 32-52)

## Kod źródłowy do refaktoryzacji
```python
    def export_grouped(self, result: AnalysisResult, output_path: str) -> None:
        """Export with grouped CFG flows by function - more readable format."""
        # Group CFG nodes by function
        from collections import defaultdict
        
        func_flows = defaultdict(list)
        
        # Group nodes by their function
        for node_id, node in result.nodes.items():
            if hasattr(node, 'function') and node.function:
                func_flows[node.function].append({
                    'id': node_id,
                    'type': getattr(node, 'type', 'unknown'),
                    'label': getattr(node, 'label', ''),
                    'line': getattr(node, 'line', None),
                })
        
        # Build flow sequences
        grouped_data = {
            'project': result.project_path,
            'analysis_mode': result.analysis_mode,
            'summary': {
                'functions': len(result.functions),
                'classes': len(result.classes),
                'modules': len(result.modules),
            },
            'control_flows': {}
        }
        
        for func_name, nodes in sorted(func_flows.items()):
            if len(nodes) < 2:
                continue
                
            # Sort nodes to create logical flow
            sorted_nodes = sorted(nodes, key=lambda n: (n['line'] or 0, n['id']))
            
            # Create flow sequence
            flow_sequence = []
            for i, node in enumerate(sorted_nodes):
                flow_sequence.append({
                    'step': i + 1,
                    'node_type': node['type'],
                    'label': node['label'][:50] if node['label'] else node['type'],
                    'line': node['line'],
                })
            
            grouped_data['control_flows'][func_name] = {
                'node_count': len(nodes),
                'flow_sequence': flow_sequence,
                'entry_point': sorted_nodes[0]['id'] if sorted_nodes else None,

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji export_grouped. Skup się na wydzieleniu operacji o największej liczbie mutacji.