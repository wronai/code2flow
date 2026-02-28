## Cel refaktoryzacji
Extract logic from `_detect_shotgun_surgery` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_shotgun_surgery' is highly complex: CC=1, fan-out=8, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 105+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_shotgun_surgery(self) -> List[CodeSmell]:
        """Detect variables whose mutation requires changes across many functions."""
        smells = []
        var_mutators = {} # variable -> set(functions)
        
        for mutation in self.result.mutations:
            if mutation.variable not in var_mutators:
                var_mutators[mutation.variable] = set()
            var_mutators[mutation.variable].add(mutation.scope)
            
        for var, funcs in var_mutators.items():
            if len(funcs) >= 5:
                # Find a representative function to report the smell
                func_name = list(funcs)[0]
                func_info = self.result.functions.get(func_name)
                if not func_info: continue
                
                smells.append(CodeSmell(
                    name=f"Shotgun Surgery: {var}",
                    type="shotgun_surgery",
                    file=func_info.file,
                    line=func_info.line,
                    severity=0.8,
                    description=f"Mutation of variable '{var}' spans {len(funcs)} functions. Changing this logic requires work in many places.",
                    context={"variable": var, "affected_functions": list(funcs)}
                ))
        return smells
    def _detect_bottlenecks(self) -> List[CodeSmell]:
        """Detect functions with high Betweenness Centrality."""
        smells = []
        # Central functions that many independent paths traverse
        for func_name, func_info in self.result.functions.items():
            if func_info.centrality > 0.1: # Heuristic threshold
                smells.append(CodeSmell(
                    name=f"Structural Bottleneck: {func_info.name}",
                    type="bottleneck",
                    file=func_info.file,
                    line=func_info.line,
                    severity=min(1.0, func_info.centrality * 5),
                    description=f"Function '{func_info.name}' is a structural bottleneck (centrality={round(func_info.centrality, 3)}). Significant logic flows through this function.",
                    context={"centrality": func_info.centrality}
                ))
        return smells

    def _detect_circular_dependencies(self) -> List[CodeSmell]:
        """Detect circular dependencies in call graph."""
        smells = []
        cycles = self.result.metrics.get("project", {}).get("circular_dependencies", [])
        
        for cycle in cycles:
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_shotgun_surgery. Skup się na wydzieleniu operacji o największej liczbie mutacji.