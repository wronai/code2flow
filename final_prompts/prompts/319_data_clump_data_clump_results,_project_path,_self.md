## Cel refaktoryzacji
Move method `results, project_path, self` from module `analyzer` to `other_module`.

## Powód (Głęboka Analiza)
- Arguments (results, project_path, self) are used together in multiple functions: code2flow.core.analyzer.ProjectAnalyzer._merge_results, code2flow.core.analyzer._merge_results.
- Status reachability: unknown
- Feature Envy: Metoda używa więcej danych z `other_module` niż z `analyzer`.
- Obce Mutacje: 

## Kontekst strukturalny
- Zależności: 
- Mutacje w module docelowym: This code mutates state in 

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/core/analyzer.py — źródło
-  — cel

## Kod źródłowy do przeniesienia
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
Zrefaktoryzuj ten fragment kodu, aby poprawić jego strukturę i zmniejszyć złożoność.