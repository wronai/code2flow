## Cel refaktoryzacji
Extract logic from `_detect_god_functions` to a new method/function.

## Powód (Głęboka Analiza)
- Function '_detect_god_functions' is highly complex: CC=1, fan-out=8, mutations=8.
- Złożoność Cyklomatyczna: N/A (Rank: N/A)
- Fan-out: 
- Mutacje: 0 modifications recorded: ...
- Reachability: unknown

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Plik i Zakres
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 24+)

## Kod źródłowy do refaktoryzacji
```python
    def _detect_god_functions(self) -> List[CodeSmell]:
        """Detect high fan-out / large functions."""
        smells = []
        for func_name, func_info in self.result.functions.items():
            metrics = self.result.metrics.get(func_name, {})
            fan_out = metrics.get('fan_out', 0)
            mutation_count = len([m for m in self.result.mutations if m.scope == func_name])
            
            # Use radon complexity if available
            complexity = func_info.complexity.get('cyclomatic', 1)
            
            if fan_out > 8 or mutation_count > 5 or complexity > 15:
                # Severity based on multiple factors
                severity = (fan_out / 15) * 0.4 + (mutation_count / 20) * 0.3 + (complexity / 25) * 0.3
                severity = min(1.0, severity)
                
                smells.append(CodeSmell(
                    name=f"God Function: {func_info.name}",
                    type="god_function",
                    file=func_info.file,
                    line=func_info.line,
                    severity=severity,
                    description=f"Function '{func_info.name}' is highly complex: CC={complexity}, fan-out={fan_out}, mutations={mutation_count}.",
                    context={"fan_out": fan_out, "mutations": mutation_count, "complexity": complexity}
                ))
        return smells
        
    def _detect_feature_envy(self) -> List[CodeSmell]:
        """Detect functions that use other objects more than their own."""
        smells = []
        # Simplified: look for functions mutating many variables in OTHER modules
        for func_name, func_info in self.result.functions.items():
            mut_mod = func_name.split('.')[0]
            foreign_mutations = []
            
            for mutation in self.result.mutations:
                if mutation.scope == func_name:
                    if '.' in mutation.variable:
                        origin_mod = mutation.variable.split('.')[0]
                        if origin_mod != mut_mod:
                            foreign_mutations.append(mutation.variable)
                            
            if len(set(foreign_mutations)) >= 3:
                smells.append(CodeSmell(
                    name=f"Feature Envy: {func_info.name}",
                    type="feature_envy",
                    file=func_info.file,
                    line=func_info.line,
                    severity=0.7,
                    description=f"Function '{func_info.name}' mutates multiple variables in other modules: {', '.join(set(foreign_mutations))}.",
```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_god_functions. Skup się na wydzieleniu operacji o największej liczbie mutacji.