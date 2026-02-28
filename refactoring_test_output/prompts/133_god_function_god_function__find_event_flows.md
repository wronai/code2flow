## Cel refaktoryzacji
Extract logic from `_find_event_flows` to a new method/function.

## Powód (z analizy DFG)
- Function '_find_event_flows' has high complexity: fan-out=9, mutations=0.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 501-521)

## Kod źródłowy do refaktoryzacji
```python
    def _find_event_flows(self, result: AnalysisResult) -> list:
        """Find event-driven patterns and callback flows."""
        flows = []
        
        # Event/callback indicators
        event_indicators = ['event', 'emit', 'trigger', 'notify', 'callback', 'handler', 'listen', 'subscribe']
        hook_indicators = ['hook', 'on_', 'before_', 'after_', 'pre_', 'post_']
        
        for func_name, func in result.functions.items():
            name_lower = func.name.lower()
            
            is_event_related = (
                any(ind in name_lower for ind in event_indicators) or
                any(name_lower.startswith(ind) for ind in hook_indicators)
            )
            
            if is_event_related:
                # Find event handlers (functions called by this that might be callbacks)
                handlers = []
                for called in func.calls[:10]:
                    called_func = result.functions.get(called)
                    if called_func:
                        called_lower = called_func.name.lower()
                        if any(ind in called_lower for ind in event_indicators + ['handle', 'process']):
                            handlers.append(called)
                
                flows.append({
                    'event_source': func_name,
                    'type': 'emitter' if 'emit' in name_lower or 'trigger' in name_lower else 'handler',
                    'handlers': handlers[:5],
                    'description': func.docstring[:150] if func.docstring else 'N/A',
                })
                
                if len(flows) >= 20:
                    break
        
        return flows
    
    def export_data_structures(self, result: AnalysisResult, output_path: str, compact: bool = True) -> None:
        """Export data structure analysis focusing on data types, flows, and optimization opportunities.
        
        Analyzes:
        - Data types and their usage patterns
        - Data flow graphs (DFG) between functions
        - Process dependencies and data transformations
        - Optimization opportunities (type reduction, process consolidation)
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _find_event_flows. Skup się na wydzieleniu operacji o największej liczbie mutacji.