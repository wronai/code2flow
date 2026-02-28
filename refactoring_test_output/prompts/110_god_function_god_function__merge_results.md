## Cel refaktoryzacji
Extract logic from `_merge_results` to a new method/function.

## Powód (z analizy DFG)
- Function '_merge_results' has high complexity: fan-out=7, mutations=10.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py (linie 546-566)

## Kod źródłowy do refaktoryzacji
```python
    def _merge_results(self, results: List[Dict], project_path: str) -> AnalysisResult:
        """Merge all file analysis results."""
        merged = AnalysisResult(
            project_path=project_path,
            analysis_mode=self.config.mode,
        )
        
        for r in results:
            if 'module' in r:
                mod = r['module']
                merged.modules[mod.name] = mod
            if 'functions' in r:
                merged.functions.update(r['functions'])
            if 'classes' in r:
                merged.classes.update(r['classes'])
            if 'nodes' in r:
                merged.nodes.update(r['nodes'])
            if 'edges' in r:
                merged.edges.extend(r['edges'])
            if 'mutations' in r:
                merged.mutations.extend(r['mutations'])
            if 'data_flows' in r:
                merged.data_flows.update(r['data_flows'])
        
        return merged
    
    def _build_call_graph(self, result: AnalysisResult) -> None:
        """Build call graph and find entry points."""
        # Map calls between functions
        for func_name, func in result.functions.items():
            for called in func.calls:
                # Try to resolve to a known function
                for known_name in result.functions:
                    if known_name.endswith(f".{called}") or known_name == called:
                        func.calls[func.calls.index(called)] = known_name
                        result.functions[known_name].called_by.append(func_name)
                        break
        
        # Find entry points (not called by anything)
        for func_name, func in result.functions.items():
            if not func.called_by:
                result.entry_points.append(func_name)
    
    def _detect_patterns(self, result: AnalysisResult) -> None:
        """Detect behavioral patterns."""
        # Detect recursion
        for func_name, func in result.functions.items():
            if func_name in func.calls:
                result.patterns.append(Pattern(
                    name=f"recursion_{func.name}",

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _merge_results. Skup się na wydzieleniu operacji o największej liczbie mutacji.