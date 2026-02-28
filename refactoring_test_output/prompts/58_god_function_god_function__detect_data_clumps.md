## Cel refaktoryzacji
Extract logic from `_detect_data_clumps` to a new method/function.

## Powód (z analizy DFG)
- Function '_detect_data_clumps' has high complexity: fan-out=9, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 71-91)

## Kod źródłowy do refaktoryzacji
```python
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
                        context={"clump": list(args), "related_functions": funcs}
                    ))
        return smells

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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_data_clumps. Skup się na wydzieleniu operacji o największej liczbie mutacji.