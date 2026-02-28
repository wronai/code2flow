## Cel refaktoryzacji
Extract logic from `name_lower` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'name_lower' spans 6 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 381-401)

## Kod źródłowy do refaktoryzacji
```python
    def _find_data_pipelines(self, result: AnalysisResult) -> list:
        """Find data transformation pipelines in the codebase."""
        pipelines = []
        
        # Data processing indicators by stage
        input_indicators = ['parse', 'load', 'read', 'fetch', 'get', 'input', 'receive', 'extract']
        transform_indicators = ['transform', 'convert', 'process', 'validate', 'filter', 'map', 'reduce', 'compute']
        output_indicators = ['serialize', 'format', 'write', 'save', 'send', 'output', 'render', 'encode']
        
        # Group functions by their data role
        input_funcs = []
        transform_funcs = []
        output_funcs = []
        
        for func_name, func in result.functions.items():
            name_lower = func.name.lower()
            
            if any(ind in name_lower for ind in input_indicators):
                input_funcs.append((func_name, func))
            elif any(ind in name_lower for ind in transform_indicators):
                transform_funcs.append((func_name, func))
            elif any(ind in name_lower for ind in output_indicators):
                output_funcs.append((func_name, func))
        
        # Find chains: input → transform → output
        for in_name, in_func in input_funcs[:20]:
            for t_name, t_func in transform_funcs[:30]:
                # Check if input calls transform
                if t_name in in_func.calls:
                    for out_name, out_func in output_funcs[:20]:
                        # Check if transform calls output
                        if out_name in t_func.calls:
                            pipelines.append({
                                'pipeline_id': f"pipeline_{len(pipelines)+1}",
                                'stages': [
                                    {'stage': 'input', 'function': in_name, 'description': in_func.docstring[:100] if in_func.docstring else 'N/A'},
                                    {'stage': 'transform', 'function': t_name, 'description': t_func.docstring[:100] if t_func.docstring else 'N/A'},
                                    {'stage': 'output', 'function': out_name, 'description': out_func.docstring[:100] if out_func.docstring else 'N/A'},
                                ],
                                'data_flow': f"{in_name} → {t_name} → {out_name}",
                            })
                            if len(pipelines) >= 15:
                                return pipelines
        
        return pipelines
    
    def _find_state_patterns(self, result: AnalysisResult) -> list:
        """Find state management patterns and lifecycles."""
        patterns = []
        

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.