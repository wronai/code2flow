## Cel refaktoryzacji
Move method `include_defaults, compact, result, self, output_path` from module `base` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (include_defaults, compact, result, self, output_path) are used together in multiple functions: code2flow.exporters.base.JSONExporter.export, code2flow.exporters.base.YAMLExporter.export.
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
    def export(self, result: AnalysisResult, output_path: str, compact: bool = True, include_defaults: bool = False) -> None:
        """Export to YAML file."""
        data = result.to_dict(compact=compact and not include_defaults)
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
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
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.