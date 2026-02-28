## Cel refaktoryzacji
Extract logic from `_deep_analyze_file` to a new method/function.

## Powód (z analizy DFG)
- Function '_deep_analyze_file' has high complexity: fan-out=4, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/streaming_analyzer.py (linie 456-476)

## Kod źródłowy do refaktoryzacji
```python
    def _deep_analyze_file(self, priority: FilePriority) -> Optional[Dict]:
        """Deep analysis with limited CFG generation."""
        result = self._quick_scan_file(priority)
        if not result:
            return None
        
        # Only build CFG for functions under node limit
        max_nodes = self.strategy.max_nodes_per_function
        
        for func_name, func in result['functions'].items():
            # Skip if too many calls (simplistic heuristic)
            if len(func.calls) > 20:
                continue
            
            # Build simplified CFG
            entry_id = f"{func_name}_entry"
            exit_id = f"{func_name}_exit"
            
            result['nodes'][entry_id] = FlowNode(
                id=entry_id, type='ENTRY', label='entry', function=func_name
            )
            result['nodes'][exit_id] = FlowNode(
                id=exit_id, type='EXIT', label='exit', function=func_name
            )
            
            # Limit total nodes
            if len(result['nodes']) > self.strategy.max_total_nodes:
                break
        
        return result
    
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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _deep_analyze_file. Skup się na wydzieleniu operacji o największej liczbie mutacji.