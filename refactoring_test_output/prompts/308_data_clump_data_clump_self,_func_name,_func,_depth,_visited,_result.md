## Cel refaktoryzacji
Extract logic from `self, func_name, func, depth, visited, result` to a new method/function.

## Powód (z analizy DFG)
- Arguments (self, func_name, func, depth, visited, result) are used together in multiple functions: code2flow.exporters.base.LLMPromptExporter._trace_flow, code2flow.exporters.base._trace_flow.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/exporters/base.py (linie 1159-1179)

## Kod źródłowy do refaktoryzacji
```python
    def _trace_flow(self, func_name: str, func, result: AnalysisResult, depth: int, visited: set = None) -> str:
        """Trace execution flow from a function with cycle detection."""
        if visited is None:
            visited = set()
        
        # Prevent cycles
        if func_name in visited or depth <= 0:
            return func_name.split('.')[-1]
        
        visited.add(func_name)
        
        short_name = func_name.split('.')[-1]
        module = func_name.rsplit('.', 1)[0] if '.' in func_name else 'root'
        
        lines = [f"{short_name} [{module}]"]
        
        # Group calls by module to show cross-module flows
        calls_by_module = {}
        for called in func.calls[:5]:  # Top 5 calls
            called_module = called.rsplit('.', 1)[0] if '.' in called else 'root'
            if called_module not in calls_by_module:
                calls_by_module[called_module] = []
            calls_by_module[called_module].append(called)
        
        # Show calls, prioritizing cross-module flows
        shown = 0
        for called_module, calls in sorted(calls_by_module.items(), 
                                           key=lambda x: x[0] != module):  # Cross-module first
            for called in calls[:2]:  # Max 2 per module
                if shown >= 3:
                    break
                    
                called_func = result.functions.get(called)
                if called_func and called not in visited:
                    sub_flow = self._trace_flow(called, called_func, result, depth - 1, visited.copy())
                    called_short = called.split('.')[-1]
                    cross_indicator = " →" if called_module != module else ""
                    lines.append(f"  └─{cross_indicator}> {called_short}")
                    
                    # Add indented sub-flow
                    sub_lines = sub_flow.split('\n')[1:]  # Skip first line (already shown)
                    for sub_line in sub_lines[:3]:  # Limit depth display
                        lines.append("    " + sub_line)
                    shown += 1
        
        return '\n'.join(lines)
    
    def _analyze_call_patterns(self, result: AnalysisResult) -> dict:
        """Analyze common call patterns in the codebase."""
        patterns = {

```

## Instrukcja
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.