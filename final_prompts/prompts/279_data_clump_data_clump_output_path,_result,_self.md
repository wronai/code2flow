## Cel refaktoryzacji
Move method `output_path, result, self` from module `base` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (output_path, result, self) are used together in multiple functions: code2flow.exporters.base.YAMLExporter.export_grouped, code2flow.exporters.base.MermaidExporter.export, code2flow.exporters.base.MermaidExporter.export_call_graph, code2flow.exporters.base.MermaidExporter.export_compact, code2flow.exporters.base.LLMPromptExporter.export, code2flow.exporters.base.export, code2flow.exporters.base.export_grouped, code2flow.exporters.base.export_call_graph, code2flow.exporters.base.export_compact.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `base`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.