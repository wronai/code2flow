## Cel refaktoryzacji
Extract logic from `parts` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'parts' spans 12 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 869-889)

## Kod źródłowy do refaktoryzacji
```python
    def export_call_graph(self, result: AnalysisResult, output_path: str) -> None:
        """Export simplified call graph."""
        lines = ["flowchart TD"]
        
        # Add nodes grouped by module
        modules: Dict[str, list] = {}
        for func_name in result.functions:
            parts = func_name.split('.')
            module = parts[0] if parts else 'unknown'
            if module not in modules:
                modules[module] = []
            modules[module].append(func_name)
        
        # Create subgraphs
        for module, funcs in sorted(modules.items()):
            safe_module = module.replace('-', '_').replace('.', '_')
            lines.append(f"    subgraph {safe_module}")
            for func_name in funcs[:50]:
                safe_id = self._safe_id(func_name)
                short_name = func_name.split('.')[-1][:30]
                lines.append(f'        {safe_id}["{short_name}"]')
            lines.append("    end")
        
        # Add edges
        edge_count = 0
        max_edges = 500
        for func_name, func in result.functions.items():
            source_id = self._safe_id(func_name)
            for called in func.calls[:10]:
                if called in result.functions:
                    target_id = self._safe_id(called)
                    lines.append(f"    {source_id} --> {target_id}")
                    edge_count += 1
                    if edge_count >= max_edges:
                        break
            if edge_count >= max_edges:
                break
        
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def export_compact(self, result: AnalysisResult, output_path: str) -> None:
        """Export compact flowchart - same as call graph for now."""
        self.export_call_graph(result, output_path)
    
    def _safe_id(self, name: str) -> str:
        """Create Mermaid-safe node ID."""
        safe = name.replace('.', '_').replace('-', '_').replace(':', '_')
        if len(safe) > 40:

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.