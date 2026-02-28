## Cel refaktoryzacji
Extract logic from `_detect_feature_envy` to a new method/function.

## Powód (z analizy DFG)
- Function '_detect_feature_envy' has high complexity: fan-out=10, mutations=0.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 44-64)

## Kod źródłowy do refaktoryzacji
```python
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
                    context={"foreign_mutations": list(set(foreign_mutations))}
                ))
        return smells

    def _detect_data_clumps(self) -> List[CodeSmell]:
        """Detect 3+ variables frequently passed together."""
        smells = []
        # Simplified: find functions with same 3+ arguments
        arg_sets = {} # frozenset(args) -> List[func_names]
        for func_name, func_info in self.result.functions.items():
            if len(func_info.args) >= 3:
                args = frozenset(func_info.args)
                if args not in arg_sets:
                    arg_sets[args] = []
                arg_sets[args].append(func_name)
                
        for args, funcs in arg_sets.items():
            if len(funcs) >= 2:
                for func_name in funcs:
                    func_info = self.result.functions[func_name]
                    smells.append(CodeSmell(
                        name=f"Data Clump: {', '.join(args)}",
                        type="data_clump",
                        file=func_info.file,
                        line=func_info.line,
                        severity=0.6,
                        description=f"Arguments ({', '.join(args)}) are used together in multiple functions: {', '.join(funcs)}.",

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_feature_envy. Skup się na wydzieleniu operacji o największej liczbie mutacji.