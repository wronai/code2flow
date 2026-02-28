## Cel refaktoryzacji
Extract logic from `func` to a new method/function.

## Powód (z analizy DFG)
- Mutation of variable 'func' spans 5 functions. Changing this logic requires work in many places.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 487-507)

## Kod źródłowy do refaktoryzacji
```python
    def _build_call_graph_streaming(self, results: List[Dict]) -> Dict[str, List[str]]:
        """Memory-efficient call graph construction."""
        call_graph = {}
        
        # Build function name lookup
        all_functions = {}
        for r in results:
            all_functions.update(r.get('functions', {}))
        
        # Resolve calls
        for r in results:
            for func_name, func in r.get('functions', {}).items():
                resolved_calls = []
                for called in func.calls:
                    # Try to resolve to known function
                    for known_name in all_functions:
                        if known_name.endswith(f".{called}") or known_name == called:
                            resolved_calls.append(known_name)
                            break
                
                func.calls = resolved_calls
                call_graph[func_name] = resolved_calls
        
        return call_graph
    
    def _select_important_files(
        self,
        prioritized: List[FilePriority],
        results: List[Dict]
    ) -> List[FilePriority]:
        """Select files for deep analysis based on importance."""
        important = []
        
        for p in prioritized:
            # Entry points are important
            if p.is_entry_point:
                important.append(p)
                continue
            
            # Find result for this file
            for r in results:
                mod = r.get('module')
                if mod and mod.name == p.module_name:
                    # Files with many functions are important
                    if len(mod.functions) > 5:
                        important.append(p)
                        break
                    
                    # Files called by many others
                    if p.import_count > 3:

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.