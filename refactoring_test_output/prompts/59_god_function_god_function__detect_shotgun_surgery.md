## Cel refaktoryzacji
Extract logic from `_detect_shotgun_surgery` to a new method/function.

## Powód (z analizy DFG)
- Function '_detect_shotgun_surgery' has high complexity: fan-out=8, mutations=8.
- Fan-out: 
- Mutacje: 

## Kontekst przepływu danych
- Wejście: 
- Mutacje: 0 modifications recorded: ...

## Dotknięte pliki
- /home/tom/github/wronai/code2flow/code2flow/analysis/smells.py (linie 98-118)

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

```

## Instrukcja
Wyekstrahuj mniejsze, spójne metody z funkcji _detect_shotgun_surgery. Skup się na wydzieleniu operacji o największej liczbie mutacji.