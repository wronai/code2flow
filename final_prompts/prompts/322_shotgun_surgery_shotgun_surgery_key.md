## Cel refaktoryzacji
Extract logic from `key` to a new method/function.

## Powód (Głęboka Analiza)
- Mutation of variable 'key' spans 5 functions. Changing this logic requires work in many places.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 463+)

## Kod źródłowy do refaktoryzacji
```python
    def _find_data_dependencies(self, result: AnalysisResult) -> list:
        """Find cross-module data dependencies."""
        deps = []
        
        # Track which modules share data
        module_data_flow = {}
        
        for func_name, func in result.functions.items():
            func_module = func_name.rsplit('.', 1)[0] if '.' in func_name else 'root'
            
            for called in func.calls[:15]:
                called_module = called.rsplit('.', 1)[0] if '.' in called else 'root'
                
                if func_module != called_module and called in result.functions:
                    key = (func_module, called_module)
                    if key not in module_data_flow:
                        module_data_flow[key] = {
                            'from_module': func_module,
                            'to_module': called_module,
                            'data_functions': [],
                            'call_count': 0,
                        }
                    
                    module_data_flow[key]['data_functions'].append({
                        'caller': func_name,
                        'callee': called,
                    })
                    module_data_flow[key]['call_count'] += 1
        
        # Convert to list and sort by call count
        deps = sorted(module_data_flow.values(), key=lambda x: x['call_count'], reverse=True)
        
        # Limit data functions per dependency
        for dep in deps:
            dep['data_functions'] = dep['data_functions'][:10]
        
        return deps[:15]
    
    def _find_event_flows(self, result: AnalysisResult) -> list:
        """Find event-driven patterns and callback flows."""
        flows = []
        
        # Event/callback indicators
        event_indicators = ['event', 'emit', 'trigger', 'notify', 'callback', 'handler', 'listen', 'subscribe']
        hook_indicators = ['hook', 'on_', 'before_', 'after_', 'pre_', 'post_']
        
        for func_name, func in result.functions.items():
            name_lower = func.name.lower()
            
            is_event_related = (
```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.